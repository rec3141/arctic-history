#!/usr/bin/env python3
"""Page-aware grep for the QTC / RCAP texts.

Usage:  pg.py <file> <regex> [context]
Prints  p.NN  line  text   for each match, with `context` lines either side.

Page number is taken from the running footers the QTC volumes carry, e.g.
    "Grise Fiord | 13"  or  "14 | Qikiqtani Truth Commission: ..."
For RCAP the footer is a bare number on its own line.
"""
import re
import sys

FOOT_R = re.compile(r'^\s*(?:([A-Z][A-Za-z \'’-]+)\s*\|\s*(\d{1,3})\s*$|(\d{1,3})\s*\|\s*[A-Z])')
# 2024 revised QTC editions: "Qikiqtani Truth Commission   3   Qimmiliriniq: ..."
QTC24_R = re.compile(r'Qikiqtani Truth Commission\s+(\d{1,3})\s+\S|\S\s+(\d{1,3})\s+Qikiqtani Truth Commission')
BARE_R = re.compile(r'^\s*(\d{1,3})\s*$')


def pagemap(lines, bare=False):
    """line index -> page number (the page that line sits on)."""
    marks = []  # (line index, page number) of each footer
    for i, ln in enumerate(lines):
        m = FOOT_R.match(ln)
        if m:
            marks.append((i, int(m.group(2) or m.group(3))))
            continue
        m = QTC24_R.search(ln)
        if m:
            marks.append((i, int(m.group(1) or m.group(2))))
            continue
        if bare:
            m = BARE_R.match(ln)
            if m and 1 <= int(m.group(1)) <= 400:
                marks.append((i, int(m.group(1))))
    pages = {}
    prev = 0
    for i, p in marks:
        for j in range(prev, i + 1):
            pages[j] = p
        prev = i + 1
    for j in range(prev, len(lines)):
        pages[j] = marks[-1][1] + 1 if marks else 0
    return pages


def main():
    path, pat = sys.argv[1], sys.argv[2]
    ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    pages = pagemap(lines, bare='rcap' in path)
    rx = re.compile(pat, re.I)
    for i, ln in enumerate(lines):
        if rx.search(ln):
            lo, hi = max(0, i - ctx), min(len(lines), i + ctx + 1)
            print(f'--- p.{pages.get(i, "?")} line {i+1}')
            for j in range(lo, hi):
                print(('>' if j == i else ' ') + lines[j])


if __name__ == '__main__':
    main()
