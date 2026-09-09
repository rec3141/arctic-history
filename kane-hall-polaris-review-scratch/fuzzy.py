#!/usr/bin/env python3
"""For each quotation, find the best-matching window in the corpus and print both."""
import re, sys, unicodedata, os, glob, difflib

FILES = sorted(glob.glob('/data/dev/arctic-history/db/history/kane-hall-polaris/files/*.txt'))

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    for a, b in [('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('—', '-'), ('–', '-'),
                 ('°', ' deg '), ('′', ' min ')]:
        s = s.replace(a, b)
    s = re.sub(r'-\s*\n\s*', '', s)
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    s = re.sub(r'\b(deg|min|degrees|minutes)\b', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

CORPUS = {}
for f in FILES:
    CORPUS[os.path.basename(f)] = norm(open(f, encoding='utf-8', errors='replace').read()).split()

def best_window(needle_words):
    n = len(needle_words)
    best = (0.0, None, None, [])
    # anchor on the rarest 3-gram of the needle
    for name, words in CORPUS.items():
        # build index of first word positions for a few anchor words
        anchors = set()
        for i in range(0, max(1, n - 2)):
            anchors.add(' '.join(needle_words[i:i + 3]))
        joined = ' '.join(words)
        positions = []
        for a in anchors:
            idx = joined.find(a)
            while idx != -1 and len(positions) < 400:
                positions.append(joined[:idx].count(' '))
                idx = joined.find(a, idx + 1)
        for p in set(positions):
            for start in (p - n, p - n // 2, p, p - n // 4):
                s = max(0, start)
                w = words[s:s + int(n * 1.6) + 6]
                sm = difflib.SequenceMatcher(None, needle_words, w)
                blocks = sm.get_matching_blocks()
                cov = sum(b.size for b in blocks) / max(1, len(needle_words))
                if cov > best[0]:
                    diff = [needle_words[i] for i in range(len(needle_words))
                            if not any(b.a <= i < b.a + b.size for b in blocks)]
                    best = (cov, name, ' '.join(w), diff)
    return best

if __name__ == '__main__':
    data = sys.stdin.read()
    for block in data.split('\n@@\n'):
        block = block.strip()
        if not block:
            continue
        label, _, q = block.partition('\n')
        q2 = re.sub(r'\[[^\]]*\]', ' ', q)
        for seg in re.split(r'\.\.\.|…', q2):
            nw = norm(seg).split()
            if len(nw) < 4:
                continue
            r, name, win, diff = best_window(nw)
            flag = 'OK  ' if r >= 0.98 else ('~~~ ' if r > 0.90 else 'BAD ')
            print(f'{flag} {label}  cov={r:.3f}  {name}  unmatched={diff}')
            if r < 0.98:
                print(f'   PAGE: {" ".join(nw)}')
                print(f'   BOOK: {win}')
