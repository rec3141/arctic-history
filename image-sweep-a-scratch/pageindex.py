#!/usr/bin/python3
"""Build a printed-page -> pdf-page index from a scanned book's running heads.

Reads the first and last non-empty line of every page, pulls a bare arabic page
number from either end, then fills gaps by interpolation and writes a JSON map.
Usage: pageindex.py <pdf> <out.json> [firstpage] [lastpage]
"""
import json, re, subprocess, sys

pdf, out = sys.argv[1], sys.argv[2]
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 1
hi = int(sys.argv[4]) if len(sys.argv) > 4 else 0

txt = subprocess.run(["pdftotext", "-layout", "-f", str(lo)] +
                     (["-l", str(hi)] if hi else []) + [pdf, "-"],
                     capture_output=True, text=True, errors="replace").stdout
pages = txt.split("\f")

NUM = re.compile(r"^\s*(\d{1,4})\b")
NUM_END = re.compile(r"\b(\d{1,4})\s*$")

obs = {}   # pdfpage -> printed
for i, p in enumerate(pages):
    n = lo + i
    lines = [l for l in p.splitlines() if l.strip()]
    if not lines:
        continue
    cands = []
    for l in (lines[0], lines[1] if len(lines) > 1 else "",
              lines[-1], lines[-2] if len(lines) > 1 else ""):
        m = NUM.match(l)
        if m: cands.append(int(m.group(1)))
        m = NUM_END.search(l)
        if m: cands.append(int(m.group(1)))
    for c in cands:
        if 1 <= c <= 2000:
            obs[n] = c
            break

# keep only observations consistent with a locally monotone offset
good = {}
keys = sorted(obs)
for k in keys:
    off = k - obs[k]
    near = [kk - obs[kk] for kk in keys if abs(kk - k) <= 6 and kk != k]
    if near and sum(1 for o in near if abs(o - off) <= 1) >= max(1, len(near) // 3):
        good[k] = obs[k]

printed2pdf = {}
for k in sorted(good):
    printed2pdf.setdefault(good[k], k)

# offset table for interpolation
offs = sorted((k - good[k], k) for k in good)
def lookup(printed):
    if printed in printed2pdf:
        return printed2pdf[printed], "exact"
    # nearest observed printed page, apply its offset
    best = min(good, key=lambda k: abs(good[k] - printed))
    return best + (printed - good[best]), f"interp from p.{good[best]}"

json.dump({"printed2pdf": {str(k): v for k, v in printed2pdf.items()},
           "obs": {str(k): v for k, v in good.items()}}, open(out, "w"))

if len(sys.argv) > 5:
    for pr in sys.argv[5].split(","):
        pg, how = lookup(int(pr))
        print(f"printed {pr} -> pdf {pg}  ({how})")
else:
    print(f"{len(good)} pages indexed, printed range "
          f"{min(good.values())}-{max(good.values())}")
    ks = sorted(good)
    print("sample offsets:", [(good[k], k - good[k]) for k in ks[::max(1, len(ks)//12)]])
