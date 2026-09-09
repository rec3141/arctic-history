#!/usr/bin/python3
"""Find illustration leaves in a scanned book PDF with no usable text layer.

Two signals, both from `pdfimages -list`:
  A. region signal - archive.org JBIG2 scans keep the bitonal text as a mask and
     store each continuous-tone patch (plate, map, photo) as its own JPX/DCT
     image. A page with a big tone region that is NOT the shape of the whole
     page is an illustration leaf.
  B. weight signal - where the whole page is one image, a halftone plate simply
     compresses far worse than a page of type. Rank leaves by compressed bytes
     and flag those well above the book's median.

Usage: plates.py <pdf> [top_n]
"""
import collections, re, statistics, subprocess, sys

pdf = sys.argv[1]
topn = int(sys.argv[2]) if len(sys.argv) > 2 else 40

SZ = re.compile(r"^([\d.]+)([BKMG])$")
def nbytes(s):
    m = SZ.match(s)
    if not m:
        return 0
    return int(float(m.group(1)) * {"B": 1, "K": 1024, "M": 1024**2,
                                    "G": 1024**3}[m.group(2)])

rows = subprocess.run(["pdfimages", "-list", pdf], capture_output=True,
                      text=True).stdout.splitlines()[2:]
weight = collections.Counter()
page_shape, regions = {}, collections.defaultdict(list)
for l in rows:
    f = l.split()
    if len(f) < 15 or f[2] not in ("image",):
        continue
    try:
        page, w, h = int(f[0]), int(f[3]), int(f[4])
    except ValueError:
        continue
    b = nbytes(f[14])
    weight[page] += b
    if w * h > 2_000_000:
        if w * h > page_shape.get(page, (0, 0, 0))[0] * page_shape.get(page, (0, 0, 0))[1]:
            page_shape[page] = (w, h, b)
    else:
        regions[page].append((w * h, w, h))

pages = sorted(weight)
med = statistics.median(weight.values()) if weight else 0
shapes = collections.Counter((w, h) for w, h, _ in page_shape.values())
pw, ph = shapes.most_common(1)[0][0] if shapes else (0, 0)
page_ar = pw / ph if ph else 0

flag = {}
for p in pages:
    reasons = []
    if regions[p]:
        a, w, h = max(regions[p])
        ar = w / h if h else 0
        # a tone patch that is not just a downscaled copy of the whole page
        if a > 30000 and (page_ar == 0 or abs(ar - page_ar) / page_ar > 0.12
                          or len(regions[p]) > 3):
            reasons.append(f"tone {w}x{h}x{len(regions[p])}")
    if med and weight[p] > 3 * med:
        reasons.append(f"heavy {weight[p]//1024}K (median {int(med)//1024}K)")
    if p in page_shape:
        w, h, _ = page_shape[p]
        if page_ar and (w / h) > 1.3 * page_ar:
            reasons.append(f"FOLDOUT {w}x{h}")
    if reasons:
        flag[p] = ", ".join(reasons)

ranked = sorted(flag, key=lambda p: -weight[p])[:topn]
for p in sorted(ranked):
    print(f"{p:5d}  {flag[p]}")
print(f"\n{len(flag)} flagged leaves of {len(pages)}; typical leaf {pw}x{ph}, "
      f"median weight {int(med)//1024}K")
