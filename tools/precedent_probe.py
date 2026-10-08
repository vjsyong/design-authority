#!/usr/bin/env python3
"""Precedent + candidate probe: scope-aware verdicts, lenient doctrine.

Asserts per synthesis pack: register counts, mandatory scope/grounds fields,
governs verdicts on policy declines, `outside` verdicts for boundary-exempt
asks (the tick regression), retired declines deferring to undefined,
candidates attaching on UNDEFINED, search kinds, gap/proposal warnings.
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

EXPECT = {"wink": (2, 1), "leader": (4, 0), "dominion": (6, 3)}

GOVERNED = {
    "wink": [("photo upload for the ritual", "precedent/declined-photographic-imagery")],
    "leader": [("add a saving spinner", "precedent/declined-motion-feedback"),
               ("delete a ritual permanently", "precedent/destructive-confirm-rejected")],
    "dominion": [("a progress ring for the day", "precedent/declined-progress-ring"),
                 ("a toast saying logged", "precedent/declined-celebration-motion-toasts")],
}
OUTSIDE = {
    "wink": ["a check control to log a ritual"],
    "leader": ["a check control to mark a ritual done"],
}
DEFERRED = {
    "wink": [("add a dark mode theme", "FALLBACK"),
             ("add a bar chart of activity", None)],
    "dominion": [("tabs across the top of the view", None)],
}
CANDIDATES = {
    "wink": [("pagination for older entries", "candidate/pager-composition")],
    "dominion": [("pagination for older entries", "candidate/paging-composition"),
                 ("a big streak counter", "candidate/streak-readout-composition")],
}
BENIGN = ("add a primary button to the page", "a form field for the borrower email")

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("ok " if cond else "FAIL", name, "  (%s)" % detail if detail else ""))


def main():
    packs = {}
    for name, (np_, nc) in EXPECT.items():
        pack = Pack(os.path.join(ROOT, "authorities", name))
        packs[name] = pack
        check("%s registers load (prec=%d, cand=%d)" % (name, np_, nc),
              len(pack.precedents) == np_ and len(pack.candidates) == nc,
              "got prec=%d cand=%d" % (len(pack.precedents), len(pack.candidates)))
        check("%s schema: grounds + scope + boundary required" % name,
              all(p.get("grounds") and (p.get("scope") or {}).get("domains")
                  and (p.get("scope") or {}).get("boundary") for p in pack.precedents))
        check("%s schema: candidates carry promote_when" % name,
              all(c.get("promote_when") for c in pack.candidates))
        ids = [p.get("id") for p in pack.precedents + pack.candidates]
        check("%s ids unique" % name, len(set(ids)) == len(ids))

    for name, cases in GOVERNED.items():
        for problem, want_id in cases:
            r = resolve(packs[name], problem)
            prec = r.get("precedents") or []
            ok = any(p["id"] == want_id and p["verdict"] == "governs" for p in prec)
            check("%s governs: %s -> %s" % (name, problem[:34], want_id.split("/")[-1]),
                  ok, "got %s" % [(p["id"], p["verdict"]) for p in prec])

    for name, asks in OUTSIDE.items():
        for ask in asks:
            res = packs[name].precedent_matches(ask)
            ok = any(m["verdict"] == "outside" for m in res) and \
                 not any(m["verdict"] == "governs" for m in res)
            check("%s outside (tick regression): %s" % (name, ask[:34]),
                  ok, "got %s" % [(m["record"]["id"], m["verdict"]) for m in res])

    for name, cases in DEFERRED.items():
        for problem, want_outcome in cases:
            r = resolve(packs[name], problem)
            ok = not r.get("precedents") and (want_outcome is None or r["outcome"] == want_outcome)
            check("%s deferred->undefined: %s" % (name, problem[:34]), ok,
                  "outcome=%s prec=%s" % (r["outcome"], r.get("precedents")))

    for name, cases in CANDIDATES.items():
        for problem, want_id in cases:
            r = resolve(packs[name], problem)
            ids = [c["id"] for c in r.get("candidates", [])]
            check("%s candidate: %s -> %s" % (name, problem[:34], want_id.split("/")[-1]),
                  r["outcome"] == "UNDEFINED" and want_id in ids,
                  "outcome=%s got=%s" % (r["outcome"], ids))

    for problem in BENIGN:
        r = resolve(packs["wink"], problem)
        check("wink benign '%s' clean" % problem[:30],
              "precedents" not in r and "candidates" not in r)

    hits = packs["leader"].search("spinner", limit=12)
    check("leader search surfaces precedent kind",
          any(h["kind"] == "precedent" for h in hits))
    hits = packs["wink"].search("pagination for older entries", limit=12)
    check("wink search surfaces candidate kind",
          any(h["kind"] == "candidate" for h in hits))

    ws = tempfile.mkdtemp(prefix="da-precedent-")
    gap = records.add_gap(packs["dominion"], ws, "a toast when the save lands")
    check("gap carries scope-verdict warnings",
          bool(gap.get("precedent_warnings")) and
          gap["precedent_warnings"][0]["id"] == "precedent/declined-celebration-motion-toasts"
          and gap["precedent_warnings"][0]["verdict"] == "governs")
    prop = records.add_proposal(
        packs["dominion"], ws, gap["id"],
        {"problem": "toast confirmation when saved",
         "insufficiency": "no toast pattern is canonical",
         "reuse_case": "any consumer wanting confirmation",
         "composition_check": "notice exists but is in-flow",
         "proposed": {"id": "component/toast", "kind": "component", "title": "Toast"},
         "depends_on": ["component/notice"],
         "new_primitives": [], "tests": {"golden": [], "checks": ["t"]}})
    check("proposal carries verdict-aware checklist",
          prop.get("precedent_warnings") and
          any("governs" in c for c in prop["review_checklist"]))

    print("\nprecedent probe: %d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
