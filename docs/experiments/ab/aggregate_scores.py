#!/usr/bin/env python3
"""Experiment 04 scorer: join the blind review with the hidden mapping.

Reads review/score.json and _mapping.json, prints per-condition aggregates
and the H1-H4 table, writes ab/score-summary.json.

    python3 aggregate_scores.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    score = json.load(open(os.path.join(HERE, "review", "score.json")))
    mapping = json.load(open(os.path.join(HERE, "_mapping.json")))

    rows = []
    for art in score["artifacts"]:
        cell = mapping[art["id"]]
        cond = "B (lexical+semantic)" if "-b" in cell else "A (lexical)"
        needs = art.get("needs") or []
        total = len(needs)
        correct = sum(1 for n in needs if n.get("correct"))
        rows.append({
            "art": art["id"], "cell": cell, "cond": cond, "brief": art["brief"],
            "needs_total": total, "needs_correct": correct,
            "false_authority": len(art.get("false_authority") or []),
            "unnecessary_gaps": len(art.get("unnecessary_gaps") or []),
            "corrections": len(art.get("corrections_required") or []),
            "gap_filed": len((art.get("gap_detection") or {}).get("filed_correctly") or []),
            "gap_missed": len((art.get("gap_detection") or {}).get("missed") or []),
            "corrections_list": art.get("corrections_required") or [],
        })

    def agg(rows):
        n = len(rows)
        return {
            "artifacts": n,
            "needs_correct": sum(r["needs_correct"] for r in rows),
            "needs_total": sum(r["needs_total"] for r in rows),
            "correct_rate": round(sum(r["needs_correct"] for r in rows) /
                                  max(1, sum(r["needs_total"] for r in rows)), 3),
            "false_authority": sum(r["false_authority"] for r in rows),
            "unnecessary_gaps": sum(r["unnecessary_gaps"] for r in rows),
            "corrections": sum(r["corrections"] for r in rows),
            "corrections_per_artifact": round(sum(r["corrections"] for r in rows) / max(1, n), 2),
            "gap_filed": sum(r["gap_filed"] for r in rows),
            "gap_missed": sum(r["gap_missed"] for r in rows),
        }

    A = [r for r in rows if r["cond"].startswith("A")]
    B = [r for r in rows if r["cond"].startswith("B")]
    summary = {"per_artifact": rows, "A": agg(A), "B": agg(B)}
    json.dump(summary, open(os.path.join(HERE, "score-summary.json"), "w"), indent=1)

    print("%-7s %-22s brief needs FA ugap corr" % ("art", "condition"))
    for r in rows:
        print("%-7s %-22s %5s %2d/%2d %2d  %2d   %2d" % (
            r["art"], r["cond"], r["brief"], r["needs_correct"], r["needs_total"],
            r["false_authority"], r["unnecessary_gaps"], r["corrections"]))
    print()
    for name, a in (("A lexical", summary["A"]), ("B +semantic", summary["B"])):
        print("%-12s correct %d/%d (%.0f%%) | false_auth %d | unnec_gaps %d | corrections %d (%.2f/artifact) | gaps filed %d missed %d" % (
            name, a["needs_correct"], a["needs_total"], 100 * a["correct_rate"],
            a["false_authority"], a["unnecessary_gaps"], a["corrections"],
            a["corrections_per_artifact"], a["gap_filed"], a["gap_missed"]))


if __name__ == "__main__":
    main()
