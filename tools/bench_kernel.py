#!/usr/bin/env python3
"""Runtime profile of the Design Authority kernel (read-only).

Measures: pack load, resolve battery, search, inspect, synthetic pack scaling,
the validator subprocess share, CLI cold-start overhead, MCP smoke, and peak RSS.
Run from the repo root:  python3 tools/bench_kernel.py
"""
import cProfile
import io
import json
import os
import pstats
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "kernel"))
from design_authority.pack import Pack          # noqa: E402
from design_authority.resolve import resolve    # noqa: E402

PACK = os.path.join(ROOT, "packs/triage")


def ns():
    return time.perf_counter_ns()


def ms(v):
    return v / 1e6


def stats_line(label, times):
    s = sorted(times)
    return "%-28s n=%3d  mean %7.3f ms  p50 %7.3f  p95 %7.3f  max %7.3f" % (
        label, len(times), ms(statistics.mean(times)), ms(s[len(s) // 2]),
        ms(s[min(int(len(s) * 0.95), len(s) - 1)]), ms(max(s)))


print("=" * 78)
print("Design Authority kernel profile  (python %s)" % sys.version.split()[0])
print("=" * 78)

# ---- 1) pack load
loads = []
for i in range(6):
    t = ns()
    pack = Pack(PACK)
    loads.append(ns() - t)
print(stats_line("pack load (cold+warm)", loads))

# ---- 2) battery of asks
asks = []
g = json.load(open(os.path.join(PACK, "golden.json")))
asks += [c["problem"] for c in g["cases"]]
cov = os.path.join(ROOT, "docs/synthesis/triage/coverage.json")
if os.path.exists(cov):
    cj = json.load(open(cov))


    def walk(o, key=None):
        out = []
        if isinstance(o, str):
            if key in ("ask", "asks", "problem", "queries", "phrase") and " " in o and len(o) < 90:
                out.append(o)
        elif isinstance(o, list):
            for x in o:
                out += walk(x)
        elif isinstance(o, dict):
            for k, v in o.items():
                out += walk(v, k)
        return out
    asks += walk(cj)
asks = list(dict.fromkeys(asks))[:260]
print("battery: %d asks (golden + coverage)" % len(asks))

times = []
for a in asks:
    t = ns()
    resolve(pack, a)
    times.append(ns() - t)
print(stats_line("resolve", times))

# ---- 3) search + inspect
sq = ["button", "banner", "dark mode", "table", "timeline", "kicker", "progress"]
st = []
for q in sq:
    t = ns()
    pack.search(q, limit=12)
    st.append(ns() - t)
print(stats_line("search", st))
ids = [a["id"] for a in [pack.by_id[k] for k in list(pack.by_id)[:20]]]
it = []
for i in ids:
    t = ns()
    pack.by_id[i]
    it.append(ns() - t)
print(stats_line("inspect (by_id hit)", it))

# ---- 4) cProfile of the resolve battery
pr = cProfile.Profile()
pr.enable()
for a in asks:
    resolve(pack, a)
pr.disable()
sio = io.StringIO()
pstats.Stats(pr, stream=sio).sort_stats("cumulative").print_stats(12)
prof = sio.getvalue()
print()
print("--- resolve profile (cumulative, top 12) ---")
for line in prof.splitlines():
    if "function calls" in line or ".py:" in line:
        print(line.strip()[:110])

# ---- 5) synthetic pack scaling
tmp = tempfile.mkdtemp(prefix="da-bench-")
art_path = os.path.join(PACK, "artifacts.json")
raw = json.load(open(art_path))
items = raw["artifacts"] if isinstance(raw, dict) and "artifacts" in raw else raw
base_n = len(items)
for mult in (1, 4, 10):
    work = os.path.join(tmp, "x%d" % mult)
    shutil.copytree(PACK, work)
    grown = list(items)
    for m in range(2, mult + 1):
        for it0 in items:
            d = dict(it0)
            d["id"] = it0["id"] + "-x%d" % m
            grown.append(d)
    out = raw if isinstance(raw, dict) else grown
    if isinstance(raw, dict):
        out = dict(raw)
        out["artifacts"] = grown
    json.dump(out, open(os.path.join(work, "artifacts.json"), "w"))
    t = ns()
    big = Pack(work)
    lt = ns() - t
    sub = asks[:60]
    tt = []
    for a in sub:
        t = ns()
        resolve(big, a)
        tt.append(ns() - t)
    print("scaling x%-2d (%4d artifacts): load %6.2f ms | resolve mean %7.3f ms  p95 %7.3f ms"
          % (mult, len(grown), ms(lt), ms(statistics.mean(tt)), ms(sorted(tt)[-max(1, int(len(tt) * 0.05))])))

# ---- 6) validator subprocess share
vj = json.load(open(os.path.join(PACK, "validators.json")))
print()
print("validators.json:", json.dumps(vj)[:400])
t = ns()
subprocess.run([sys.executable, "tools/da.py", "--pack", "packs/triage", "validate",
                "examples/designauthority-site"], cwd=ROOT, capture_output=True, text=True)
print("validate (concept site, end to end): %.0f ms" % ms(ns() - t))

# ---- 7) CLI cold start
cold = []
for i in range(3):
    t = ns()
    subprocess.run([sys.executable, "tools/da.py", "resolve", "a primary button"],
                   cwd=ROOT, capture_output=True, text=True)
    cold.append(ns() - t)
print(stats_line("CLI cold (resolve)", cold))

# ---- 8) MCP smoke (server startup + full battery)
t = ns()
r = subprocess.run([sys.executable, "tools/mcp_smoke.py"], cwd=ROOT, capture_output=True, text=True)
print("MCP smoke (startup + 20 checks): %.0f ms | %s" % (ms(ns() - t), (r.stdout or "").strip().splitlines()[-1][:60]))

# ---- 9) peak RSS
r = subprocess.run(["/usr/bin/time", "-v", sys.executable, "tools/da.py", "overview"],
                   cwd=ROOT, capture_output=True, text=True)
for line in (r.stderr or "").splitlines():
    if "Maximum resident" in line:
        print(line.strip())
