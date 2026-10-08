#!/usr/bin/env python3
"""Verification experiment — Phase 0 baseline capture.

Snapshots hashes/immutable references for everything the experiment measures,
then writes docs/verification/raw/baseline-hashes.json (+ a markdown fragment
that 00-baseline.md embeds). Read-only: touches nothing it measures.
"""
import hashlib
import json
import os
import subprocess
import time

REPO = "/home/xrim/design-authority"
OUT = os.path.join(REPO, "docs", "verification")
RAW = os.path.join(OUT, "raw")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_hashes(root):
    """{relpath: sha256} for every file under root (sorted)."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            out[os.path.relpath(full, root)] = sha256(full)
    return out


def rollup(hashes):
    h = hashlib.sha256()
    for k in sorted(hashes):
        h.update(("%s %s\n" % (k, hashes[k])).encode())
    return h.hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True).stdout.strip()


data = {"captured": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())}

data["git"] = {"head": git("rev-parse", "HEAD"), "describe": git("describe", "--tags"),
               "branch": git("rev-parse", "--abbrev-ref", "HEAD")}
data["version_file"] = open(os.path.join(REPO, "VERSION")).read().strip()

data["kernel"] = tree_hashes(os.path.join(REPO, "kernel", "design_authority"))
data["tools"] = {f: sha256(os.path.join(REPO, "tools", f))
                 for f in sorted(os.listdir(os.path.join(REPO, "tools")))
                 if os.path.isfile(os.path.join(REPO, "tools", f))}

data["packs"] = {}
for p in ("wink", "leader", "dominion", "triage", "triage-evolution"):
    d = os.path.join(REPO, "packs", p)
    if os.path.isdir(d):
        hs = tree_hashes(d)
        data["packs"][p] = {"rollup": rollup(hs), "files": hs}

data["builds"] = {}
for b in ("cadence-wink", "cadence-leader", "cadence-dominion",
          "cadence3-wink", "cadence3-leader", "cadence3-dominion"):
    d = os.path.join(REPO, "examples", b)
    if not os.path.isdir(d):
        continue
    hs = tree_hashes(d)
    data["builds"][b] = {"rollup": rollup(hs), "n_files": len(hs),
                         "files": {k: v for k, v in hs.items()}}

data["review_data"] = {}
vd = os.path.join(REPO, "docs", "synthesis", "review-app", "data", "stress-verdicts.json")
if os.path.exists(vd):
    data["review_data"]["stress-verdicts.json"] = sha256(vd)
fd = os.path.join(REPO, "docs", "synthesis", "review-app", "data", "feedback.json")
if os.path.exists(fd):
    data["review_data"]["feedback.json"] = sha256(fd)

# resolution behavior snapshot: run the first N golden asks per pack through resolve
snap = {"captured": data["captured"], "results": {}}
for p in ("wink", "leader", "dominion"):
    packdir = os.path.join(REPO, "packs", p)
    golden = os.path.join(packdir, "golden.json")
    if not os.path.exists(golden):
        continue
    g = json.load(open(golden))
    cases = (g.get("cases") or g.get("golden") or [])[:10]
    rows = []
    for c in cases:
        r = subprocess.run(["python3", os.path.join(REPO, "tools", "da.py"),
                            "--pack", packdir, "resolve", c["problem"], "--json"],
                           capture_output=True, text=True)
        try:
            out = json.loads(r.stdout)
            rows.append({"problem": c["problem"], "outcome": out.get("outcome"),
                         "resolution_id": ((out.get("resolution") or {}).get("artifact") or
                                           (out.get("resolution") or {}).get("recipe") or
                                           (out.get("resolution") or {}).get("fallback") or
                                           {}).get("id")})
        except Exception as exc:
            rows.append({"problem": c["problem"], "error": str(exc)})
    snap["results"][p] = rows
data["resolution_snapshot"] = snap

os.makedirs(RAW, exist_ok=True)
with open(os.path.join(RAW, "baseline-hashes.json"), "w") as fh:
    json.dump(data, fh, indent=1)

print("git:", data["git"]["head"][:12], data["git"]["describe"], "| VERSION:", data["version_file"])
for p, v in data["packs"].items():
    print("pack", p, v["rollup"][:16], "(%d files)" % len(v["files"]))
for b, v in data["builds"].items():
    print("build", b, v["rollup"][:16], "(%d files)" % v["n_files"])
for p, rows in snap["results"].items():
    print("resolve-snapshot", p, len(rows), "asks ->",
          {r.get("outcome") for r in rows})
