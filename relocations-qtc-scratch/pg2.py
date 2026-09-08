#!/usr/bin/env python3
"""Page-aware grep over a pdftotext -raw dump that keeps form feeds.

Usage: pg2.py <pdf> <regex> [before] [after]

Splits the raw text on form feeds (one chunk per PDF page), works out the
printed page number for each chunk from the QTC running footer, and prints
matches with `p.NN` labels. Falls back to "pdf p.N" when no printed number
is on the page.
"""
import re
import subprocess
import sys

FOOT = re.compile(r'^\s*(\d{1,3})\s*$')


def pages(pdf):
    txt = subprocess.run(['pdftotext', '-raw', pdf, '-'],
                         capture_output=True, text=True).stdout
    out = []
    for n, chunk in enumerate(txt.split('\f'), 1):
        lines = chunk.split('\n')
        printed = None
        # QTC footer: "Qikiqtani Truth Commission" / "<n>" / "<report title>"
        for i, ln in enumerate(lines):
            if ln.strip() == 'Qikiqtani Truth Commission' and i + 1 < len(lines):
                m = FOOT.match(lines[i + 1])
                if m:
                    printed = int(m.group(1))
            if 'Qikiqtani Truth Commission' in ln and i > 0:
                m = FOOT.match(lines[i - 1])
                if m:
                    printed = int(m.group(1))
        out.append((n, printed, chunk))
    return out


def main():
    pdf, pat = sys.argv[1], sys.argv[2]
    before = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    after = int(sys.argv[4]) if len(sys.argv) > 4 else before
    rx = re.compile(pat, re.I)
    for n, printed, chunk in pages(pdf):
        lines = chunk.split('\n')
        for i, ln in enumerate(lines):
            if rx.search(ln):
                label = f'p.{printed}' if printed else f'pdf p.{n}'
                print(f'--- {label} (pdf {n}) line {i+1}')
                for j in range(max(0, i - before), min(len(lines), i + after + 1)):
                    print(('>' if j == i else ' ') + lines[j])


if __name__ == '__main__':
    main()
