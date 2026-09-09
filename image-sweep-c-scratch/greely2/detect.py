#!/usr/bin/env python3
import sys, glob, os
from PIL import Image
import numpy as np

thumbs_dir = "/data/dev/arctic-history/image-sweep-c-scratch/thumbs/threeyearsofarct02gree"
results = []
for path in sorted(glob.glob(os.path.join(thumbs_dir, "n*.jpg")), key=lambda p: int(os.path.basename(p)[1:-4])):
    n = int(os.path.basename(path)[1:-4])
    try:
        im = Image.open(path).convert("L")
    except Exception as e:
        print(f"ERR {n}: {e}", file=sys.stderr)
        continue
    arr = np.asarray(im, dtype=np.float64)
    h, w = arr.shape
    ch = int(h * 0.06)
    cw = int(w * 0.06)
    crop = arr[ch:h-ch, cw:w-cw]
    if crop.size == 0:
        continue
    frac_dark = (crop < 140).mean()
    row_means = crop.mean(axis=1)
    p10 = np.percentile(row_means, 10)
    flag = frac_dark > 0.028 or p10 < 150
    if flag:
        results.append((n, round(frac_dark, 4), round(p10, 1)))

print(f"Total candidates: {len(results)}")
for n, fd, p10 in results:
    print(n, fd, p10)
