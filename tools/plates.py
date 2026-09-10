#!/usr/bin/env python3
"""The plates page: every figure and diagram the natural-history researchers
drew, and a strip of sample images per nature topic, on one page for the
owner to look at. Written under db/history/_ledger/routing/nature/ so the
gallery server already running there serves it:

    python3 tools/plates.py
    http://127.0.0.1:8766/nature/plates.html
"""
import html
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arctic_history as H          # noqa: E402

OUT = H.HISTORY_DIR / "_ledger" / "routing" / "nature"
OUT.mkdir(parents=True, exist_ok=True)
c = H.connect(H.HISTORY_DB, create=False)


def rel(local):
    """A path the gallery server can serve: a symlink under nature/files/."""
    src = H.HISTORY_DIR / local
    if not src.is_file():
        return ""
    link = OUT / "files" / Path(local).name
    link.parent.mkdir(exist_ok=True)
    if not link.exists():
        os.symlink(src, link)
    return f"files/{link.name}"


parts = ["""<!doctype html><meta charset=utf-8><title>The plates</title>
<style>body{font-family:Georgia,serif;background:#f7f3ea;color:#2a2620;margin:2em auto;max-width:1500px;padding:0 1em}
h1,h2{font-weight:normal}h2{margin-top:2.5em;border-bottom:1px solid #d9d2c3}
.plate{margin:1.5em 0}.plate img{max-width:100%;border:1px solid #d9d2c3}
.plate p{color:#7a7264;font-size:.95em;max-width:70em}
.strip{display:flex;flex-wrap:wrap;gap:6px}.strip a img{height:140px;object-fit:cover;border:1px solid #d9d2c3}
.meta{color:#7a7264;font-size:.9em}</style>
<h1>The plates</h1><p class=meta>Every figure and diagram the natural-history researchers drew, by topic, with a strip of a dozen other images each topic holds.</p>"""]
topics = c.execute("SELECT slug, title FROM topics WHERE domain='nature' ORDER BY title").fetchall()
for t in topics:
    figs = c.execute("SELECT id, title, description, local_file, tags FROM artifacts WHERE topic=? AND type='image' "
                     "AND (tags LIKE '%\"figure\"%' OR tags LIKE '%\"diagram\"%') ORDER BY id", (t["slug"],)).fetchall()
    n_img = c.execute("SELECT COUNT(*) AS n FROM artifacts WHERE topic=? AND type IN ('image','map')", (t["slug"],)).fetchone()["n"]
    n_obs = c.execute("SELECT COUNT(*) AS n FROM observations WHERE topic=?", (t["slug"],)).fetchone()["n"]
    if not n_img and not n_obs:
        continue
    parts.append(f"<h2>{html.escape(t['title'])}</h2><p class=meta>{n_obs} observations · {n_img} images · {len(figs)} plates</p>")
    for f in figs:
        p = rel(f["local_file"])
        if p:
            parts.append(f"<div class=plate><img src='{p}' loading=lazy><p><b>{html.escape(f['title'])}</b> "
                         f"<span class=meta>{f['id']}</span><br>{html.escape((f['description'] or '')[:400])}</p></div>")
    strip = c.execute("SELECT id, title, local_file FROM artifacts WHERE topic=? AND type IN ('image','map') "
                      "AND NOT (tags LIKE '%\"figure\"%' OR tags LIKE '%\"diagram\"%') AND local_file<>'' "
                      "ORDER BY random() LIMIT 12", (t["slug"],)).fetchall()
    cells = []
    for s in strip:
        p = rel(s["local_file"])
        if p and H.is_raster(s["local_file"]):
            cells.append(f"<a href='{p}' title='{html.escape(s['title'])}'><img src='{p}' loading=lazy></a>")
    if cells:
        parts.append("<div class=strip>" + "".join(cells) + "</div>")
(OUT / "plates.html").write_text("\n".join(parts), encoding="utf-8")
print(OUT / "plates.html")
