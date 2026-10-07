#!/usr/bin/env python3
"""Precedent-layer probe: asserts the negative-precedent machinery end to end.

Checks per synthesis pack: register counts, resolve-attachment for declined
asks (attached even when another outcome applies), absence on benign asks,
search surfacing, and gap/proposal warnings in a scratch workspace.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "kernel"))

from design_authority.pack import Pack            # noqa: E402
from design_authority.resolve import resolve      # noqa: E402
from design_authority import records              # noqa: E402

EXPECT_COUNTS = {"wink": 8, "leader": 10, "dominion": 7}
CASES = {
    "wink": [
        ("add a bar chart of activity", "precedent/declined-chart-treatments", None),
        ("add a dark mode theme", "precedent/declined-dark-mode", "FALLBACK"),
    ],
    "leader": [
        ("add a saving spinner", "precedent/declined-saving-state-spinner", None),
        ("delete a ritual permanently", "precedent/destructive-confirm-rejected", None),
    ],
    "dominion": [
        ("a progress ring for the day", "precedent/declined-progress-ring-badges", None),
        ("photo upload for the ritual", "precedent/declined-photographic-imagery", None),
        ("tabs across the top of the view", "precedent/declined-view-tabs-paging", None),
    ],
}
BENIGN = ("add a primary button to the page", "a form field for the borrower email")

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("ok " if cond else "FAIL", name, "  (%s)" % detail if detail else ""))


def main():
    packs = {}
    for name, count in EXPECT_COUNTS.items():
        pack = Pack(os.path.join(ROOT, "packs", name))
        packs[name] = pack
        check("%s precedents load (%d)" % (name, count), len(pack.precedents) == count,
              "got %d" % len(pack.precedents))
        ids = [p.get("id") for p in pack.precedents]
        check("%s ids unique + fields" % name,
              len(set(ids)) == len(ids) and all(
                  p.get("request") and p.get("decision") == "declined" and p.get("reason")
                  and p.get("try") for p in pack.precedents))

    for name, cases in CASES.items():
        for problem, want_id, want_outcome in cases:
            r = resolve(packs[name], problem)
            got_ids = [p["id"] for p in r.get("precedents", [])]
            ok = want_id in got_ids and (want_outcome is None or r["outcome"] == want_outcome)
            check("%s resolve('%s') attaches %s" % (name, problem, want_id.split("/")[-1]),
                  ok, "outcome=%s got=%s" % (r["outcome"], got_ids))

    for problem in BENIGN:
        r = resolve(packs["wink"], problem)
        check("wink benign '%s' has no precedents" % problem[:30], "precedents" not in r)

    hits = packs["wink"].search("bar chart", limit=12)
    check("wink search surfaces precedent kind",
          any(h["kind"] == "precedent" for h in hits),
          ",".join(h["id"] for h in hits[:4]))

    ws = tempfile.mkdtemp(prefix="da-precedent-")
    gap = records.add_gap(packs["dominion"], ws, "a toast when the save lands")
    check("gap carries precedent_warnings",
          gap.get("precedent_warnings") and
          gap["precedent_warnings"][0]["id"] == "precedent/declined-saving-and-celebration")
    prop = records.add_proposal(
        packs["dominion"], ws, gap["id"],
        {"problem": "toast confirmation when saved",
         "insufficiency": "no toast pattern is canonical",
         "reuse_case": "any consumer wanting confirmation",
         "composition_check": "notice exists but is in-flow",
         "proposed": {"id": "component/toast", "kind": "component", "title": "Toast"},
         "depends_on": ["component/notice"],
         "new_primitives": [], "tests": {"golden": [], "checks": ["t"]}})
    check("proposal carries precedent_warnings",
          prop.get("precedent_warnings") and
          any("Prior declines" in c for c in prop["review_checklist"]))

    print("\nprecedent probe: %d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
