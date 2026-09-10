#!/usr/bin/env python3
"""Write to the shared history database: db/history/history.sqlite.

Every researcher writes through this one tool, so the schema, the credit lines
and the bibliography stay consistent across twenty topics. Writes are short
transactions on a write-ahead log, so many researchers may work at once.

    history-db.py topic     --slug franklin-1845 --title "The Franklin expedition" --summary "..."
    history-db.py source    --bibkey mcclintock1859voyage --title "The Voyage of the Fox..." \
                            --author "McClintock, Francis Leopold" --year 1859 --primary \
                            --publisher John Murray --url https://... --licence public-domain \
                            --archive "Internet Archive" --note "the Victory Point record in facsimile"
    history-db.py bib       --topic franklin-1845 --file refs.bib      # import a whole BibTeX file
    history-db.py artifact  --id franklin-1845-004 --topic franklin-1845 --type quote \
                            --title "The Victory Point record" --date 1848-04-25 \
                            --lat 69.97 --lon -98.55 --bibkey mcclintock1859voyage --pages "p. 283" \
                            --credit "Royal Museums Greenwich" --licence public-domain \
                            --description "..." --tags franklin,abandonment --people "Crozier;Fitzjames"
    history-db.py track     --id franklin-1845-001 --topic franklin-1845 --title "Erebus and Terror" \
                            --bibkey cyriax1939franklin --credit "..." --waypoints waypoints.json
    history-db.py person    --name Tookoolito --also "Hannah; Taqulittuq" --indigenous \
                            --role "interpreter and guide" --born 1838 --died 1876 --topic kane-hall-polaris
    history-db.py vessel    --name "HMS Investigator" --kind barque \
                            --kind-note "purchased into the Navy" --built "1848, Greenock" \
                            --lost "abandoned in the Bay of Mercy, 3 June 1853" --topic mcclure-investigator
    history-db.py place     --name "Beechey Island" --lat 74.7139 --lon -91.8472 --kind site \
                            --historic "Beechey Island" --topic franklin-1845
    history-db.py event     --topic franklin-1845 --date 1847-06-11 --title "Franklin dies" \
                            --lat 70.08 --lon -98.4 --bibkey mcclintock1859voyage
    history-db.py page      --slug franklin-the-death-march --title "The death march" \
                            --topic franklin-1845 --file page.md --summary "..."
    history-db.py stats
    history-db.py check                     # what is missing or wrong
    history-db.py wanted                    # wikilinks named but not yet written
    history-db.py show      --slug franklin-the-death-march
    history-db.py export    --bib out.bib

A page body is Markdown holding ``[[wikilinks]]``:

    [[artifact:franklin-1845-004]]  [[source:mcclintock1859voyage]]
    [[person:John Rae]]  [[place:Beechey Island]]  [[topic:franklin-search]]
    [[page:the-death-march]]        [[artifact:franklin-1845-004|the record itself]]

A link to something not written yet is kept and listed by ``wanted``; it marks
work to do rather than breaking anything.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arctic_history import *  # noqa: F401,F403
import arctic_history as H          # noqa: E402

TAGS_HELP = ("comma separated, stored one per tag: lowercase, words hyphenated at the boundary "
             "(musk-ox, fort-conger, full-text) and singular (dog, wreck, vessel), a proper name "
             "as it is written (queen-elizabeth-islands)")
LICENCE_HELP = ("a code: " + ", ".join(H.LICENCE_CODES) +
                ", or cc-by / cc-by-sa / cc-by-nc-sa / cc-by-nc-nd with a version (cc-by-4.0)")
RIGHTS_HELP = ("free text behind the code: the holder, the term and why it is expired, "
               "the request number, what is and is not held")
KIND_HELP = "a vessel's hull or craft type, one code: " + ", ".join(H.VESSEL_KINDS)
KIND_NOTE_HELP = ("free text behind the code: the class, the aircraft model, the trade she "
                  "worked, a conversion, the navy or company that bought her")
ENTRY_TYPE_HELP = "what the work is; choose one, do not leave it at misc. " + \
                  "; ".join(f"{k}: {v}" for k, v in H.ENTRY_TYPES.items())
ARCHIVE_HELP = ("the institution or platform holding the copy, under its own name "
                "(\"Arctic Institute of North America\", not \"Arctic (AINA)\"); "
                "the journal goes in --container, the numbers in --callno")
CALLNO_HELP = "the identifier of the copy: an accession, catalogue, item or microform number"


def _read(value: str | None, file: str | None) -> str:
    """A field given inline, or from a file when it is long (a page body, a
    list of waypoints). ``-`` reads standard input."""
    if file:
        return sys.stdin.read() if file == "-" else Path(file).read_text(encoding="utf-8")
    return value or ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="history-db.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", type=Path, default=None, help="the database (default db/history/history.sqlite)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("topic", help="declare a topic")
    t.add_argument("--slug", required=True)
    t.add_argument("--title", help="required for a new topic; optional when updating")
    t.add_argument("--summary")
    t.add_argument("--researcher")
    t.add_argument("--status", choices=["open", "drafted", "done"])

    s = sub.add_parser("source", help="add or update a bibliography entry")
    s.add_argument("--bibkey", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--entry-type", default="misc", help=ENTRY_TYPE_HELP)
    for f in ("author", "year", "container", "publisher", "address", "volume", "pages",
              "url", "urldate", "doi", "archive", "callno", "licence", "rights-note", "note", "local-file", "topic",
              "language", "orig-language", "translator"):
        s.add_argument(f"--{f}", default=None,
                       help=LICENCE_HELP if f == "licence" else RIGHTS_HELP if f == "rights-note"
                       else ARCHIVE_HELP if f == "archive" else CALLNO_HELP if f == "callno" else None)
    s.add_argument("--primary", action="store_true", help="a primary source: a journal, log, narrative or testimony")

    b = sub.add_parser("bib", help="import a BibTeX file")
    b.add_argument("--file", required=True)
    b.add_argument("--topic", default="")

    for name, helptext in (("artifact", "add or update an artifact"),
                           ("track", "add or update a ship track (an artifact of type track)")):
        a = sub.add_parser(name, help=helptext)
        a.add_argument("--id", required=True)
        a.add_argument("--topic", required=True)
        a.add_argument("--title", required=True)
        a.add_argument("--bibkey", required=True)
        a.add_argument("--credit", required=True)
        if name == "artifact":
            a.add_argument("--type", required=True, choices=list(H.ARTIFACT_TYPES))
        a.add_argument("--date", default="")
        a.add_argument("--date-end", default="")
        a.add_argument("--creator", default="")
        a.add_argument("--description", default="")
        a.add_argument("--description-file", default=None)
        a.add_argument("--lat", type=float, default=None)
        a.add_argument("--lon", type=float, default=None)
        a.add_argument("--geometry", default=None, help="GeoJSON geometry, inline")
        a.add_argument("--geometry-file", default=None)
        a.add_argument("--waypoints", default=None, help="[{date,lat,lon,note}], inline")
        a.add_argument("--waypoints-file", default=None)
        a.add_argument("--source-url", default="")
        a.add_argument("--download-url", default="")
        a.add_argument("--local-file", default="", help="a downloaded copy, relative to db/history/")
        a.add_argument("--licence", default="", help=LICENCE_HELP)
        a.add_argument("--rights-note", default="", help=RIGHTS_HELP)
        a.add_argument("--pages", default="", help="where in the cited work")
        a.add_argument("--language", default="", help="of a text or quote, when not English (ISO 639-1)")
        a.add_argument("--people", default="", help="semicolon separated")
        a.add_argument("--tags", default="", help=TAGS_HELP)
        a.add_argument("--view-file", default=None,
                       help="a raster view of a non-raster local file (PDF page, page screenshot, GeoTIFF), relative to db/history/")
        a.add_argument("--routing", default=None, choices=["", "water", "as-given", "terrain"],
                       help="tracks: draw the line routed through water, as the waypoints are given, or "
                            "routed over the terrain (the line from tools/digitize-tracks.py)")

    p = sub.add_parser("person", help="add or update a person")
    p.add_argument("--name", required=True)
    for f in ("also", "role", "born", "died", "affiliation", "note", "bibkey", "topic"):
        p.add_argument(f"--{f}", default=None)
    p.add_argument("--indigenous", action="store_true", help="an Inuit, Inughuit or other Indigenous participant")

    an = sub.add_parser("animal", help="add or update a named animal: a dog, a pony, a ship's cat, a bear cub")
    an.add_argument("--name", required=True)
    for f in ("kind", "also", "role", "born", "died", "affiliation", "note", "bibkey", "topic"):
        an.add_argument(f"--{f}", default=None)
    ve = sub.add_parser("vessel", help="add or update a ship, boat or aircraft")
    ve.add_argument("--name", required=True)
    for f in ("kind", "kind-note", "also", "role", "built", "lost", "affiliation", "tonnage",
              "note", "bibkey", "topic"):
        ve.add_argument(f"--{f}", default=None,
                        help=KIND_HELP if f == "kind" else KIND_NOTE_HELP if f == "kind-note" else None)

    pl = sub.add_parser("place", help="add or update a place")
    pl.add_argument("--name", required=True)
    pl.add_argument("--lat", type=float, default=None)
    pl.add_argument("--lon", type=float, default=None)
    for f in ("historic", "inuktitut", "kind", "note", "bibkey", "topic"):
        pl.add_argument(f"--{f}", default=None)

    e = sub.add_parser("event", help="add a dated event to the timeline")
    e.add_argument("--topic", required=True)
    e.add_argument("--date", required=True)
    e.add_argument("--title", required=True)
    e.add_argument("--date-end", default="")
    e.add_argument("--detail", default="")
    e.add_argument("--lat", type=float, default=None)
    e.add_argument("--lon", type=float, default=None)
    e.add_argument("--place", default="")
    e.add_argument("--people", default="")
    e.add_argument("--bibkey", default="")
    e.add_argument("--tags", default="", help=TAGS_HELP)
    e.add_argument("--precision", default=None, choices=list(H.PRECISIONS),
                   help="how much of the date the source gives (guessed from its shape by default)")
    e.add_argument("--qualifier", default="", choices=list(H.QUALIFIERS),
                   help="the source's own hedge: circa, before, after, by, early, mid, late")

    d = sub.add_parser("date", help="record one atomic date on any record")
    d.add_argument("--kind", required=True, choices=["artifact", "event", "person", "place", "source", "page", "topic", "animal", "vessel"])
    d.add_argument("--id", required=True, help="the artifact id, event id, person or place name, bibkey or page slug")
    d.add_argument("--date", required=True, help="YYYY, YYYY-MM or YYYY-MM-DD")
    d.add_argument("--role", default="point", choices=list(H.DATE_ROLES))
    d.add_argument("--precision", default=None, choices=list(H.PRECISIONS),
                   help="how much of the date the source gives (guessed from its shape by default)")
    d.add_argument("--qualifier", default="", choices=list(H.QUALIFIERS),
                   help="the source's own hedge: circa, before, after, by, early, mid, late")
    d.add_argument("--span", default="", help="ties a start row to its end row")
    d.add_argument("--label", default="", help="what happened on this date")
    d.add_argument("--lat", type=float, default=None)
    d.add_argument("--lon", type=float, default=None)
    d.add_argument("--place", default="")
    d.add_argument("--topic", default="")
    d.add_argument("--bibkey", default="")

    ac = sub.add_parser("activity", help="a time-limited activity: a wintering, a beset, a sledge journey, "
                                         "a post's working life. Its start and end are stored as two atomic dates.")
    ac.add_argument("--topic", required=True)
    ac.add_argument("--title", required=True)
    ac.add_argument("--date", required=True, help="when it began")
    ac.add_argument("--date-end", required=True, help="when it ended")
    ac.add_argument("--detail", default="")
    ac.add_argument("--lat", type=float, default=None)
    ac.add_argument("--lon", type=float, default=None)
    ac.add_argument("--place", default="")
    ac.add_argument("--people", default="")
    ac.add_argument("--bibkey", default="")
    ac.add_argument("--tags", default="", help=TAGS_HELP)
    ac.add_argument("--precision", default=None, choices=list(H.PRECISIONS))
    ac.add_argument("--qualifier", default="", choices=list(H.QUALIFIERS))

    tl = sub.add_parser("timeline", help="the atomic dates, in order")
    tl.add_argument("--topic", default="")
    tl.add_argument("--from", dest="since", default="")
    tl.add_argument("--to", dest="until", default="")

    pg = sub.add_parser("page", help="write or replace a narrative wiki page")
    pg.add_argument("--slug", required=True)
    pg.add_argument("--title", required=True)
    pg.add_argument("--topic", default="")
    pg.add_argument("--summary", default="")
    pg.add_argument("--body", default="")
    pg.add_argument("--file", default=None, help="the Markdown body, or - for stdin")
    pg.add_argument("--ordering", type=int, default=100, help="lower sorts earlier in the topic")
    pg.add_argument("--people", default=None,
                    help="semicolon separated: the people this page is about, for exact "
                         "People strips and backlinks (bare name mentions are also indexed)")
    pg.add_argument("--status", default=None, choices=list(H.PAGE_STATUS),
                    help="draft (the default for a new page) or good; a rewrite keeps the "
                         "status it had unless told otherwise, and every save keeps the "
                         "replaced version in the page's history")

    vs = sub.add_parser("versions", help="a page's saved versions, oldest first")
    vs.add_argument("--slug", required=True)

    fg = sub.add_parser("forget", help="delete one mistaken row and the dates attached to it — "
                                       "a duplicate person, a stray date. For errors, not "
                                       "revisions; note what you removed in the worklog.")
    fg.add_argument("--kind", required=True, choices=["artifact", "event", "person", "place", "source", "date", "animal", "vessel"])
    fg.add_argument("--id", required=True,
                    help="the artifact id, the event or date row number, or the person or place name")

    lg = sub.add_parser("log", help="write a worklog line: what is now in the database, and what comes next")
    lg.add_argument("--topic", required=True)
    lg.add_argument("--done", required=True, help="what this step put into the database")
    lg.add_argument("--next", default="", help="the step after this one")
    lg.add_argument("--open", default="", help="questions and doubts still open")
    lg.add_argument("--who", default="", help="the run or person writing")

    rs = sub.add_parser("resume", help="everything a run needs to carry a topic on")
    rs.add_argument("--topic", required=True)

    rq = sub.add_parser("request", help="ask a person for something you cannot do alone: a download over "
                                        "50 MB, an API key, a judgement call, a question")
    rq.add_argument("--topic", required=True)
    rq.add_argument("--kind", required=True, choices=list(H.REQUEST_KINDS))
    rq.add_argument("--what", required=True, help="one line: what is wanted")
    rq.add_argument("--why", required=True,
                    help="full instructions for a person acting alone, later: why the topic "
                         "needs it, why it needs a person (what you tried, what only they "
                         "can do), exactly where to get it (URL, title, edition, volume, "
                         "which account, which form; a found address and a drafted email if "
                         "they must write to someone), and what you will do with the answer")
    rq.add_argument("--url", default="")
    rq.add_argument("--size-mb", type=float, default=None)
    rq.add_argument("--dest", default="", help="where a download should land, relative to db/history/")
    rq.add_argument("--who", default="")

    rqs = sub.add_parser("requests", help="list requests and their answers")
    rqs.add_argument("--topic", default="")
    rqs.add_argument("--status", default="", choices=["", *H.REQUEST_STATUS])

    an = sub.add_parser("answer", help="answer a request (a person does this; the dashboard page does the same)")
    an.add_argument("--id", type=int, required=True)
    an.add_argument("--status", required=True, choices=list(H.REQUEST_STATUS))
    an.add_argument("--answer", default="")

    fc = sub.add_parser("face", help="record one face cut from an image artifact (issue #2)")
    fc.add_argument("--artifact", required=True)
    fc.add_argument("--n", required=True, type=int, help="the face's number within the image, from 1")
    fc.add_argument("--file", required=True, help="the crop, relative to db/history/, under <topic>/files/faces/")
    fc.add_argument("--box", default="", help="[x, y, w, h] in the original raster, JSON")
    fc.add_argument("--kind", default="person", choices=["person", "animal", "vessel"],
                    help="what the crop shows; --person then names a row of people, animals or vessels")
    fc.add_argument("--person", default="", help="a name in people (or animals, vessels), or nothing when unidentified")
    fc.add_argument("--confidence", type=float, default=None)
    fc.add_argument("--method", default="", help="detector and identification rule, e.g. yunet; single-name-in-people")
    fc.add_argument("--forget", action="store_true", help="delete every face of this artifact instead")
    kwp = sub.add_parser("keyword", help="subject paths on an artifact, 'Level > Level > Level' (issue #3)")
    kwp.add_argument("--artifact", required=True)
    kwp.add_argument("--path", action="append", default=[], help="repeatable, up to three")
    kwp.add_argument("--source", default="crew", help="'crew' or 'llm:<model>'")
    kwp.add_argument("--keep", action="store_true", help="add to that source's existing paths instead of replacing them")
    on = sub.add_parser("ontology", help="the keyword tree (issue #3): set it from a JSON file, or show it")
    on.add_argument("--file", default=None, help='{"Level 1": {"Level 2": ["Level 3", ...]}}')
    on.add_argument("--model", default="")
    sub.add_parser("stats", help="row counts")
    sub.add_parser("check", help="what is missing or inconsistent")
    sub.add_parser("wanted", help="wikilinks named but not written")
    sh = sub.add_parser("show", help="print one page as stored")
    sh.add_argument("--slug", required=True)
    li = sub.add_parser("list", help="list rows of one kind")
    li.add_argument("--what", required=True, choices=["topics", "sources", "artifacts", "pages", "people", "places", "events", "animals", "vessels"])
    li.add_argument("--topic", default="")
    ex = sub.add_parser("export", help="write the bibliography out")
    ex.add_argument("--bib", required=True)

    a = ap.parse_args(argv)
    c = H.connect(a.db)
    try:
        return run(a, c)
    finally:
        c.close()


def run(a, c) -> int:                                   # noqa: C901 — one branch per subcommand
    if a.cmd == "topic":
        print(H.add_topic(c, a.slug, a.title, summary=a.summary, researcher=a.researcher, status=a.status))
    elif a.cmd == "source":
        kw = {k.replace("-", "_"): v for k, v in vars(a).items()
              if k not in {"cmd", "db", "bibkey", "title"} and v is not None}
        print(H.add_source(c, a.bibkey, a.title, **kw))
    elif a.cmd == "bib":
        keys = H.import_bib(c, Path(a.file).read_text(encoding="utf-8"), a.topic)
        print(f"{len(keys)} entries: {' '.join(keys)}")
    elif a.cmd in ("artifact", "track"):
        kw = dict(date=a.date, date_end=a.date_end, creator=a.creator,
                  description=_read(a.description, a.description_file),
                  lat=a.lat, lon=a.lon, source_url=a.source_url, download_url=a.download_url,
                  local_file=a.local_file, licence=a.licence, rights_note=a.rights_note,
                  credit=a.credit, bibkey=a.bibkey,
                  pages=a.pages, people=a.people, tags=a.tags, language=a.language,
                  view_file=a.view_file, routing=a.routing)
        geom = _read(a.geometry, a.geometry_file)
        way = _read(a.waypoints, a.waypoints_file)
        if way:
            kw["waypoints"] = way
            if not geom:
                # a track's line follows its waypoints unless a geometry is given
                pts = json.loads(way)
                coords = [[w["lon"], w["lat"]] for w in pts if w.get("lat") is not None]
                if len(coords) > 1:
                    geom = json.dumps({"type": "LineString", "coordinates": coords})
                if kw.get("lat") is None and coords:
                    kw["lat"], kw["lon"] = pts[0]["lat"], pts[0]["lon"]
        if geom:
            kw["geometry"] = geom
        print(H.add_artifact(c, a.id, a.topic, "track" if a.cmd == "track" else a.type, a.title, **kw))
    elif a.cmd == "person":
        kw = {k: v for k, v in vars(a).items() if k not in {"cmd", "db", "name"} and v is not None}
        print(H.add_person(c, a.name, **kw))
    elif a.cmd == "animal":
        kw = {k: v for k, v in vars(a).items() if k not in {"cmd", "db", "name"} and v is not None}
        print(H.add_animal(c, a.name, **kw))
    elif a.cmd == "vessel":
        kw = {k: v for k, v in vars(a).items() if k not in {"cmd", "db", "name"} and v is not None}
        print(H.add_vessel(c, a.name, **kw))
    elif a.cmd == "place":
        kw = {k: v for k, v in vars(a).items() if k not in {"cmd", "db", "name"} and v is not None}
        print(H.add_place(c, a.name, **kw))
    elif a.cmd == "event":
        ident = H.add_event(c, a.topic, a.date, a.title, date_end=a.date_end, detail=a.detail,
                            lat=a.lat, lon=a.lon, place=a.place, people=a.people,
                            bibkey=a.bibkey, tags=a.tags)
        if a.precision or a.qualifier:
            # replaces the guessed row: same entity, date, role and label upsert
            if a.date_end and a.date_end != a.date:
                H.span_dates(c, "event", str(ident), a.date, a.date_end, precision=a.precision,
                             qualifier=a.qualifier, label=a.title, topic=a.topic, place=a.place,
                             lat=a.lat, lon=a.lon, bibkey=a.bibkey)
            else:
                H.add_date(c, "event", str(ident), a.date, precision=a.precision,
                           qualifier=a.qualifier, role="point", label=a.title, topic=a.topic,
                           place=a.place, lat=a.lat, lon=a.lon, bibkey=a.bibkey)
        print(ident)
    elif a.cmd == "date":
        print(H.add_date(c, a.kind, a.id, a.date, role=a.role, precision=a.precision,
                         qualifier=a.qualifier, span=a.span, label=a.label, lat=a.lat, lon=a.lon,
                         place=a.place, topic=a.topic, bibkey=a.bibkey))
    elif a.cmd == "activity":
        ident = H.add_event(c, a.topic, a.date, a.title, date_end=a.date_end, detail=a.detail,
                            lat=a.lat, lon=a.lon, place=a.place, people=a.people,
                            bibkey=a.bibkey, tags=a.tags)
        if a.precision or a.qualifier:
            # the guessed precision is replaced when the researcher states one
            H.span_dates(c, "event", str(ident), a.date, a.date_end, precision=a.precision,
                         qualifier=a.qualifier, label=a.title, topic=a.topic, place=a.place,
                         lat=a.lat, lon=a.lon, bibkey=a.bibkey)
        print(ident)
    elif a.cmd == "timeline":
        q = ("SELECT date, precision, qualifier, role, span, entity_kind, entity_id, topic, label "
             "FROM dates WHERE 1=1")
        args: list = []
        if a.topic:
            q += " AND topic=?"
            args.append(a.topic)
        if a.since:
            q += " AND date>=?"
            args.append(a.since)
        if a.until:
            q += " AND date<=?"
            args.append(a.until)
        for r in c.execute(q + f" ORDER BY {H.date_order('date')}, role DESC", tuple(args)):
            mark = {"point": " ", "start": "[", "end": "]"}[r["role"]]
            qual = f"{r['qualifier']} " if r["qualifier"] else ""
            print(f"{mark} {qual}{H.date_display(r['date']):<12s} {r['precision']:<7s} {r['entity_kind']:<8s} "
                  f"{r['entity_id']:<20s} {r['label']}")
    elif a.cmd == "page":
        body = _read(a.body, a.file)
        if not body.strip():
            print("a page needs a body (--body or --file)", file=sys.stderr)
            return 2
        print(H.add_page(c, a.slug, a.title, body, topic=a.topic, summary=a.summary,
                         ordering=a.ordering, status=a.status, people=a.people))
    elif a.cmd == "forget":
        r = H.forget(c, a.kind, a.id)
        print(f"{r['deleted']}; {r['dates']} date row(s) went with it")
    elif a.cmd == "versions":
        cur = c.execute("SELECT status, length(body) AS n, updated FROM pages WHERE slug=?", (a.slug,)).fetchone()
        if not cur:
            print(f"no page {a.slug!r}", file=sys.stderr)
            return 1
        for r in c.execute("SELECT id, saved, status, length(body) AS n FROM page_history "
                           "WHERE slug=? ORDER BY id", (a.slug,)):
            print(f"  {r['saved'][:19]}  {r['status']:6s} {r['n']:7d} chars   (replaced)")
        print(f"  {(cur['updated'] or '')[:19]:19s}  {cur['status']:6s} {cur['n']:7d} chars   (current)")
    elif a.cmd == "request":
        ident = H.add_request(c, a.topic, a.kind, a.what, why=a.why, url=a.url, size_mb=a.size_mb,
                              dest=a.dest, who=a.who)
        print(f"{ident}  (open; a person answers it on the review page, possibly days from now. "
              f"Do not wait or poll: carry on with other work now. This run may never see the "
              f"answer — `resume` shows it to whichever run comes after it arrives.)")
    elif a.cmd == "requests":
        for r in H.list_requests(c, a.status or None, a.topic or None):
            size = f" {r['size_mb']:.0f} MB" if r["size_mb"] else ""
            print(f"#{r['id']:<4d} {r['status']:9s} {r['kind']:9s} {r['topic']:26s} {r['what']}{size}")
            if r["url"]:
                print(f"      {r['url']}")
            if r["answer"]:
                print(f"      answer: {r['answer']}")
    elif a.cmd == "answer":
        r = H.answer_request(c, a.id, a.status, a.answer)
        print(f"#{r['id']} {r['status']}")
    elif a.cmd == "log":
        print(H.add_worklog(c, a.topic, a.done, a.next, a.open, a.who))
    elif a.cmd == "resume":
        st = H.resume_state(c, a.topic)
        t = st["topic"]
        if not t:
            print(f"no topic {a.topic!r}; declare it with `topic` first", file=sys.stderr)
            return 1
        print(f"# {t['title']}  [{t['slug']} · {t['status']}]")
        if t["summary"]:
            print(t["summary"])
        print("\n## In the database")
        print("  " + "  ".join(f"{k} {v}" for k, v in st["counts"].items()))
        if st["counts"]["artifacts"] >= 10 and st["counts"]["pages"] == 0:
            print("\n!! PAGES OWED: this topic has rows but not one page, and the wiki is the point.")
            print("!! Draft the overview page FIRST, before entering more rows. Rough is fine:")
            print("!! pages are status 'draft' by default and every save keeps the old version.")
        if st["sources"]:
            print("\n## Sources (" + str(len(st["sources"])) + ")")
            for r in st["sources"]:
                print(f"  {r['bibkey']:34s} {r['year']:6s} {r['title'][:70]}")
        if st["artifacts"]:
            print("\n## Artifacts (" + str(len(st["artifacts"])) + ")")
            for r in st["artifacts"]:
                print(f"  {r['id']:28s} {r['type']:7s} {r['date_text']:12s} {r['title'][:60]}")
        if st["pages"]:
            print("\n## Pages (" + str(len(st["pages"])) + ")")
            for r in st["pages"]:
                print(f"  {r['ordering']:4d} {r['status']:6s} {r['slug']:44s} {r['words']:6d} chars  {r['title'][:44]}")
        print(f"\n## Files on disk ({len(st['files'])}; {len(st['unregistered_files'])} not yet registered as artifacts)")
        for f in st["unregistered_files"]:
            print(f"  UNREGISTERED  {f}")
        if st["wanted"]:
            print(f"\n## Links owed ({len(st['wanted'])})")
            for w in st["wanted"]:
                print(f"  {w['kind'] + ':' if w['kind'] else ''}{w['name']:40s} from {w['src']}")
        if st["problems"]:
            print(f"\n## Problems ({len(st['problems'])})")
            for p in st["problems"]:
                print(f"  {p['kind']:9s} {p['what']:34s} {p['detail']}")
        open_req = [r for r in st["requests"] if r["status"] == "open"]
        answered = [r for r in st["requests"] if r["status"] != "open"]
        if st["requests"]:
            print(f"\n## Requests ({len(open_req)} waiting, {len(answered)} answered)")
            for r in st["requests"]:
                print(f"  #{r['id']} {r['status']:9s} {r['kind']:9s} {r['what']}")
                if r["answer"]:
                    print(f"      answer: {r['answer']}")
        print("\n## Worklog (newest first)")
        if not st["worklog"]:
            print("  (nothing yet: this topic has not been worked)")
        for r in st["worklog"]:
            print(f"  {r['at'][:16]}  {r['who']}")
            print(f"     done: {r['done']}")
            if r["next"]:
                print(f"     next: {r['next']}")
            if r["open"]:
                print(f"     open: {r['open']}")
    elif a.cmd == "face":
        if a.forget:
            print(f"forgot {H.forget_faces(c, a.artifact)} faces of {a.artifact}")
        else:
            print(H.add_face(c, a.artifact, a.n, a.file, box=a.box, person=a.person, kind=a.kind,
                             confidence=a.confidence, method=a.method))
    elif a.cmd == "keyword":
        n = H.add_keywords(c, a.artifact, a.path, source=a.source, replace=not a.keep)
        print(f"{a.artifact}: {n} path(s) from {a.source}; published as {H.artifact_keywords(c, a.artifact)}")
    elif a.cmd == "ontology":
        if a.file:
            H.set_ontology(c, json.loads(Path(a.file).read_text()), model=a.model)
        o = H.get_ontology(c)
        print(json.dumps(o, ensure_ascii=False, indent=1) if o else "no ontology yet")
    elif a.cmd == "stats":
        v = H.validate(c)
        for k, n in v["stats"].items():
            print(f"{k:10s} {n}")
        print(f"{'problems':10s} {len(v['problems'])}")
        print(f"{'notes':10s} {len(v['notes'])}")
    elif a.cmd == "check":
        v = H.validate(c)
        for p in v["problems"]:
            print(f"{p['kind']:9s} {p['what']:34s} {p['detail']}")
        if v["notes"]:
            print(f"\n-- notes ({len(v['notes'])}): nothing wrong, but worth a look")
            for p in v["notes"]:
                print(f"{p['kind']:9s} {p['what']:34s} {p['detail']}")
        print(f"-- {len(v['problems'])} problems, {len(v['notes'])} notes", file=sys.stderr)
        return 1 if v["problems"] else 0
    elif a.cmd == "wanted":
        info = H.reindex_links(c)
        for name, srcs in sorted(info["wanted"].items()):
            print(f"{name:50s} wanted by {', '.join(srcs)}")
        print(f"-- {info['links']} links on {info['pages']} pages, {len(info['wanted'])} wanted", file=sys.stderr)
    elif a.cmd == "show":
        r = c.execute("SELECT * FROM pages WHERE slug=?", (a.slug,)).fetchone()
        if not r:
            print(f"no page {a.slug!r}", file=sys.stderr)
            return 1
        print(f"# {r['title']}\n[{r['kind']} · {r['topic']} · {r['status']}]\n\n{r['body']}")
    elif a.cmd == "list":
        cols = {"topics": "slug, title, status", "sources": "bibkey, year, title",
                "artifacts": "id, type, date_text, title", "pages": "slug, kind, status, title",
                "people": "name, role", "places": "name, lat, lon", "events": "date_start, topic, title",
                "animals": "name, kind, role", "vessels": "name, kind, built"}[a.what]
        q = f"SELECT {cols} FROM {a.what}"
        args: tuple = ()
        if a.topic and a.what != "topics":
            q += " WHERE topic=?"
            args = (a.topic,)
        for r in c.execute(q, args):
            print(" · ".join("" if x is None else str(x) for x in tuple(r)))
    elif a.cmd == "export":
        Path(a.bib).write_text(H.to_bibtex(c.execute("SELECT * FROM sources ORDER BY bibkey")), encoding="utf-8")
        print(a.bib)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
