"""Kernel unit tests: pack loads, goldens agree, resolution semantics hold,
gap/proposal records round-trip."""
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack, norm_tokens  # noqa: E402
from design_authority.lex import canonicalize  # noqa: E402
from design_authority.resolve import resolve, resolve_golden  # noqa: E402
from design_authority import records  # noqa: E402

PACK_DIR = os.path.join(ROOT, "authorities", "triage")


class TestPack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = Pack(PACK_DIR)

    def test_identity(self):
        ident = self.pack.identity()
        self.assertEqual(ident["authority"], "triage")
        # identity pins the source repo's commit (the synthesis lineage builds from
        # the live triage repo, so the sha moves with it — the invariant is the pin)
        self.assertRegex(ident["commit"], r"^[0-9a-f]{40}$")

    def test_counts(self):
        kinds = {}
        for a in self.pack.artifacts:
            kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
        # 35 states-matrix components + 21 furniture components documented in core
        self.assertEqual(kinds.get("component"), 56)
        self.assertEqual(kinds.get("pattern"), 7)
        # interaction standard + consumption + verification levels + 7 foundations
        self.assertEqual(kinds.get("guideline"), 10)
        # the 15 TDS lint rules plus the 4 binding interaction rules
        self.assertEqual(len(self.pack.rules), 19)
        # the synthesis lineage carries no flow recipes yet; the kit curation holds
        # 15 (a recorded merge item, not silently invented)
        self.assertEqual(len(self.pack.recipes), 0)


class TestResolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = Pack(PACK_DIR)

    def test_golden_set(self):
        with open(os.path.join(PACK_DIR, "golden.json")) as fh:
            cases = json.load(fh)["cases"]
        report = resolve_golden(self.pack, cases)
        misses = [r for r in report["rows"] if not r["ok"]]
        self.assertEqual(report["passed"], report["total"],
                         "golden misses: %s" % json.dumps(misses, indent=1))

    def test_undefined_is_structured(self):
        r = resolve(self.pack, "add a carousel of screenshots to the homepage")
        self.assertEqual(r["outcome"], "UNDEFINED")
        self.assertIsNone(r["resolution"])
        self.assertIn("closest", r)
        self.assertIn("search_trace", r)
        self.assertIn("fallback_policy", r)
        self.assertIn("note", r["fallback_policy"])

    def test_conflict_cites_rule(self):
        r = resolve(self.pack, "make all the buttons rounded")
        self.assertEqual(r["outcome"], "CONFLICT")
        self.assertEqual(r["resolution"]["rule"]["id"], "TDS003")

    def test_resolved_cites_existing_artifact(self):
        r = resolve(self.pack, "show an empty state when there are no requests")
        self.assertEqual(r["outcome"], "RESOLVED")
        aid = r["resolution"]["artifact"]["id"]
        self.assertIn(aid, self.pack.by_id)

    def test_every_outcome_carries_authority_echo(self):
        for problem in ("make it rounded", "show an empty state", "waiting for approval"):
            r = resolve(self.pack, problem)
            self.assertIn("authority", r)
            self.assertIn("version", r["authority"])


class TestRecords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = Pack(PACK_DIR)

    def test_gap_and_proposal_roundtrip(self):
        with tempfile.TemporaryDirectory() as ws:
            gap = records.add_gap(self.pack, ws, "show progress of a background job",
                                  context={"page": "jobs"}, scope_hint="system-wide")
            self.assertTrue(gap["id"].startswith("gap/"))
            self.assertEqual(len(records.list_gaps(ws)), 1)
            fetched = records.get_gap(ws, gap["id"])
            assert fetched is not None
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched["need"], "show progress of a background job")
            proposal = records.add_proposal(self.pack, ws, gap["id"], {
                "problem": "No progress treatment for long-running work",
                "insufficiency": "spinner only expresses activity",
                "reuse_case": "any consumer with background jobs",
                "composition_check": "spinner+text cannot express progress",
                "proposed": [{"kind": "component", "name": "progress"}],
                "depends_on": ["component/spinner"],
                "new_primitives": ["determinate progress"],
                "tests": [{"description": "progress element renders with aria", "deterministic": True}],
            })
            self.assertEqual(proposal["status"], "candidate")
            self.assertEqual(len(records.list_proposals(ws)), 1)

    def test_proposal_rejects_unknown_dependency(self):
        with tempfile.TemporaryDirectory() as ws:
            gap = records.add_gap(self.pack, ws, "x")
            with self.assertRaises(ValueError):
                records.add_proposal(self.pack, ws, gap["id"], {
                    "problem": "p", "insufficiency": "i", "reuse_case": "r",
                    "composition_check": "c",
                    "proposed": [{"kind": "component", "name": "n"}],
                    "depends_on": ["component/does-not-exist"], "tests": [{}],
                })


    def test_proposal_review_transitions(self):
        with tempfile.TemporaryDirectory() as ws:
            gap = records.add_gap(self.pack, ws, "x")
            prop = records.add_proposal(self.pack, ws, gap["id"], {
                "problem": "p", "insufficiency": "i", "reuse_case": "r",
                "composition_check": "c",
                "proposed": [{"kind": "component", "name": "n"}],
                "tests": [{}],
            })
            reviewed = records.set_proposal_review(ws, prop["id"], "needs-info",
                                                   notes="more evidence required")
            self.assertEqual(reviewed["status"], "needs-info")
            self.assertEqual(reviewed["review"]["verdict"], "needs-info")
            with self.assertRaises(ValueError):
                records.set_proposal_review(ws, prop["id"], "maybe")


class TestPrecedents(unittest.TestCase):
    """Scope-aware precedents + candidates (lenient doctrine)."""

    @classmethod
    def setUpClass(cls):
        cls.pack = Pack(os.path.join(ROOT, "authorities", "wink"))
        cls.dom = Pack(os.path.join(ROOT, "authorities", "dominion"))

    def test_pack_without_precedents_loads_empty(self):
        # a pack whose precedents/candidates files are absent loads with empties
        with tempfile.TemporaryDirectory() as td:
            for f in os.listdir(PACK_DIR):
                src = os.path.join(PACK_DIR, f)
                if f in ("precedents.json", "candidates.json") or not os.path.isfile(src):
                    continue
                shutil.copy(src, os.path.join(td, f))
            p = Pack(td)
            self.assertEqual(p.precedents, [])
            self.assertEqual(p.candidates, [])

    def test_governs_on_policy_decline(self):
        r = resolve(self.pack, "photo upload for the ritual")
        prec = r.get("precedents") or []
        self.assertTrue(prec and prec[0]["verdict"] == "governs")
        self.assertEqual(prec[0]["id"], "precedent/declined-photographic-imagery")

    def test_outside_verdict_exempts_functional_controls(self):
        res = self.pack.precedent_matches("a check control to log a ritual")
        self.assertTrue(any(m["verdict"] == "outside" for m in res))

    def test_retired_decline_defers_to_undefined(self):
        r = resolve(self.pack, "add a dark mode theme")
        self.assertEqual(r["outcome"], "FALLBACK")
        self.assertNotIn("precedents", r)
        r2 = resolve(self.pack, "add a bar chart of activity")
        self.assertNotIn("precedents", r2)

    def test_candidates_attach_on_undefined(self):
        r = resolve(self.dom, "pagination for older entries")
        self.assertEqual(r["outcome"], "UNDEFINED")
        ids = [c["id"] for c in r.get("candidates", [])]
        self.assertIn("candidate/paging-composition", ids)

    def test_benign_ask_has_no_precedents(self):
        r = resolve(self.pack, "add a primary button to the page")
        self.assertNotIn("precedents", r)
        self.assertNotIn("candidates", r)

    def test_gap_carries_precedent_warnings(self):
        with tempfile.TemporaryDirectory() as ws:
            gap = records.add_gap(self.pack, ws, "an avatar photo for sam")
            self.assertTrue(gap.get("precedent_warnings"))


class TestRecipeCompose(unittest.TestCase):
    """COMPOSE coverage: a recipe-bearing pack turns a matching ask into a recipe answer."""

    @classmethod
    def setUpClass(cls):
        cls.dom = Pack(os.path.join(ROOT, "authorities", "dominion"))

    def test_compose_cites_recipe(self):
        r = resolve(self.dom, "retire a ritual from the register")
        self.assertEqual(r["outcome"], "COMPOSE")
        self.assertEqual(r["resolution"]["recipe"]["id"], "recipe/retire-confirm")


class TestLexicalNormalisation(unittest.TestCase):
    """0.3 lexical layer: spelling variants meet on one canonical form.

    The layer is retrieval-side only: it never changes the outcome taxonomy,
    thresholds or precedence, and every query rewrite is reported in
    `normalized` so the mapping stays auditable.
    """

    @classmethod
    def setUpClass(cls):
        cls.pack = Pack(PACK_DIR)

    def test_variant_pairs_meet(self):
        for a, b in [("colour", "color"), ("centre", "center"),
                     ("customise", "customize"), ("behaviour", "behavior"),
                     ("behavioural", "behavioral"), ("dialogue", "dialog"),
                     ("licence", "license"), ("travelling", "traveling"),
                     ("organised", "organized"), ("customising", "customizing"),
                     ("customisable", "customizable"), ("colours", "colors"),
                     ("buttons", "button")]:
            self.assertEqual(norm_tokens(a), norm_tokens(b), "%s vs %s" % (a, b))

    def test_canonicalise_is_idempotent_and_table_bounded(self):
        for w in ("color", "center", "customize", "gray", "behavior"):
            self.assertEqual(canonicalize(w), canonicalize(canonicalize(w)))
        for w in ("hour", "promise", "rise", "genre", "board", "available"):
            self.assertEqual(canonicalize(w), w)

    def test_search_is_spelling_symmetric(self):
        for a, b in [("colour", "color"), ("dialogue", "dialog")]:
            self.assertEqual([h["id"] for h in self.pack.search(a, limit=3)],
                             [h["id"] for h in self.pack.search(b, limit=3)], a)

    def test_resolve_reports_the_mapping(self):
        r = resolve(self.pack, "colour tokens")
        self.assertEqual(r["outcome"], "RESOLVED")
        self.assertEqual(r["resolution"]["artifact"]["id"], "token-set/colour")
        self.assertEqual(r["normalized"], {"colour": "color"})
        r2 = resolve(self.pack, "color tokens")
        self.assertNotIn("normalized", r2)
        self.assertEqual(r2["resolution"]["artifact"]["id"], "token-set/colour")

    def test_us_spelling_reaches_curated_vocabulary(self):
        r = resolve(self.pack, "a dialogue")
        self.assertEqual(r["outcome"], "RESOLVED")
        self.assertEqual(r["resolution"]["artifact"]["id"], "component/dlg")
        ids = [c.get("id") for c in self.pack.candidate_matches("behavioral verification", limit=2)]
        self.assertIn("candidate/behavioural-verification", ids)


if __name__ == "__main__":
    unittest.main()
