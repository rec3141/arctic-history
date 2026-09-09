#!/usr/bin/env python3
"""Subject keywords for the images, maps and quotes (issue #3).

Two passes against the local model on grid's Ollama (gemma4), both resumable:

  1. ``tree``  reads every image, map and quote, asks the model for candidate
     subject headings a batch of ~60 at a time, then makes ONE consolidation
     call that returns a tree of two to three levels: picture branches carry
     subjects (People & portraits, Ships & boats, Ice & sea ...) and word
     branches carry themes (Naming, Hardship, Encounter, Ice ...).  The tree
     is written to the ``ontology`` table with ``H.set_ontology`` and copied,
     with the picture/word side of each first-level branch, to
     ``db/history/_ledger/ontology.json``.

  2. ``tag``   asks the model, one call per artifact, for one to three paths
     taken FROM the tree, validates each against the tree, retries once with
     a stricter prompt, drops what is still invalid, and writes the survivors
     with ``H.add_keywords(..., source="llm:gemma4")``.  Rows whose source is
     ``crew`` are never read, replaced or deleted: a crew path outranks the
     model's and ``artifact_keywords`` puts it first.

THE STABILITY RULE.  The tree is the deliverable that must stay put; the tags
can be regenerated at will.  A later run therefore only ever EXTENDS the tree
that is already in the database: no first- or second-level branch is renamed,
reordered or dropped, whatever the model proposes, because the ship's pages
make a section per first level and a heading per second and would reshuffle
under the crew's feet.  New third-level terms met while tagging are added to
the tree (``--no-new-level3`` forbids it, ``--max-new-level3`` caps them); a
path whose first or second level is not already in the tree is dropped, not
invented.  Only a person editing the tree by hand and calling
``tools/history-db.py ontology --file tree.json`` may change what exists.

Runs (from /data/dev/arctic-history, with the model loaded on Ollama):

    /usr/bin/python3 tools/keywords.py all            # tree if none, then the untagged
    /usr/bin/python3 tools/keywords.py tag            # the incremental rerun
    /usr/bin/python3 tools/keywords.py tag --force    # retag everything
    /usr/bin/python3 tools/keywords.py tree --extend  # widen the tree, keeping every branch
    /usr/bin/python3 tools/keywords.py show           # the tree and what is tagged

``tag`` picks up artifacts with no path from this model and artifacts edited
since their paths were written, so it can be interrupted and rerun; every
artifact is committed as it is answered.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import arctic_history as H                                       # noqa: E402

OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = "gemma4:26b"
KINDS = ("image", "map", "quote")
LEDGER = ROOT / "db" / "history" / "_ledger" / "ontology.json"

# the branches the ship asked for, offered to the consolidation call as a spine
SEED_PICTURES = ["People & portraits", "Ships & boats", "Ice & sea", "Land & settlements",
                 "Camps & winterings", "Inuit life", "Documents & charts",
                 "Objects & equipment", "Graves & relics"]
SEED_WORDS = ["Naming", "Hardship", "Encounter", "Ice", "Navigation", "Science",
              "Death", "Return", "Humour"]

STATS = {"calls": 0, "seconds": 0.0, "prompt_tokens": 0, "tokens": 0, "errors": 0}


# ------------------------------------------------------------------ the model
def chat(messages, model=MODEL, temperature=0.0, timeout=600, num_predict=None):
    """One request, one in flight at a time. Returns the assistant's text."""
    opts = {"temperature": temperature}
    if num_predict:
        opts["num_predict"] = num_predict
    body = {"model": model, "stream": False, "think": False, "options": opts,
            "messages": messages}
    req = urllib.request.Request(OLLAMA + "/api/chat",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, OSError) as e:
        STATS["errors"] += 1
        raise RuntimeError("ollama at %s: %s" % (OLLAMA, e))
    STATS["calls"] += 1
    STATS["seconds"] += time.time() - t0
    STATS["prompt_tokens"] += int(d.get("prompt_eval_count") or 0)
    STATS["tokens"] += int(d.get("eval_count") or 0)
    return (d.get("message") or {}).get("content") or ""


_FENCE = re.compile(r"```(?:json|JSON)?\s*(.*?)```", re.S)


def _balanced(text, open_ch, close_ch):
    i = text.find(open_ch)
    if i < 0:
        return None
    depth, in_str, esc = 0, False, False
    for j in range(i, len(text)):
        ch = text[j]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    return None


def parse_json(text):
    """gemma4 wraps its JSON in ``` fences and sometimes chats around it."""
    t = (text or "").strip()
    m = _FENCE.search(t)
    if m:
        t = m.group(1).strip()
    for cand in (t, _balanced(t, "{", "}"), _balanced(t, "[", "]")):
        if not cand:
            continue
        try:
            return json.loads(cand)
        except ValueError:
            continue
    return None


# ------------------------------------------------------------ the artifacts
def _tags(raw):
    try:
        v = json.loads(raw or "[]")
    except ValueError:
        v = [raw]
    out = []
    for item in v if isinstance(v, list) else [v]:
        for part in str(item).split(","):
            part = part.strip()
            if part and part not in out:
                out.append(part)
    return out


_QUOTE_PAIRS = (('"', '"'), ("“", "”"), ("'", "'"), ("‘", "’"))


def quote_words(desc):
    """The words themselves, not the note on the source. Quote artifacts put
    the passage in ``description``, usually after a sentence of setting; the
    passage is what carries the theme, so pull the quoted spans out and keep
    the rest only as a short hint."""
    desc = desc or ""
    found = []
    for op, cl in _QUOTE_PAIRS:
        pat = re.escape(op) + "([^" + re.escape(op + cl) + "]{25,})" + re.escape(cl)
        for m in re.finditer(pat, desc):
            found.append((m.start(), m.end(), m.group(1).strip()))
    found.sort(key=lambda s: (s[0], -s[1]))
    spans, kept = [], []
    for st, en, txt in found:                    # outermost only: 'x' inside "..." is not a second quote
        if any(st >= a and en <= b for a, b in kept):
            continue
        kept.append((st, en))
        spans.append(txt)
    words = " ... ".join(spans)
    if len(words) < 40:
        return desc.strip(), ""
    note = desc
    for s in spans:
        note = note.replace(s, " ")
    note = re.sub(r"[\s\"'“”‘’.]{2,}", " ", note).strip()
    return words, note


def brief(a, n=260):
    if a["type"] == "quote":
        words, note = quote_words(a["description"])
        out = "WORDS: " + words[:n]
        if note:
            out += "  (source note: " + note[:90] + ")"
        return out
    return (a["description"] or "")[:n].strip()


def line(a, n=170):
    bits = [a["title"] or "(untitled)"]
    b = brief(a, n)
    if b:
        bits.append(b)
    t = _tags(a["tags"])
    if t:
        bits.append("tags: " + ", ".join(t[:6]))
    return "- [%s] %s" % (a["type"], " | ".join(bits))


def load_artifacts(c, kinds=KINDS):
    marks = ",".join("?" * len(kinds))
    rows = c.execute("SELECT * FROM artifacts WHERE type IN (%s) ORDER BY type, topic, id" % marks,
                     tuple(kinds)).fetchall()
    return [dict(r) for r in rows]


# ----------------------------------------------------------------- the tree
def norm_tree(raw):
    """Coerce whatever the model returned into {L1: {L2: [L3, ...]}}."""
    tree = {}
    if not isinstance(raw, dict):
        return tree
    for l1, subs in raw.items():
        l1 = str(l1).strip()
        if not l1 or l1.lower() in ("pictures", "words", "images", "quotes"):
            continue
        node = tree.setdefault(l1, {})
        if isinstance(subs, dict):
            items = subs.items()
        elif isinstance(subs, list):
            items = [(s, []) for s in subs]
        else:
            items = [(subs, [])]
        for l2, l3s in items:
            l2 = str(l2).strip()
            if not l2:
                continue
            leaves = node.setdefault(l2, [])
            if isinstance(l3s, dict):
                l3s = list(l3s.keys())
            if isinstance(l3s, str):
                l3s = [l3s]
            for l3 in l3s or []:
                l3 = str(l3).strip()
                if l3 and l3.lower() not in [x.lower() for x in leaves]:
                    leaves.append(l3)
    return tree


def merge_tree(base, extra):
    """Extend only: a branch already in ``base`` keeps its name and its
    place, and nothing is ever removed."""
    out = json.loads(json.dumps(base))
    lower1 = dict((k.lower(), k) for k in out)
    added = {"l1": 0, "l2": 0, "l3": 0}
    for l1, subs in (extra or {}).items():
        k1 = lower1.get(l1.lower())
        if k1 is None:
            k1 = l1
            out[k1] = {}
            lower1[l1.lower()] = k1
            added["l1"] += 1
        lower2 = dict((k.lower(), k) for k in out[k1])
        for l2, l3s in subs.items():
            k2 = lower2.get(l2.lower())
            if k2 is None:
                k2 = l2
                out[k1][k2] = []
                lower2[l2.lower()] = k2
                added["l2"] += 1
            have = [x.lower() for x in out[k1][k2]]
            for l3 in l3s:
                if l3.lower() not in have:
                    out[k1][k2].append(l3)
                    have.append(l3.lower())
                    added["l3"] += 1
    return out, added


def compact(tree, only=None):
    """The tree as the prompt sees it: one first level per stanza."""
    out = []
    for l1, subs in tree.items():
        if only and l1 not in only:
            continue
        out.append(l1)
        for l2, l3s in subs.items():
            out.append("  %s%s" % (l2, (": " + " | ".join(l3s)) if l3s else ""))
    return "\n".join(out)


BATCH_SYS = ("You are a librarian building subject headings for a historical archive of the "
             "Canadian Arctic Archipelago and Baffin Bay: expedition photographs and engravings, "
             "charts, and short verbatim passages from journals and testimony. "
             "Answer with JSON only, no commentary.")


def batch_headings(items, kind, model):
    """Candidate headings for one batch of ~60 artifacts."""
    if kind == "pictures":
        want = ("subject headings for PICTURES: what is shown in the image or chart "
                "(people, ships, ice, land, camps, Inuit life, documents, objects, graves)")
    else:
        want = ("theme headings for WORDS: what the passage is about "
                "(naming, hardship, encounter, ice, navigation, science, death, return, humour)")
    user = ("Here are %d items from the archive.\n\n%s\n\nPropose %s. "
            "Give 8 to 14 headings that between them cover these items, each with 2 to 5 "
            "sub-headings. Short noun phrases, title case, no numbering.\n"
            "Answer as JSON: {\"Heading\": [\"sub-heading\", ...], ...}"
            % (len(items), "\n".join(line(a) for a in items), want))
    raw = parse_json(chat([{"role": "system", "content": BATCH_SYS},
                           {"role": "user", "content": user}], model=model))
    if not isinstance(raw, dict):
        return {}
    shaped = {}
    for k, v in raw.items():
        if isinstance(v, dict):
            shaped[k] = v
        else:
            subs = v if isinstance(v, list) else [v]
            shaped[k] = dict((str(s), []) for s in subs)
    return norm_tree(shaped)


def consolidate(cands_pic, cands_word, model, existing=None):
    """One tree from all the batches' candidates. With an existing tree, ask
    only for what is missing: nothing already there may be renamed."""
    pic = "\n".join("- %s: %s" % (k, ", ".join(v)) for k, v in cands_pic.items())
    word = "\n".join("- %s: %s" % (k, ", ".join(v)) for k, v in cands_word.items())
    keep = ""
    if existing:
        keep = ("\nA tree already exists and MUST NOT change: every branch below keeps its "
                "exact name and none may be dropped or merged. Return the whole tree with "
                "these branches unchanged, adding only what is genuinely missing.\n\n"
                "EXISTING TREE:\n%s\n" % compact(existing))
    user = (
        "Candidate subject headings proposed for the PICTURES (images and maps):\n%s\n\n"
        "Candidate theme headings proposed for the WORDS (quoted passages):\n%s\n%s\n"
        "Consolidate these into ONE subject tree for the archive, two to three levels deep, "
        "with 12 to 16 first-level branches in all. Merge synonyms; drop headings that would "
        "hold only one or two items.\n"
        "Keep the picture branches and the word branches separate. Picture branches are "
        "subjects of a photograph, engraving or chart, along the lines of: %s. Word branches "
        "are themes of a quoted passage, along the lines of: %s. Use those names where they "
        "fit; you may rename, add or leave one out where the material asks for it.\n"
        "Each first-level branch gets 3 to 6 second-level branches; a second-level branch gets "
        "0 to 6 third-level terms. Short noun phrases, title case.\n"
        "Answer as JSON and nothing else:\n"
        "{\"pictures\": {\"Level 1\": {\"Level 2\": [\"Level 3\", ...], ...}, ...}, "
        "\"words\": {\"Level 1\": {\"Level 2\": [\"Level 3\", ...], ...}, ...}}"
        % (pic, word, keep, ", ".join(SEED_PICTURES), ", ".join(SEED_WORDS)))
    raw = parse_json(chat([{"role": "system", "content": BATCH_SYS},
                           {"role": "user", "content": user}], model=model, timeout=900))
    if not isinstance(raw, dict):
        return {}, {}
    sides = {}
    tree = {}
    for side in ("pictures", "words"):
        part = norm_tree(raw.get(side) or {})
        for l1 in part:
            sides.setdefault(l1, side)
        tree, _ = merge_tree(tree, part)
    if not tree:                                   # the model ignored the split
        tree = norm_tree(raw)
        for l1 in tree:
            sides.setdefault(l1, "pictures")
    return tree, sides


def read_sides():
    try:
        return json.loads(LEDGER.read_text()).get("sides") or {}
    except Exception:
        return {}


def write_ledger(tree, sides, model):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps({"generated": H.now(), "model": model,
                                  "sides": sides, "tree": tree},
                                 ensure_ascii=False, indent=1) + "\n")


def build_tree(c, model, batch=60, extend=False, kinds=KINDS):
    arts = load_artifacts(c, kinds)
    pics = [a for a in arts if a["type"] in ("image", "map")]
    words = [a for a in arts if a["type"] == "quote"]
    existing = (H.get_ontology(c) or {}).get("tree") or {}
    if existing and not extend:
        print("ontology already in the database: %d first-level branches, kept as it is "
              "(pass --extend to widen it)" % len(existing))
        return existing, read_sides()
    cands_pic, cands_word = {}, {}
    for name, rows, bag in (("pictures", pics, cands_pic), ("words", words, cands_word)):
        for i in range(0, len(rows), batch):
            chunk = rows[i:i + batch]
            got = batch_headings(chunk, name, model)
            for l1, subs in got.items():
                bag.setdefault(l1, [])
                for l2 in subs:
                    if l2 not in bag[l1]:
                        bag[l1].append(l2)
            print("  %s batch %d/%d: %d headings (%d so far)"
                  % (name, i // batch + 1, (len(rows) + batch - 1) // batch, len(got), len(bag)))
    print("consolidating %d picture and %d word candidate headings ..."
          % (len(cands_pic), len(cands_word)))
    fresh, sides = consolidate(cands_pic, cands_word, model, existing or None)
    if not fresh:
        raise SystemExit("the model returned no usable tree; nothing written")
    tree, added = merge_tree(existing, fresh)      # extend only, never rename or drop
    old_sides = read_sides()
    old_sides.update(dict((k, v) for k, v in sides.items() if k not in old_sides))
    H.set_ontology(c, tree, model=model)
    write_ledger(tree, old_sides, model)
    print("tree: %d first-level branches, %d second, %d third (+%d/+%d/+%d this run)"
          % (len(tree), sum(len(v) for v in tree.values()),
             sum(len(x) for v in tree.values() for x in v.values()),
             added["l1"], added["l2"], added["l3"]))
    return tree, old_sides


# ------------------------------------------------------------------ the tags
TAG_SYS = ("You index a historical archive of the Canadian Arctic. You are given a fixed "
           "subject tree and one artifact, and you answer with subject paths taken from that "
           "tree. Never invent a first- or second-level branch. Answer with JSON only.")


def artifact_block(a):
    out = ["type: " + a["type"], "title: " + (a["title"] or "")]
    if a["creator"]:
        out.append("creator: " + a["creator"])
    if a["date_text"]:
        out.append("date: " + a["date_text"])
    out.append("topic: " + (a["topic"] or ""))
    t = _tags(a["tags"])
    if t:
        out.append("tags: " + ", ".join(t))
    b = brief(a, 700)
    if b:
        out.append(("words" if a["type"] == "quote" else "description") + ": " + b)
    return "\n".join(out)


def tag_prompt(a, tree_text, strict=False):
    aim = ("This is a quoted passage: tag the THEME of the words themselves, not the note on "
           "the source, and not the expedition it belongs to." if a["type"] == "quote" else
           "This is a picture: tag what it SHOWS, not the medium it is in. Do not tag a "
           "photograph as a photograph or an engraving as an engraving; use the documents "
           "and charts branch only when the item itself is a map, chart, plan or document.")
    tail = ("\nYour previous answer was rejected. Copy the levels EXACTLY as spelled in the "
            "tree above, character for character. Do not translate, shorten or pluralise them."
            if strict else "")
    return [{"role": "system", "content": TAG_SYS + "\n\nTREE:\n" + tree_text},
            {"role": "user",
             "content": ("ARTIFACT\n%s\n\n%s\nGive one to three paths from the tree, best "
                         "first. A path is \"Level 1 > Level 2\" or \"Level 1 > Level 2 > "
                         "Level 3\". Level 1 and Level 2 must appear in the tree exactly as "
                         "written there.%s\nAnswer as a JSON list of strings and nothing else."
                         % (artifact_block(a), aim, tail))}]


def paths_from(raw):
    if isinstance(raw, dict):
        for k in ("paths", "keywords", "subjects", "answer"):
            if isinstance(raw.get(k), list):
                raw = raw[k]
                break
        else:
            raw = list(raw.values())
    if isinstance(raw, str):
        raw = [raw]
    out = []
    for p in raw if isinstance(raw, list) else []:
        if isinstance(p, list):
            p = " > ".join(str(x) for x in p)
        p = str(p).strip()
        if p:
            out.append(p)
    return out


class Validator(object):
    """Level 1 and 2 must already be in the tree (matched case-insensitively
    and spelled back the tree's way). A new level 3 may be admitted, and is
    then added to the tree; nothing else is ever created."""

    def __init__(self, tree, allow_new_l3=True, cap=80):
        self.tree = tree
        self.allow = allow_new_l3
        self.cap = cap
        self.new_l3 = []
        self.reindex()

    def reindex(self):
        self.i1 = dict((k.lower(), k) for k in self.tree)
        self.i2 = dict((k.lower(), dict((x.lower(), x) for x in v)) for k, v in self.tree.items())
        self.i3 = dict((k.lower(), dict((x.lower(), dict((y.lower(), y) for y in ys))
                                        for x, ys in v.items()))
                       for k, v in self.tree.items())

    def check(self, path):
        """-> (canonical path, verdict) with verdict in ok / trimmed / new3 / bad."""
        # the model sometimes copies the tree's own "Level 2: Level 3" layout
        parts = [p.strip() for p in str(path).replace(":", ">").split(">") if p.strip()]
        if len(parts) < 2:
            return None, "bad"
        l1 = self.i1.get(parts[0].lower())
        if not l1:
            return None, "bad"
        l2 = self.i2[l1.lower()].get(parts[1].lower())
        if not l2:
            # a level 3 given where level 2 belongs: put the missing level back
            for k2, leaves in self.i3[l1.lower()].items():
                if parts[1].lower() in leaves:
                    return "%s > %s > %s" % (l1, self.i2[l1.lower()][k2], leaves[parts[1].lower()]), "ok"
            return None, "bad"
        if len(parts) == 2:
            return "%s > %s" % (l1, l2), "ok"
        # "|" separates the tree's own third-level terms: the model sometimes copies the row
        cand = parts[2].split("|")[0].strip()[:40].strip()
        l3 = self.i3[l1.lower()][l2.lower()].get(cand.lower())
        if l3:
            return "%s > %s > %s" % (l1, l2, l3), "ok"
        if self.allow and len(self.new_l3) < self.cap and 2 < len(cand) <= 40:
            self.tree[l1][l2].append(cand)
            self.new_l3.append("%s > %s > %s" % (l1, l2, cand))
            self.reindex()
            return "%s > %s > %s" % (l1, l2, cand), "new3"
        return "%s > %s" % (l1, l2), "trimmed"


def needing(c, model_source, kinds=KINDS, force=False):
    marks = ",".join("?" * len(kinds))
    if force:
        return [dict(r) for r in c.execute(
            "SELECT * FROM artifacts WHERE type IN (%s) ORDER BY type, topic, id" % marks,
            tuple(kinds))]
    q = ("SELECT a.* FROM artifacts a LEFT JOIN "
         "(SELECT artifact_id, MAX(updated) AS u FROM keywords WHERE source=? GROUP BY artifact_id) k "
         "ON k.artifact_id = a.id "
         "WHERE a.type IN (%s) AND (k.u IS NULL OR k.u < a.updated) "
         "ORDER BY a.type, a.topic, a.id" % marks)
    return [dict(r) for r in c.execute(q, (model_source,) + tuple(kinds))]


def run_tags(c, tree, sides, model, source, force=False, kinds=KINDS, limit=0,
             allow_new_l3=True, cap=80, verbose=False):
    todo = needing(c, source, kinds, force)
    if limit:
        todo = todo[:limit]
    v = Validator(tree, allow_new_l3, cap)
    pic_side = [k for k in tree if sides.get(k, "pictures") == "pictures"]
    word_side = [k for k in tree if sides.get(k) == "words"]
    text_pic = compact(tree, pic_side or None)
    text_word = compact(tree, word_side or None)
    counts = {"tagged": 0, "none": 0, "paths": 0, "ok": 0, "bad": 0, "trimmed": 0, "new3": 0,
              "retried": 0, "unparsed": 0}
    per_type = {}
    per_topic = {}
    t0 = time.time()
    for n, a in enumerate(todo, 1):
        text = text_word if (a["type"] == "quote" and word_side) else text_pic
        good = []
        for attempt in (0, 1):
            try:
                raw = chat(tag_prompt(a, text, strict=bool(attempt)), model=model, num_predict=200)
            except RuntimeError as e:
                print("  ! %s: %s" % (a["id"], e))
                break
            cand = paths_from(parse_json(raw))
            if not cand:
                counts["unparsed"] += 1
            for p in cand:
                canon, verdict = v.check(p)
                counts[verdict] = counts.get(verdict, 0) + 1
                if verdict == "bad":
                    continue
                if canon and canon not in good:
                    good.append(canon)
            if good or attempt:
                break
            counts["retried"] += 1
        good = good[:3]
        if good:
            H.add_keywords(c, a["id"], good, source=source, replace=True)
            counts["tagged"] += 1
            counts["paths"] += len(good)
            per_type[a["type"]] = per_type.get(a["type"], 0) + 1
            per_topic[a["topic"]] = per_topic.get(a["topic"], 0) + 1
        else:
            counts["none"] += 1
        if verbose or n % 25 == 0 or n == len(todo):
            el = time.time() - t0
            print("  %4d/%d  %-28s %-6s %s  [%.1fs, %.2fs/artifact]"
                  % (n, len(todo), a["id"], a["type"], " ; ".join(good) or "(none)",
                     el, el / max(n, 1)))
    if v.new_l3:
        H.set_ontology(c, v.tree, model=model)
        write_ledger(v.tree, sides, model)
        print("tree extended with %d new third-level terms: %s"
              % (len(v.new_l3), "; ".join(v.new_l3[:12]) + (" ..." if len(v.new_l3) > 12 else "")))
    counts["seconds"] = time.time() - t0
    return counts, per_type, per_topic


def worklog(c, per_topic, when, kinds):
    for topic in sorted(per_topic):
        H.add_worklog(c, topic,
                      done=("keywords: %d %s artifacts tagged with paths from the subject "
                            "ontology (source llm:%s)"
                            % (per_topic[topic], "/".join(kinds), MODEL.split(":")[0])),
                      next="", open="", who="keywords run, " + when)


# ---------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", nargs="?", default="all", choices=("all", "tree", "tag", "show"))
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--types", default=",".join(KINDS))
    ap.add_argument("--batch", type=int, default=60)
    ap.add_argument("--limit", type=int, default=0, help="stop after this many artifacts")
    ap.add_argument("--force", action="store_true", help="retag artifacts that already have paths")
    ap.add_argument("--extend", action="store_true", help="tree: widen an existing tree")
    ap.add_argument("--no-new-level3", action="store_true", help="never add a third level")
    ap.add_argument("--max-new-level3", type=int, default=80)
    ap.add_argument("--who", default=time.strftime("%Y-%m-%d"))
    ap.add_argument("--no-worklog", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)

    kinds = tuple(x.strip() for x in a.types.split(",") if x.strip())
    source = "llm:" + a.model.split(":")[0]
    c = H.connect()

    if a.cmd == "show":
        o = H.get_ontology(c) or {}
        print(compact(o.get("tree") or {}) or "no ontology yet")
        for r in c.execute("SELECT a.type, k.source, count(DISTINCT a.id) n FROM artifacts a "
                           "JOIN keywords k ON k.artifact_id=a.id GROUP BY a.type, k.source"):
            print("%s %s: %d tagged" % (r["type"], r["source"], r["n"]))
        return 0

    tree, sides = {}, {}
    if a.cmd in ("all", "tree"):
        tree, sides = build_tree(c, a.model, a.batch, a.extend, kinds)
    if a.cmd == "tree":
        return 0

    if not tree:
        o = H.get_ontology(c) or {}
        tree, sides = o.get("tree") or {}, read_sides()
    if not tree:
        raise SystemExit("no ontology in the database; run `keywords.py tree` first")

    counts, per_type, per_topic = run_tags(
        c, tree, sides, a.model, source, force=a.force, kinds=kinds, limit=a.limit,
        allow_new_l3=not a.no_new_level3, cap=a.max_new_level3, verbose=a.verbose)
    if per_topic and not a.no_worklog:
        worklog(c, per_topic, a.who, kinds)
    print("\n%s" % json.dumps({"counts": counts, "per_type": per_type,
                               "topics": len(per_topic), "model": STATS}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
