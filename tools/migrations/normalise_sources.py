"""Two cleanups on the sources table, in one pass. Read-only without --apply.

1. `archive` becomes the holding institution's own name. The variants live in
   ARCHIVE_ALIASES in arctic_history; this script applies them to the rows that
   were written before the table existed, and moves what the field was carrying
   besides the name: an item, microform, catalogue or lot number to `callno`,
   a volume, a page range or a route ("via the Wayback Machine") to `note`.
   A citation that only repeats the row's own `volume` and `pages` is dropped.

2. `entry_type` stops being misc wherever the row says what the work is. The
   rules, first match wins:

     thesis        a thesis or dissertation marker in the title or the note
     article       the container is a journal, magazine or newspaper; a volume
                   with a container is taken as the same evidence
     incollection  the container is a book, a report series or a named volume
     online        a web page: a news site, an encyclopaedia, a museum or
                   government page, a catalogue or database record
     report        a government printer, department, board or commission
                   publishes it and the title reads like a report
     book          a standalone work with a publisher and a year
     misc          none of the above, and printed for review: an artwork, a
                   photograph, an object, a manuscript, a statute

   Anything the rules cannot place stays misc. `article` and `online` put the
   container in the BibTeX `journal` field and `incollection` puts it in
   `booktitle`, so the two are never guessed from a bare publisher: a row whose
   journal sits in `publisher` rather than `container` is listed for review
   instead of being called an article with no journal.

    python3 sources-cleanup-scratch/normalise_sources.py            # dry run
    python3 sources-cleanup-scratch/normalise_sources.py --apply    # backs up, rewrites
"""
import argparse
import re
import shutil
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arctic_history as H          # noqa: E402

OUT = Path(__file__).with_name("mapping.md")

# ---------------------------------------------------------------- entry_type
# periodicals: a piece in one of these is an article
JOURNAL_RX = re.compile(
    r"^(Arctic|Polar Record|Polar Geography|Arctic Anthropology|Antiquity|Archivaria|Nature|Science"
    r"|Science Advances|Geoarchaeology|Canadian Geographic|Journal of Glaciology|Etudes/Inuit/Studies"
    r"|Eos\b|The Geographical Journal|The Geographical Review|American Antiquity|Arctic Yearbook \d{4})$"
    r"|\b(Journal|Review|Bulletin|Proceedings of the|Quarterly|Magazine|Annals|Newsletter|Transactions"
    r"|Reviews|Letters|Studies|News|Gazette|Times|Herald|Weekly)\b", re.I)
# a newspaper or news website: cited as a page, not as a journal article
NEWS_RX = re.compile(r"nunatsiaq\.com|cbc\.ca|explorersweb\.com|legionmagazine\.com|guinnessworldrecords\.com"
                     r"|thecanadianencyclopedia\.ca|nationalgeographic\.com|theguardian\.com|ctvnews\.ca", re.I)
NEWS_PUB_RX = re.compile(r"^(Nunatsiaq News|CBC News|Explorersweb|Legion Magazine|Guinness World Records"
                         r"|Historica Canada)", re.I)
# a book, a monograph series or a named volume: a piece in one is a chapter
BOOK_CONTAINER_RX = re.compile(r"Mercury Series|Paper No\.|Paper \d|Memoir|Series \d|Report of the Fifth Thule"
                               r"|Dictionary of Canadian Biography|Divers Voyages|Sessional Paper"
                               r"|Colonization|Objects$", re.I)
DCB_RX = re.compile(r"Dictionary of Canadian Biography|biographi\.ca", re.I)
THESIS_RX = re.compile(r"\b(PhD|Ph\.D\.|doctoral|master's|MA|MSc|M\.Sc\.) (thesis|dissertation)\b"
                       r"|\b(thesis|dissertation)\b,? (submitted|presented|University)", re.I)
# the journal is in the publisher field, not the container: the row needs a
# person before it can be called an article, so it is listed rather than typed
JOURNAL_IN_PUB_RX = re.compile(r"\bvols?\.?\s*[\dIVXL]|\b\d+\s*\(\d+\)|\bpp\.\s*\d"
                               r"|American Association for the Advancement of Science|American Geographical Society"
                               r"|Society for American Archaeology|Cambridge University Press for", re.I)
JOURNAL_URL_RX = re.compile(r"pubs\.aina\.ucalgary\.ca|journalhosting\.ucalgary\.ca|jstor|doi\.org/10\.(14430|1017|7202"
                            r"|1080|1029|1126)", re.I)
# an official printer: what it prints with no container is a government report
GOV_PRINTER_RX = re.compile(r"King's Printer|Queen's Printer|Printer to the King|Government Printing"
                            r"|Stationery Office|Eyre and Spottiswoode|Government Printer", re.I)
# a department, board, commission or survey that publishes its own findings
GOV_PUB_RX = re.compile(r"Government of (Canada|Nunavut)|Defence Research|Department of|Research Establishment"
                        r"|Northern Science Research Group|Canada Communication Group|Indian and Northern Affairs"
                        r"|Natural Resources Canada|Fisheries and Oceans|Transportation Safety Board"
                        r"|Veterans Affairs|Qikiqtani Inuit Association|Geological Survey|Royal Commission"
                        r"|Geographical Branch|Polar Continental Shelf|Bureau of Ethnology", re.I)
# a research establishment publishes reports whatever it calls them
GOV_RESEARCH_RX = re.compile(r"Defence Research|Research Establishment|Northern Science Research Group"
                             r"|Geographical Branch|Geological Survey|Polar Continental Shelf", re.I)
REPORT_TITLE_RX = re.compile(r"^Report\b|\bReport of\b|\bReport on\b|\bReport,|\bReports\b|Report$"
                             r"|Truth Commission|Community Histories|Thematic Report|Investigation Report"
                             r"|Proceedings of the|^Inventory of|preliminary report|Expedition to December"
                             r"|Papers [Rr]elative to|Field Work|Court of Inquiry", re.I)
# a web page rather than a work: the host serves pages, not scans, files or
# catalogue records of objects
WEB_HOST_RX = re.compile(r"^https?://(www\.)?("
                         r"en\.wikipedia\.org|hbcheritage\.ca|frammuseum\.no|parks\.canada\.ca|pc\.gc\.ca"
                         r"|canada\.ca|[\w.-]*\.gc\.ca|gov\.nu\.ca|tunngavik\.com|qtcommission\.ca"
                         r"|historymuseum\.ca|vanmaritime\.com|spri\.cam\.ac\.uk|arktiskebilleder\.dk"
                         r"|oqaasileriffik\.gl|library\.osu\.edu|amundsenscience\.com|forfreedom\.ca"
                         r"|queensu\.ca|rcmpveteransvancouver\.com|nlchs\.org|westbaffin\.com|manitoba\.ca"
                         r"|hudoc\.echr\.coe\.int|moravianchurcharchives\.org|arctic\.noaa\.gov"
                         r"|asn\.flightsafety\.org|treaty-accord\.gc\.ca|laws-lois\.justice\.gc\.ca"
                         r"|canadianmysteries\.ca|publications\.gc\.ca"
                         r")", re.I)
# a thing rather than a text: an artwork, a photograph, an object
OBJECT_RX = re.compile(r"\((photograph|photographs|oil on canvas|engraving|painting|drawing|watercolour"
                       r"|stereo photograph|exhibit)[^)]*\)$", re.I)
# a manuscript, a set of papers or a run of photographs: nobody published it
MANUSCRIPT_RX = re.compile(r"^(Photographs?|Drawings?|Charts?|Journals?|Field note|Lists of photographs"
                           r"|Maskette|A Set of|A View|Crayon drawing|MODIS images)\b", re.I)
# the holder is a gallery or a picture collection: what it holds is an object.
# A museum that publishes a monograph series is not one of these
MUSEUM_PUB_RX = re.compile(r"Royal Museums|Naval History and Heritage|Norfolk Museums|Wellcome|Tekniska"
                           r"|Maritime Museum|Historical Society|Picture Library|Art Gallery|National Galler", re.I)
# a journal name with its citation run together in the publisher field: the
# name in front is the container the row should have had
JOURNAL_PUB_RX = re.compile(r"^(?P<journal>[A-Z][^,;(]{2,60}?)[,;]?\s*(?:\(|\d+\s*\(\d+\)|vols?\.)")
SOCIETY_RX = re.compile(r"^(Society|Association|American Association|University|Cambridge|Oxford|Government)"
                        r"|(Society|Press|Association|Institute|Museum|Office|Bureau)$", re.I)
# Arctic's own DOI prefix and its two addresses: the journal is not in doubt
ARCTIC_URL_RX = re.compile(r"pubs\.aina\.ucalgary\.ca|journalhosting\.ucalgary\.ca|doi\.org/10\.14430", re.I)
DATA_URL_RX = re.compile(r"/api/|api\.|\.json|^ftp|ftp\.|geonames|/collections/climate", re.I)


def infer_entry_type(r):                                # noqa: C901 - one branch per rule, read top to bottom
    """(type, evidence) for a row that is still misc, or (None, why not). The
    two rules that recover a journal name add it as a third element, the
    container the row should have carried."""
    title, container, publisher = r["title"] or "", r["container"] or "", r["publisher"] or ""
    url, volume, note = r["url"] or "", r["volume"] or "", r["note"] or ""
    archive = r["archive"] or ""
    if THESIS_RX.search(title) or THESIS_RX.search(note):
        return "thesis", "thesis marker in the title or the note"
    if container:
        if NEWS_RX.search(url) or NEWS_PUB_RX.match(container):
            return "online", f"a news site: container {container!r}, {url[:40]}"
        if BOOK_CONTAINER_RX.search(container):
            return "incollection", f"container {container!r} is a book or a report series"
        if JOURNAL_RX.search(container):
            return "article", f"container {container!r} is a periodical" + (f", volume {volume}" if volume else "")
        if volume:
            return "article", f"container {container!r} with volume {volume}"
        return None, f"container {container!r}: journal or book?"
    if DCB_RX.search(publisher) or DCB_RX.search(archive) or DCB_RX.search(url):
        return "incollection", "a life in the Dictionary of Canadian Biography"
    if NEWS_RX.search(url) or NEWS_PUB_RX.match(publisher):
        return "online", f"a news site: {publisher or url[:40]}"
    if DATA_URL_RX.search(url):
        return "dataset", f"a data service: {url[:50]}"
    # the journal was written into the publisher field or is only in the URL.
    # Where the name is beyond doubt it becomes the container and the row is an
    # article; where it is not, the row is listed for a person to finish
    if JOURNAL_IN_PUB_RX.search(publisher) or JOURNAL_URL_RX.search(url):
        m = JOURNAL_PUB_RX.match(publisher)
        if m and not SOCIETY_RX.search(m.group("journal").strip()):
            journal = m.group("journal").strip()
            return "article", f"container from --publisher: {journal!r}", journal
        if ARCTIC_URL_RX.search(url):
            return "article", "container from the URL: 'Arctic'", "Arctic"
        return None, f"the journal is in --publisher or the URL, not --container: {(publisher or url)[:45]!r}"
    if GOV_PRINTER_RX.search(publisher) or GOV_RESEARCH_RX.search(publisher):
        return "report", f"published by {publisher[:45]!r}"
    if GOV_PUB_RX.search(publisher) and REPORT_TITLE_RX.search(title):
        return "report", f"{publisher[:40]!r} publishes it and the title reads as a report"
    if WEB_HOST_RX.match(url):
        return "online", f"a web page at {re.sub(r'^https?://', '', url)[:45]}"
    if OBJECT_RX.search(title) or (MANUSCRIPT_RX.match(title) and not publisher):
        return None, "an object, an image or a manuscript, not a published work"
    if MUSEUM_PUB_RX.search(publisher):
        return None, f"{publisher[:40]!r} holds it: an object or an image, not a published work"
    if not publisher:
        return None, "no publisher and no container"
    if GOV_PUB_RX.search(publisher):
        return None, f"{publisher[:40]!r} is an official publisher but the title is not a report"
    if r["year"]:
        return "book", f"a standalone work, {publisher[:40]!r} {r['year']}"
    return None, "no year"


# ---------------------------------------------------------------- archive
CITE_ONLY_RX = re.compile(r"^[\d\s()\[\]:,.–-]+")


def archive_changes(r):
    """(archive, callno, note, dropped) for one row: the canonical name, what the
    field's identifiers and citation detail become, and what was dropped as
    already recorded in the row's own columns."""
    name, callno, detail = H.normalise_archive(r["archive"] or "")
    keep, dropped = [], []
    for piece in (x.strip() for x in detail.split(";") if x.strip()):
        rest = CITE_ONLY_RX.sub("", piece).strip(" ()")
        if rest != piece and (r["volume"] or "") and (r["pages"] or ""):
            (keep if rest else dropped).append(rest or piece)
        else:
            keep.append(piece)
    return name, callno, "; ".join(keep), "; ".join(dropped)


def merged(old, extra):
    """Add to a field without repeating what it already says."""
    old, extra = (old or "").strip(), (extra or "").strip()
    if not extra or extra in old:
        return old
    return f"{old}; {extra}" if old else extra


def changes(c):
    rows = [dict(r) for r in c.execute("SELECT * FROM sources ORDER BY bibkey")]
    out = []
    for r in rows:
        name, callno, note, dropped = archive_changes(r)
        new = {}
        if r["archive"] and (name != r["archive"] or callno or note):
            new["archive"] = name
            if callno:
                new["callno"] = merged(r["callno"], callno)
            if note:
                new["note"] = merged(r["note"], note)
        et, why = (None, "already typed")
        if r["entry_type"] == "misc":
            got = infer_entry_type(r)
            et, why = got[0], got[1]
            if et:
                new["entry_type"] = et
            if len(got) > 2 and not r["container"]:
                new["container"] = got[2]
        out.append((r, new, et, why, dropped))
    return out


# ---------------------------------------------------------------- output
JUDGEMENT = """
1. **A paper in *Arctic* is held at the Arctic Institute of North America**, not
   at "Arctic", "ARCTIC journal" or "University of Calgary Journal Hosting". The
   institute publishes the journal and serves the back run at
   pubs.aina.ucalgary.ca; the University of Calgary's journal hosting is where
   the current issues sit, an address rather than a holder. The journal title is
   what `container` is for, so putting it in `archive` as well says nothing and
   spells it eight ways. Eleven variants, forty-two rows.
2. **Polar Record goes to Cambridge Core**, the platform the copies were read
   from, on the same reasoning: the journal belongs in `container`.
3. **Three merges drop words.** "Canadiana / Government of Canada sessional
   papers" becomes Canadiana (the rows carry "Sessional Paper No. N" in
   `volume`); "Parks Canada, Directory of Federal Heritage Designations" becomes
   Parks Canada; "Wikimedia Commons / Government of Canada Publications" becomes
   Wikimedia Commons, keeping the catalogue number in `callno`. Say so if the
   dropped words were worth keeping.
4. **Canadian Parks Service becomes Parks Canada**: the same institution under
   the name it uses now.
5. **Two notes now carry a remark about this host** ("canada.ca times out from
   this host"), moved out of the archive field rather than invented. They are
   reader-facing on the source page; trim them if that is wrong.
6. **A newspaper or a news site is `online`, not `article`.** The BibTeX export
   now writes the container of an `online` entry as `journal`, so
   `journal = {Nunatsiaq News}` still comes out right.
7. **A statute or a treaty read on the Justice Laws Website is `online`.** The
   vocabulary has no type for legislation and `misc` says less.
8. **Eleven rows had the journal in `publisher`.** Where the name in front of the
   citation is beyond doubt ("Arctic (Arctic Institute of North America),
   39(4), 350-359", "Polar Geography 26(1), pp. 39-52") it is copied into the
   empty `container` and the row becomes an article, so the export has a journal
   to print. Fifteen more, where the name is a society or a press rather than a
   journal, are left misc under "Still misc" for a person to finish.
9. **An artwork, a photograph, a manuscript journal and a run of expedition
   negatives stay `misc`.** That is what the type is for, and forty of the
   fifty-seven left are exactly that.
""".strip()


def report(rows):
    arch = [(r, new) for r, new, et, why, d in rows if "archive" in new]
    types = [(r, et, why) for r, new, et, why, d in rows if et]
    left = [(r, why) for r, new, et, why, d in rows if r["entry_type"] == "misc" and not et]

    before = Counter(r["archive"] for r in (x[0] for x in rows) if r["archive"])
    after = Counter()
    for r, new, et, why, d in rows:
        if r["archive"]:
            after[new.get("archive", r["archive"])] += 1

    lines = ["# Sources cleanup: archive names and entry types", "",
             f"{len(rows)} sources. `archive` holds {len(before)} distinct values in "
             f"{sum(before.values())} rows; the alias table and the detail rules bring them to "
             f"{len(after)} names, rewriting {len(arch)} rows.",
             f"`entry_type` is misc on {sum(1 for r in (x[0] for x in rows) if r['entry_type'] == 'misc')} rows; "
             f"the rules type {len(types)} of them and leave {len(left)} for review.", "",
             "## The archive field, before and after", "",
             "A name in **bold** is the one the variants merge into. `callno` takes the identifiers "
             "of the copy, `note` the citation and the route. A citation that only repeats the row's "
             "own volume and pages is dropped, and shown here in brackets.", "",
             "| rows | before | after | to callno | to note |", "|---:|---|---|---|---|"]
    by_after = defaultdict(list)
    for v, n in before.items():
        by_after[H.normalise_archive(v)[0]].append((n, v))
    for name in sorted(by_after, key=lambda k: (-after[k], k)):
        for n, v in sorted(by_after[name], key=lambda x: -x[0]):
            row = next((x for x in rows if x[0]["archive"] == v), None)
            _, callno, note, dropped = archive_changes(row[0]) if row else ("", "", "", "")
            same = v == name
            lines.append(f"| {n} | {v} | {'(unchanged)' if same else '**' + name + '**'} | "
                         f"{callno} | {note}{' [' + dropped + ']' if dropped else ''} |")
    lines += ["", "## The calls worth arguing with", "", JUDGEMENT, "",
              "## The archives used by one source only", "",
              "Not wrong, but the place drift shows first.", ""]
    lines += [f"- {name} ({[r['bibkey'] for r, new, et, why, d in rows if new.get('archive', r['archive']) == name][0]})"
              for name in sorted(after) if after[name] == 1]

    lines += ["", "## entry_type: what the rules assign", ""]
    for t in ("article", "incollection", "report", "book", "online", "thesis", "dataset"):
        got = [(r, why) for r, et, why in types if et == t]
        if not got:
            continue
        lines += [f"### {t} ({len(got)})", "", "| bibkey | title | evidence |", "|---|---|---|"]
        for r, why in sorted(got, key=lambda x: x[0]["bibkey"]):
            lines.append(f"| {r['bibkey']} | {r['title'][:70].replace('|', '/')} | {why.replace('|', '/')} |")
        lines.append("")
    lines += [f"## Still misc ({len(left)})", "",
              "| bibkey | title | publisher | why not |", "|---|---|---|---|"]
    for r, why in sorted(left, key=lambda x: x[0]["bibkey"]):
        lines.append(f"| {r['bibkey']} | {r['title'][:60].replace('|', '/')} | "
                     f"{(r['publisher'] or '')[:40].replace('|', '/')} | {why.replace('|', '/')} |")
    lines.append("")
    return "\n".join(lines)


def apply(c, db, rows):
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    bak = db.parent / "_backups" / f"history-{stamp}-pre-sources-cleanup.sqlite"
    bak.parent.mkdir(parents=True, exist_ok=True)
    c.execute("PRAGMA wal_checkpoint(FULL)")
    shutil.copy2(db, bak)
    print("backup:", bak)
    n = 0
    for r, new, et, why, dropped in rows:
        if not new:
            continue
        sets = ", ".join(f"{k}=?" for k in new)
        c.execute(f"UPDATE sources SET {sets}, updated=? WHERE bibkey=?",
                  tuple(new.values()) + (H.now(), r["bibkey"]))
        n += 1
    c.commit()
    print(f"{n} rows rewritten")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", default=str(H.HISTORY_DB))
    p.add_argument("--apply", action="store_true", help="back up and rewrite the rows")
    a = p.parse_args()
    db = Path(a.db)
    c = sqlite3.connect(db if a.apply else f"file:{db}?mode=ro", uri=not a.apply)
    c.row_factory = sqlite3.Row
    rows = changes(c)
    if a.apply:
        apply(c, db, rows)
        return
    text = report(rows)
    OUT.write_text(text)
    print(text)
    arch = sum(1 for r, new, et, why, d in rows if "archive" in new)
    typed = Counter(et for r, new, et, why, d in rows if et)
    misc = sum(1 for r, new, et, why, d in rows if r["entry_type"] == "misc" and not et)
    print(f"-- {arch} rows change archive; {sum(typed.values())} rows get a type "
          f"({', '.join(f'{k} {v}' for k, v in typed.most_common())}); {misc} stay misc; "
          f"the same text is in {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
