#!/usr/bin/env python3
"""Cut every face out of the photographs, engravings and paintings.

For issue #2: the ship's History tab has a People page whose right-hand column
is filled with faces cut from the artifacts.  This script detects the faces,
writes a square JPEG crop per face under ``db/history/<topic>/files/faces/``
(so the ship's pull, which syncs ``*/files/**``, brings them), and records each
one in the ``faces`` table through :func:`arctic_history.add_face` -- the same
function ``tools/history-db.py face`` calls.  ``publish()`` then writes
``data/history/faces.json`` and copies the crops.

How to run it
-------------
The detector needs OpenCV, so run this with the OCR virtualenv's Python (3.11,
OpenCV 4.11 with ``cv2.FaceDetectorYN``), from the repository root::

    .ocr-venv/bin/python tools/faces.py                 # every image and map raster
    .ocr-venv/bin/python tools/faces.py --topic whaling # one topic
    .ocr-venv/bin/python tools/faces.py --artifact whaling-042 --force
    .ocr-venv/bin/python tools/faces.py --dry-run       # detect, crop nothing, write nothing

The model is ``tools/models/face_detection_yunet_2023mar.onnx`` (YuNet, 230 KB,
from opencv_zoo).  If it is missing, fetch it once with::

    curl -sSL -o tools/models/face_detection_yunet_2023mar.onnx \
      https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx

Rerunning it
------------
The run is resumable and idempotent.  An artifact whose faces are already in
the table is skipped unless its raster is newer than the newest of its face
rows (file mtime vs. the ``updated`` column) or ``--force`` is given.  When an
artifact is redone, :func:`arctic_history.forget_faces` clears its rows and the
old crops are deleted first, so a re-detection that finds fewer faces does not
leave stragglers behind.

So a second run over an unchanged database writes no face rows and cuts no
crops.  It does re-detect the rasters that yielded nothing -- a chart, a ship, a
landscape has no row to compare a date against -- which is a couple of minutes
and is what you want after retuning ``--score``; the images that did yield faces
are skipped.  ``--force`` redoes everything and lands on the same rows.
``--no-log`` suppresses the per-topic worklog line, which is otherwise written on
every run that was not a ``--dry-run``.

How it detects
--------------
YuNet is fully convolutional but sees only the input size it is given, so a
single pass over a shrunk group photograph misses the small faces.  Every image
is loaded through Pillow with ``Image.MAX_IMAGE_PIXELS = None`` and
``draft``/``thumbnail`` down to a long edge of ``--max-edge`` (3000 px by
default -- two of the Bernier chart scans are half a gigapixel), then detected
in several passes: the whole frame at a long edge of 1024 and again at 2048, the
whole frame at native size, the whole frame doubled when it is small, and a grid
of overlapping 768 px tiles at the working resolution.  The unions are merged by
non-maximum suppression and mapped back to original coordinates, which is what
the ``box`` column holds.

The score threshold is 0.70 -- the issue suggests about 0.6, but between 0.60 and
0.70 this collection returns roughly two false positives for every real face: a
sledge dog's muzzle, a lichened boulder, the word "Park" inked across a chart.
Above 0.70 the survivors are overwhelmingly faces (a few huskies aside, which
YuNet scores as high as 0.93 and no threshold will separate).

The smallest face kept is ``--min-face``, 32 px in the detection frame (never
smaller than that in the original, since the frame is only ever shrunk).  The issue asks for about 40 px; 32 is the useful floor here,
because most of this collection is 500-1000 px web scans in which a ship's
company has faces thirty pixels across, and a 40 px floor drops whole group
photographs -- the Gjoa's crew at Nome, the Beard daguerreotype plate of Franklin
and his officers -- while going below about 24 adds only blur.

How it identifies
-----------------
Conservatively, and only with names that are already in the ``people`` table
(``add_face`` refuses any other).  A face gets a name only when the image holds
exactly one face and either

  * the artifact's ``people`` list holds exactly one name  (``single-face-single-name``), or
  * the title or description says "portrait of X"          (``caption-portrait-of``), or
  * the title reads "X, 1894"                              (``caption-name-year``), or
  * the title leads with a name the artifact also lists    (``caption-title-leads``).

Everything else is published unidentified, linking to the photograph.  The rule
used is recorded in the ``method`` column beside the detector's name.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import cv2                                    # noqa: E402
import numpy as np                            # noqa: E402
from PIL import Image, ImageOps               # noqa: E402

import arctic_history as H                    # noqa: E402

Image.MAX_IMAGE_PIXELS = None                 # the Bernier scans are half a gigapixel

MODEL = ROOT / "tools" / "models" / "face_detection_yunet_2023mar.onnx"
MODEL_URL = ("https://media.githubusercontent.com/media/opencv/opencv_zoo/main/"
             "models/face_detection_yunet/face_detection_yunet_2023mar.onnx")
DETECTOR = "yunet-2023mar"
RASTER = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".gif", ".bmp", ".webp"}


# ------------------------------------------------------------------ loading
def load_working(path: Path, max_edge: int):
    """Return (BGR array, scale, original size).  ``scale`` multiplies working
    coordinates back into the original raster."""
    im = Image.open(path)
    # honour the camera's EXIF orientation before any size or pixel is read,
    # matching the ship's thumbnailer, so crops from a turned photograph come
    # out upright; a turned photo forgoes the cheap JPEG draft
    if (im.getexif().get(0x0112) or 1) != 1:
        im = ImageOps.exif_transpose(im)
    ow, oh = im.size
    if max(ow, oh) > max_edge:
        try:
            im.draft("RGB", (max_edge, max_edge))   # cheap JPEG DCT downscale
        except Exception:
            pass
    im = im.convert("RGB")
    if max(im.size) > max_edge:
        im.thumbnail((max_edge, max_edge), Image.LANCZOS)
    scale = ow / im.size[0]
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR), scale, (ow, oh)


# ---------------------------------------------------------------- detection
def _pad32(img):
    h, w = img.shape[:2]
    ph, pw = (-h) % 32, (-w) % 32
    if ph or pw:
        img = cv2.copyMakeBorder(img, 0, ph, 0, pw, cv2.BORDER_REPLICATE)
    return img


def _run(det, img):
    """Raw YuNet pass over one array; returns [x, y, w, h, conf] in its coords."""
    padded = _pad32(img)
    h, w = padded.shape[:2]
    if w < 32 or h < 32:
        return []
    det.setInputSize((w, h))
    try:
        _, faces = det.detect(padded)
    except cv2.error:
        return []
    if faces is None:
        return []
    return [[float(f[0]), float(f[1]), float(f[2]), float(f[3]), float(f[-1])] for f in faces]


def _nms(boxes, thresh=0.35):
    """Merge boxes from the several passes, keeping the most confident."""
    if not boxes:
        return []
    boxes = sorted(boxes, key=lambda b: -b[4])
    kept = []
    for b in boxes:
        bx, by, bw, bh = b[:4]
        ba = bw * bh
        for k in kept:
            kx, ky, kw, kh = k[:4]
            ix = max(0.0, min(bx + bw, kx + kw) - max(bx, kx))
            iy = max(0.0, min(by + bh, ky + kh) - max(by, ky))
            inter = ix * iy
            if inter and inter / min(ba, kw * kh) > thresh:
                break
        else:
            kept.append(b)
    return kept


def detect(det, work, min_face, tile=768, overlap=0.25):
    """Several passes over the working image: the whole frame at two sizes and
    a grid of overlapping tiles at full working resolution."""
    h, w = work.shape[:2]
    found = []

    # whole-frame passes: shrunk for the big faces, native, and doubled for the
    # small ones -- most of this collection is 600 px web scans in which a
    # crew's faces are twenty pixels across and YuNet needs the extra scale
    scales = {1.0}
    if max(h, w) > 1024:
        scales.add(1024 / max(h, w))
    if max(h, w) > 2048:
        scales.add(2048 / max(h, w))
    if max(h, w) <= 1200:
        scales.add(2.0)
    for s in sorted(scales):
        img = work if s == 1.0 else cv2.resize(
            work, (max(1, round(w * s)), max(1, round(h * s))),
            interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        for b in _run(det, img):
            found.append([b[0] / s, b[1] / s, b[2] / s, b[3] / s, b[4]])

    if max(h, w) > 1400:
        step = max(64, int(tile * (1 - overlap)))
        ys = list(range(0, max(1, h - tile) + 1, step)) or [0]
        xs = list(range(0, max(1, w - tile) + 1, step)) or [0]
        if ys[-1] + tile < h:
            ys.append(max(0, h - tile))
        if xs[-1] + tile < w:
            xs.append(max(0, w - tile))
        for y0 in ys:
            for x0 in xs:
                sub = work[y0:y0 + tile, x0:x0 + tile]
                for b in _run(det, sub):
                    found.append([b[0] + x0, b[1] + y0, b[2], b[3], b[4]])

    out = []
    for b in _nms(found):
        x, y, bw, bh = b[:4]
        x, y = max(0.0, x), max(0.0, y)
        bw, bh = min(bw, w - x), min(bh, h - y)
        if bw <= 0 or bh <= 0 or min(bw, bh) < min_face:
            continue
        out.append([x, y, bw, bh, b[4]])
    out.sort(key=lambda b: (b[0], b[1]))          # left to right; n counts from 1
    return out


# -------------------------------------------------------------------- crops
def crop_square(img, box, margin=0.40, least=160):
    """A square around the face with ``margin`` of its size on each side,
    upscaled gently to ``least`` px if the source is smaller."""
    h, w = img.shape[:2]
    x, y, bw, bh = box[:4]
    cx, cy = x + bw / 2.0, y + bh / 2.0
    side = max(bw, bh) * (1 + 2 * margin)
    side = min(side, float(min(w, h)))
    x0 = int(round(min(max(0.0, cx - side / 2), w - side)))
    y0 = int(round(min(max(0.0, cy - side / 2), h - side)))
    s = int(round(side))
    cut = img[y0:y0 + s, x0:x0 + s]
    if cut.size == 0:
        return None
    if cut.shape[0] < least:
        cut = cv2.resize(cut, (least, least), interpolation=cv2.INTER_LANCZOS4)
    return cut


# ----------------------------------------------------------- identification
HONORIFIC = re.compile(r"^(sir|dr|doctor|mr|mrs|miss|rev|capt|captain|cmdr|commander|lt|"
                       r"lieut|lieutenant|col|colonel|gen|general|adm|admiral|prof|professor|"
                       r"cst|constable|sgt|sergeant|insp|inspector)\.?\s+", re.I)
PORTRAIT = re.compile(r"portraits?\s+of\s+([^,;.:()\[\]\n]{3,70})", re.I)
NAME_YEAR = re.compile(r"^\s*([^,;:()\[\]\n]{3,70}),\s*(?:c\.\s*)?(1[4-9]\d\d|20\d\d)\b")


def _strip(phrase: str) -> str:
    p = re.sub(r"\s+", " ", phrase).strip(" \t'\"“”‘’-—")
    p = re.sub(r"^(a|an|the)\s+", "", p, flags=re.I)
    while True:
        q = HONORIFIC.sub("", p)
        if q == p:
            return p
        p = q


def resolve(phrase: str, index: dict) -> str:
    """The people-table name a caption phrase means, or ''.  Tries the phrase,
    then shorter and shorter prefixes of it, so 'John Ross in his cabin' still
    resolves to 'John Ross' -- but only ever to a name already in people."""
    p = _strip(phrase or "")
    if not p:
        return ""
    words = p.split(" ")
    for k in range(len(words), 1, -1):           # at least two words: no bare surnames
        cand = " ".join(words[:k]).strip(" ,.;:'\"")
        hit = index.get(cand.lower())
        if hit:
            return hit
    return ""


def exact(phrase: str, index: dict) -> str:
    """The people-table name a phrase *is*, honorific aside, or ''."""
    return index.get(_strip(phrase or "").strip(" ,.;:'\"").lower(), "")


def identify(art, faces, index) -> tuple[str, str]:
    """(person, rule).  Only ever names a face when the image holds one face."""
    if len(faces) != 1:
        return "", "unidentified"
    try:
        listed = json.loads(art["people"]) if art["people"] else []
    except Exception:
        listed = [s.strip() for s in (art["people"] or "").split(";") if s.strip()]
    if len(listed) == 1:
        hit = index.get(str(listed[0]).strip().lower())
        if hit:
            return hit, "single-face-single-name"
    title, desc = art["title"] or "", art["description"] or ""
    m = PORTRAIT.search(title) or PORTRAIT.search(desc)
    if m:
        hit = resolve(m.group(1), index)
        if hit:
            return hit, "caption-portrait-of"
    m = NAME_YEAR.match(title)
    if m:
        hit = exact(m.group(1), index)
        if hit:
            return hit, "caption-name-year"
    # the title leads with the sitter's name and the artifact lists them: the
    # whole phrase before the first comma has to *be* a name, so
    # "Oomna, an Iglulingmiut woman, 1823" counts and "Mutch and the crew" does not
    lead = exact(title.split(",")[0], index)
    if lead and lead in [str(x).strip() for x in listed]:
        return lead, "caption-title-leads"
    return "", "unidentified"


# ---------------------------------------------------------------- the run
def candidates(c, topic=None, artifact=None):
    """Every image artifact, and every map with a raster, that has a file on
    disk.  A map rendered to a raster view is scanned through its view."""
    sql = ("SELECT * FROM artifacts WHERE type IN ('image','map') "
           "AND ((local_file IS NOT NULL AND local_file != '') "
           "  OR (view_file IS NOT NULL AND view_file != '')) ")
    args = []
    if topic:
        sql += "AND topic = ? "
        args.append(topic)
    if artifact:
        sql += "AND id = ? "
        args.append(artifact)
    out = []
    for r in c.execute(sql + "ORDER BY id", args):
        for col in ("local_file", "view_file"):
            rel = r[col]
            if not rel or Path(rel).suffix.lower() not in RASTER:
                continue
            p = H.HISTORY_DIR / rel
            if p.is_file():
                out.append((r, p))
                break
    return out


def needs_work(c, art_id, path, force):
    """Skip an artifact whose faces are already there and no older than its
    raster.  ``updated`` is ISO 8601 with an offset; compare as epoch seconds."""
    if force:
        return True
    rows = list(c.execute("SELECT updated FROM faces WHERE artifact_id=?", (art_id,)))
    if not rows:
        return True
    newest = max((r["updated"] or "") for r in rows)
    try:
        from datetime import datetime
        stamp = datetime.fromisoformat(newest).timestamp()
    except Exception:
        return True
    return path.stat().st_mtime > stamp + 1


def clear(c, art_id, topic, via_cli):
    """Drop this artifact's face rows and the crops they named."""
    if via_cli:
        subprocess.run(["/usr/bin/python3",
                        str(ROOT / "tools" / "history-db.py"), "face",
                        "--artifact", art_id, "--n", "1", "--file", "x", "--forget"],
                       cwd=ROOT, check=True, capture_output=True)
    else:
        H.forget_faces(c, art_id)
    d = H.HISTORY_DIR / topic / "files" / "faces"
    for old in d.glob(f"{art_id}-*.jpg"):
        old.unlink()


def record(c, art_id, n, rel, box, person, conf, method, via_cli):
    if via_cli:
        cmd = ["/usr/bin/python3", str(ROOT / "tools" / "history-db.py"), "face",
               "--artifact", art_id, "--n", str(n), "--file", rel,
               "--box", json.dumps(box), "--confidence", f"{conf:.4f}", "--method", method]
        if person:
            cmd += ["--person", person]
        subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True)
    else:
        H.add_face(c, art_id, n, rel, box=box, person=person, confidence=conf, method=method)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--topic", help="one topic slug instead of all")
    ap.add_argument("--artifact", help="one artifact id")
    ap.add_argument("--force", action="store_true", help="redo artifacts already done")
    ap.add_argument("--dry-run", action="store_true", help="detect only: no crops, no rows, no log")
    ap.add_argument("--no-log", action="store_true", help="skip the per-topic worklog line")
    ap.add_argument("--via-cli", action="store_true",
                    help="write through tools/history-db.py rather than add_face in process")
    ap.add_argument("--score", type=float, default=0.70, help="YuNet score threshold (default 0.70)")
    ap.add_argument("--nms", type=float, default=0.3, help="YuNet NMS threshold (default 0.3)")
    ap.add_argument("--min-face", type=int, default=32,
                    help="smallest face kept, px in the detection frame (default 32)")
    ap.add_argument("--max-edge", type=int, default=3000, help="detect at this long edge (default 3000)")
    ap.add_argument("--margin", type=float, default=0.40, help="crop margin each side (default 0.40)")
    ap.add_argument("--least", type=int, default=160, help="smallest crop, px (default 160)")
    ap.add_argument("--who", default=f"faces run, {time.strftime('%Y-%m-%d')}")
    ap.add_argument("--limit", type=int, help="stop after this many artifacts (for trying it out)")
    ap.add_argument("--boxes-to", help="directory for full frames with the boxes drawn, to eyeball")
    a = ap.parse_args(argv)

    if not MODEL.is_file():
        sys.exit(f"missing {MODEL}\n  curl -sSL -o {MODEL} {MODEL_URL}")
    det = cv2.FaceDetectorYN.create(str(MODEL), "", (320, 320), a.score, a.nms, 5000)

    c = H.connect()
    index = {r["name"].lower(): r["name"] for r in c.execute("SELECT name FROM people")}
    jobs = candidates(c, a.topic, a.artifact)
    if a.limit:
        jobs = jobs[:a.limit]

    per_topic, biggest, scanned, skipped, total, named = {}, [], 0, 0, 0, 0
    for art, path in jobs:
        if not needs_work(c, art["id"], path, a.force or a.dry_run):
            skipped += 1
            continue
        try:
            work, scale, orig = load_working(path, a.max_edge)
        except Exception as e:
            print(f"  ! {art['id']}: cannot read {path.name}: {e}", file=sys.stderr)
            continue
        scanned += 1
        boxes = detect(det, work, a.min_face)
        person, rule = identify(art, boxes, index)
        method = f"{DETECTOR}; {rule}"
        t = per_topic.setdefault(art["topic"], {"images": 0, "faces": 0, "named": 0})
        t["images"] += 1
        if boxes:
            biggest.append((len(boxes), art["id"], art["title"] or ""))

        if not a.dry_run:
            # always first, so a re-detection that finds fewer faces (or none)
            # leaves no stragglers behind
            clear(c, art["id"], art["topic"], a.via_cli)

        outdir = H.HISTORY_DIR / art["topic"] / "files" / "faces"
        for n, b in enumerate(boxes, 1):
            ob = [int(round(b[0] * scale)), int(round(b[1] * scale)),
                  int(round(b[2] * scale)), int(round(b[3] * scale))]
            total += 1
            t["faces"] += 1
            if person:
                named += 1
                t["named"] += 1
            if a.dry_run:
                continue
            outdir.mkdir(parents=True, exist_ok=True)
            cut = crop_square(work, b, a.margin, a.least)
            if cut is None:
                continue
            name = f"{art['id']}-{n}.jpg"
            cv2.imwrite(str(outdir / name), cut, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            record(c, art["id"], n, f"{art['topic']}/files/faces/{name}", ob,
                   person, b[4], method, a.via_cli)

        if a.boxes_to and boxes:
            d = Path(a.boxes_to)
            d.mkdir(parents=True, exist_ok=True)
            marked = work.copy()
            for n, b in enumerate(boxes, 1):
                p1 = (int(b[0]), int(b[1])); p2 = (int(b[0] + b[2]), int(b[1] + b[3]))
                cv2.rectangle(marked, p1, p2, (0, 0, 255), 2)
                cv2.putText(marked, f"{n}:{b[4]:.2f}", (p1[0], max(12, p1[1] - 4)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.imwrite(str(d / f"{art['id']}.jpg"), marked, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

        print(f"{art['id']:36s} {len(boxes):3d} face(s)"
              f"{'  -> ' + person if person else ''}  {orig[0]}x{orig[1]}")

    print(f"\nscanned {scanned}, skipped {skipped} already done, "
          f"{total} faces, {named} identified, {total - named} not")
    biggest.sort(reverse=True)
    for n, aid, title in biggest[:10]:
        print(f"  {n:3d}  {aid:34s} {title[:60]}")

    if not a.dry_run and not a.no_log:
        for topic, t in sorted(per_topic.items()):
            done = (f"faces: {t['images']} rasters scanned with {DETECTOR}, {t['faces']} faces cut "
                    f"to files/faces/, {t['named']} identified, {t['faces'] - t['named']} left "
                    f"unidentified; rows in the faces table, crops published by publish()")
            subprocess.run(["/usr/bin/python3", str(ROOT / "tools" / "history-db.py"), "log",
                            "--topic", topic, "--who", a.who, "--done", done,
                            "--next", "re-run tools/faces.py when new images land; it only "
                                      "re-detects rasters newer than their face rows"],
                           cwd=ROOT, check=True, capture_output=True)
        print(f"worklog written for {len(per_topic)} topic(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
