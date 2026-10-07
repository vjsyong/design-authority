"""Load and index a Design Authority pack (a directory of JSON files)."""
import json
import os
import re

STOPWORDS = {
    "a", "an", "the", "to", "for", "of", "in", "on", "at", "with", "and", "or",
    "is", "are", "be", "it", "its", "this", "that", "we", "i", "you", "they",
    "our", "your", "their", "need", "needs", "want", "wants", "should", "must",
    "can", "could", "would", "add", "some", "way", "like", "please", "new",
    "when", "where", "how", "use", "using", "user", "users", "them", "there",
    "have", "has", "do", "does", "make", "making", "get", "got", "also",
    "show", "display", "let", "give", "see", "which", "after", "before",
}


def _stem(tok):
    """Tiny, consistent suffix normaliser (applied to both sides of matching)."""
    if len(tok) <= 3:
        return tok
    if tok.endswith("able") and len(tok) > 7:      # searchable -> search (not enable -> en)
        tok = tok[:-4]
    elif tok.endswith("s") and not tok.endswith(("ss", "us", "is")):
        tok = tok[:-1]
    if tok.endswith("e") and len(tok) > 3:
        tok = tok[:-1]
    return tok


def norm_tokens(text):
    out = []
    for t in re.findall(r"[a-z0-9][a-z0-9-]*", str(text).lower()):
        if t in STOPWORDS or len(t) <= 1:
            continue
        out.append(_stem(t))
    return out


def norm_phrase(text):
    return " ".join(norm_tokens(text))


class PackError(Exception):
    pass


class Pack(object):
    def __init__(self, path):
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            raise PackError("pack directory not found: %s" % self.path)

        def load(name, required=True):
            p = os.path.join(self.path, name)
            if not os.path.exists(p):
                if required:
                    raise PackError("missing pack file: %s" % name)
                return None
            with open(p) as fh:
                return json.load(fh)

        def load_opt(name, key):
            p = os.path.join(self.path, name)
            if not os.path.exists(p):
                return []
            with open(p) as fh:
                return (json.load(fh) or {}).get(key, [])

        self.manifest = load("authority.json")
        ep = self.manifest.get("entrypoints", {})
        self.artifacts = load(ep.get("artifacts", "artifacts.json"))["artifacts"]
        self.rules = load(ep.get("rules", "rules.json"))["rules"]
        self.recipes = load_opt(ep.get("recipes", "recipes.json"), "recipes")
        self.fallbacks = load_opt(ep.get("fallbacks", "fallbacks.json"), "fallbacks")
        self.prohibitions = load_opt(ep.get("prohibitions", "prohibitions.json"),
                                     "prohibitions")
        self.validators = load_opt(ep.get("validators", "validators.json"), "validators")
        scoring = load(ep.get("scoring", "scoring.json"), False)
        self.scoring = scoring or {}

        self.by_id = {}
        for entry in (self.artifacts + self.recipes + self.fallbacks
                      + self.prohibitions):
            eid = entry.get("id")
            if not eid:
                raise PackError("entry without id")
            if eid in self.by_id:
                raise PackError("duplicate id: %s" % eid)
            self.by_id[eid] = entry
        for r in self.rules:
            self.by_id.setdefault(r["id"], r)

        self._docs = None

    # -- identity -------------------------------------------------------------
    def identity(self):
        s = self.manifest.get("snapshot", {})
        return {"authority": self.manifest.get("id"),
                "version": self.manifest.get("version"),
                "commit": s.get("commit")}

    def rule(self, rid):
        for r in self.rules:
            if r["id"] == rid:
                return r
        return None

    # -- search index -----------------------------------------------------------
    def docs(self):
        """Searchable docs: {id, kind, title, weights: {token: w}, phrases: [...], raw}."""
        if self._docs is not None:
            return self._docs
        out = []

        def add(entry, fields, phrases=()):
            w = {}
            for text, weight in fields:
                for tok in norm_tokens(text):
                    if weight > w.get(tok, 0):
                        w[tok] = weight
            out.append({"id": entry["id"], "kind": entry.get("kind", "?"),
                        "title": entry.get("title") or entry["id"],
                        "weights": w,
                        "phrases": [norm_phrase(p) for p in phrases if p],
                        "raw": entry})

        for a in self.artifacts:
            body = a.get("body", {}) or {}
            fields = [(a.get("title", ""), 3.0), (a.get("summary", ""), 1.5)]
            for alias in a.get("aliases", []):
                fields.append((alias, 4.0))
            if isinstance(body.get("class"), str):
                fields.append((body["class"], 2.5))
            for key in ("states", "a11y", "do", "dont", "quote", "statement"):
                val = body.get(key)
                if isinstance(val, list):
                    for item in val:
                        fields.append((item, 1.0))
                elif isinstance(val, str):
                    fields.append((val, 1.0))
            if isinstance(body.get("group"), str):
                fields.append((body["group"], 1.0))
            s = a.get("source", {})
            fields.append((s.get("path", ""), 1.0))
            add(a, fields, phrases=a.get("aliases", []))

        for r in self.recipes:
            fields = [(r.get("title", ""), 3.0), (r.get("summary", ""), 1.5)]
            for n in r.get("needs", []):
                fields.append((n, 3.0))
            for c in r.get("constraints", []):
                fields.append((c, 1.0))
            add(r, fields, phrases=r.get("needs", []))

        for f in self.fallbacks:
            fields = [(f.get("title", ""), 2.0), (f.get("statement", ""), 1.5)]
            for sc in f.get("scope", []):
                fields.append((sc, 2.5))
            add(f, fields)

        self._docs = out
        return out

    def search(self, query, kinds=None, limit=10):
        """Ranked search over the index. Returns [{id, kind, title, score, matched}]."""
        q = norm_tokens(query)
        qtext = " ".join(q)
        qset = set(q)
        results = []
        for doc in self.docs():
            if kinds and doc["kind"] not in kinds:
                continue
            score = 0.0
            matched = []
            for tok in qset:
                w = doc["weights"].get(tok)
                if w:
                    score += w
                    matched.append(tok)
            for phrase in doc["phrases"]:
                if " " in phrase:
                    if all(t in qset for t in phrase.split()):
                        score += 5.0
                        matched.append("~" + phrase)
                elif qtext == phrase:
                    score += 5.0
                    matched.append("~" + phrase)
            if score > 0:
                results.append({"id": doc["id"], "kind": doc["kind"],
                                "title": doc["title"], "score": round(score, 2),
                                "matched": matched})
        results.sort(key=lambda r: (-r["score"], r["id"]))
        return results[:limit]
