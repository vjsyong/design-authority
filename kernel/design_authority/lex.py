"""Lexical normalisation layer (retrieval-side only).

Canonicalises common English spelling variants (chiefly US/UK pairs) so that a
query and the indexed text meet on one form before the frozen resolution
pipeline runs. Retrieval may become fuzzy here; authority determination does
not: this module only rewrites TOKENS. Outcome taxonomy, thresholds,
precedence and citation rules are untouched, and every rewrite a query
undergoes is reported back in the output's `normalized` field.

Design rules (0.3, layer version 1):
- an explicit, curated variant table of readable pairs: extend the table, never
  add suffix heuristics with unbounded reach;
- canonical direction: US spelling;
- lookup forms per token, tried in order: the token itself; a guarded plural
  (trailing `s` unless ss/us/is); `-ing` / `-ed` / `-able` reductions (each
  with an `e`-restore retry). A reduction only fires when the reduced form is a
  table member, so the table's curated space bounds every rewrite;
- idempotent: canonical forms map to themselves; the table is validated at
  import for conflicts.

This layer runs BEFORE the stemmer, so its output is stemmed downstream like
any other token. It applies identically to queries, index fields, alias
phrases, scopes and precedent/candidate vocabularies.
"""

LEX_VERSION = "1"

# variant -> canonical (US). Curated for precision; extend as misses surface.
VARIANT_PAIRS = {
    # -our / -or
    "colour": "color", "colourful": "colorful", "colours": "colors",
    "behaviour": "behavior", "behavioural": "behavioral",
    "favourite": "favorite", "flavour": "flavor", "labour": "labor",
    "neighbour": "neighbor", "honour": "honor", "humour": "humor",
    "rumour": "rumor", "vapour": "vapor", "odour": "odor",
    "endeavour": "endeavor", "harbour": "harbor", "parlour": "parlor",
    "rigour": "rigor", "savour": "savor", "splendour": "splendor",
    "tumour": "tumor", "vigour": "vigor", "clamour": "clamor",
    # -re / -er
    "centre": "center", "metre": "meter", "litre": "liter",
    "theatre": "theater", "fibre": "fiber", "calibre": "caliber",
    "sombre": "somber", "spectre": "specter", "lustre": "luster",
    "manoeuvre": "maneuver",
    # -ce / -se
    "defence": "defense", "offence": "offense", "licence": "license",
    "pretence": "pretense", "practise": "practice",
    # -ogue / -og and friends
    "catalogue": "catalog", "dialogue": "dialog", "analogue": "analog",
    "programme": "program",
    # doubles-l inflections (US single l)
    "cancelled": "canceled", "cancelling": "canceling",
    "travelled": "traveled", "travelling": "traveling", "traveller": "traveler",
    "labelled": "labeled", "labelling": "labeling",
    "modelled": "modeled", "modelling": "modeling",
    "signalled": "signaled", "signalling": "signaling",
    "fuelled": "fueled", "fuelling": "fueling",
    "dialled": "dialed", "dialling": "dialing",
    "marvellous": "marvelous", "jewellery": "jewelry",
    "counsellor": "counselor", "counselling": "counseling",
    # -ise / -ize (curated, high-frequency)
    "organise": "organize", "organisation": "organization",
    "realise": "realize", "recognise": "recognize", "customise": "customize",
    "optimise": "optimize", "optimisation": "optimization",
    "normalise": "normalize", "normalisation": "normalization",
    "standardise": "standardize", "prioritise": "prioritize",
    "summarise": "summarize", "minimise": "minimize", "maximise": "maximize",
    "visualise": "visualize", "visualisation": "visualization",
    "categorise": "categorize", "analyse": "analyze",
    "serialise": "serialize", "initialise": "initialize",
    "initialisation": "initialization", "sanitise": "sanitize",
    "itemise": "itemize", "memorise": "memorize", "memoise": "memoize",
    "apologise": "apologize", "emphasise": "emphasize", "utilise": "utilize",
    "stabilise": "stabilize", "localise": "localize",
    "localisation": "localization", "personalise": "personalize",
    "personalisation": "personalization", "centralise": "centralize",
    "characterise": "characterize", "specialise": "specialize",
    "generalise": "generalize", "hypothesise": "hypothesize",
    "legalise": "legalize", "mobilise": "mobilize", "modernise": "modernize",
    "neutralise": "neutralize", "polarise": "polarize",
    "popularise": "popularize", "publicise": "publicize",
    "scrutinise": "scrutinize", "socialise": "socialize",
    "authorise": "authorize", "authorisation": "authorization",
    "capitalise": "capitalize", "capitalisation": "capitalization",
    "civilise": "civilize", "criticise": "criticize", "finalise": "finalize",
    "formalise": "formalize", "globalise": "globalize",
    "harmonise": "harmonize", "industrialise": "industrialize",
    "materialise": "materialize", "patronise": "patronize",
    "penalise": "penalize", "plagiarise": "plagiarize",
    "pressurise": "pressurize", "privatise": "privatize",
    "rationalise": "rationalize", "revolutionise": "revolutionize",
    "subsidise": "subsidize", "symbolise": "symbolize",
    "sympathise": "sympathize", "terrorise": "terrorize",
    "theorise": "theorize",
    # misc
    "grey": "gray", "greyscale": "grayscale",
    "ageing": "aging", "judgement": "judgment",
    "acknowledgement": "acknowledgment", "fulfil": "fulfill",
    "fulfilment": "fulfillment", "enrol": "enroll",
    "enrolment": "enrollment", "instalment": "installment",
    "instil": "instill", "distil": "distill", "skilful": "skillful",
    "wilful": "willful", "aluminium": "aluminum", "speciality": "specialty",
    "cosy": "cozy", "storey": "story", "tyre": "tire", "kerb": "curb",
    "moustache": "mustache", "sulphur": "sulfur", "plough": "plow",
    "draught": "draft", "chequer": "checker",
}

# ---- derived lookup + validation -------------------------------------------
_LOOKUP = {}
for _k, _v in VARIANT_PAIRS.items():
    _LOOKUP[_k] = _v
for _v in set(VARIANT_PAIRS.values()):
    _LOOKUP.setdefault(_v, _v)

def _validate_table():
    """A canonical value must never itself be a conflicting key."""
    for k, v in VARIANT_PAIRS.items():
        if v in VARIANT_PAIRS and VARIANT_PAIRS[v] != v:
            raise AssertionError(
                "lexical variant conflict: %s -> %s but %s maps to %s"
                % (k, v, v, VARIANT_PAIRS[v]))


_validate_table()


def _forms(token):
    """Reduction candidates, bounded by the table (first table hit wins)."""
    yield token
    if len(token) > 3 and token.endswith("s") and not token.endswith(("ss", "us", "is")):
        yield token[:-1]
    if len(token) > 5 and token.endswith("ing"):
        yield token[:-3]
        yield token[:-3] + "e"
    if len(token) > 4 and token.endswith("ed"):
        yield token[:-2]
        yield token[:-2] + "e"
    if len(token) > 7 and token.endswith("able"):
        yield token[:-4]
        yield token[:-4] + "e"


def canonicalize(token):
    """Map one lowercased token to its canonical spelling (idempotent)."""
    for form in _forms(token):
        hit = _LOOKUP.get(form)
        if hit is not None:
            return hit
    return token
