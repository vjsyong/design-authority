#!/usr/bin/env python3
"""da_sem — optional semantic discovery for Design Authority packs.

A retrieval-side extension, never an authority. It proposes candidate records
from a pack; the frozen resolver still decides every outcome. Design rules:

  * Retrieval never establishes authority. A similarity of 0.9 means
    "inspect this candidate", never RESOLVED.
  * Jurisdictions stay separate. `canonical` records are the current binding
    family; `history` records (precedents, candidates) are searchable but are
    never treated as canon.
  * Deterministic in practice: the index records the model name/version and a
    pack content hash; the same text embeds to the same vector on the same
    runtime, and the whole index is regenerable from the pack.

Stack: SQLite FTS5 (BM25) + FastEmbed `BAAI/bge-small-en-v1.5` (ONNX, CPU,
384-d) + NumPy cosine, fused with Reciprocal Rank Fusion (RRF, k=60).
Brute-force matrix multiply; the packs are small by design.

Commands

    build  --pack DIR [--index PATH] [--model NAME]
    query  "QUERY" [--index PATH] [--k N] [--class canonical|history|all]
    info   [--index PATH]
    stale  [--index PATH]           # exit 3 when the pack changed since build
    serve  [--index PATH]           # JSON-lines on stdio; model loaded once

Index location: --index, else $DA_SEARCH_INDEX, else
~/.design-authority/search/<pack-id>@<version>.sqlite
"""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "kernel"))

try:
    from design_authority.pack import Pack, norm_tokens, norm_phrase
except Exception:  # pragma: no cover - kernel must exist beside this tool
    print(json.dumps({"error": "kernel not found beside tools/da_sem.py"}))
    raise SystemExit(4)

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
RRF_K = 60
READY_FAMILIES = ("artifacts.json", "rules.json", "recipes.json",
                  "fallbacks.json", "prohibitions.json", "precedents.json",
                  "candidates.json", "authority.json")


def _deps():
    try:
        import numpy as np  # noqa: F401
        from fastembed import TextEmbedding  # noqa: F401
        return True
    except ImportError:
        return False


def _dep_error():
    return {
        "error": "semantic extras not installed",
        "install": "python3 -m pip install fastembed numpy",
        "or_use": "the lexical tools: da search / da resolve (unchanged)",
    }


def pack_hash(pack_dir):
    h = hashlib.sha256()
    for name in READY_FAMILIES:
        path = os.path.join(pack_dir, name)
        if os.path.exists(path):
            h.update(name.encode())
            h.update(b"\0")
            h.update(open(path, "rb").read())
            h.update(b"\0")
    return h.hexdigest()


def default_index_path(pack_dir):
    pack = Pack(pack_dir)
    ident = pack.identity()
    base = os.environ.get("DA_SEARCH_INDEX")
    if base:
        return base
    return os.path.join(os.path.expanduser("~"), ".design-authority", "search",
                        "%s@%s.sqlite" % (ident["authority"], ident["version"]))


# ---------------------------------------------------------------- rendering --
def render_lean(kind, e):
    """Compact semantic text: what the record is and what it answers to.
    (The rich rendering stays for the lexical leg.)"""
    parts = ["%s." % (e.get("title") or e.get("id"))]
    if e.get("summary"):
        parts.append(str(e["summary"]))
    al = e.get("aliases") or e.get("matches") or []
    if al:
        parts.append("Also known as: " + ", ".join(al) + ".")
    body = e.get("body") or {}
    for key in ("class", "statement"):
        v = body.get(key) or e.get(key)
        if isinstance(v, str) and v:
            parts.append(v + ".")
    if kind == "rule" and e.get("fix"):
        parts.append(e["fix"])
    if kind == "precedent":
        for key in ("request", "reason"):
            if e.get(key):
                parts.append(str(e[key]))
    if kind == "candidate" and e.get("request"):
        parts.append(str(e["request"]))
    return " ".join(parts)


def render_record(kind, e):
    lines = ["ID: %s" % e.get("id"), "Kind: %s" % kind,
             "Name: %s" % (e.get("title") or "")]
    aliases = e.get("aliases") or e.get("matches") or []
    if aliases:
        lines.append("Aliases: " + "; ".join(aliases))
    for key, label in (("summary", "Summary"), ("description", "Description")):
        if e.get(key):
            lines.append("%s: %s" % (label, e[key]))
    body = e.get("body") or {}
    for key in ("class", "group", "statement", "quote"):
        v = body.get(key, e.get(key) if key == "statement" else None)
        if isinstance(v, str) and v:
            lines.append("%s: %s" % (key.capitalize(), v))
    for key, label in (("states", "States"), ("a11y", "Accessibility"),
                       ("do", "Do"), ("dont", "Don't"), ("constraints", "Constraints"),
                       ("scope", "Scope"), ("needs", "Needs"), ("try", "Try"),
                       ("promote_when", "Promote when")):
        v = body.get(key) if isinstance(body, dict) else None
        v = v if v is not None else e.get(key)
        if isinstance(v, list) and v:
            lines.append("%s: %s" % (label, "; ".join(str(x) for x in v)))
        elif isinstance(v, str) and v:
            lines.append("%s: %s" % (label, v))
    if kind == "rule":
        for key, label in (("severity", "Severity"), ("fix", "Fix")):
            if e.get(key):
                lines.append("%s: %s" % (label, e[key]))
    if kind == "prohibition":
        for key, label in (("signals", "Signals"), ("signals_all", "Signals (all)")):
            v = e.get(key)
            if v:
                lines.append("%s: %s" % (label, "; ".join(
                    "+".join(g) if isinstance(g, list) else str(g) for g in v)))
    if kind in ("precedent",):
        for key, label in (("request", "Request"), ("decision", "Decision"),
                           ("reason", "Reason"), ("grounds", "Grounds")):
            if e.get(key):
                lines.append("%s: %s" % (label, e[key]))
    if kind == "candidate" and e.get("request"):
        lines.append("Request: %s" % e["request"])
    src = e.get("source") or {}
    if src.get("path"):
        lines.append("Source: %s" % src["path"])
    return "\n".join(lines)


def collect_docs(pack_dir):
    pack = Pack(pack_dir)
    out = []
    for a in pack.artifacts:
        out.append(("canonical", "artifact", a))
    for r in pack.rules:
        out.append(("canonical", "rule", r))
    for r in pack.recipes:
        out.append(("canonical", "recipe", r))
    for f in pack.fallbacks:
        out.append(("canonical", "fallback", f))
    for p in pack.prohibitions:
        out.append(("canonical", "prohibition", p))
    for p in pack.precedents:
        out.append(("history", "precedent", p))
    for c in pack.candidates:
        out.append(("history", "candidate", c))
    return pack, out


# ------------------------------------------------------------------ engines --
class Embedder(object):
    def __init__(self, model_name=DEFAULT_MODEL):
        from fastembed import TextEmbedding
        self.model_name = model_name
        self.model = TextEmbedding(model_name=model_name)

    def embed(self, texts):
        import numpy as np
        arr = np.asarray(list(self.model.embed(texts)), dtype=np.float32)
        return arr

    def embed_query(self, text):
        import numpy as np
        v = np.asarray(list(self.model.query_embed(text))[0], dtype=np.float32)
        return v


def _fts_query(qtoks):
    # OR of quoted tokens; FTS5 unicode61 tokenizer handles the rest.
    seen, parts = set(), []
    for t in qtoks:
        if t and t not in seen:
            seen.add(t)
            parts.append('"%s"' % t.replace('"', '""'))
    return " OR ".join(parts)


_EMB_CACHE = {}


def get_embedder(model_name=DEFAULT_MODEL):
    """One embedder per process (model load is the only real cost)."""
    key = model_name
    if key not in _EMB_CACHE:
        _EMB_CACHE[key] = Embedder(model_name)
    return _EMB_CACHE[key]


def rrf_fuse(lex_ids, sem_ids, k=RRF_K):
    """Reciprocal Rank Fusion over two ranked id lists. Pure; order-stable."""
    scores = {}
    for ranked in (lex_ids, sem_ids):
        for i, cid in enumerate(ranked):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + i + 1)
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


def build_index(pack_dir, index_path, model_name=DEFAULT_MODEL, quiet=False):
    t0 = time.time()
    pack, entries = collect_docs(pack_dir)
    ident = pack.identity()
    phash = pack_hash(pack_dir)

    emb = Embedder(model_name)
    texts = [render_record(kind, e) for _, kind, e in entries]
    lean = [render_lean(kind, e) for _, kind, e in entries]
    t_embed = time.time()
    vecs = emb.embed(lean)

    tmp = index_path + ".tmp"
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    if os.path.exists(tmp):
        os.remove(tmp)
    con = sqlite3.connect(tmp)
    con.executescript("""
        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE docs (rowid_ INTEGER PRIMARY KEY, id TEXT UNIQUE, kind TEXT,
                           class TEXT, title TEXT, text TEXT, toks TEXT, vec BLOB);
        CREATE VIRTUAL TABLE docs_fts USING fts5(id, toks, title, tokenize='unicode61');
    """)
    for ridx, ((cls, kind, e), text) in enumerate(zip(entries, texts), start=1):
        toks = " ".join(norm_tokens(text))
        vec = vecs[ridx - 1].tobytes()
        con.execute("INSERT INTO docs VALUES (?,?,?,?,?,?,?,?)",
                    (ridx, e["id"], kind, cls, e.get("title") or e["id"], text, toks, vec))
        con.execute("INSERT INTO docs_fts VALUES (?,?,?)",
                    (e["id"], toks, e.get("title") or e["id"]))
    from fastembed import TextEmbedding as _T  # noqa: F401  (version probe)
    import importlib.metadata as _md
    try:
        fev = _md.version("fastembed")
    except Exception:
        fev = "unknown"
    meta = {"format": "da-sem/1", "pack_id": ident["authority"],
            "pack_version": ident["version"], "pack_hash": phash,
            "model": model_name, "dim": str(vecs.shape[1]), "fastembed": fev,
            "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "counts": json.dumps({"canonical": sum(1 for c, _, _ in entries if c == "canonical"),
                                  "history": sum(1 for c, _, _ in entries if c == "history")})}
    con.executemany("INSERT INTO meta VALUES (?,?)", list(meta.items()))
    con.commit()
    con.close()
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    os.replace(tmp, index_path)
    info = dict(meta)
    info["index"] = index_path
    info["build_seconds"] = round(time.time() - t0, 2)
    info["embed_seconds"] = round(time.time() - t_embed, 2)
    info["size_mb"] = round(os.path.getsize(index_path) / 1e6, 2)
    info["docs"] = len(entries)
    if not quiet:
        print(json.dumps(info, indent=1))
    return info


def _load_db(index_path):
    con = sqlite3.connect(index_path)
    con.row_factory = sqlite3.Row
    meta = {r["key"]: r["value"] for r in con.execute("SELECT key, value FROM meta")}
    return con, meta


def query_index(index_path, query, k=8, cls="canonical", embedder=None, legs=False):
    import numpy as np
    t0 = time.time()
    con, meta = _load_db(index_path)
    qts = norm_tokens(query)
    fts_expr = _fts_query(qts)

    lex = []
    if fts_expr:
        for r in con.execute(
                "SELECT id, bm25(docs_fts) AS b FROM docs_fts "
                "WHERE docs_fts MATCH ? ORDER BY b LIMIT 50", (fts_expr,)):
            lex.append({"id": r["id"], "bm25": round(-r["b"], 3)})
    lex_rank = {e["id"]: i + 1 for i, e in enumerate(lex)}

    rows = con.execute("SELECT id, kind, class, title, vec, text FROM docs").fetchall()
    ids = [r["id"] for r in rows]
    mat = np.vstack([np.frombuffer(r["vec"], dtype=np.float32) for r in rows])
    mat /= np.maximum(np.linalg.norm(mat, axis=1, keepdims=True), 1e-12)

    if embedder is None:
        embedder = get_embedder(meta["model"])
    q = embedder.embed_query(query)
    q = q / max(float(np.linalg.norm(q)), 1e-12)
    sims = mat @ q
    order = list(np.argsort(-sims))
    sem = [{"id": ids[i], "cos": round(float(sims[i]), 4)} for i in order]
    sem_rank = {e["id"]: i + 1 for i, e in enumerate(sem)}

    fused = rrf_fuse([e["id"] for e in lex], [e["id"] for e in sem])
    meta_by_id = {r["id"]: r for r in rows}
    out = []
    for cid, score in fused:
        r = meta_by_id[cid]
        if cls != "all" and r["class"] != cls:
            continue
        hit = {"id": cid, "kind": r["kind"], "class": r["class"], "title": r["title"],
               "lex_rank": lex_rank.get(cid), "bm25": next((e["bm25"] for e in lex if e["id"] == cid), None),
               "sem_rank": sem_rank.get(cid), "cos": next((e["cos"] for e in sem if e["id"] == cid), None),
               "rrf": round(score, 6)}
        if legs:
            hit["snippet"] = (r["text"] or "")[:160]
        out.append(hit)
        if len(out) >= k:
            break

    con.close()
    result = {
        "engine": "hybrid:fts5-bm25 + %s(%sd) + rrf(k=%d)" % (meta["model"], meta["dim"], RRF_K),
        "index": {"path": index_path, "pack_id": meta["pack_id"],
                  "pack_version": meta["pack_version"], "built_at": meta["built_at"]},
        "query": query, "class": cls, "k": k,
        "candidates": out,
        "query_ms": round((time.time() - t0) * 1000, 1),
        "note": "retrieval signal only; inspect each id; resolution stays lexical",
    }
    if legs:
        result["legs"] = {"fts5": lex[:20], "semantic": sem[:20]}
    return result


def info_index(index_path):
    con, meta = _load_db(index_path)
    counts = json.loads(meta.get("counts", "{}"))
    con.close()
    return {"index": index_path, "meta": meta, "counts": counts,
            "size_mb": round(os.path.getsize(index_path) / 1e6, 2)}


def stale_index(index_path):
    con, meta = _load_db(index_path)
    con.close()
    current = pack_hash(os.path.join(ROOT, "packs", meta["pack_id"]))
    return {"stale": current != meta["pack_hash"], "pack_hash": meta["pack_hash"],
            "current": current}


# -------------------------------------------------------------------- serve --
def serve(index_path):
    """JSON-lines stdio server: {"cmd": "query", "query": ..., "k": ..., "class": ...}"""
    embedder = None
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            cmd = req.get("cmd")
            if cmd == "ping":
                resp = {"ok": True}
            elif cmd == "query":
                if embedder is None:
                    _, meta = _load_db(index_path)
                    embedder = Embedder(meta["model"])
                resp = query_index(index_path, req["query"], k=int(req.get("k", 8)),
                                   cls=req.get("class", "canonical"), embedder=embedder)
            elif cmd == "info":
                resp = info_index(index_path)
            else:
                resp = {"error": "unknown cmd: %s" % cmd}
        except Exception as exc:  # keep the sidecar alive; report per request
            resp = {"error": "%s: %s" % (type(exc).__name__, exc)}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="da_sem", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("build")
    p.add_argument("--pack", required=True)
    p.add_argument("--index", default=None)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--quiet", action="store_true")

    p = sub.add_parser("query")
    p.add_argument("query")
    p.add_argument("--index", default=None)
    p.add_argument("--pack", default=None)
    p.add_argument("--k", type=int, default=8)
    p.add_argument("--class", dest="cls", default="canonical",
                   choices=["canonical", "history", "all"])
    p.add_argument("--legs", action="store_true")

    p = sub.add_parser("info"); p.add_argument("--index", default=None); p.add_argument("--pack", default=None)
    p = sub.add_parser("stale"); p.add_argument("--index", default=None); p.add_argument("--pack", default=None)
    p = sub.add_parser("serve"); p.add_argument("--index", default=None); p.add_argument("--pack", default=None)

    args = ap.parse_args(argv)

    if not _deps():
        print(json.dumps(_dep_error(), indent=1))
        return 4

    if args.cmd == "build":
        index = args.index or default_index_path(args.pack)
        build_index(args.pack, index, model_name=args.model, quiet=args.quiet)
        return 0

    idx = args.index or os.environ.get("DA_SEARCH_INDEX")
    if not idx and getattr(args, "pack", None):
        idx = default_index_path(args.pack)
    if not idx:
        search_dir = os.path.join(os.path.expanduser("~"), ".design-authority", "search")
        found = sorted(f for f in os.listdir(search_dir) if f.endswith(".sqlite")) \
            if os.path.isdir(search_dir) else []
        if len(found) == 1:
            idx = os.path.join(search_dir, found[0])
        else:
            print(json.dumps({"error": "no index; pass --index/--pack, set DA_SEARCH_INDEX, "
                                       "or build one", "available": found}))
            return 4
    if not os.path.exists(idx):
        print(json.dumps({"error": "index not found: %s" % idx,
                          "hint": "python3 tools/da_sem.py build --pack packs/<name>"}))
        return 4

    if args.cmd == "query":
        print(json.dumps(query_index(idx, args.query, k=args.k, cls=args.cls,
                                     legs=args.legs), indent=1))
    elif args.cmd == "info":
        print(json.dumps(info_index(idx), indent=1))
    elif args.cmd == "stale":
        st = stale_index(idx)
        print(json.dumps(st, indent=1))
        return 3 if st["stale"] else 0
    elif args.cmd == "serve":
        serve(idx)
    return 0


if __name__ == "__main__":
    sys.exit(main())
