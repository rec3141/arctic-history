#!/usr/bin/python3
"""Cut plates/figures/tables out of PDFs already on disk and register each as an
artifact.  Driven by a TSV job file; one line per cut.

TSV columns (tab separated), header line ignored if it starts with '#':
  short   pdfpage   printed   type   title   creator   description   lat   lon   people   tags   date

Constant fields (topic, pdf, bibkey, credit, licence, source_url, id prefix and
first number, dpi) come from the command line.
"""
import argparse, csv, os, subprocess, sys

ROOT = "/data/dev/arctic-history"
DBH = os.path.join(ROOT, "db", "history")

ap = argparse.ArgumentParser()
ap.add_argument("--jobs", required=True)
ap.add_argument("--topic", required=True)
ap.add_argument("--pdf", required=True, help="path relative to db/history")
ap.add_argument("--bibkey", required=True)
ap.add_argument("--credit", required=True)
ap.add_argument("--licence", default="public domain")
ap.add_argument("--source-url", default="")
ap.add_argument("--start", type=int, required=True, help="first artifact number")
ap.add_argument("--dpi", default="300")
ap.add_argument("--leaf-note", default="", help="appended to --pages, e.g. 'PDF leaf'")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

pdf = os.path.join(DBH, a.pdf)
outdir = os.path.join(DBH, a.topic, "files")
os.makedirs(outdir, exist_ok=True)

rows = []
with open(a.jobs) as fh:
    for line in fh:
        if not line.strip() or line.startswith("#"):
            continue
        rows.append(line.rstrip("\n").split("\t"))

n = a.start
made, failed = [], []
for r in rows:
    r = (r + [""] * 12)[:12]
    short, pdfpage, printed, typ, title, creator, desc, lat, lon, people, tags, date = r
    aid = f"{a.topic}-{n:03d}"
    n += 1
    base = f"{a.topic}-{short}"
    png = os.path.join(outdir, base + ".png")
    if not os.path.exists(png):
        cmd = ["pdftoppm", "-png", "-r", a.dpi, "-f", pdfpage, "-l", pdfpage,
               "-singlefile", pdf, os.path.join(outdir, base)]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode != 0 or not os.path.exists(png):
            failed.append((aid, short, p.stderr.strip()[:200]))
            continue
    pages = f"p. {printed}" if printed else ""
    if a.leaf_note:
        pages = (pages + ", " if pages else "") + f"{a.leaf_note} {pdfpage}"
    cmd = ["/usr/bin/python3", os.path.join(ROOT, "tools", "history-db.py"), "artifact",
           "--id", aid, "--topic", a.topic, "--type", typ, "--title", title,
           "--bibkey", a.bibkey, "--credit", a.credit, "--licence", a.licence,
           "--pages", pages,
           "--local-file", f"{a.topic}/files/{base}.png"]
    if creator: cmd += ["--creator", creator]
    if desc: cmd += ["--description", desc]
    if lat and lon: cmd += ["--lat", lat, "--lon", lon]
    if people: cmd += ["--people", people]
    if tags: cmd += ["--tags", tags]
    if date: cmd += ["--date", date]
    if a.source_url: cmd += ["--source-url", a.source_url]
    if a.dry_run:
        print(" ".join(cmd)); continue
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if p.returncode != 0:
        failed.append((aid, short, (p.stderr or p.stdout).strip()[:300]))
    else:
        made.append((aid, base, os.path.getsize(png)))

for aid, base, sz in made:
    print(f"OK   {aid}  {base}.png  {sz//1024}K")
for aid, short, err in failed:
    print(f"FAIL {aid}  {short}  {err}")
print(f"\n{len(made)} registered, {len(failed)} failed. Next id: {a.topic}-{n:03d}")
