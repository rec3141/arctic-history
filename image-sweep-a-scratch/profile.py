#!/usr/bin/python3
"""Profile a PDF page by page: char count + first line of text.
Used to spot plates (very low text) and tables/contents (keyword hits)."""
import subprocess, sys, re, os

pdf = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "plates"
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 1
hi = int(sys.argv[4]) if len(sys.argv) > 4 else 0

out = subprocess.run(["pdftotext", "-layout", "-f", str(lo)] +
                     (["-l", str(hi)] if hi else []) + [pdf, "-"],
                     capture_output=True, text=True, errors="replace").stdout
pages = out.split("\f")
KW = re.compile(r"(CONTENTS|LIST OF ILLUSTRATIONS|ILLUSTRATIONS|PLATE|APPENDIX|"
                r"Meteorological|MAGNETIC|Provisions|PROVISIONS|Victualling|"
                r"stores|Table |TABLE|Register|REGISTER|Abstract|Chart|CHART|"
                r"Equipment|Sledge|Temperature|Thermometer|Observations)")
for i, p in enumerate(pages):
    n = lo + i
    txt = p.strip()
    first = " ".join(txt.split())[:110]
    if mode == "plates":
        if len(txt) < 220:
            print(f"{n:5d} {len(txt):6d}  {first}")
    elif mode == "kw":
        if KW.search(txt):
            print(f"{n:5d} {len(txt):6d}  {first}")
    else:
        print(f"{n:5d} {len(txt):6d}  {first}")
