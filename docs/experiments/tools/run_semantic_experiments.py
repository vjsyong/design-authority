#!/usr/bin/env python3
"""Run the pre-registered semantic-retrieval experiment (docs/experiments/01).

Engines: E0 kernel lexical, E1 FTS5-only, E2 hybrid (RRF), E2+ resolve assist.
Datasets: D1 goldens, D2 coverage sweep, D3 held-out paraphrase, D4 negatives.
Writes docs/experiments/01-semantic-retrieval-results.json and prints a table.

    .venv/bin/python3 docs/experiments/tools/run_semantic_experiments.py
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "kernel"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import da_sem  # noqa: E402
from design_authority.pack import Pack  # noqa: E402
from design_authority.resolve import resolve  # noqa: E402

PACK_DIR = os.path.join(ROOT, "packs", "triage")
INDEX = os.path.join(os.path.expanduser("~"), ".design-authority", "search",
                     "triage@0.12.1.sqlite")
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python3")
OUT = os.path.join(ROOT, "docs", "experiments", "01-semantic-retrieval-results.json")


def load_datasets():
    g = json.load(open(os.path.join(ROOT, "packs", "triage", "golden.json")))["cases"]
    d1 = [{"set": "D1", "query": c["problem"], "expect": c["expect"],
           "expect_id": c.get("expect_id")} for c in g]
    cov = json.load(open(os.path.join(ROOT, "docs", "synthesis", "triage",
                                      "coverage.json")))["cases"]
    d2 = [{"set": "D2", "query": c["ask"], "expect": "RESOLVED",
           "expect_id": c.get("expect_id")} for c in cov]
    d3 = json.load(open(os.path.join(ROOT, "docs", "experiments", "datasets",
                                     "paraphrase.json")))["cases"]
    d3 = [{"set": "D3", "query": c["query"], "expect": "RESOLVED",
           "expect_id": c["expect_id"],
           "probe": bool(c.get("implementation_probe"))} for c in d3]
    d4 = json.load(open(os.path.join(ROOT, "docs", "experiments", "datasets",
                                     "hard-negatives.json")))["cases"]
    return d1, d2, d3, d4


def outcome_id(r):
    res = r.get("resolution") or {}
    for key in ("artifact", "recipe", "fallback", "prohibition"):
        v = res.get(key)
        if isinstance(v, dict) and v.get("id"):
            return v["id"]
    return None


def main():
    pack = Pack(PACK_DIR)
    d1, d2, d3, d4 = load_datasets()
    all_labeled = d1 + d2 + d3
    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "pack": pack.identity(), "index": da_sem.info_index(INDEX)["meta"]}

    # warm the embedder once
    t0 = time.time()
    sem = da_sem.get_embedder()
    sem.embed_query("warm")
    report["warm_model_load_s"] = round(time.time() - t0, 2)

    def engine_top3(query):
        """Returns (e0, e1, e2) top-3 id lists."""
        e0 = [h["id"] for h in pack.search(query, limit=3)]
        qr = da_sem.query_index(INDEX, query, k=3, cls="canonical", embedder=sem,
                                legs=True)
        e1 = [c["id"] for c in qr["legs"]["fts5"][:3]]
        e2 = [c["id"] for c in qr["candidates"]]
        return e0, e1, e2

    # -- E0 vs E1 vs E2: top-3 recall per set --------------------------------
    recall = {}
    for name, rows in (("D1", d1), ("D2", d2), ("D3", d3)):
        counts = {"E0": 0, "E1": 0, "E2": 0}
        n = len([r for r in rows if r.get("expect_id")])
        details = []
        for r in rows:
            if not r.get("expect_id"):
                continue
            e0, e1, e2 = engine_top3(r["query"])
            ok = {"E0": r["expect_id"] in e0, "E1": r["expect_id"] in e1,
                  "E2": r["expect_id"] in e2}
            for k in counts:
                counts[k] += ok[k]
            details.append({"query": r["query"], "want": r["expect_id"],
                            "e0": e0, "e1": e1, "e2": e2, "ok": ok,
                            "probe": r.get("probe", False)})
        recall[name] = {"n": n, "counts": counts, "details": details}
    report["top3_recall"] = {k: {"n": v["n"], "counts": v["counts"]}
                             for k, v in recall.items()}

    # formal D3 stats exclude the two implementation probes (reported apart)
    d3_formal = [d for d in recall["D3"]["details"] if not d["probe"]]
    report["d3_formal"] = {
        "n": len(d3_formal),
        "E0": sum(1 for d in d3_formal if d["ok"]["E0"]),
        "E2": sum(1 for d in d3_formal if d["ok"]["E2"]),
        "E1": sum(1 for d in d3_formal if d["ok"]["E1"]),
    }

    # -- E2+ : resolve assist end-to-end (CLI subprocess), class safety ------
    safety = {"checked": 0, "class_changes": [], "undef_total": 0,
              "rescuable": [], "false_resolved": []}
    baseline = {}
    for r in all_labeled:
        base = resolve(pack, r["query"])
        base_out, base_id = base.get("outcome"), outcome_id(base)
        baseline[r["query"]] = (base_out, base_id)
        if r.get("expect") == "RESOLVED" and r.get("expect_id"):
            if base_out == "RESOLVED" and base_id != r["expect_id"]:
                safety["false_resolved"].append({"query": r["query"],
                                                 "got": base_id,
                                                 "want": r["expect_id"],
                                                 "arm": "E0"})
        if base_out == "UNDEFINED":
            safety["undef_total"] += 1

    # subprocess through the real CLI for every D3 query (assist on)
    for r in d3:
        p = subprocess.run([VENV_PY, os.path.join(ROOT, "tools", "da.py"),
                            "resolve", r["query"], "--assist", "semantic", "--json"],
                           capture_output=True, text=True, timeout=120)
        try:
            out = json.loads(p.stdout)
        except ValueError:
            continue
        b_out, b_id = baseline[r["query"]]
        safety["checked"] += 1
        if out.get("outcome") != b_out:
            safety["class_changes"].append({"query": r["query"],
                                            "off": b_out, "on": out.get("outcome")})
        if out.get("outcome") == "RESOLVED" and r.get("expect_id") \
                and outcome_id(out) != r["expect_id"]:
            safety["false_resolved"].append({"query": r["query"], "arm": "E2+",
                                             "got": outcome_id(out),
                                             "want": r["expect_id"]})
        blk = out.get("retrieval_assist") or {}
        if out.get("outcome") == "UNDEFINED" and blk.get("status") == "ok":
            got = [c["id"] for c in blk["candidates"]]
            if r.get("expect_id") in got:
                safety["rescuable"].append({"query": r["query"],
                                            "want": r["expect_id"],
                                            "top3": got[:3]})
    report["assist_safety"] = {k: v for k, v in safety.items() if k != "rescuable"}
    report["rescuable_undef"] = safety["rescuable"]

    # -- D4 hard negatives ----------------------------------------------------
    neg = []
    for c in d4:
        e0, e1, e2 = engine_top3(c["query"])
        bad = set(c["forbid_top3"])
        neg.append({"query": c["query"], "forbid": c["forbid_top3"],
                    "viol_e0": sorted(bad & set(e0)),
                    "viol_e1": sorted(bad & set(e1)),
                    "viol_e2": sorted(bad & set(e2)),
                    "e2_top3": e2})
    report["negatives"] = neg

    # -- latency --------------------------------------------------------------
    lat = {}
    t0 = time.time()
    for r in all_labeled + [{"query": c["query"]} for c in d4]:
        pack.search(r["query"], limit=8)
    lat["e0_search_ms_avg_all"] = round((time.time() - t0) * 1000 / (len(all_labeled) + len(d4)), 2)
    warm = []
    for _ in range(3):
        for r in d3:
            t0 = time.time()
            da_sem.query_index(INDEX, r["query"], k=8, embedder=sem)
            warm.append((time.time() - t0) * 1000)
    warm.sort()
    lat["e2_warm_ms_p50"] = round(warm[len(warm) // 2], 1)
    lat["e2_warm_ms_p95"] = round(warm[int(len(warm) * 0.95) - 1], 1)
    t0 = time.time()
    subprocess.run([VENV_PY, os.path.join(ROOT, "tools", "da_sem.py"), "query",
                    "a primary button", "--k", "3"], capture_output=True, timeout=120)
    lat["e2_cold_query_s"] = round(time.time() - t0, 2)
    t0 = time.time()
    da_sem.build_index(PACK_DIR, "/tmp/da_sem_timing.sqlite", quiet=True)
    lat["build_s"] = round(time.time() - t0, 1)
    lat["index_mb"] = da_sem.info_index(INDEX)["size_mb"]
    os.remove("/tmp/da_sem_timing.sqlite")
    report["latency"] = lat

    with open(OUT, "w") as fh:
        json.dump(report, fh, indent=1)

    # -- print -----------------------------------------------------------------
    print("top-3 recall (paired):")
    for k, v in report["top3_recall"].items():
        print("  %s n=%d  E0=%d  E1=%d  E2=%d" % (k, v["n"], v["counts"]["E0"],
                                                  v["counts"]["E1"], v["counts"]["E2"]))
    f = report["d3_formal"]
    print("  D3 formal (excl 2 probes) n=%d  E0=%d  E1=%d  E2=%d" %
          (f["n"], f["E0"], f["E1"], f["E2"]))
    print("assist safety: checked=%d class_changes=%d false_resolved=%d undef=%d rescuable=%d"
          % (safety["checked"], len(safety["class_changes"]),
             len(safety["false_resolved"]), safety["undef_total"],
             len(safety["rescuable"])))
    print("negatives: E0 violations=%d E1=%d E2=%d"
          % (sum(1 for n in neg if n["viol_e0"]), sum(1 for n in neg if n["viol_e1"]),
             sum(1 for n in neg if n["viol_e2"])))
    print("latency:", json.dumps(lat))
    print("report:", OUT)


if __name__ == "__main__":
    main()
