"""Unit tests for the optional semantic layer (stdlib-only interpreter safe).

These run under plain python3 in the repo gates: tools/da_sem.py must import
without fastembed or numpy, so the kernel stays usable when the extras are
absent. The heavy paths are exercised by tools/sem_selftest.py (venv).
"""
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import da_sem  # noqa: E402


class TestSemanticLayer(unittest.TestCase):

    def test_import_without_extras(self):
        # importing da_sem must not require fastembed/numpy
        self.assertTrue(hasattr(da_sem, "rrf_fuse"))
        self.assertTrue(hasattr(da_sem, "render_lean"))

    def test_rrf_fuse_scores(self):
        fused = dict(da_sem.rrf_fuse(["a", "b", "c"], ["c", "a"]))
        self.assertAlmostEqual(fused["a"], 1 / 61 + 1 / 62, places=9)
        self.assertAlmostEqual(fused["b"], 1 / 62, places=9)
        self.assertAlmostEqual(fused["c"], 1 / 61 + 1 / 63, places=9)

    def test_rrf_fuse_order_stable(self):
        order = [k for k, _ in da_sem.rrf_fuse([], ["x", "y"])]
        self.assertEqual(order, ["x", "y"])

    def test_fts_query_escapes_and_dedupes(self):
        expr = da_sem._fts_query(["colr", "buton", "buton"])
        self.assertEqual(expr, '"colr" OR "buton"')
        self.assertEqual(da_sem._fts_query([]), "")

    def test_render_lean_shape(self):
        entry = {"id": "component/x", "title": "Thing", "summary": "Does things.",
                 "aliases": ["thang"]}
        text = da_sem.render_lean("artifact", entry)
        self.assertIn("Thing.", text)
        self.assertIn("Also known as: thang.", text)
        self.assertNotIn("ID:", text)

    def test_render_record_rich_shape(self):
        entry = {"id": "component/x", "title": "Thing", "summary": "Does things."}
        text = da_sem.render_record("artifact", entry)
        self.assertIn("ID: component/x", text)
        self.assertIn("Name: Thing", text)

    def test_collect_docs_classes_and_ids(self):
        pack_dir = os.path.join(ROOT, "packs", "triage")
        if not os.path.exists(pack_dir):
            self.skipTest("triage pack not present")
        _, entries = da_sem.collect_docs(pack_dir)
        classes = set(c for c, _, _ in entries)
        self.assertEqual(classes, {"canonical", "history"})
        ids = [e["id"] for _, _, e in entries]
        self.assertIn("component/btn", ids)
        self.assertGreater(len(entries), 50)


if __name__ == "__main__":
    unittest.main()
