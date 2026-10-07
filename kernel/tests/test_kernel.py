"""Kernel unit tests: pack loads, goldens agree, resolution semantics hold,
gap/proposal records round-trip."""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack  # noqa: E402
from design_authority.resolve import resolve, resolve_golden  # noqa: E402
from design_authority import records  # noqa: E402

PACK_DIR = os.path.join(ROOT, "packs", "triage")


class TestPack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = Pack(PACK_DIR)

    def test_identity(self):
        ident = self.pack.identity()
        self.assertEqual(ident["authority"], "triage")
        self.assertTrue(ident["commit"].startswith("e374f3803d5a"))

    def test_counts(self):
        kinds = {}
        for a in self.pack.artifacts:
            kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
        self.assertEqual(kinds.get("component"), 35)
        self.assertEqual(kinds.get("pattern"), 7)
        self.assertEqual(len(self.pack.rules), 15)
        self.assertEqual(len(self.pack.recipes), 15)


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
        r = resolve(self.pack, "add a progress bar for a long-running background job")
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


if __name__ == "__main__":
    unittest.main()
