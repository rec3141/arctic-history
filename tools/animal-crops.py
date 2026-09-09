#!/usr/bin/env python3
"""Cut every dog, pony, cat, bear, musk-ox and ship out of the photographs.

The companion to ``tools/faces.py``.  That script cuts human faces for the
History tab's People page; this one does the same for the expeditions' animals
and their vessels, which the brief makes first class alongside people: a named
sledge dog is a row in ``animals``, a ship is a row in ``vessels``, and both get
their own wiki page.  Every detection becomes a JPEG crop under
``db/history/<topic>/files/faces/`` (the ship's pull syncs ``*/files/**``) and a
row in the same ``faces`` table through :func:`arctic_history.add_face`, with
``kind`` set to ``animal`` or ``vessel``.  ``publish()`` exports every face row
with its kind, so the crops reach the tab beside the human ones.

The crop numbers are deliberately disjoint from faces.py's: animals are
numbered from 100 and vessels from 200, so the two scripts never collide on the
``(artifact_id, n)`` key and never overwrite one another's files.  For the same
reason this script never calls ``forget_faces`` -- that would delete the human
faces too.  It deletes only its own rows::

    DELETE FROM faces WHERE artifact_id=? AND kind IN ('animal','vessel')

How to run it
-------------
Detection needs torch and ultralytics, so run it with the OCR virtualenv's
Python (3.11, torch 2.5.1+cu121, ultralytics 8.4), from the repository root::

    .ocr-venv/bin/python tools/animal-crops.py                  # every raster
    .ocr-venv/bin/python tools/animal-crops.py --topic whaling
    .ocr-venv/bin/python tools/animal-crops.py --artifact whaling-042 --force
    .ocr-venv/bin/python tools/animal-crops.py --dry-run        # detect only
    .ocr-venv/bin/python tools/animal-crops.py --identify       # names only

``--boxes-to DIR`` writes each frame with its boxes drawn on it and
``--detections-to FILE`` a JSONL line per raster; between them they are how the
thresholds below were chosen, and neither touches the database.

The model is YOLO11x, ``tools/models/yolo11x.pt`` (115 MB).  **It is not
committed** -- it is a build artifact like the OCR virtualenv; fetch it once
with::

    curl -sSL -o tools/models/yolo11x.pt \
      https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt

What it keeps
-------------
Of the COCO classes, six become ``animal`` crops -- ``dog`` (the sledge dogs,
and the ship's dogs), ``horse`` (Scott-style ponies, and the horses in the
outfitting photographs), ``cat`` (the ship's cats), ``bear`` (live cubs and the
occasional shot polar bear) and ``cow`` (which is what a musk-ox trips, and
sometimes a caribou; the crop is kept as an animal with ``cow`` recorded as the
class in ``method``, because the herd photographs are worth having) -- and two
become ``vessel`` crops, ``boat`` (ships, boats and the occasional beset hull)
and ``airplane`` (the 1947 aerial-survey topics).  Nothing else is kept: on this
collection the other classes are almost all noise, ``bird`` above all.

Detection runs on the whole frame; on a frame shorter than ``--up-below`` it
runs again at double size, and on one longer than ``--tile-above`` over a grid
of overlapping tiles as well.  The passes are merged by non-maximum suppression
across classes, since a hull in an engraving comes back as both a boat and a
bear.  The extra passes are what find the far dogs of a sledge trace and the
ships at the horizon of a whaling-ground panorama: most of this collection is
600-1200 px web scans, where a whole-frame pass alone sees only the near end of
a team.

Images are loaded through Pillow with ``Image.MAX_IMAGE_PIXELS = None`` and
shrunk to a long edge of ``--max-edge`` (3000 px; two of the Bernier chart scans
are half a gigapixel) before detection, and every box is mapped back to original
raster coordinates for the ``box`` column.

Thresholds, and what the contact sheets showed
---------------------------------------------
The floor is ``--conf`` 0.30, with the per-class floors of ``--class-conf``
above it: ``cat=0.70``, ``bear=0.45``, ``airplane=0.45``, ``cow=0.40``.

The issue suggests 0.35.  Every detection in the collection was cut at 0.25 and
laid out class by class in confidence order (``--detections-to`` writes the
JSONL that makes those sheets cheap to build), and the sheets say the right
threshold is not one number:

  * ``boat`` is the strong class.  Ships in steel engravings, watercolours and
    half-tones are found down to 0.27, and between 0.30 and 0.44 nearly every
    box is a real vessel -- a barque under sail, a whaler's masts over a floe.
    0.30 is right for it; below that the icebergs start.
  * ``dog`` holds up to about 0.30 as well: many true dogs sit at 0.32-0.45,
    since a husky in a 1900 half-tone is nothing like a COCO retriever.  Under
    0.30 come mittens, boots and dark patches of shadow.
  * ``bear`` needs 0.45.  A lichened boulder is scored as high as 0.82, so no
    threshold clears the rocks out; 0.45 keeps the real bears and musk-oxen and
    drops the worst of the scree.
  * ``cow`` needs 0.40.  It is the musk-ox class here (and sometimes caribou),
    and the herd photographs sit between 0.40 and 0.72.
  * ``airplane`` needs 0.45.  Above it are aircraft and aircraft wrecks; below
    it is a schooner's rigging seen against the sky.
  * ``cat`` needs 0.70, and even then most of what it keeps is a dog.  The fur
    ruff of a parka hood with a face inside it scores 0.35-0.65 as a cat, over
    and over; above 0.70 the boxes are at least animals.

So: 0.30 globally, and the four floors above.  Every crop keeps its score in
``confidence``, so a stricter view can be taken later without re-detecting.

Sledge-dog teams
----------------
A team is a photograph in its own right.  When more than ``--team`` dogs (6) are
detected in one image, the union of their boxes is cut as an extra crop, the
first animal crop of that artifact, with ``dog-team`` in its method; the
individual dogs are then kept as usual but capped at the ``--team-cap`` (12)
largest, because the far end of a fourteen-dog trace is forty pixels of blur.

Rerunning it
------------
Resumable and idempotent, the same way faces.py is.  An artifact that already
has animal or vessel rows is skipped unless its raster is newer than the newest
of them or ``--force`` is given.  When an artifact is redone, its own animal and
vessel rows and their crops are deleted first, so a re-detection that finds
fewer animals leaves no stragglers; the human faces are never touched.

How it identifies
-----------------
Conservatively, in a separate ``--identify`` pass that can be rerun as often as
you like -- the animals and vessels tables are filled by the topic runs, so most
crops are cut before their subject has a name.  ``--identify`` re-reads every
animal and vessel row already in the table and updates only its ``person``; it
detects nothing and cuts nothing.

An animal crop is named only when

  * the artifact's title or description names exactly one animal that is in the
    ``animals`` table -- by its name or any of its ``also`` spellings, matched on
    whole words -- and
  * exactly one animal of that crop's class was detected in the image, and
  * the named animal's own kind does not contradict the class (a ``dog``
    detection will not take the name of an animal recorded as a cat; a pony
    takes a ``horse`` detection, a musk-ox a ``cow``).

recorded as ``yolo11x:dog; single-dog-single-name``.

A vessel crop is named when the title or description names exactly one vessel
in ``vessels`` (by name or ``also``: "Karluk", "HMS Investigator", "the Fram").
Several boats in one image with one vessel named is fine -- the name goes to the
largest detection only, ``single-name-largest``, and the rest stay unidentified.

Four things stop a name being read out of a caption that does not carry one.
This history is full of ships called Bear, Active, Discovery and Arctic and
dogs called Lion, Punch and Husky, and without them half the crops would be
named after the weather:

  * a mention must be capitalised as a name, so "tracks of the bear" is not the
    sealing steamer *Bear*;
  * a spelling made only of ordinary English words -- ``Bear``, ``Polar Bear``,
    ``United States``, ``Prince of Wales`` -- counts only when a cue stands
    within the three words before it (``HMS``, ``schooner``, ``whaler``,
    ``aboard``... for a vessel; ``dog``, ``team``, ``sledge``, ``pup``... for an
    animal), which is what lets "his dog Mike" name a crop and "in the Arctic"
    name nothing.  The ordinary words are ``/usr/share/dict/words`` plus a short
    list of this record's own vocabulary (``esquimaux``, ``kayak``, ``floe``);
  * a mention swallowed by a longer proper name is not a mention: "the Fram
    Museum", "Gjoa Haven", "Lady Franklin Bay", "Prince of Wales Strait";
  * a spelling that two rows share, or that is also a place in ``places``, is
    ambiguous -- Amundsen's sloop *Gjoa* and Amundsen's dog Gjoa, the vessel
    *Eagle* and Eagle River -- and an artifact whose caption uses one names
    nothing at all (``ambiguous-name``).

A crop the detector was unsure of is never named either, whatever the caption
says: below ``--name-conf`` (0.45) the box is as likely to be a hut or a
hummock as a hull, and a shaky box with a confident name is the worst row this
table can hold.

Everything else is published unidentified (``yolo11x:boat; unidentified``),
linking to the photograph.  Nothing is ever guessed.  What survives all of that
is still only as good as the caption: a photograph captioned "The Phoenix and
the Breadalbane" with one of the two in ``vessels`` gives its name to the larger
hull, and it may be the wrong hull -- the ``method`` column says which rule was
used, so such rows can be found again.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import cv2                                    # noqa: E402
import numpy as np                            # noqa: E402
from PIL import Image                         # noqa: E402

import arctic_history as H                    # noqa: E402

Image.MAX_IMAGE_PIXELS = None                 # the Bernier scans are half a gigapixel

MODEL = ROOT / "tools" / "models" / "yolo11x.pt"
MODEL_URL = ("https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt")
DETECTOR = "yolo11x"
RASTER = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".gif", ".bmp", ".webp"}

# COCO classes worth keeping, and the kind each becomes
ANIMAL_CLASSES = ("dog", "horse", "cat", "bear", "cow")
VESSEL_CLASSES = ("boat", "airplane")
KIND_OF = {**{k: "animal" for k in ANIMAL_CLASSES}, **{k: "vessel" for k in VESSEL_CLASSES}}

FIRST_N = {"animal": 100, "vessel": 200}      # never collide with faces.py, which counts from 1
MARGIN = {"animal": 0.20, "vessel": 0.10}

# classes that need more than --conf before they are believed here, read off
# the contact sheets (see the docstring): the fur ruff of a parka hood is the
# most cat-like thing in this collection, a lichened boulder the most bear-like,
# and a schooner's rigging the most aeroplane-like
CLASS_FLOOR = {"cat": 0.70, "bear": 0.45, "airplane": 0.45, "cow": 0.40}

# what an animals-table `kind` may be, per detected class; anything not listed
# is treated as unknown and does not block a name
KIND_WORDS = {
    "dog": {"dog", "sledge dog", "sled dog", "sledge-dog", "husky", "huskie", "puppy", "pup", "bitch"},
    "horse": {"horse", "pony", "mare", "mule"},
    "cat": {"cat", "kitten", "ship's cat", "ships cat"},
    "bear": {"bear", "polar bear", "cub", "bear cub"},
    "cow": {"cow", "ox", "oxen", "musk-ox", "musk ox", "muskox", "muskoxen", "caribou",
            "reindeer", "cattle", "bull", "calf"},
}


# ------------------------------------------------------------------ loading
def load_working(path: Path, max_edge: int):
    """Return (BGR array, scale, original size).  ``scale`` multiplies working
    coordinates back into the original raster."""
    im = Image.open(path)
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
def _predict(model, img, conf, imgsz, keep):
    """One YOLO pass over a BGR array; returns [x, y, w, h, conf, class]."""
    if img.shape[0] < 32 or img.shape[1] < 32:
        return []
    res = model.predict(img, conf=conf, imgsz=imgsz, verbose=False, device=0)
    out = []
    for r in res:
        names = r.names
        for b in r.boxes:
            cls = names[int(b.cls.item())]
            if cls not in keep:
                continue
            x1, y1, x2, y2 = (float(v) for v in b.xyxy[0].tolist())
            out.append([x1, y1, x2 - x1, y2 - y1, float(b.conf.item()), cls])
    return out


def _nms(boxes, thresh=0.45):
    """Merge boxes from the several passes, keeping the most confident.  Boxes
    of different classes are compared too: a hull is often both boat and bear."""
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
            if inter and inter / max(1.0, min(ba, kw * kh)) > thresh:
                break
        else:
            kept.append(b)
    return kept


def detect(model, work, conf, imgsz, keep, tile=1024, tile_above=1600, overlap=0.25, min_side=24,
           floors=None, up_below=1400):
    """The whole frame, plus a grid of overlapping tiles for anything big
    enough to hide a distant dog or a ship on the horizon."""
    h, w = work.shape[:2]
    found = list(_predict(model, work, conf, imgsz, keep))

    # most of this collection is 600-1200 px web scans in which a sledge team's
    # far dogs are twenty pixels long; a doubled pass finds them, as it does in
    # faces.py
    if max(h, w) <= up_below:
        big = cv2.resize(work, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
        for b in _predict(model, big, conf, imgsz, keep):
            found.append([b[0] / 2, b[1] / 2, b[2] / 2, b[3] / 2, b[4], b[5]])

    if max(h, w) > tile_above:
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
                for b in _predict(model, sub, conf, imgsz, keep):
                    found.append([b[0] + x0, b[1] + y0, b[2], b[3], b[4], b[5]])

    floors = floors or {}
    out = []
    for b in _nms(found):
        x, y, bw, bh = b[:4]
        x, y = max(0.0, x), max(0.0, y)
        bw, bh = min(bw, w - x), min(bh, h - y)
        if bw <= 0 or bh <= 0 or min(bw, bh) < min_side:
            continue
        if b[4] < floors.get(b[5], 0.0):
            continue
        out.append([x, y, bw, bh, b[4], b[5]])
    return out


def arrange(boxes, shape, team=6, cap=12):
    """Split the detections into (animals, vessels), each a list of
    [x, y, w, h, conf, class, note], ordered as they will be numbered.

    Sledge teams: more than ``team`` dogs and the union of the dogs is cut
    first as a ``dog-team`` crop, the individuals capped at the ``cap``
    largest.  The union is skipped when it swallows most of the frame -- half
    this collection is book plates carrying three unrelated photographs, and a
    crop of the whole page is not a picture of a team."""
    animals = [b for b in boxes if KIND_OF.get(b[5]) == "animal"]
    vessels = [b for b in boxes if KIND_OF.get(b[5]) == "vessel"]

    dogs = [b for b in animals if b[5] == "dog"]
    others = [b for b in animals if b[5] != "dog"]
    lead = []
    if len(dogs) > team:
        x0 = min(b[0] for b in dogs); y0 = min(b[1] for b in dogs)
        x1 = max(b[0] + b[2] for b in dogs); y1 = max(b[1] + b[3] for b in dogs)
        h, w = shape[:2]
        if (x1 - x0) * (y1 - y0) <= 0.6 * h * w:
            lead = [[x0, y0, x1 - x0, y1 - y0, max(b[4] for b in dogs), "dog",
                     f"dog-team-{len(dogs)}"]]
        dogs = sorted(dogs, key=lambda b: -(b[2] * b[3]))[:cap]

    def order(bs):                                    # left to right, like faces.py
        return sorted(bs, key=lambda b: (b[0], b[1]))

    animals = lead + [list(b) + [""] for b in order(dogs + others)]
    vessels = [list(b) + [""] for b in sorted(vessels, key=lambda b: -(b[2] * b[3]))]
    return animals, vessels


# -------------------------------------------------------------------- crops
def crop_box(img, box, margin, least=160):
    """The detection with ``margin`` of its size added on each side, keeping
    its shape (a ship is wide, a sitting dog is tall), upscaled gently so the
    short side is at least ``least`` px."""
    h, w = img.shape[:2]
    x, y, bw, bh = box[:4]
    x0 = int(round(max(0.0, x - bw * margin)))
    y0 = int(round(max(0.0, y - bh * margin)))
    x1 = int(round(min(float(w), x + bw * (1 + margin))))
    y1 = int(round(min(float(h), y + bh * (1 + margin))))
    if x1 - x0 < 2 or y1 - y0 < 2:
        return None
    cut = img[y0:y1, x0:x1]
    if cut.size == 0:
        return None
    short = min(cut.shape[:2])
    if short < least:
        f = least / short
        cut = cv2.resize(cut, (max(1, round(cut.shape[1] * f)), max(1, round(cut.shape[0] * f))),
                         interpolation=cv2.INTER_LANCZOS4)
    return cut


# ----------------------------------------------------------- identification
WORDLIST = Path("/usr/share/dict/words")
PREFIX = re.compile(r"^(hms|hmcs|uss|ccgs|rms|ss|mv|dgs|cgs|d\.g\.s\.|c\.g\.s\.|the)\s+", re.I)
VESSEL_CUE = {"hms", "hmcs", "uss", "ccgs", "rms", "ss", "mv", "dgs", "cgs", "d.g.s.", "c.g.s.",
              "ship", "ships", "schooner", "whaler", "whalers", "brig", "brigantine", "barque",
              "bark", "steamer", "steamship", "sealer", "cutter", "vessel", "yacht", "sloop",
              "ketch", "boat", "icebreaker", "aircraft", "aeroplane", "airplane", "plane",
              "wreck", "hulk", "aboard", "board", "deck", "decks", "crew", "bows", "stern",
              "moored", "beset", "frozen", "winter", "wintering", "quarters"}
ANIMAL_CUE = {"dog", "dogs", "dog's", "bitch", "pup", "pups", "puppy", "sledge", "sled", "sledges",
              "team", "teams", "lead", "leader", "husky", "huskies", "pony", "ponies", "horse",
              "cat", "cat's", "kitten", "bear", "cub", "ox", "musk-ox", "muskox", "mascot",
              "harness", "trace", "traces", "kennel", "driver", "driving", "named", "called"}


# ordinary words of this record that a dictionary of American English does not
# carry, and which are vessel names besides
EXTRA_PLAIN = {"esquimaux", "esquimau", "eskimaux", "eskimo", "eskimos", "inuit", "innuit",
               "umiak", "umiaq", "kayak", "qajaq", "komatik", "amauti", "iglu", "igloo",
               "floe", "floeberg", "nunatak", "sastrugi", "polynya"}


def _plain_words():
    """The ordinary English words, so that a vessel called Bear or a dog called
    Punch is not read out of every sentence that happens to use the word."""
    try:
        words = {w.strip().lower() for w in WORDLIST.read_text(errors="ignore").splitlines()
                 if w.strip() and "'" not in w}
    except Exception:
        words = set()
    return words | EXTRA_PLAIN


PLAIN = _plain_words()


def name_index(c, table):
    """{lowercase spelling: {canonical names}} over the table's names and every
    ``also`` spelling, plus each row's own kind for the sanity check.  A
    spelling two rows share (two dogs called Lion) keeps both names, so a
    mention of it is ambiguous and names nothing."""
    index, kinds = {}, {}
    for r in c.execute(f"SELECT name, kind, also FROM {table}"):
        name = r["name"]
        kinds[name] = (r["kind"] or "").strip().lower()
        spellings = [name] + [s.strip() for s in (r["also"] or "").split(";")]
        more = []
        for s in spellings:
            more.append(re.sub(r"\s*\([^)]*\)\s*", " ", s).strip())   # "Alert (whaler)" -> "Alert"
            more.append(PREFIX.sub("", s).strip())                    # "HMS Investigator" -> "Investigator"
        for s in spellings + more:
            s = s.strip(" ,.;:'\"")
            if len(s) >= 3:
                index.setdefault(s.lower(), set()).add(name)
    return index, kinds


def disambiguate(c, animals_index, vessels_index):
    """Drop the spellings that cannot tell one thing from another: a place of
    the same name (the vessel *Eagle* and Eagle River), and the spellings the
    two tables share (Amundsen's dog Gjoa and Amundsen's sloop Gjoa)."""
    places = {r["name"].strip().lower() for r in c.execute("SELECT name FROM places")}
    both = set(animals_index) & set(vessels_index)
    dropped = {}
    for index in (animals_index, vessels_index):
        for s in list(index):
            if s in places or s in both:
                dropped.setdefault(s, set()).update(index.pop(s))
    return dropped


FOLLOWER = {"museum", "bay", "island", "islands", "strait", "straits", "sound", "harbour",
            "harbor", "river", "point", "cape", "fiord", "fjord", "land", "lake", "glacier",
            "haven", "inlet", "peninsula", "channel", "expedition", "society", "company",
            "institute", "institution", "channel", "basin", "banks", "range", "mountains"}


def mentioned(text: str, index: dict, cues: set) -> set:
    """Every canonical name the text names, on whole words and capitalised as a
    name is (so "the bear" is not the sealing steamer *Bear*).  A spelling that
    is also an ordinary English word -- Bear, Punch, Discovery, Arctic -- counts
    only when one of ``cues`` stands within the three words before it."""
    hits = set()
    clean = re.sub(r"\s+", " ", text or "")
    low = clean.lower()
    for spelling, names in index.items():
        # a spelling made of nothing but ordinary words -- "Bear", "Polar Bear",
        # "United States", "Prince of Wales" -- is a name only with a cue
        tokens = [t for t in re.findall(r"[a-z']+", spelling) if t not in ("of", "the", "and")]
        needs_cue = bool(tokens) and all(t in PLAIN for t in tokens)
        for m in re.finditer(r"(?<![\w'-])" + re.escape(spelling) + r"(?![\w'-])", low):
            if not clean[m.start():m.start() + 1].isupper():
                continue                                   # a name is capitalised
            if needs_cue:
                before = re.findall(r"[\w.'-]+", low[max(0, m.start() - 40):m.start()])[-3:]
                if not any(w in cues for w in before):
                    continue
            # "the Fram Museum", "Gjoa Haven", "Lady Franklin Bay": the name is
            # part of a longer one and is not the thing in the picture
            after = re.findall(r"[\w'-]+", low[m.end():m.end() + 24])[:1]
            if after and after[0] in FOLLOWER:
                continue
            hits |= names
            break
    return hits


def kind_allows(cls: str, kind: str) -> bool:
    """Does an animals row recorded as ``kind`` fit a ``cls`` detection?  An
    unrecorded or unrecognised kind is not evidence either way, so it passes."""
    kind = (kind or "").strip().lower()
    if not kind:
        return True
    words = KIND_WORDS.get(cls, set())
    if any(w in kind for w in words):
        return True
    # a kind that plainly belongs to another of our classes rules the crop out
    for other, ws in KIND_WORDS.items():
        if other != cls and any(w in kind for w in ws):
            return False
    return True


def class_of(method: str) -> str:
    """The COCO class recorded in a row's method, e.g. 'yolo11x:dog; ...'."""
    m = re.match(r"[^:;]+:([a-z]+)", method or "")
    return m.group(1) if m else ""


def identify_rows(art, rows, animals_index, animals_kind, vessels_index, ambiguous=None,
                  floor=0.45):
    """{n: (person, rule)} for one artifact's animal and vessel rows."""
    text = " ".join([art["title"] or "", art["description"] or ""])
    out = {}

    # a caption that says "Gjoa" may mean Amundsen's sloop or Amundsen's dog:
    # an artifact that names an ambiguous thing names nothing
    if ambiguous and mentioned(text, ambiguous, ANIMAL_CUE | VESSEL_CUE):
        return {r["n"]: ("", "ambiguous-name") for r in rows}

    a_hits = mentioned(text, animals_index, ANIMAL_CUE)
    v_hits = mentioned(text, vessels_index, VESSEL_CUE)

    animal_rows = [r for r in rows if (r["kind"] or "") == "animal"]
    vessel_rows = [r for r in rows if (r["kind"] or "") == "vessel"]

    for r in animal_rows:
        cls = class_of(r["method"])
        rule = "unidentified"
        person = ""
        singles = [x for x in animal_rows
                   if class_of(x["method"]) == cls and "dog-team" not in (x["method"] or "")]
        if (len(a_hits) == 1 and len(singles) == 1 and "dog-team" not in (r["method"] or "")
                and cls and (r["confidence"] or 0) >= floor):
            name = next(iter(a_hits))
            if kind_allows(cls, animals_kind.get(name, "")):
                person, rule = name, f"single-{cls}-single-name"
        out[r["n"]] = (person, rule)

    if len(v_hits) == 1 and vessel_rows:
        name = next(iter(v_hits))
        def area(r):
            try:
                b = json.loads(r["box"] or "[]")
                return b[2] * b[3] if len(b) == 4 else 0
            except Exception:
                return 0
        biggest = max(vessel_rows, key=area)
        rule = (f"single-{class_of(biggest['method']) or 'boat'}-single-name"
                if len(vessel_rows) == 1 else "single-name-largest")
        named = biggest["n"] if (biggest["confidence"] or 0) >= floor else None
        for r in vessel_rows:
            out[r["n"]] = ((name, rule) if r["n"] == named else ("", "unidentified"))
    else:
        for r in vessel_rows:
            out[r["n"]] = ("", "unidentified")
    return out


# ------------------------------------------------------------------ the run
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


def mine(c, art_id):
    """This script's rows for one artifact, in n order."""
    return list(c.execute("SELECT * FROM faces WHERE artifact_id=? AND kind IN ('animal','vessel') "
                          "ORDER BY n", (art_id,)))


def needs_work(c, art_id, path, force):
    """Skip an artifact whose animal and vessel rows are there and no older
    than its raster.  Human face rows are ignored: they are faces.py's."""
    if force:
        return True
    rows = mine(c, art_id)
    if not rows:
        return True
    newest = max((r["updated"] or "") for r in rows)
    try:
        stamp = datetime.fromisoformat(newest).timestamp()
    except Exception:
        return True
    return path.stat().st_mtime > stamp + 1


def clear(c, art_id, topic):
    """Drop this artifact's animal and vessel rows and the crops they named.
    Never forget_faces: that would take the human faces with them."""
    c.execute("DELETE FROM faces WHERE artifact_id=? AND kind IN ('animal','vessel')", (art_id,))
    c.commit()
    d = H.HISTORY_DIR / topic / "files" / "faces"
    for old in d.glob(f"{art_id}-*.jpg"):
        m = re.search(r"-(\d+)\.jpg$", old.name)
        if m and int(m.group(1)) >= FIRST_N["animal"]:
            old.unlink()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--topic", help="one topic slug instead of all")
    ap.add_argument("--artifact", help="one artifact id")
    ap.add_argument("--force", action="store_true", help="redo artifacts already done")
    ap.add_argument("--dry-run", action="store_true", help="detect only: no crops, no rows, no log")
    ap.add_argument("--no-log", action="store_true", help="skip the per-topic worklog line")
    ap.add_argument("--identify", action="store_true",
                    help="name existing crops from the animals and vessels tables; detects nothing")
    ap.add_argument("--conf", type=float, default=0.30, help="confidence floor (default 0.30)")
    ap.add_argument("--name-conf", type=float, default=0.45,
                    help="--identify never names a detection scored below this (default 0.45)")
    ap.add_argument("--class-conf", default=",".join(f"{k}={v}" for k, v in CLASS_FLOOR.items()),
                    help="per-class floors above --conf, e.g. cat=0.55,cow=0.40 ('' for none)")
    ap.add_argument("--imgsz", type=int, default=1280, help="YOLO input size (default 1280)")
    ap.add_argument("--max-edge", type=int, default=3000, help="detect at this long edge (default 3000)")
    ap.add_argument("--tile", type=int, default=1024, help="tile size, px of the working frame")
    ap.add_argument("--tile-above", type=int, default=1600, help="tile frames longer than this (0: never)")
    ap.add_argument("--up-below", type=int, default=1400,
                    help="also detect at 2x on frames shorter than this (0: never)")
    ap.add_argument("--min-side", type=int, default=24, help="smallest detection kept, px in the frame")
    ap.add_argument("--least", type=int, default=160, help="smallest crop's short side, px (default 160)")
    ap.add_argument("--team", type=int, default=6, help="dogs above which a team crop is cut (default 6)")
    ap.add_argument("--team-cap", type=int, default=12, help="individual dogs kept from a team (default 12)")
    ap.add_argument("--who", default=f"animal crops run, {time.strftime('%Y-%m-%d')}")
    ap.add_argument("--limit", type=int, help="stop after this many artifacts (for trying it out)")
    ap.add_argument("--boxes-to", help="directory for full frames with the boxes drawn, to eyeball")
    ap.add_argument("--detections-to", help="JSONL of every detection, for tuning without re-detecting")
    a = ap.parse_args(argv)

    c = H.connect()

    # ------------------------------------------------------ the naming pass
    if a.identify:
        animals_index, animals_kind = name_index(c, "animals")
        vessels_index, _ = name_index(c, "vessels")
        ambiguous = disambiguate(c, animals_index, vessels_index)
        print(f"{len(animals_index)} animal spellings, {len(vessels_index)} vessel spellings; "
              f"{len(ambiguous)} dropped as ambiguous"
              + (f": {', '.join(sorted(ambiguous))}" if ambiguous else ""))
        ids = [r[0] for r in c.execute(
            "SELECT DISTINCT artifact_id FROM faces WHERE kind IN ('animal','vessel')")]
        named = changed = looked = 0
        for art_id in sorted(ids):
            art = c.execute("SELECT * FROM artifacts WHERE id=?", (art_id,)).fetchone()
            if not art:
                continue
            if a.topic and art["topic"] != a.topic:
                continue
            if a.artifact and art_id != a.artifact:
                continue
            rows = mine(c, art_id)
            looked += len(rows)
            verdict = identify_rows(art, rows, animals_index, animals_kind, vessels_index,
                                    ambiguous, a.name_conf)
            for r in rows:
                person, rule = verdict.get(r["n"], ("", "unidentified"))
                method = f"{DETECTOR}:{class_of(r['method']) or '?'}"
                note = re.search(r"dog-team-\d+", r["method"] or "")
                if note:
                    method += f" {note.group(0)}"
                method += f"; {rule}"
                if person:
                    named += 1
                if (r["person"] or "") != person or (r["method"] or "") != method:
                    if not a.dry_run:
                        H.add_face(c, art_id, r["n"], r["file"], box=r["box"], kind=r["kind"],
                                   person=person, confidence=r["confidence"], method=method)
                    changed += 1
                    if person:
                        print(f"  {art_id:34s} n={r['n']:3d} -> {person}  ({rule})")
        print(f"\nlooked at {looked} animal/vessel crops, {named} carry a name, {changed} rows updated")
        return 0

    # ---------------------------------------------------------- the detector
    if not MODEL.is_file():
        sys.exit(f"missing {MODEL}\n  curl -sSL -o {MODEL} {MODEL_URL}")
    from ultralytics import YOLO
    model = YOLO(str(MODEL))
    keep = set(KIND_OF)
    floors = {}
    for part in (a.class_conf or "").split(","):
        if part.strip():
            cls, _, v = part.partition("=")
            floors[cls.strip()] = float(v)
    dump = open(a.detections_to, "w") if a.detections_to else None

    jobs = candidates(c, a.topic, a.artifact)
    if a.limit:
        jobs = jobs[:a.limit]

    per_topic, per_class, dogs_in, scanned, skipped, total = {}, {}, [], 0, 0, 0
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
        boxes = detect(model, work, a.conf, a.imgsz, keep,
                       tile=a.tile, tile_above=a.tile_above or 10 ** 9, min_side=a.min_side,
                       floors=floors, up_below=a.up_below)
        animals, vessels = arrange(boxes, work.shape, a.team, a.team_cap)
        if dump:
            dump.write(json.dumps({"id": art["id"], "topic": art["topic"], "file": str(path),
                                   "size": list(orig), "scale": scale,
                                   "title": (art["title"] or "")[:120],
                                   "dets": [[round(v, 2) if isinstance(v, float) else v for v in b]
                                            for b in boxes]}) + "\n")
            dump.flush()
        n_dogs = sum(1 for b in boxes if b[5] == "dog")
        if n_dogs:
            dogs_in.append((n_dogs, art["id"], art["title"] or ""))

        t = per_topic.setdefault(art["topic"], {"images": 0, "animals": 0, "vessels": 0})
        t["images"] += 1

        if not a.dry_run and (animals or vessels or mine(c, art["id"])):
            clear(c, art["id"], art["topic"])          # only ever our own rows and crops

        outdir = H.HISTORY_DIR / art["topic"] / "files" / "faces"
        for kind, group in (("animal", animals), ("vessel", vessels)):
            for i, b in enumerate(group):
                n = FIRST_N[kind] + i
                ob = [int(round(b[0] * scale)), int(round(b[1] * scale)),
                      int(round(b[2] * scale)), int(round(b[3] * scale))]
                total += 1
                t[kind + "s"] += 1
                per_class[b[5]] = per_class.get(b[5], 0) + 1
                if a.dry_run:
                    continue
                outdir.mkdir(parents=True, exist_ok=True)
                cut = crop_box(work, b, MARGIN[kind], a.least)
                if cut is None:
                    continue
                name = f"{art['id']}-{n}.jpg"
                cv2.imwrite(str(outdir / name), cut, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                method = f"{DETECTOR}:{b[5]}" + (f" {b[6]}" if b[6] else "") + "; unidentified"
                H.add_face(c, art["id"], n, f"{art['topic']}/files/faces/{name}", box=ob,
                           kind=kind, person="", confidence=b[4], method=method)

        if a.boxes_to and (animals or vessels):
            d = Path(a.boxes_to)
            d.mkdir(parents=True, exist_ok=True)
            marked = work.copy()
            for kind, group in (("animal", animals), ("vessel", vessels)):
                col = (0, 0, 255) if kind == "animal" else (255, 128, 0)
                for i, b in enumerate(group):
                    p1 = (int(b[0]), int(b[1])); p2 = (int(b[0] + b[2]), int(b[1] + b[3]))
                    cv2.rectangle(marked, p1, p2, col, 2)
                    cv2.putText(marked, f"{FIRST_N[kind] + i}:{b[5]}:{b[4]:.2f}",
                                (p1[0], max(12, p1[1] - 4)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 1)
            cv2.imwrite(str(d / f"{art['id']}.jpg"), marked, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

        if animals or vessels:
            what = ", ".join(f"{b[5]}{'*' if b[6] else ''} {b[4]:.2f}" for b in animals + vessels)
            print(f"{art['id']:36s} {len(animals):2d}a {len(vessels):2d}v  {orig[0]}x{orig[1]}  {what[:80]}")

    if dump:
        dump.close()
    print(f"\nscanned {scanned}, skipped {skipped} already done, {total} crops")
    for cls, n in sorted(per_class.items(), key=lambda kv: -kv[1]):
        print(f"  {cls:9s} {n:5d}  ({KIND_OF[cls]})")
    print("\nmost dogs in one image:")
    dogs_in.sort(reverse=True)
    for n, aid, title in dogs_in[:10]:
        print(f"  {n:3d}  {aid:34s} {title[:60]}")

    if not a.dry_run and not a.no_log:
        for topic, t in sorted(per_topic.items()):
            done = (f"animal and vessel crops: {t['images']} rasters scanned with {DETECTOR} "
                    f"(conf {a.conf}), {t['animals']} animal and {t['vessels']} vessel crops cut to "
                    f"files/faces/ (numbered from 100 and 200, beside faces.py's human faces); rows "
                    f"in the faces table with kind, published by publish()")
            subprocess.run(["/usr/bin/python3", str(ROOT / "tools" / "history-db.py"), "log",
                            "--topic", topic, "--who", a.who, "--done", done,
                            "--next", "tools/animal-crops.py --identify once the animals and "
                                      "vessels tables have this topic's names; detection re-runs "
                                      "only on rasters newer than their crops"],
                           cwd=ROOT, check=True, capture_output=True)
        print(f"worklog written for {len(per_topic)} topic(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
