"""Unit tests for disputed resolutions (0.5): consumer-side records that a
RESOLVED outcome did not govern the need. Distinct from gaps; replayable."""
import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack  # noqa: E402
from design_authority import records  # noqa: E402
from design_authority.resolve import replay_disputes  # noqa: E402

PACK = os.path.join(ROOT, "packs", "triage")


class TestDisputes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pack = Pack(PACK)

    def test_add_requires_existing_target(self):
        with tempfile.TemporaryDirectory() as ws:
            with self.assertRaises(ValueError):
                records.add_dispute(self.pack, ws, "a skip link", "component/ghost",
                                    "unknown id must be rejected")

    def test_add_and_list(self):
        with tempfile.TemporaryDirectory() as ws:
            rec = records.add_dispute(
                self.pack, ws, "a skip link to jump past the navigation",
                "component/nav-item", "a skip link is not a nav item")
            self.assertTrue(rec["id"].startswith("dispute/"))
            self.assertEqual(rec["kind"], "disputed-resolution")
            self.assertEqual(rec["authority"]["authority"], "triage")
            listed = records.list_disputes(ws)
            self.assertEqual(len(listed), 1)
            self.assertEqual(listed[0]["status"], "open")

    def test_replay_stands_and_clears(self):
        with tempfile.TemporaryDirectory() as ws:
            records.add_dispute(self.pack, ws,
                                "a skip link to jump past the navigation",
                                "component/nav-item", "wrong match")
            records.add_dispute(self.pack, ws, "a carousel of marketing images",
                                "component/img", "not canon")
            rep = replay_disputes(self.pack, records.list_disputes(ws, status="open"))
            by_query = {r["query"]: r for r in rep["rows"]}
            self.assertTrue(by_query["a skip link to jump past the navigation"]["still_stands"])
            self.assertFalse(by_query["a carousel of marketing images"]["still_stands"])
            self.assertEqual(rep["standing"], 1)
            self.assertEqual(rep["cleared"], 1)

    def test_set_status(self):
        with tempfile.TemporaryDirectory() as ws:
            rec = records.add_dispute(self.pack, ws,
                                      "a skip link to jump past the navigation",
                                      "component/nav-item", "wrong match")
            updated = records.set_dispute_status(ws, rec["id"], "accepted",
                                                 note="confirmed upstream")
            self.assertEqual(updated["status"], "accepted")
            self.assertEqual(records.list_disputes(ws, status="open"), [])
            with self.assertRaises(ValueError):
                records.set_dispute_status(ws, rec["id"], "banana")


if __name__ == "__main__":
    unittest.main()
