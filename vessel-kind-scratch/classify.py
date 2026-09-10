"""Draft classifier: free-text vessel kind -> controlled code + kind_note.

Reads every distinct kind value from vessels, assigns a code and the note that
carries what the code drops, and writes mapping.md for review. Read-only
against the DB unless --apply is given.

The rule: the code names what the vessel is (the rig or the hull) where the
entry names it, and what she was built or fitted for where that is all the
entry gives. A whaling barque is a `barque` whose note says "whaler"; a whaler
whose rig no source records is a `whaler`. Rig spellings and near neighbours
are folded (bark to barque, brigantine to brig), propulsion is a note rather
than a code (except steam-whaler, an era of its own), and the note keeps the
class, the aircraft type, the trade, the conversion and the purchaser.

Codes (rigs, then small craft, then power, then the trades and the work):
  ship barque brig schooner sloop yacht bomb-vessel
  boat umiak
  steamer tender icebreaker submarine
  whaler steam-whaler sealer
  research-vessel cruise-ship transport freighter tanker aircraft
"""
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arctic_history as H          # noqa: E402

DB = H.HISTORY_DB                   # ARCTIC_HISTORY_DB_DIR moves it
OUT = Path(__file__).with_name("mapping.md")

TAIL = object()          # the note is whatever follows the first comma


# (regex, code, note, judgement call or None). First match wins; order matters.
RULES = [
    # --- aircraft: the type is the note ------------------------------------
    (r"^aircraft, ", "aircraft", TAIL, None),

    # --- the trades, where no rig is named ---------------------------------
    (r"^steam whaler and sealer$", "steam-whaler", "also a sealer", None),
    (r"^steam whaler$", "steam-whaler", "", None),
    (r"^whaler, ", "whaler", TAIL, None),
    (r"^whaler$", "whaler", "", None),
    (r"^sealing steamer$", "sealer", "steam", None),
    (r"^sealing steamer, ", "sealer", "steam, purchased by the United States Navy",
     "bought for the Greely relief and kept in government service; coded by the trade she was built for"),
    (r"^steam sealer, converted$", "sealer", "steam, converted", None),
    (r"^steam sealer$", "sealer", "steam", None),
    (r"^motor sealer$", "sealer", "motor", None),

    # --- whaling and other trades under a named rig: the rig wins ----------
    (r"^whaling barque$", "barque", "whaler", "rig stated, so the rig is the code and the trade the note"),
    (r"^whaling brig$", "brig", "whaler", "rig stated, so the rig is the code and the trade the note"),
    (r"^barque, whaler$", "barque", "whaler", None),
    (r"^brig, whaler$", "brig", "whaler", None),
    (r"^schooner, whaler$", "schooner", "whaler", None),
    (r"^brigantine, former whaler$", "brig", "brigantine, formerly a whaler",
     "brigantine folded into brig; the rig is kept in the note"),

    # --- sailing rigs ------------------------------------------------------
    (r"^barque, ", "barque", TAIL, None),
    (r"^barque$", "barque", "", None),
    (r"^bark$", "barque", "",
     "the Elizabethan 'bark' means a small vessel, not the later barque rig"),
    (r"^busse$", "barque", "busse",
     "a busse is an Elizabethan fishing vessel; filed with the small Elizabethan hulls"),
    (r"^brig, ", "brig", TAIL, None),
    (r"^brig$", "brig", "", None),
    (r"^gun-brig$", "brig", "gun-brig", None),
    (r"^screw schooner yacht$", "yacht", "screw schooner", None),
    (r"^screw steam yacht$", "yacht", "screw steam", None),
    (r"^yacht$", "yacht", "", None),
    (r"^three-masted schooner, purpose-built for the ice$", "schooner",
     "three-masted, purpose-built for the ice", None),
    (r"^three-masted auxiliary schooner$", "schooner", "three-masted, auxiliary", None),
    (r"^auxiliary schooner, ice-strengthened$", "schooner", "auxiliary, ice-strengthened", None),
    (r"^steam schooner, purpose-built for ice$", "schooner", "steam, purpose-built for ice", None),
    (r"^motor schooner$", "schooner", "motor", None),
    (r"^Gloucester fishing schooner$", "schooner", "Gloucester fishing", None),
    (r"^mail schooner$", "schooner", "mail", None),
    (r"^walrus schooner$", "schooner", "walrus hunting", None),
    (r"^schooner, ", "schooner", TAIL, None),
    (r"^schooner$", "schooner", "", None),
    (r"^sloop, ", "sloop", TAIL, None),
    (r"^sloop$", "sloop", "", None),
    (r"^bomb vessel$", "bomb-vessel", "", None),
    (r"^frigate$", "ship", "frigate",
     "no frigate code: a frigate is full-rigged, so she is filed as a ship"),
    (r"^ship of the Queen's navy$", "ship", "of the Queen's navy", None),
    (r"^ship$", "ship", "", None),

    # --- small craft -------------------------------------------------------
    (r"^pinnace$", "boat", "pinnace", None),
    (r"^steam launch$", "boat", "steam launch", None),
    (r"^ship's boats?$", "boat", "", None),
    (r"^open skin boat$", "umiak", "", None),

    # --- power -------------------------------------------------------------
    (r"^icebreaker, ", "icebreaker", TAIL, None),
    (r"^icebreaker$", "icebreaker", "", None),
    (r"^heavy icebreaker, Polar class$", "icebreaker", "heavy, Polar class", None),
    (r"^heavy icebreaker$", "icebreaker", "heavy", None),
    (r"^icebreaker and polar research vessel$", "icebreaker", "also a polar research vessel",
     "an icebreaker that also does science: coded by the hull, the science in the note"),
    (r"^medium icebreaker and research vessel, Arctic Class 3$", "icebreaker",
     "medium; research vessel, Arctic Class 3",
     "an icebreaker that also does science: coded by the hull, the science in the note"),
    (r"^steel screw semi-icebreaker$", "icebreaker", None,
     "a semi-icebreaker: ice-strengthened rather than a true icebreaker, so the note keeps 'semi'"),
    (r"^nuclear submarine, Skate class$", "submarine", "nuclear, Skate class", None),
    (r"^nuclear submarine$", "submarine", "nuclear", None),
    (r"^screw steam tender$", "tender", "screw steam", None),
    (r"^screw steam tug, rebuilt$", "steamer", None, None),
    (r"^paddle steamer$", "steamer", "paddle", None),
    (r"^screw steamer$", "steamer", "screw", None),
    (r"^government steamer$", "steamer", "government", None),
    (r"^naval gunboat$", "steamer", "naval gunboat",
     "no warship code: a screw gunboat is filed as a steamer, the service in the note"),
    (r"^revenue cutter$", "steamer", "revenue cutter",
     "no cutter code: a steam revenue cutter is filed as a steamer, the service in the note"),
    (r"^steamer$", "steamer", "", None),

    # --- the work ----------------------------------------------------------
    (r"^ice-strengthened research and supply vessel$", "research-vessel",
     "ice-strengthened, also a supply vessel", None),
    (r"^research vessel, ", "research-vessel", TAIL, None),
    (r"^survey ship$", "research-vessel", "",
     "a full-rigged naval ship employed on survey: coded by her work, not her rig"),
    (r"^expedition cruise ship$", "cruise-ship", "expedition cruising", None),
    (r"^cruise ship$", "cruise-ship", "", None),
    (r"^storeship$", "transport", "storeship", None),
    (r"^transport$", "transport", "", None),
    (r"^Hudson's Bay Company supply vessel$", "transport", "Hudson's Bay Company", None),
    (r"^government supply and hospital ship$", "transport", "government hospital ship", None),
    (r"^freighter$", "freighter", "", None),
    (r"^oil tanker, ice-strengthened$", "tanker", "oil, ice-strengthened", None),
]

ORDER = ["ship", "barque", "brig", "schooner", "sloop", "yacht", "bomb-vessel",
         "boat", "umiak", "steamer", "tender", "icebreaker", "submarine",
         "whaler", "steam-whaler", "sealer", "research-vessel", "cruise-ship",
         "transport", "freighter", "tanker", "aircraft", "UNMATCHED"]


def classify(v):
    """(code, note, judgement call) for one free-text kind."""
    for pat, code, note, call in RULES:
        if re.search(pat, v):
            if note is TAIL:
                note = v.split(",", 1)[1].strip()
            elif note is None:
                note = v                      # the whole value says more than the code does
            return code, note, call
    return "UNMATCHED", v, None


def apply(c):
    """Put the code in kind and the rest in kind_note. Backs up first."""
    import shutil
    from datetime import datetime
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    bak = DB.parent / "_backups" / f"history-{stamp}-pre-vessel-kinds.sqlite"
    c.execute("PRAGMA wal_checkpoint(FULL)")
    shutil.copy2(DB, bak)
    print("backup:", bak)
    cols = {r[1] for r in c.execute("PRAGMA table_info(vessels)")}
    if "kind_note" not in cols:
        c.execute("ALTER TABLE vessels ADD COLUMN kind_note TEXT DEFAULT ''")
    n = 0
    for name, old in c.execute("SELECT name, kind FROM vessels WHERE kind<>''").fetchall():
        code, note, _ = classify(old)
        if code == "UNMATCHED":
            raise SystemExit(f"unmatched: {old!r}")
        c.execute("UPDATE vessels SET kind=?, kind_note=? WHERE name=?", (code, note, name))
        n += 1
    c.commit()
    print(f"{n} vessels recoded")


def main():
    if "--apply" in sys.argv:
        apply(sqlite3.connect(DB))
        return
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    counts = {v: n for v, n in c.execute("SELECT kind, count(*) FROM vessels GROUP BY kind")}
    by_code = defaultdict(list)
    for v, n in counts.items():
        code, note, call = classify(v)
        by_code[code].append((n, v, note, call))

    total = sum(counts.values())
    lines = ["# Vessel kind: draft mapping for review", "",
             f"{len(counts)} distinct values over {total} vessels, mapped to {len(by_code)} codes.",
             "Proposed: `kind` takes the code; what the code does not say moves to a new `kind_note`",
             "column, so the wiki still reads `barque, purchased into the Navy`.",
             "Rows marked with a diamond are judgement calls; please check those first.", "",
             "The rule: the code names the rig or the hull where the entry names one, and the work",
             "the vessel was built or fitted for where that is all the entry gives. So a whaling",
             "barque is a `barque` whose note says whaler, while a whaler whose rig no source",
             "records is a `whaler`. Anyone filtering for whaling vessels wants both the `whaler`",
             "and `steam-whaler` codes and the notes.", "",
             "| code | label | values | vessels |", "|---|---|---:|---:|"]
    for code in ORDER:
        if code in by_code:
            rows = by_code[code]
            lines.append(f"| {code} | {H.vessel_kind_label(code)} | {len(rows)} | "
                         f"{sum(r[0] for r in rows)} |")
    lines.append("")
    for code in ORDER + sorted(k for k in by_code if k not in ORDER):
        if code not in by_code:
            continue
        lines += [f"## {code}", "", "| n | value | kind_note | reads as |", "|---:|---|---|---|"]
        for n, v, note, call in sorted(by_code[code], key=lambda r: (-r[0], r[1])):
            reads = H.vessel_kind_label(code) + (f", {note}" if note else "")
            mark = f" ◆ {call}" if call else ""
            lines.append(f"| {n} | {v.replace('|', '-')} | {note.replace('|', '-')}{mark} | {reads} |")
        lines.append("")
    OUT.write_text("\n".join(lines) + "\n")
    print(f"{len(counts)} values -> {len(by_code)} codes; "
          f"UNMATCHED: {len(by_code.get('UNMATCHED', []))}")
    for r in by_code.get("UNMATCHED", []):
        print("  ", r[1])


if __name__ == "__main__":
    main()
