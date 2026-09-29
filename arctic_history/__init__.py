"""Arctic history: artifacts, sources, dates and a wiki, in one SQLite file.

``db/history/history.sqlite`` holds everything the research crew writes:

* ``sources``   one row per bibliography entry, keyed by its BibTeX key
* ``artifacts`` one row per thing the map can show (an image, a text, a ship
  track, a place, an event, a quote), each carrying a credit line and the
  bibkey it comes from
* ``pages``     the wiki: narrative pages written by hand, plus a generated
  page for every artifact, source, person and place
* ``people``, ``places``, ``events``  the entities the narrative cross-links to
* ``links``     one row per ``[[wikilink]]``, resolved at publish time

Pages are Markdown with ``[[kind:name]]`` links (``[[artifact:frobisher-004]]``,
``[[source:best1578discourse]]``, ``[[person:Tookoolito]]``,
``[[place:Kodlunarn Island]]``, ``[[page:the-death-march]]``). A bare
``[[Some Title]]`` resolves by title across every kind. A link to something
that does not exist yet is kept and reported as wanted, so it marks work still
to do rather than breaking the build.

Writers reach this through ``tools/history-db.py``; a consumer (the CCGS
Amundsen dashboard's History tab) calls :func:`publish`, which renders the wiki,
the map layer, the timeline and the bibliography into ``<root>/data/history/``.
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import os

# the database lives in the repository's db/ directory unless told otherwise
DB_DIR = Path(os.environ.get("ARCTIC_HISTORY_DB_DIR", Path(__file__).resolve().parents[1] / "db"))

log = logging.getLogger(__name__)

HISTORY_DIR = DB_DIR / "history"
HISTORY_DB = HISTORY_DIR / "history.sqlite"

# the kinds of thing a wiki page can be about; `page` is a hand-written narrative
KINDS = ("page", "artifact", "source", "person", "place", "event", "topic", "animal", "vessel", "subject")
ARTIFACT_TYPES = ("image", "text", "track", "place", "event", "map", "quote", "object")
# `licence` is a code from this vocabulary; what the code does not say (the
# holder, the term, the request number, why it is thought expired) goes in
# `rights_note`, free text. Most permissive first.
LICENCE_CODES = {
    "public-domain": "public domain",
    "cc0": "CC0",
    "crown-expired": "Crown copyright expired; public domain",
    "crown-open": "Crown copyright; non-commercial reproduction permitted",
    "open-access": "open access, free to read",
    "attribution": "reusable with attribution",
    "permission": "reproduced by permission",
    "fair-dealing": "in copyright; quoted under fair dealing",
    "in-copyright-licensed": "in copyright; held for internal research use under licence",
    "in-copyright-cited": "in copyright; cited, not reproduced",
    "rights-reserved": "all rights reserved; held under the holder's terms",
    "not-cleared": "NOT CLEARED for reuse",
    "unknown": "copyright status unknown",
}
# Creative Commons keeps its version: cc-by-4.0, cc-by-sa-2.5, cc-by-nc-nd-4.0, cc-by (unversioned)
_CC_CODE = re.compile(r"^cc-by(-nc)?(-sa|-nd)?(-\d\.\d)?$")


def is_licence_code(code: str) -> bool:
    return code in LICENCE_CODES or bool(_CC_CODE.match(code))


def licence_label(code: str) -> str:
    """The reader's phrase for a code: `cc-by-sa-4.0` reads as CC BY-SA 4.0."""
    if code in LICENCE_CODES:
        return LICENCE_CODES[code]
    m = _CC_CODE.match(code)
    if m:
        name = "BY" + (m.group(1) or "").upper() + (m.group(2) or "").upper()
        return "CC " + name + (" " + m.group(3)[1:] if m.group(3) else "")
    return code


def rights_text(r) -> str:
    """The reader's line: the code's phrase, then the note if there is one.
    A legacy free-text licence (pre-vocabulary) is shown as it stands."""
    code = r["licence"] or ""
    note = (r["rights_note"] or "") if "rights_note" in r.keys() else ""
    text = licence_label(code) if is_licence_code(code) else code
    return f"{text}. {note}" if note and text else (note or text)


def _check_licence(code: str) -> None:
    if code and not is_licence_code(code):
        raise ValueError(f"licence must be a code, not free text: {code!r}. One of "
                         f"{', '.join(LICENCE_CODES)}, or cc-by / cc-by-sa / cc-by-nc-sa / cc-by-nc-nd "
                         f"with a version (cc-by-4.0). Put the detail in --rights-note.")


# A tag has a shape: lowercase, one tag per array element, words joined by
# hyphens at the boundary (`musk-ox`, `fort-conger`, `full-text`), and singular,
# because a tag names a kind of thing and not a count. A proper name keeps the
# form it is written in, plural included (`queen-elizabeth-islands`). The
# writers put every tag into that shape; this table then folds the spellings
# already in use into the one form the layer searches on. `leads` (the open
# water in the ice) is deliberately not folded to `lead`, which tags the metal
# in the Franklin bones.
TAG_ALIASES = {
    # run together where the words divide
    "axelheiberg": "axel-heiberg",
    "banksisland": "banks-island",
    "barrowstrait": "barrow-strait",
    "breakup": "break-up",
    "capecolumbia": "cape-columbia",
    "capesabine": "cape-sabine",
    "capethomashubbard": "cape-thomas-hubbard",
    "capeyork": "cape-york",
    "crockerland": "crocker-land",
    "davisstrait": "davis-strait",
    "dewline": "dew-line",
    "eurekasound": "eureka-sound",
    "fifththule": "fifth-thule",
    "fortconger": "fort-conger",
    "franklinsearch": "franklin-search",
    "fulltext": "full-text",
    "icecap": "ice-cap",
    "iceisland": "ice-island",
    "iceshelf": "ice-shelf",
    "kingchristian": "king-christian",
    "kingwilliamisland": "king-william-island",
    "manhauling": "man-hauling",
    "massbalance": "mass-balance",
    "melvillebay": "melville-bay",
    "mercybay": "mercy-bay",
    "mouldbay": "mould-bay",
    "muskox": "musk-ox",
    "northgreenland": "north-greenland",
    "oralhistory": "oral-history",
    "payerharbour": "payer-harbour",
    "polarsea": "polar-sea",
    "pressureridge": "pressure-ridge",
    "primarysource": "primary-source",
    "queenelizabethislands": "queen-elizabeth-islands",
    "r.c.m.p.": "rcmp",
    "resolutionisland": "resolution-island",
    "seaice": "sea-ice",
    "searchandrescue": "search-and-rescue",
    "smithsound": "smith-sound",
    "snowhouse": "snow-house",
    "stroch": "st-roch",
    "supplyship": "supply-ship",
    "sverdruppass": "sverdrup-pass",
    "t3": "t-3",
    "wardhunt": "ward-hunt",
    "wellingtonchannel": "wellington-channel",
    # plural where the tag names a kind of thing
    "archives": "archive",
    "bears": "bear",
    "boats": "boat",
    "buildings": "building",
    "cairns": "cairn",
    "clouds": "cloud",
    "communications": "communication",
    "corrections": "correction",
    "deaths": "death",
    "documents": "document",
    "dogs": "dog",
    "drawings": "drawing",
    "encounters": "encounter",
    "events": "event",
    "expeditions": "expedition",
    "families": "family",
    "floebergs": "floeberg",
    "glaciers": "glacier",
    "graves": "grave",
    "icebergs": "iceberg",
    "icebreakers": "icebreaker",
    "instruments": "instrument",
    "maps": "map",
    "meteorites": "meteorite",
    "missions": "mission",
    "new-islands": "new-island",
    "orders": "order",
    "photographs": "photograph",
    "plans": "plan",
    "posts": "post",
    "rations": "ration",
    "relics": "relic",
    "routes": "route",
    "settlements": "settlement",
    "ships": "ship",
    "skills": "skill",
    "specimens": "specimen",
    "supplies": "supply",
    "survivors": "survivor",
    "tent-rings": "tent-ring",
    "vessels": "vessel",
    "weather-stations": "weather-station",
    "wrecks": "wreck",
}


def normalise_tag(tag: str) -> str:
    """One tag in the form it is stored in: lowercase, trimmed, spaces and
    underscores hyphenated, a known variant folded to its canonical form."""
    t = re.sub(r"[\s_]+", "-", str(tag or "").strip().lower())
    t = re.sub(r"-{2,}", "-", t).strip("-")
    return TAG_ALIASES.get(t, t)


def normalise_tags(v) -> list:
    """Tags as they are written to the database: one per element, in the order
    given, with a comma-joined string taken apart and empties and repeats
    dropped. Accepts a list, a JSON array, or a comma or semicolon separated
    string, so an older row re-read from the database comes back clean."""
    if v is None or v == "":
        return []
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
        except (json.JSONDecodeError, ValueError):
            items = [v]
        else:
            items = parsed if isinstance(parsed, list) else [v]
    elif isinstance(v, (list, tuple)):
        items = list(v)
    else:
        items = [v]
    out: list = []
    for item in items:
        for part in re.split(r"[,;]", str(item)):
            t = normalise_tag(part)
            if t and t not in out:
                out.append(t)
    return out


def stored_tags(raw) -> list:
    """The tag elements of a row as they stand, unnormalised: what `check`
    reads to find a row written before the vocabulary settled."""
    try:
        v = json.loads(raw or "[]")
    except (json.JSONDecodeError, ValueError):
        return [str(raw)]
    return [str(x) for x in v] if isinstance(v, list) else [str(v)]


# A vessel's `kind` is a code from this vocabulary: the hull, rig or craft
# type at the level the map and the wiki filter on. Everything the code does
# not say (the class, the aircraft model, the trade she worked, a conversion,
# the navy that bought her) goes in `kind_note`, free text.
#
# Choosing between two readings of the same entry: the code names what the
# vessel is where the entry names a rig or a hull, and what she was built or
# fitted for where that is all the entry gives. So a whaling barque is a
# `barque` with "whaler" in the note, while a whaler whose rig no source
# records is a `whaler`. Rig spellings and near neighbours are folded (bark to
# barque, brigantine to brig), and propulsion is a note, not a code, except for
# `steam-whaler`, which is an era of its own. Sailing rigs first, then small
# craft, then power, then the trades and the work.
VESSEL_KINDS = {
    "ship": "full-rigged ship",
    "barque": "barque",
    "brig": "brig",
    "schooner": "schooner",
    "sloop": "sloop",
    "yacht": "yacht",
    "bomb-vessel": "bomb vessel",
    "boat": "ship's boat",
    "umiak": "umiak, an open skin boat",
    "steamer": "steamer",
    "tender": "tender",
    "icebreaker": "icebreaker",
    "submarine": "submarine",
    "whaler": "whaler",
    "steam-whaler": "steam whaler",
    "sealer": "sealer",
    "research-vessel": "research or survey vessel",
    "cruise-ship": "cruise ship",
    "transport": "transport or supply ship",
    "freighter": "freighter",
    "tanker": "tanker",
    "aircraft": "aircraft",
}


def is_vessel_kind(code: str) -> bool:
    return code in VESSEL_KINDS


def vessel_kind_label(code: str) -> str:
    return VESSEL_KINDS.get(code, code)


def vessel_kind_text(r) -> str:
    """The reader's line: the code's word, then the note if there is one, so
    that `barque` and "purchased into the Navy" read as they were written. A
    legacy free-text kind (pre-vocabulary) is shown as it stands."""
    code = r["kind"] or ""
    note = (r["kind_note"] or "") if "kind_note" in r.keys() else ""
    text = vessel_kind_label(code)
    return f"{text}, {note}" if note and text else (note or text)


def _check_vessel_kind(code: str) -> None:
    if code and not is_vessel_kind(code):
        raise ValueError(f"a vessel's kind must be a code, not free text: {code!r}. One of "
                         f"{', '.join(VESSEL_KINDS)}. Put the class, the model, the trade, "
                         f"the conversion or the owner in --kind-note.")

# what a source is, in the shape the bibliography needs; `misc` is the last resort
ENTRY_TYPES = {
    "book": "a standalone work: a narrative, a monograph, an edited volume",
    "article": "a piece in a journal, magazine or newspaper; its title goes in --container",
    "incollection": "a chapter or paper in a book, a report series or a collection",
    "report": "a government or institutional report, memoir, bulletin or inquiry",
    "thesis": "a doctoral or master's thesis",
    "online": "a web page, database entry or catalogue record cited as a page",
    "dataset": "a data file, a data service or a database queried for values",
    "misc": "none of the above: an artwork, a photograph, an object, a manuscript",
}
# BibTeX and biblatex spell some of these differently; an import lands on ours
ENTRY_TYPE_ALIASES = {
    "inbook": "incollection", "inproceedings": "incollection", "conference": "incollection",
    "techreport": "report", "manual": "report", "phdthesis": "thesis", "mastersthesis": "thesis",
    "electronic": "online", "www": "online", "webpage": "online",
    "unpublished": "misc", "booklet": "book", "proceedings": "book", "data": "dataset",
}


def entry_type_code(value: str) -> str:
    """The type as this database spells it. A BibTeX synonym (techreport,
    phdthesis, inbook) lands on ours; anything else is refused."""
    t = (value or "").strip().lower() or "misc"
    t = ENTRY_TYPE_ALIASES.get(t, t)
    if t not in ENTRY_TYPES:
        raise ValueError(f"entry_type must be one of {', '.join(ENTRY_TYPES)}, not {value!r}")
    return t


# ---------------------------------------------------------------- archives
# `archive` is the institution or platform that holds the copy, under the name
# the institution itself uses. These are the variants the crew has written for
# names already in the database; an archive not listed here is taken as written,
# so this is a spelling table, not a closed vocabulary.
#
# The journal *Arctic* is published by the Arctic Institute of North America,
# which serves the back run at pubs.aina.ucalgary.ca and the current issues on
# the University of Calgary's journal hosting. The institute is the holder and
# the journal is the container, so a paper in *Arctic* is held at the Arctic
# Institute of North America whichever address it was read from.
ARCHIVE_ALIASES = {
    "Arctic": "Arctic Institute of North America",
    "Arctic (AINA)": "Arctic Institute of North America",
    "AINA": "Arctic Institute of North America",
    "ARCTIC journal": "Arctic Institute of North America",
    "Arctic journal": "Arctic Institute of North America",
    "Arctic (journal), University of Calgary": "Arctic Institute of North America",
    "ARCTIC (University of Calgary)": "Arctic Institute of North America",
    "Arctic, journalhosting.ucalgary.ca": "Arctic Institute of North America",
    "ARCTIC, University of Calgary journal hosting": "Arctic Institute of North America",
    "University of Calgary Journal Hosting": "Arctic Institute of North America",
    "journalhosting.ucalgary.ca": "Arctic Institute of North America",
    "pubs.aina.ucalgary.ca": "Arctic Institute of North America",
    # Polar Record is Cambridge University Press's; the copies are on Cambridge Core
    "Polar Record": "Cambridge Core",
    "Cambridge University Press": "Cambridge Core",
    "cambridge.org": "Cambridge Core",
    "Dictionary of Canadian Biography / Dictionnaire biographique du Canada": "Dictionary of Canadian Biography",
    "Dictionnaire biographique du Canada": "Dictionary of Canadian Biography",
    "DCB": "Dictionary of Canadian Biography",
    "biographi.ca": "Dictionary of Canadian Biography",
    "archive.org": "Internet Archive",
    "Internet Archive (Wayback capture)": "Internet Archive Wayback Machine",
    "Wayback Machine": "Internet Archive Wayback Machine",
    "web.archive.org": "Internet Archive Wayback Machine",
    "Publications du gouvernement du Canada / Government of Canada Publications":
        "Government of Canada Publications",
    "Publications du gouvernement du Canada": "Government of Canada Publications",
    "publications.gc.ca": "Government of Canada Publications",
    "Canadiana / Government of Canada sessional papers": "Canadiana",
    "Canadiana / Natural Resources Canada": "Canadiana",
    "canadiana.ca": "Canadiana",
    "Public Safety Canada library": "Public Safety Canada Library",
    "AMNH": "American Museum of Natural History",
    "Library of Congress Prints and Photographs Division": "Library of Congress, Prints and Photographs Division",
    "SPRI": "Scott Polar Research Institute",
    "commons.wikimedia.org": "Wikimedia Commons",
    "Wikimedia Commons / Government of Canada Publications": "Wikimedia Commons",
    "wikisource.org": "Wikisource",
    "Canadian Parks Service": "Parks Canada",
    "Parks Canada, Directory of Federal Heritage Designations": "Parks Canada",
    "GeoGratis / Open Maps, Natural Resources Canada": "Natural Resources Canada",
    "LAC": "Library and Archives Canada",
    "Bibliotheque et Archives Canada": "Library and Archives Canada",
    "gutenberg.org": "Project Gutenberg",
    "hathitrust.org": "HathiTrust",
    "jstor.org": "JSTOR",
}


def _archive_key(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().strip(".,;").casefold()


_ARCHIVE_BY_KEY = {_archive_key(k): v for k, v in ARCHIVE_ALIASES.items()}
# the names we recognise: enough to tell a holding institution with a detail
# hanging off it from an institution whose own name has a comma in it
_ARCHIVE_NAMES = {_archive_key(x) for x in ARCHIVE_ALIASES} | {_archive_key(x) for x in ARCHIVE_ALIASES.values()}
# an identifier of the copy: it belongs in callno
_ARCHIVE_ID = re.compile(r"^(?:items?|nos?|cat|catalogue no|call ?no|accession|shelfmark|lot|MSS?|CIHM|"
                         r"microform|microfiche|photograph|negative)\b\.?[^\d]*\d"
                         r"|^[A-Za-z]{0,6}[-.]?\d{4,}[\w./-]*$", re.I)
# a citation of where in the work: volume, issue, pages. It belongs in the note
_ARCHIVE_CITE = re.compile(r"^(?:vols?\.?|nos?\.)\s*[\dIVXL]|^\d+\s*\(\d+\)|^pp?\.\s*\d|^\d+\s*[:,]\s*\d", re.I)
# how the copy was reached, or which copy it is: it belongs in the note
_ARCHIVE_ROUTE = re.compile(r"^(?:via|from|reproduced|sold)\b|^Flickr Commons$|^Wayback capture$|^borrow only$", re.I)
_ARCHIVE_DETAIL = re.compile(r"\b(?:collections?|cop(?:y|ies)|fonds|papers|archives|microform|microfiche|capture)\b",
                             re.I)
# "Arctic 36(4): 380-381 (Arctic Profiles)": a citation written into the field
_ARCHIVE_JOURNAL = re.compile(r"^(?P<name>.+?)\s+(?P<cite>\d+\s*\(\d+\)\s*[:,].*)$")


def canonical_archive(value: str) -> str:
    """The name to file this holding under. A known variant becomes the
    canonical name; anything else is returned as written."""
    raw = re.sub(r"\s+", " ", value or "").strip()
    return _ARCHIVE_BY_KEY.get(_archive_key(raw), raw)


def _archive_detail(piece: str) -> str:
    if _ARCHIVE_ID.match(piece):
        return "callno"
    if _ARCHIVE_CITE.match(piece) or _ARCHIVE_ROUTE.match(piece) or _ARCHIVE_DETAIL.search(piece):
        return "note"
    return ""


def normalise_archive(value: str) -> tuple[str, str, str]:
    """Split an archive field into (institution, callno, note): the holding
    institution under its canonical name, the identifiers of the copy, and the
    citation or provenance detail that is neither."""
    raw = re.sub(r"\s+", " ", value or "").strip()
    if not raw:
        return "", "", ""
    if _archive_key(raw) in _ARCHIVE_BY_KEY:
        return _ARCHIVE_BY_KEY[_archive_key(raw)], "", ""
    head, callno, note = raw, [], []
    m = _ARCHIVE_JOURNAL.match(head)
    if m and _archive_key(m.group("name")) in _ARCHIVE_NAMES:
        note.append(m.group("cite").strip())
        head = m.group("name").strip()
    if ";" in head:                       # "A; B": A holds the copy, B is the rest of the story
        head, rest = head.split(";", 1)
        head, rest = head.strip(), rest.strip()
        if rest:
            note.append(rest)
    peeled: list[str] = []
    while True:
        m = re.search(r"\s*\((?P<detail>[^()]*)\)$", head) or re.search(r"\s*,\s*(?P<detail>[^,()]+)$", head)
        if not m:
            break
        rest = head[:m.start()].strip().strip(",")
        pieces = [p.strip() for p in m.group("detail").split(",") if p.strip()]
        if not rest or not pieces:
            break
        known = _archive_key(rest) in _ARCHIVE_NAMES
        if not known and not any(_archive_detail(p) for p in pieces):
            break
        keep = []
        for p in pieces:
            (callno if _archive_detail(p) == "callno" else keep).append(p)
        if keep:
            peeled.append(", ".join(keep))
        head = rest
    note += reversed(peeled)
    return canonical_archive(head), "; ".join(callno), "; ".join(note)


SCHEMA = """
CREATE TABLE IF NOT EXISTS topics (
  slug        TEXT PRIMARY KEY,
  title       TEXT NOT NULL,
  summary     TEXT DEFAULT '',
  researcher  TEXT DEFAULT '',
  status      TEXT DEFAULT 'open',
  updated     TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS sources (
  bibkey      TEXT PRIMARY KEY,
  entry_type  TEXT NOT NULL DEFAULT 'misc',   -- one of ENTRY_TYPES; chosen, not left at misc
  author      TEXT DEFAULT '',
  title       TEXT NOT NULL,
  year        TEXT DEFAULT '',
  container   TEXT DEFAULT '',            -- journal, book or collection it sits in
  publisher   TEXT DEFAULT '',
  address     TEXT DEFAULT '',
  volume      TEXT DEFAULT '',
  pages       TEXT DEFAULT '',
  url         TEXT DEFAULT '',
  urldate     TEXT DEFAULT '',
  doi         TEXT DEFAULT '',
  archive     TEXT DEFAULT '',            -- holding institution, under its own name
  language    TEXT DEFAULT '',            -- of the text as held (ISO 639-1: en, fr, da, no, de, iu...)
  orig_language TEXT DEFAULT '',          -- when the work is a translation
  translator  TEXT DEFAULT '',
  callno      TEXT DEFAULT '',            -- accession or catalogue number
  licence     TEXT DEFAULT '',            -- a code from LICENCE_CODES
  rights_note TEXT DEFAULT '',            -- the holder, the term, the reasoning: free text
  note        TEXT DEFAULT '',
  primary_src INTEGER NOT NULL DEFAULT 0,
  local_file  TEXT DEFAULT '',            -- a downloaded copy, relative to db/history/
  topic       TEXT DEFAULT '',            -- the topic that entered it
  updated     TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS artifacts (
  id          TEXT PRIMARY KEY,
  topic       TEXT NOT NULL,
  type        TEXT NOT NULL,
  title       TEXT NOT NULL,
  date_text   TEXT DEFAULT '',            -- as written: 1845, 1845-08, 1845/1848
  date_start  TEXT DEFAULT '',            -- ISO, for sorting and the timeline
  date_end    TEXT DEFAULT '',
  creator     TEXT DEFAULT '',
  description TEXT DEFAULT '',
  lat         REAL,
  lon         REAL,
  geometry    TEXT DEFAULT '',            -- GeoJSON geometry, JSON
  waypoints   TEXT DEFAULT '',            -- [{date, lat, lon, note}], JSON
  source_url  TEXT DEFAULT '',
  download_url TEXT DEFAULT '',
  local_file  TEXT DEFAULT '',            -- relative to db/history/
  licence     TEXT DEFAULT '',            -- a code from LICENCE_CODES
  rights_note TEXT DEFAULT '',            -- the holder, the term, the reasoning: free text
  credit      TEXT NOT NULL DEFAULT '',
  bibkey      TEXT NOT NULL DEFAULT '',
  pages       TEXT DEFAULT '',            -- where in the cited work
  people      TEXT DEFAULT '[]',          -- JSON array of names
  tags        TEXT DEFAULT '[]',          -- JSON array
  updated     TEXT DEFAULT '',
  FOREIGN KEY (bibkey) REFERENCES sources (bibkey)
);
CREATE INDEX IF NOT EXISTS artifacts_topic ON artifacts (topic);
CREATE INDEX IF NOT EXISTS artifacts_type ON artifacts (type);
CREATE INDEX IF NOT EXISTS artifacts_date ON artifacts (date_start);

CREATE TABLE IF NOT EXISTS pages (
  slug        TEXT PRIMARY KEY,
  kind        TEXT NOT NULL DEFAULT 'page',
  title       TEXT NOT NULL,
  topic       TEXT DEFAULT '',
  summary     TEXT DEFAULT '',
  body        TEXT DEFAULT '',            -- Markdown with [[wikilinks]]
  ordering    INTEGER NOT NULL DEFAULT 100,
  status      TEXT NOT NULL DEFAULT 'draft',   -- draft, good
  updated     TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS pages_topic ON pages (topic);
CREATE INDEX IF NOT EXISTS pages_kind ON pages (kind);

-- every save of a page keeps the version it replaced, so a rough draft
-- costs nothing and no wording is ever lost
CREATE TABLE IF NOT EXISTS page_history (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  slug        TEXT NOT NULL,
  title       TEXT DEFAULT '',
  summary     TEXT DEFAULT '',
  body        TEXT DEFAULT '',
  status      TEXT DEFAULT '',
  saved       TEXT NOT NULL                -- when this version was replaced
);
CREATE INDEX IF NOT EXISTS page_history_slug ON page_history (slug, id);

-- every replacement of an artifact keeps the row it overwrote, with a
-- message saying why: the detail that belongs in a commit message, not in
-- the entry a reader sees
CREATE TABLE IF NOT EXISTS artifact_history (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  artifact_id TEXT NOT NULL,
  row         TEXT NOT NULL,               -- the replaced row, as JSON
  message     TEXT DEFAULT '',             -- why it was replaced
  who         TEXT DEFAULT '',             -- the run or person writing
  saved       TEXT NOT NULL                -- when this version was replaced
);
CREATE INDEX IF NOT EXISTS artifact_history_id ON artifact_history (artifact_id, id);

CREATE TABLE IF NOT EXISTS people (
  name        TEXT PRIMARY KEY,
  also        TEXT DEFAULT '',            -- other spellings, semicolon separated
  role        TEXT DEFAULT '',
  born        TEXT DEFAULT '',
  died        TEXT DEFAULT '',
  affiliation TEXT DEFAULT '',            -- expedition, ship, community, service
  indigenous  INTEGER NOT NULL DEFAULT 0,
  note        TEXT DEFAULT '',
  bibkey      TEXT DEFAULT '',
  topic       TEXT DEFAULT '',
  updated     TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS places (
  name        TEXT PRIMARY KEY,           -- the modern name
  historic    TEXT DEFAULT '',            -- the name in the sources
  inuktitut   TEXT DEFAULT '',
  lat         REAL,
  lon         REAL,
  kind        TEXT DEFAULT '',            -- community, harbour, cape, strait, site, wreck
  note        TEXT DEFAULT '',
  bibkey      TEXT DEFAULT '',
  topic       TEXT DEFAULT '',
  updated     TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS events (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  topic       TEXT NOT NULL,
  date_start  TEXT NOT NULL,
  date_end    TEXT DEFAULT '',
  date_text   TEXT DEFAULT '',
  title       TEXT NOT NULL,
  detail      TEXT DEFAULT '',
  lat         REAL,
  lon         REAL,
  place       TEXT DEFAULT '',
  people      TEXT DEFAULT '[]',
  bibkey      TEXT DEFAULT '',
  tags        TEXT DEFAULT '[]',
  updated     TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS events_date ON events (date_start);
CREATE INDEX IF NOT EXISTS events_topic ON events (topic);

-- Every date is its own row. A range is two rows sharing a span, one with
-- role 'start' and one with role 'end', so a timeline never has to take a
-- record apart to find out when it begins. `precision` says how much of the
-- date the source actually gives, and `qualifier` carries the source's own
-- hedge ("circa", "before", "by"), so "the summer of 1848" and
-- "25 April 1848" can sit on one axis without pretending to equal accuracy.
CREATE TABLE IF NOT EXISTS dates (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_kind TEXT NOT NULL,              -- artifact, event, person, place, source, page, topic
  entity_id   TEXT NOT NULL,
  topic       TEXT DEFAULT '',
  date        TEXT NOT NULL,              -- ISO: YYYY, YYYY-MM or YYYY-MM-DD
  precision   TEXT NOT NULL DEFAULT 'day',   -- day, month, season, year, decade, century
  qualifier   TEXT DEFAULT '',            -- '', circa, before, after, by, early, late
  role        TEXT NOT NULL DEFAULT 'point', -- point, start, end
  span        TEXT DEFAULT '',            -- ties a start to its end
  label       TEXT DEFAULT '',            -- what happened on this date
  lat         REAL,
  lon         REAL,
  place       TEXT DEFAULT '',
  bibkey      TEXT DEFAULT '',
  updated     TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS dates_date ON dates (date);
CREATE INDEX IF NOT EXISTS dates_entity ON dates (entity_kind, entity_id);
CREATE INDEX IF NOT EXISTS dates_topic ON dates (topic);
CREATE UNIQUE INDEX IF NOT EXISTS dates_unique ON dates (entity_kind, entity_id, date, role, label);

-- The worklog is the project's memory between runs. A researcher writes a
-- line after every milestone saying what is now in the database and what the
-- next step is, so a run that is cut off, or a run months later, starts from
-- the last line rather than from nothing.
CREATE TABLE IF NOT EXISTS worklog (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  topic       TEXT NOT NULL,
  at          TEXT NOT NULL,
  who         TEXT DEFAULT '',            -- the run or person writing
  done        TEXT NOT NULL,              -- what is now in the database
  next        TEXT DEFAULT '',            -- the step after this one
  open        TEXT DEFAULT ''             -- questions and doubts still open
);
CREATE INDEX IF NOT EXISTS worklog_topic ON worklog (topic, id);

-- Things a researcher cannot do alone: a download over the size limit, an API
-- key, a judgement call, a question only a person can answer. A request waits
-- here until someone answers it on the dashboard's /history/requests page.
CREATE TABLE IF NOT EXISTS requests (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  topic       TEXT NOT NULL,
  kind        TEXT NOT NULL,              -- download, api_key, question, access, other
  what        TEXT NOT NULL,              -- one line: what is wanted
  why         TEXT DEFAULT '',            -- what it is for
  url         TEXT DEFAULT '',
  size_mb     REAL,
  dest        TEXT DEFAULT '',            -- where a download should land, relative to db/history/
  who         TEXT DEFAULT '',
  status      TEXT NOT NULL DEFAULT 'open',   -- open, approved, denied, done
  answer      TEXT DEFAULT '',            -- the person's reply
  created     TEXT NOT NULL,
  resolved    TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS requests_status ON requests (status, id);

CREATE TABLE IF NOT EXISTS links (
  src         TEXT NOT NULL,              -- page slug the link is written on
  kind        TEXT NOT NULL,              -- target kind
  name        TEXT NOT NULL,              -- target name as written
  target      TEXT DEFAULT '',            -- resolved page slug, '' when wanted
  PRIMARY KEY (src, kind, name)
);
CREATE INDEX IF NOT EXISTS links_target ON links (target);
"""


# ---------------------------------------------------------------- plumbing
SCHEMA_EXTRA = """
-- faces cut from the photographs for the People page (issue #2)
CREATE TABLE IF NOT EXISTS faces (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  artifact_id TEXT NOT NULL,
  n           INTEGER NOT NULL,
  file        TEXT NOT NULL,               -- relative to db/history/, under <topic>/files/faces/
  box         TEXT DEFAULT '',             -- [x, y, w, h] in the original raster, JSON
  person      TEXT DEFAULT '',             -- a name in people, or '' when unidentified
  confidence  REAL,
  method      TEXT DEFAULT '',             -- detector and identification rule
  updated     TEXT DEFAULT '',
  UNIQUE (artifact_id, n)
);
-- subject paths on artifacts, from the crew or a local model (issue #3)
CREATE TABLE IF NOT EXISTS keywords (
  artifact_id TEXT NOT NULL,
  path        TEXT NOT NULL,               -- levels joined by ' > '
  ordinal     INTEGER NOT NULL DEFAULT 0,
  source      TEXT NOT NULL DEFAULT 'crew', -- 'crew' or 'llm:<model>'
  updated     TEXT DEFAULT '',
  PRIMARY KEY (artifact_id, path, source)
);
-- the one ontology tree the keyword paths belong to
CREATE TABLE IF NOT EXISTS ontology (
  id          INTEGER PRIMARY KEY CHECK (id = 1),
  tree        TEXT NOT NULL DEFAULT '{}',  -- {"Level 1": {"Level 2": ["Level 3", ...]}}, JSON
  model       TEXT DEFAULT '',
  generated   TEXT DEFAULT ''
);
"""

SCHEMA_ANIMALS_VESSELS = """
-- the dogs, ponies, cats and bear cubs of the expeditions, first-class like people
CREATE TABLE IF NOT EXISTS animals (
  name        TEXT PRIMARY KEY,
  kind        TEXT DEFAULT '',             -- dog, pony, cat, bear, ox, fox, ...
  also        TEXT DEFAULT '',             -- other names or spellings, semicolon separated
  role        TEXT DEFAULT '',             -- lead dog of the 1909 polar party; ship's cat of the Karluk
  born        TEXT DEFAULT '',
  died        TEXT DEFAULT '',
  affiliation TEXT DEFAULT '',             -- expedition, ship, owner or driver
  note        TEXT DEFAULT '',
  bibkey      TEXT DEFAULT '',
  topic       TEXT DEFAULT '',
  updated     TEXT DEFAULT ''
);
-- the ships, boats and aircraft, first-class like people
CREATE TABLE IF NOT EXISTS vessels (
  name        TEXT PRIMARY KEY,            -- as usually written: HMS Investigator, Gjoa, CCGS Amundsen
  kind        TEXT DEFAULT '',             -- a code from VESSEL_KINDS: barque, whaler, icebreaker, aircraft
  kind_note   TEXT DEFAULT '',             -- what the code does not say: Wind class, DHC-3 Otter: free text
  also        TEXT DEFAULT '',             -- former or later names, semicolon separated
  role        TEXT DEFAULT '',             -- what she did in this history
  built       TEXT DEFAULT '',             -- year, yard, place
  lost        TEXT DEFAULT '',             -- fate, with a date
  affiliation TEXT DEFAULT '',             -- navy, owner, expedition, port
  tonnage     TEXT DEFAULT '',
  note        TEXT DEFAULT '',
  bibkey      TEXT DEFAULT '',
  topic       TEXT DEFAULT '',
  updated     TEXT DEFAULT ''
);
"""

SCHEMA_NATURE = """
-- The natural half of the layer. A subject is what an observation is of: a
-- species, a rock unit, a fossil bed, a kind of ice, a variable like air
-- temperature, a named thing that happens like an aurora or a magnetic storm.
-- One table for every kind, because the wiki wants one kind of page and one
-- link form ([[subject:Ovibos moschatus]], [[subject:muskox]], [[subject:umingmak]]).
CREATE TABLE IF NOT EXISTS subjects (
  name        TEXT PRIMARY KEY,            -- Ovibos moschatus; Eureka Sound Group; aurora; air temperature
  kind        TEXT NOT NULL DEFAULT '',    -- a code from SUBJECT_KINDS
  domain      TEXT NOT NULL DEFAULT '',    -- a code from DOMAINS
  rank        TEXT DEFAULT '',             -- taxa and rock units: species, genus, family; formation, group
  parent      TEXT DEFAULT '',             -- the next rank up, by name: the tree
  english     TEXT DEFAULT '',
  french      TEXT DEFAULT '',
  inuktitut   TEXT DEFAULT '',
  kalaallisut TEXT DEFAULT '',
  also        TEXT DEFAULT '',             -- other names, synonyms, spellings; semicolon separated
  unit        TEXT DEFAULT '',             -- for a variable: F, C, fathoms, m, deg, hPa, cm
  status      TEXT DEFAULT '',             -- COSEWIC or IUCN code with its year, for a taxon
  backbone_id TEXT DEFAULT '',             -- GBIF or WoRMS id; a WEBLEX unit id; an IAU or SIMBAD name
  note        TEXT DEFAULT '',             -- the reader's paragraph: the generated page's body
  bibkey      TEXT DEFAULT '',
  topic       TEXT DEFAULT '',
  updated     TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS subjects_kind ON subjects (kind);
CREATE INDEX IF NOT EXISTS subjects_domain ON subjects (domain);

-- The observation is the atom of the natural half, as the date is of the
-- timeline: one subject, one date, one position, one source, and where there
-- is a number, the number in the unit it was written in.
CREATE TABLE IF NOT EXISTS observations (
  id          TEXT PRIMARY KEY,            -- <topic>-<nnn> from research; amundsen-<date>-<nnn> from the ship
  topic       TEXT NOT NULL,
  subject     TEXT NOT NULL,               -- subjects.name; the writer resolves any of its names
  date_text   TEXT DEFAULT '',             -- as written
  date_start  TEXT DEFAULT '',             -- ISO
  date_end    TEXT DEFAULT '',
  lat         REAL,
  lon         REAL,
  place       TEXT DEFAULT '',             -- places.name; fills lat/lon when they are not given
  depth       REAL,                        -- metres below the surface: the water column, a core
  height      REAL,                        -- metres above: the sky and the air
  value       REAL,                        -- the number, when there is one
  unit        TEXT DEFAULT '',             -- as written: F, fathoms, feet, deg, cm; never converted here
  count       TEXT DEFAULT '',             -- living things: "about 200", "12", "a herd", "present", "absent"
  qualifier   TEXT DEFAULT '',             -- "first of the season", "coldest of the winter", "no bottom at"
  stage       TEXT DEFAULT '',             -- calf, juvenile, adult; flowering; in seed
  sex         TEXT DEFAULT '',
  behaviour   TEXT DEFAULT '',             -- hauled out, feeding, migrating, denning
  method      TEXT DEFAULT '',             -- a code from METHODS
  instrument  TEXT DEFAULT '',             -- the thermometer, the dip circle, the lead line, the CTD
  observer    TEXT DEFAULT '',             -- people.name, or the party or the watch
  vessel      TEXT DEFAULT '',             -- vessels.name when it applies
  detail      TEXT NOT NULL DEFAULT '',    -- the sentence that says what was seen, naming the observer
  confidence  TEXT DEFAULT '',             -- certain, probable, doubtful: the identification or the reading
  artifact_id TEXT DEFAULT '',             -- the photograph, quote, chart or object that is the evidence
  event_id    INTEGER,                     -- the human-history event this also is
  sensitive   INTEGER NOT NULL DEFAULT 0,  -- a den, a nest, a haul-out, a fossil site at risk: published coarsened
  origin      TEXT NOT NULL DEFAULT 'research',  -- research, ship, crew
  bibkey      TEXT NOT NULL DEFAULT '',
  pages       TEXT DEFAULT '',
  tags        TEXT DEFAULT '[]',
  updated     TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS observations_subject ON observations (subject);
CREATE INDEX IF NOT EXISTS observations_topic ON observations (topic);
CREATE INDEX IF NOT EXISTS observations_date ON observations (date_start);
"""

SUBJECT_KINDS = {
    "taxon": "a living thing at any rank: Ovibos moschatus, Cetacea, Saxifraga oppositifolia, a sea-ice diatom",
    "unit": "a rock unit or structure: Eureka Sound Group, Strand Fiord Formation, the Sverdrup Basin, a salt diapir",
    "fossil": "a fossil bed or find: the Geodetic Hills forest, a Devonian fish from Ellesmere, the Miocene beaver pond",
    "mineral": "a mineral, ore or meteorite: the Cape York irons, native iron of Disko, coal at Bache Peninsula",
    "landform": "a form of the land surface: pingo, patterned ground, raised beach, ice-wedge polygon",
    "ice": "a kind of ice or ice event: ice shelf, ice island, glacier surge, sikuliaq, multiyear floe, polynya",
    "water": "the water column and the sea floor: sounding, water temperature, salinity, current, tide, wave",
    "weather": "a weather variable or phenomenon: air temperature, pressure, wind, fog, blizzard, parhelion",
    "sky": "the sky: aurora, the midnight sun, an eclipse, a comet, Venus in daylight",
    "field": "the magnetic field: declination, dip, the North Magnetic Pole, a magnetic storm",
    "phenomenon": "anything else that happens: mirage and looming, a rock fall, an earthquake felt",
}
DOMAINS = ("biology", "geology", "glaciology", "oceanography", "sea-ice", "meteorology", "astronomy",
           "geomagnetism", "hydrography", "freshwater")
TOPIC_DOMAINS = ("history", "nature")
METHODS = ("sighting", "hunt", "specimen", "transect", "aerial-survey", "camera", "acoustic", "edna",
           "catch-record", "testimony", "instrument", "sounding", "dredge", "trawl", "net", "trap", "core",
           "sample", "station-record", "survey", "satellite", "chart")
CONFIDENCE = ("", "certain", "probable", "doubtful")
ORIGINS = ("research", "ship", "crew")
# the kinds of places the natural half adds to the human half's vocabulary
PLACE_KINDS = ("community", "harbour", "cape", "strait", "site", "wreck", "station", "post", "island",
               "region", "port", "river", "bay", "lake", "sound", "channel", "range", "basin", "fiord",
               "glacier", "ice-cap", "ice-shelf", "ice-island", "polynya", "bird-cliff", "haul-out",
               "denning-area", "calving-ground", "fossil-site", "outcrop", "meteorite-fall", "hot-spring",
               "pingo", "ice-core-site", "tide-station", "magnetic-station", "weather-station")

RASTER_SUFFIXES = (".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp")
ROUTING = ("", "water", "as-given", "terrain")   # how a track's line is drawn: routed through water, as its
                                                 # waypoints, or routed over the terrain (tools/digitize-tracks.py)


def is_raster(name: str) -> bool:
    return str(name or "").lower().endswith(RASTER_SUFFIXES)


def connect(path: Path | None = None, create: bool = True) -> sqlite3.Connection:
    """Open the history database. Twenty researchers write at once, so every
    connection uses the write-ahead log and waits rather than failing."""
    p = Path(path or HISTORY_DB)
    if create:
        p.parent.mkdir(parents=True, exist_ok=True)
    elif not p.exists():
        raise FileNotFoundError(f"no history database at {p}")
    c = sqlite3.connect(p, timeout=60)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=60000")
    c.execute("PRAGMA foreign_keys=OFF")     # sources may arrive after the artifact citing them
    if create:
        c.executescript(SCHEMA)
        c.executescript(SCHEMA_EXTRA)
        c.executescript(SCHEMA_ANIMALS_VESSELS)
        c.executescript(SCHEMA_NATURE)
        if "kind" not in {r[1] for r in c.execute("PRAGMA table_info(faces)")}:
            c.execute("ALTER TABLE faces ADD COLUMN kind TEXT NOT NULL DEFAULT 'person'")
        if "status" not in {r[1] for r in c.execute("PRAGMA table_info(pages)")}:
            c.execute("ALTER TABLE pages ADD COLUMN status TEXT NOT NULL DEFAULT 'draft'")
        for table, col, default in (("sources", "language", "''"), ("sources", "orig_language", "''"),
                                    ("sources", "translator", "''"), ("artifacts", "language", "''"),
                                    ("pages", "language", "'en'"),
                                    ("artifacts", "view_file", "''"), ("artifacts", "routing", "''"),
                                    ("pages", "people", "'[]'"),
                                    ("sources", "rights_note", "''"), ("artifacts", "rights_note", "''"),
                                    ("vessels", "kind_note", "''"),
                                    ("topics", "domain", "'history'"), ("animals", "subject", "''")):
            if col not in {r[1] for r in c.execute(f"PRAGMA table_info({table})")}:
                c.execute(f"ALTER TABLE {table} ADD COLUMN {col} TEXT DEFAULT {default}")
        c.commit()
    return c


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(text: str, limit: int = 80) -> str:
    """A page slug: ASCII, lowercase, hyphens. Inuktitut and Norse spellings
    keep their letters' base forms rather than being dropped."""
    s = unicodedata.normalize("NFKD", str(text or ""))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace("ø", "o").replace("Ø", "o").replace("æ", "ae").replace("Æ", "ae")
    s = s.replace("ð", "d").replace("Ð", "d").replace("þ", "th").replace("Þ", "th")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:limit] or "untitled"


def page_slug(kind: str, name: str) -> str:
    """Where a thing's page lives. Narrative pages own the bare slug; the
    generated kinds are namespaced so a person and a place may share a name."""
    kind = kind if kind in KINDS else "page"
    return slugify(name) if kind == "page" else f"{kind}/{slugify(name)}"


def _json_list(v) -> str:
    if v is None or v == "":
        return "[]"
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
            return json.dumps(parsed if isinstance(parsed, list) else [parsed], ensure_ascii=False)
        except json.JSONDecodeError:
            return json.dumps([x.strip() for x in v.split(";") if x.strip()], ensure_ascii=False)
    return json.dumps(list(v), ensure_ascii=False)


def _tag_list(v) -> str:
    """Tags, stored one per element in the canonical form."""
    return json.dumps(normalise_tags(v), ensure_ascii=False)


def _iso(v: str) -> str:
    """The sortable form of a date written as a year, a month or a full date.
    A range ("1845/1848") yields its first date; anything unparseable is ''.

    Years BC are negative, and may run past four digits ("-35700"). Free text
    is read only for what it unambiguously says: "2500 BC" is -2500, "35,700
    years ago" or "35,700 BP" is counted back from 1950 (the radiocarbon
    convention), and a bare number inside other text is taken only when it is
    three or four digits and not part of a larger figure such as "35,700"."""
    s = str(v or "").strip().split("/")[0].strip()
    m = re.match(r"^(-\d{1,6}|\d{1,4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?$", s)
    if not m:
        num = r"(\d{1,3}(?:,\d{3})+|\d+)"
        bc = re.search(num + r"\s*(?:BC|BCE|B\.C\.?|B\.C\.E\.?)\b", s)
        if bc:
            return f"-{int(bc.group(1).replace(',', ''))}"
        bp = re.search(num + r"\s*(?:cal(?:ibrated)?\s*)?(?:years?\s+ago|yr\s*BP|BP|years?\s+BP|ka\b)", s, re.I)
        if bp:
            n = int(bp.group(1).replace(",", ""))
            if re.search(r"\bka\b", bp.group(0), re.I):
                n *= 1000
            y = 1950 - n
            return f"{y:04d}" if y > 0 else f"-{abs(y)}"
        m2 = re.search(r"(?<![\d.])(?<!\d,)(\d{3,4})(?!\d)(?!,\d{3})", s)
        return f"{int(m2.group(1)):04d}" if m2 else ""
    y, mo, d = m.group(1), m.group(2), m.group(3)
    out = f"{int(y):04d}" if not y.startswith("-") else y   # BC kept as written
    if mo:
        out += f"-{int(mo):02d}"
        if d:
            out += f"-{int(d):02d}"
    return out


def date_order(col: str) -> str:
    """An ORDER BY expression that puts ISO dates in calendar order even when
    some are BC: '-2500' before '-1900' before '0001'. Text order alone gets
    BC backwards, which the thule-dorset run noticed in its timeline."""
    # the year is everything before the next '-': four digits AD, up to six BC
    return (f"CASE WHEN substr({col},1,1)='-' THEN "
            f"-CAST(substr({col},2,instr(substr({col},2)||'-','-')-1) AS INTEGER) "
            f"ELSE CAST(substr({col},1,4) AS INTEGER) END, {col}")


PRECISIONS = ("day", "month", "season", "year", "decade", "century")
QUALIFIERS = ("", "circa", "before", "after", "by", "early", "mid", "late")
DATE_ROLES = ("point", "start", "end")


def date_display(d: str) -> str:
    """A date as a reader should see it: negative ISO years read as BC."""
    if d.startswith("-"):
        y = d.lstrip("-").split("-")[0]
        return f"{int(y)} BC"
    return d


def date_precision(raw: str) -> str:
    """How much of a date the source actually gives, read off its shape."""
    s = _iso(raw)
    if not s:
        return "year"
    parts = s.lstrip("-").split("-")
    if len(parts) >= 3:
        return "day"
    if len(parts) == 2:
        return "month"
    return "decade" if s.endswith("0") and re.search(r"\bs\b|s$", str(raw)) else "year"


def add_date(c, entity_kind: str, entity_id: str, date: str, **kw) -> int:
    """Record one atomic date. Call it once per date a source gives, rather
    than folding a range into a single row: a range is two calls, ``role``
    'start' and 'end', sharing a ``span``."""
    iso = _iso(date)
    if not iso:
        raise ValueError(f"unparseable date: {date!r}")
    prec = kw.get("precision") or date_precision(date)
    if prec not in PRECISIONS:
        raise ValueError(f"precision must be one of {', '.join(PRECISIONS)}")
    role = kw.get("role", "point")
    if role not in DATE_ROLES:
        raise ValueError(f"role must be one of {', '.join(DATE_ROLES)}")
    qual = kw.get("qualifier", "") or ""
    if qual not in QUALIFIERS:
        raise ValueError("qualifier must be one of " + ", ".join(q or "(none)" for q in QUALIFIERS))
    row = {"entity_kind": entity_kind, "entity_id": str(entity_id), "date": iso,
           "topic": slugify(kw["topic"]) if kw.get("topic") else "", "precision": prec,
           "qualifier": qual, "role": role, "span": kw.get("span", "") or "",
           "label": kw.get("label", "") or "", "place": kw.get("place", "") or "",
           "bibkey": kw.get("bibkey", "") or "", "updated": now(),
           "lat": None if kw.get("lat") in (None, "") else float(kw["lat"]),
           "lon": None if kw.get("lon") in (None, "") else float(kw["lon"])}
    cols = ",".join(row)
    c.execute(f"INSERT INTO dates ({cols}) VALUES ({','.join('?' * len(row))}) "
              f"ON CONFLICT (entity_kind, entity_id, date, role, label) DO UPDATE SET "
              + ",".join(f"{k}=excluded.{k}" for k in row if k not in
                         ("entity_kind", "entity_id", "date", "role", "label")),
              tuple(row.values()))
    c.commit()
    r = c.execute("SELECT id FROM dates WHERE entity_kind=? AND entity_id=? AND date=? AND role=? AND label=?",
                  (row["entity_kind"], row["entity_id"], iso, role, row["label"])).fetchone()
    return int(r["id"])


def span_dates(c, entity_kind: str, entity_id: str, start: str, end: str, **kw) -> list[int]:
    """A range, as its two atomic endpoints sharing one span name. Each end
    keeps its own precision — a day-precise departure does not lend day
    precision to a month-precise return — unless one is stated for both."""
    span = kw.pop("span", None) or f"{entity_id}:{_iso(start)}"
    label = kw.pop("label", "")
    start_label = kw.pop("start_label", label)
    end_label = kw.pop("end_label", label)
    prec = kw.pop("precision", None)
    end_prec = kw.pop("end_precision", None) or prec
    out = [add_date(c, entity_kind, entity_id, start, role="start", span=span, label=start_label,
                    precision=prec, **kw)]
    if end:
        out.append(add_date(c, entity_kind, entity_id, end, role="end", span=span, label=end_label,
                            precision=end_prec, **kw))
    return out


def _upsert(c: sqlite3.Connection, table: str, key: str, row: dict) -> str:
    row = {k: v for k, v in row.items() if v is not None}
    row["updated"] = now()
    cols = ",".join(row)
    marks = ",".join("?" * len(row))
    sets = ",".join(f"{k}=excluded.{k}" for k in row if k != key)
    c.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks}) "
              f"ON CONFLICT({key}) DO UPDATE SET {sets}", tuple(row.values()))
    c.commit()
    return str(row[key])


# ------------------------------------------------- licensed-platform pacing
PLATFORM_GAP = 3600      # seconds between download sessions on one platform


def platform_session_gate(ledger: Path, platform: str, now_ts: float, gap: int = PLATFORM_GAP) -> float:
    """How long (seconds) until `platform` may be used again; 0 means go, and
    the ledger is stamped. Every researcher shares one ledger, so the rule the
    person set — one download session per platform per hour — holds across
    the whole crew, not per run."""
    ledger.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(ledger.read_text())
    except (OSError, ValueError):
        data = {}
    if platform in data:
        wait = float(data[platform]) + gap - now_ts
        if wait > 0:
            return wait
    data[platform] = now_ts
    ledger.write_text(json.dumps(data, indent=1))
    return 0.0


def platform_session_release(ledger: Path, platform: str, previous: float | None) -> None:
    """Undo a stamp when the platform refused and nothing was downloaded."""
    try:
        data = json.loads(ledger.read_text())
    except (OSError, ValueError):
        return
    if previous is None:
        data.pop(platform, None)
    else:
        data[platform] = previous
    ledger.write_text(json.dumps(data, indent=1))


# ---------------------------------------------------------------- writers
def add_topic(c, slug: str, title: str | None = None, **kw) -> str:
    """Declare a topic, or update the fields given. A later call that only
    sets --status must not blank the title or the summary: two runs lost
    their summaries that way before this guard."""
    row = {"slug": slugify(slug)}
    if title:
        row["title"] = title
    for f in ("summary", "researcher", "status", "domain"):
        if kw.get(f) not in (None, ""):
            row[f] = kw[f]
    if row.get("domain", "history") not in TOPIC_DOMAINS:
        raise ValueError(f"a topic's domain is one of {', '.join(TOPIC_DOMAINS)}")
    exists = c.execute("SELECT 1 FROM topics WHERE slug=?", (row["slug"],)).fetchone()
    if exists:
        # a plain UPDATE: an upsert's INSERT half would trip the NOT NULL title
        fields = {k: v for k, v in row.items() if k != "slug"}
        if fields:
            sets = ",".join(f"{k}=?" for k in fields) + ",updated=?"
            c.execute(f"UPDATE topics SET {sets} WHERE slug=?", (*fields.values(), now(), row["slug"]))
            c.commit()
        return row["slug"]
    if "title" not in row:
        raise ValueError(f"new topic {row['slug']!r} needs a title")
    row.setdefault("summary", "")
    row.setdefault("researcher", "")
    row.setdefault("status", "open")
    row.setdefault("domain", "history")
    return _upsert(c, "topics", "slug", row)


def add_source(c, bibkey: str, title: str, **kw) -> str:
    key = re.sub(r"[^a-z0-9]", "", str(bibkey).lower()) or slugify(title).replace("-", "")
    row = {"bibkey": key, "title": title, "entry_type": entry_type_code(kw.get("entry_type", "misc"))}
    for f in ("author", "year", "container", "publisher", "address", "volume", "pages", "url",
              "urldate", "doi", "archive", "callno", "licence", "rights_note", "note", "local_file", "topic",
              "language", "orig_language", "translator"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    _check_licence(row.get("licence", ""))
    if row.get("archive"):
        row["archive"] = canonical_archive(row["archive"])
    row["primary_src"] = 1 if kw.get("primary") else 0
    return _upsert(c, "sources", "bibkey", row)


def add_artifact(c, id: str, topic: str, type: str, title: str, **kw) -> str:
    if type not in ARTIFACT_TYPES:
        raise ValueError(f"artifact type must be one of {', '.join(ARTIFACT_TYPES)}, not {type!r}")
    if not kw.get("credit"):
        raise ValueError("every artifact needs a credit line")
    if not kw.get("bibkey"):
        raise ValueError("every artifact needs a bibkey naming its source")
    date_text = str(kw.get("date", kw.get("date_text", "")) or "")
    row = {"id": str(id).strip(), "topic": slugify(topic), "type": type, "title": title,
           "date_text": date_text,
           "date_start": _iso(kw.get("date_start") or date_text),
           "date_end": _iso(kw.get("date_end") or (date_text.split("/")[-1] if "/" in date_text else "")),
           "people": _json_list(kw.get("people")), "tags": _tag_list(kw.get("tags")),
           "lat": None if kw.get("lat") in (None, "") else float(kw["lat"]),
           "lon": None if kw.get("lon") in (None, "") else float(kw["lon"])}
    for f in ("creator", "description", "source_url", "download_url", "local_file",
              "licence", "rights_note", "credit", "bibkey", "pages", "language", "view_file", "routing"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    _check_licence(row.get("licence", ""))
    if row.get("routing", "") not in ROUTING:
        raise ValueError(f"routing must be one of {', '.join(repr(x) for x in ROUTING)}")
    for f in ("geometry", "waypoints"):
        v = kw.get(f)
        if v not in (None, ""):
            row[f] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    if row["lat"] is not None and not -90 <= row["lat"] <= 90:
        raise ValueError(f"latitude out of range: {row['lat']}")
    if row["lon"] is not None and not -180 <= row["lon"] <= 180:
        raise ValueError(f"longitude out of range: {row['lon']}")
    prev = c.execute("SELECT * FROM artifacts WHERE id=?", (row["id"],)).fetchone()
    if prev is not None:
        # a re-run merges: a field not passed keeps what the row holds, and an
        # explicit "" clears it.  The strings are merged by _upsert, which
        # skips None; the dates, people and tags are built above from nothing
        # and are merged here, so a run that passes only the field it changes
        # leaves the rest of the row as it was
        if kw.get("date") is None and kw.get("date_text") is None:
            row["date_text"], row["date_start"] = prev["date_text"], prev["date_start"]
            row["date_end"] = _iso(kw["date_end"]) if kw.get("date_end") is not None else prev["date_end"]
        if kw.get("people") is None:
            row["people"] = prev["people"]
        if kw.get("tags") is None:
            row["tags"] = prev["tags"]
        if row["lat"] is None and kw.get("lat") is None:
            row["lat"], row["lon"] = prev["lat"], prev["lon"]
    if row["lat"] is None and not row.get("geometry") and not (prev is not None and prev["geometry"]):
        raise ValueError("an artifact needs a lat/lon, or a geometry if it is a track")
    if prev is not None and artifact_changes(dict(prev), row):
        # the replaced version is kept, with the message that explains the change
        c.execute("INSERT INTO artifact_history (artifact_id, row, message, who, saved) VALUES (?,?,?,?,?)",
                  (row["id"], json.dumps(dict(prev), ensure_ascii=False),
                   str(kw.get("message") or ""), str(kw.get("who") or ""), now()))
    out = _upsert(c, "artifacts", "id", row)
    _record_dates(c, "artifact", out, row["date_start"], row["date_end"], date_text,
                  old=dict(prev) if prev else None,
                  topic=row["topic"], label=title, lat=row["lat"], lon=row["lon"],
                  bibkey=row.get("bibkey", ""))
    return out


def artifact_changes(before: dict, after: dict) -> list:
    """The fields whose stored value `after` changes, ignoring the timestamp
    and fields it does not set."""
    return [k for k, v in after.items()
            if k != "updated" and v is not None and k in before and before[k] != v]


def artifact_versions(c, artifact_id: str) -> list:
    """An artifact's saved versions, oldest first, each with the fields the
    next version changed: the row as JSON, the message, who, when."""
    rows = [dict(r) for r in c.execute("SELECT * FROM artifact_history WHERE artifact_id=? ORDER BY id",
                                       (artifact_id,))]
    cur = c.execute("SELECT * FROM artifacts WHERE id=?", (artifact_id,)).fetchone()
    out = []
    for i, r in enumerate(rows):
        this = json.loads(r["row"])
        nxt = json.loads(rows[i + 1]["row"]) if i + 1 < len(rows) else (dict(cur) if cur else {})
        out.append(dict(id=r["id"], saved=r["saved"], message=r["message"], who=r["who"], row=this,
                        changed=artifact_changes(this, nxt)))
    return out


def _record_dates(c, kind: str, ident: str, start: str, end: str, raw: str = "",
                  old: dict | None = None, **kw) -> None:
    """Put a record's own dates into the ``dates`` table, one row each, so the
    timeline reads from one place. A record with an end date is a time-limited
    activity and gets a start/end pair sharing a span; anything else is a
    single point.

    ``old`` is the record as it stood before this write: the rows its previous
    date and title created are deleted first, so re-dating a record replaces
    its timeline entry instead of leaving the stale one beside it. Dates
    attached separately with ``add_date`` are not touched."""
    if old and old.get("date_start"):
        if old.get("date_end") and old["date_end"] != old["date_start"]:
            c.execute("DELETE FROM dates WHERE entity_kind=? AND entity_id=? AND span=?",
                      (kind, str(ident), f"{ident}:{old['date_start']}"))
        else:
            c.execute("DELETE FROM dates WHERE entity_kind=? AND entity_id=? AND role='point' "
                      "AND span='' AND date=? AND label=?",
                      (kind, str(ident), old["date_start"], old.get("title", "")))
        c.commit()
    if not start:
        return
    if end and end != start:
        # each endpoint reads its precision off its own shape
        span_dates(c, kind, ident, start, end, precision=date_precision(start),
                   end_precision=date_precision(end), **kw)
    else:
        add_date(c, kind, ident, start, precision=date_precision(raw or start), role="point", **kw)


def forget(c, kind: str, ident) -> dict:
    """Delete one mistaken row, and the date rows attached to it: a duplicate
    person, an artifact entered under the wrong id, a stray date. For errors,
    not revisions — a change of content is a re-run of the writer, which
    replaces. Say what you removed and why in the worklog."""
    if kind == "date":
        r = c.execute("SELECT * FROM dates WHERE id=?", (int(ident),)).fetchone()
        if not r:
            raise ValueError(f"no date row {ident}")
        c.execute("DELETE FROM dates WHERE id=?", (int(ident),))
        c.commit()
        return {"deleted": f"date {ident} ({r['date']} {r['role']} {r['label']})", "dates": 1}
    tables = {"artifact": ("artifacts", "id"), "event": ("events", "id"),
              "person": ("people", "name"), "place": ("places", "name"),
              "animal": ("animals", "name"), "vessel": ("vessels", "name"),
              "source": ("sources", "bibkey"), "subject": ("subjects", "name"),
              "observation": ("observations", "id")}
    if kind not in tables:
        raise ValueError(f"kind must be date or one of {', '.join(tables)}")
    table, key = tables[kind]
    r = c.execute(f"SELECT * FROM {table} WHERE {key}=?", (ident,)).fetchone()
    if not r:
        raise ValueError(f"no {kind} {ident!r}")
    if kind == "source":
        users = [t for t in ("artifacts", "events", "people", "places", "observations", "subjects")
                 if c.execute(f"SELECT 1 FROM {t} WHERE bibkey=? LIMIT 1", (ident,)).fetchone()]
        if users:
            raise ValueError(f"source {ident!r} is still cited by rows in {', '.join(users)}; re-point them first")
    if kind == "subject":
        n_obs = c.execute("SELECT COUNT(*) AS n FROM observations WHERE subject=?", (ident,)).fetchone()["n"]
        if n_obs:
            raise ValueError(f"subject {ident!r} has {n_obs} observation(s); re-point or forget them first")
    n = c.execute("DELETE FROM dates WHERE entity_kind=? AND entity_id=?", (kind, str(ident))).rowcount
    c.execute(f"DELETE FROM {table} WHERE {key}=?", (ident,))
    c.commit()
    return {"deleted": f"{kind} {ident}", "dates": n}


PAGE_STATUS = ("draft", "good")


def add_page(c, slug: str, title: str, body: str, **kw) -> str:
    """Write or replace a page. Pages are drafts unless said otherwise, and
    every replacement keeps the version it overwrote in page_history — so a
    rough page now beats a perfect page never."""
    kind = kw.get("kind", "page")
    s = page_slug(kind, slug) if kind != "page" else slugify(slug)
    old = c.execute("SELECT * FROM pages WHERE slug=?", (s,)).fetchone()
    status = kw.get("status") or (old["status"] if old else "draft")
    if status not in PAGE_STATUS:
        raise ValueError(f"status must be one of {', '.join(PAGE_STATUS)}")
    # a re-run keeps the summary and the ordering it does not pass, as the
    # artifact writer does; an explicit "" clears the summary
    summary = kw.get("summary")
    if summary is None:
        summary = old["summary"] if old else ""
    ordering = kw.get("ordering")
    if ordering is None:
        ordering = old["ordering"] if old else 100
    if old and (old["body"] != body or old["title"] != title or old["summary"] != summary):
        c.execute("INSERT INTO page_history (slug, title, summary, body, status, saved) "
                  "VALUES (?,?,?,?,?,?)",
                  (s, old["title"], old["summary"], old["body"], old["status"], now()))
    row = {"slug": s, "kind": kind if kind in KINDS else "page", "title": title, "body": body,
           "topic": slugify(kw["topic"]) if kw.get("topic") else "",
           "summary": summary, "ordering": int(ordering), "status": status,
           "people": _json_list(kw["people"]) if kw.get("people") is not None
                     else (old["people"] if old else "[]")}
    return _upsert(c, "pages", "slug", row)


def _keep_home_topic(c, table: str, name: str, kw: dict) -> dict:
    """People and places belong to the topic that first entered them. A later
    run from another topic enriches the row without moving it — Tulluahiu is
    not stolen from inuit-oral-history by a ross-victory re-run. To really
    reassign, `forget` the row and re-enter it."""
    if kw.get("topic"):
        old = c.execute(f"SELECT * FROM {table} WHERE name=?", (name.strip(),)).fetchone()
        if old and old["topic"] and old["topic"] != slugify(kw["topic"]):
            # enrich only: a foreign run fills fields the home topic left
            # empty and touches nothing else. Robert Bartlett, master of the
            # Roosevelt, was once rewritten as a schooner captain at Frobisher
            # Bay by a south-Baffin run that did not check first.
            kw = {k: v for k, v in kw.items()
                  if k != "topic" and (k not in old.keys() or old[k] in (None, ""))}
    return kw


def add_person(c, name: str, **kw) -> str:
    kw = _keep_home_topic(c, "people", name, kw)
    # the flag is set by any run and unset by none: an enriching re-run
    # without --indigenous must not quietly clear it
    old = c.execute("SELECT indigenous FROM people WHERE name=?", (name.strip(),)).fetchone()
    row = {"name": name.strip(),
           # an explicit True or False sets the flag; not passing it keeps the row's
           "indigenous": (1 if kw["indigenous"] else 0) if kw.get("indigenous") is not None
                         else (old["indigenous"] if old else 0)}
    for f in ("also", "role", "born", "died", "affiliation", "note", "bibkey", "topic"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    return _upsert(c, "people", "name", row)


def add_place(c, name: str, **kw) -> str:
    kw = _keep_home_topic(c, "places", name, kw)
    row = {"name": name.strip(),
           "lat": None if kw.get("lat") in (None, "") else float(kw["lat"]),
           "lon": None if kw.get("lon") in (None, "") else float(kw["lon"])}
    for f in ("historic", "inuktitut", "kind", "note", "bibkey", "topic"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    return _upsert(c, "places", "name", row)


def add_animal(c, name: str, **kw) -> str:
    """A named animal — a dog, a pony, a ship's cat, a bear cub. Like people:
    the topic that first entered it keeps it, later runs fill blanks."""
    kw = _keep_home_topic(c, "animals", name, kw)
    row = {"name": name.strip()}
    for f in ("kind", "also", "role", "born", "died", "affiliation", "note", "bibkey", "topic", "subject"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    if row.get("subject"):
        row["subject"] = resolve_subject(c, row["subject"]) or row["subject"]
    return _upsert(c, "animals", "name", row)


def add_vessel(c, name: str, **kw) -> str:
    """A ship, boat or aircraft, by the name it is usually written under."""
    kw = _keep_home_topic(c, "vessels", name, kw)
    row = {"name": name.strip()}
    for f in ("kind", "kind_note", "also", "role", "built", "lost", "affiliation", "tonnage",
              "note", "bibkey", "topic"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    _check_vessel_kind(row.get("kind", ""))
    return _upsert(c, "vessels", "name", row)


# ---------------------------------------------------------------- the natural half
def resolve_subject(c, name: str) -> str:
    """The subjects.name behind any of a subject's names: the scientific or
    technical name itself, or its English, French, Inuktitut or Kalaallisut
    name, or a synonym in ``also``. '' when nothing matches."""
    n = (name or "").strip()
    if not n:
        return ""
    r = c.execute("SELECT name FROM subjects WHERE name=? COLLATE NOCASE", (n,)).fetchone()
    if r:
        return r["name"]
    for col in ("english", "french", "inuktitut", "kalaallisut"):
        r = c.execute(f"SELECT name FROM subjects WHERE {col}=? COLLATE NOCASE", (n,)).fetchone()
        if r:
            return r["name"]
    low = n.lower()
    for r in c.execute("SELECT name, also FROM subjects WHERE also<>''"):
        if low in [x.strip().lower() for x in r["also"].split(";")]:
            return r["name"]
    return ""


def add_subject(c, name: str, **kw) -> str:
    """A subject of observation: a taxon, a rock unit, a kind of ice, a
    variable, a thing in the sky. Like people: the topic that first entered
    it keeps it, later runs fill blanks. ``kind`` and ``domain`` are codes."""
    kw = _keep_home_topic(c, "subjects", name, kw)
    row = {"name": name.strip()}
    for f in ("kind", "domain", "rank", "parent", "english", "french", "inuktitut", "kalaallisut",
              "also", "unit", "status", "backbone_id", "note", "bibkey", "topic"):
        if kw.get(f) is not None:
            row[f] = str(kw[f]).strip()
    old = c.execute("SELECT kind, domain FROM subjects WHERE name=?", (row["name"],)).fetchone()
    kind = row.get("kind") or (old["kind"] if old else "")
    domain = row.get("domain") or (old["domain"] if old else "")
    if kind not in SUBJECT_KINDS:
        raise ValueError(f"a subject's kind is a code: {', '.join(SUBJECT_KINDS)}")
    if domain not in DOMAINS:
        raise ValueError(f"a subject's domain is a code: {', '.join(DOMAINS)}")
    if row.get("parent"):
        row["parent"] = resolve_subject(c, row["parent"]) or row["parent"]
    return _upsert(c, "subjects", "name", row)


def add_observation(c, id: str, topic: str, subject: str, **kw) -> str:
    """One observation of nature: a subject, a date, a position, a source,
    and the number as written. Refused without a subject that exists, a
    date, a position or a place, and a bibkey — as an artifact is refused
    without a credit. A variable (a subject with a unit) wants a value."""
    ident = str(id).strip()
    if not ident:
        raise ValueError("an observation needs an id: <topic>-<nnn>, or amundsen-<date>-<nnn> from the ship")
    name = resolve_subject(c, subject)
    if not name:
        raise ValueError(f"no subject {subject!r}: enter it with `subject` first (any of its names resolves)")
    if not kw.get("bibkey"):
        raise ValueError("every observation cites a bibkey")
    date_text = str(kw.get("date", kw.get("date_text", "")) or "")
    row = {"id": ident, "topic": slugify(topic), "subject": name, "date_text": date_text,
           "date_start": _iso(kw.get("date_start") or date_text),
           "date_end": _iso(kw.get("date_end") or (date_text.split("/")[-1] if "/" in date_text else "")),
           "tags": _tag_list(kw.get("tags")),
           "sensitive": 1 if kw.get("sensitive") else 0,
           "origin": kw.get("origin") or "research"}
    if not row["date_start"]:
        raise ValueError(f"an observation needs a date; {date_text!r} is not one")
    for f in ("lat", "lon", "depth", "height", "value"):
        row[f] = None if kw.get(f) in (None, "") else float(kw[f])
    for f in ("place", "unit", "count", "qualifier", "stage", "sex", "behaviour", "method", "instrument",
              "observer", "vessel", "detail", "confidence", "artifact_id", "bibkey", "pages"):
        if kw.get(f) is not None:
            row[f] = str(kw[f]).strip()
    if kw.get("event_id") not in (None, ""):
        row["event_id"] = int(kw["event_id"])
    if row.get("place") and (row["lat"] is None or row["lon"] is None):
        pl = c.execute("SELECT lat, lon FROM places WHERE name=?", (row["place"],)).fetchone()
        if pl and pl["lat"] is not None:
            row["lat"], row["lon"] = pl["lat"], pl["lon"]
    if row["lat"] is None or row["lon"] is None:
        if not row.get("place"):
            raise ValueError("an observation needs a lat/lon, or a place that has one")
        if not c.execute("SELECT 1 FROM places WHERE name=?", (row["place"],)).fetchone():
            raise ValueError(f"no place {row['place']!r} to take a position from: enter it, or give --lat/--lon")
    if row["lat"] is not None and not -90 <= row["lat"] <= 90:
        raise ValueError(f"latitude out of range: {row['lat']}")
    if row["lon"] is not None and not -180 <= row["lon"] <= 180:
        raise ValueError(f"longitude out of range: {row['lon']}")
    if row.get("method", "") not in METHODS:
        raise ValueError(f"method is a code: {', '.join(METHODS)}")
    if row.get("confidence", "") not in CONFIDENCE:
        raise ValueError("confidence is certain, probable or doubtful")
    if row["origin"] not in ORIGINS:
        raise ValueError(f"origin is one of {', '.join(ORIGINS)}")
    if not row.get("detail"):
        raise ValueError("an observation needs a detail: the sentence saying what was seen, naming the observer")
    subj = c.execute("SELECT unit FROM subjects WHERE name=?", (name,)).fetchone()
    if subj["unit"] and row.get("value") is None and not row.get("qualifier"):
        raise ValueError(f"{name} is a variable in {subj['unit']}: give --value (and --unit as written), "
                         "or a --qualifier saying why there is no number")
    if row.get("value") is not None and not row.get("unit"):
        raise ValueError("a value needs its unit, as written in the source")
    prev = c.execute("SELECT date_start, date_end FROM observations WHERE id=?", (ident,)).fetchone()
    out = _upsert(c, "observations", "id", row)
    label = _observation_label(row)
    _record_dates(c, "observation", out, row["date_start"], row["date_end"], date_text,
                  old={**dict(prev), "title": _observation_label(dict(prev, **{k: row[k] for k in row if k not in prev.keys()}))} if prev else None,
                  topic=row["topic"], label=label, lat=row["lat"], lon=row["lon"],
                  place=row.get("place", ""), bibkey=row["bibkey"])
    return out


def _observation_label(row: dict) -> str:
    """What the timeline shows for an observation: the subject, the number
    or count, the qualifier."""
    bits = [row.get("subject", "")]
    if row.get("value") is not None:
        bits.append(f"{row['value']:g} {row.get('unit', '')}".strip())
    elif row.get("count"):
        bits.append(str(row["count"]))
    if row.get("qualifier"):
        bits.append(row["qualifier"])
    return ", ".join(b for b in bits if b)


def coarsen(lat, lon, step: float = 0.5):
    """A sensitive site's published position: rounded to the grid."""
    if lat is None or lon is None:
        return lat, lon
    return round(round(lat / step) * step, 2), round(round(lon / step) * step, 2)


def ingest_journal(c, path: Path, who: str = "ship") -> dict:
    """The ship's journal: one JSON object per line, in the CLI's own
    vocabulary, appended aboard and rsynced up. Each line becomes a row
    through the same writers as everything else, so the brief's rules apply;
    idempotent on id, so a corrected line replaces the row. A line that fails
    is reported, not dropped silently, and the rest go in."""
    done, failed = [], []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            d = json.loads(line)
            kind = d.pop("kind", "observation")
            if kind == "subject":
                name = d.pop("name")
                d.setdefault("topic", JOURNAL_TOPIC)
                done.append(("subject", add_subject(c, name, **d)))
                continue
            if kind != "observation":
                raise ValueError(f"unknown journal kind {kind!r}")
            ident = d.pop("id")
            subject = d.pop("subject")
            topic = d.pop("topic", JOURNAL_TOPIC)
            d.setdefault("origin", "ship")
            d.setdefault("bibkey", JOURNAL_BIBKEY)
            date = d.pop("date", d.pop("date_text", ""))
            image = d.pop("artifact_file", "")
            if not c.execute("SELECT 1 FROM topics WHERE slug=?", (slugify(topic),)).fetchone():
                add_topic(c, topic, "The ship's journal", domain="nature",
                          summary="What the Amundsen's own people saw and measured, entered aboard")
            if d["bibkey"] == JOURNAL_BIBKEY and not c.execute(
                    "SELECT 1 FROM sources WHERE bibkey=?", (JOURNAL_BIBKEY,)).fetchone():
                add_source(c, JOURNAL_BIBKEY, "CCGS Amundsen natural-history journal", entry_type="dataset",
                           author="the ship's company", year=str(datetime.now().year), licence="attribution",
                           url="https://github.com/rec3141/arctic-history", topic=topic,
                           rights_note="entered aboard by the crew and the resident scientist; credit the observer named")
            if image:
                image = _journal_file(Path(path), image)
                photographer = d.get("observer", "the ship's company")
                add_artifact(c, f"{ident}-img", topic, "image", f"{subject}, {date}",
                             date=date, lat=d.get("lat"), lon=d.get("lon"), local_file=image,
                             credit=f"Photograph: {photographer}, CCGS Amundsen", licence=d.pop("licence", "attribution"),
                             bibkey=d["bibkey"], description=d.get("detail", ""), tags=d.get("tags", ""),
                             people=[photographer] if c.execute("SELECT 1 FROM people WHERE name=?", (photographer,)).fetchone() else [])
                d.setdefault("artifact_id", f"{ident}-img")
            done.append(("observation", add_observation(c, ident, topic, subject, date=date, **d)))
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            failed.append({"line": n, "error": f"{type(e).__name__}: {e}", "text": line[:200]})
    if done:
        add_worklog(c, JOURNAL_TOPIC, f"journal ingest: {len(done)} line(s) from {Path(path).name}"
                    + (f"; {len(failed)} failed" if failed else ""), who=who)
    return {"done": done, "failed": failed}


def _journal_file(journal: Path, rel: str) -> str:
    """Where a journal line's photograph is on grid. Aboard, the line says
    `_journal/img/<name>`; push-journal lands the whole directory under
    `_journal/incoming/`, so the path is resolved against the journal file's
    own directory and returned relative to db/history/. A photograph that is
    not there fails the line rather than registering a dangling artifact."""
    rel = str(rel).strip()
    tail = rel.split("_journal/", 1)[1] if "_journal/" in rel else rel
    base = Path(journal).resolve().parent
    for candidate in (base / tail, HISTORY_DIR / rel, Path(rel)):
        if candidate.is_file():
            try:
                return str(candidate.resolve().relative_to(HISTORY_DIR.resolve()))
            except ValueError:
                return str(candidate)
    raise ValueError(f"photograph {rel!r} not found beside the journal ({base / tail})")


JOURNAL_TOPIC = "ship-journal"
JOURNAL_BIBKEY = "amundsenjournal"


def add_event(c, topic: str, date: str, title: str, **kw) -> int:
    row = {"topic": slugify(topic), "date_text": str(date), "date_start": _iso(date),
           "date_end": _iso(kw.get("date_end", "")), "title": title,
           "detail": kw.get("detail", ""), "place": kw.get("place", ""),
           "bibkey": kw.get("bibkey", ""), "people": _json_list(kw.get("people")),
           "tags": _tag_list(kw.get("tags")), "updated": now(),
           "lat": None if kw.get("lat") in (None, "") else float(kw["lat"]),
           "lon": None if kw.get("lon") in (None, "") else float(kw["lon"])}
    if not row["date_start"]:
        raise ValueError(f"unparseable event date: {date!r}")
    # an event is identified by its topic, date and title, so a re-run updates
    # rather than piling up duplicates
    old = c.execute("SELECT id, date_start, date_end FROM events WHERE topic=? AND date_start=? AND title=?",
                    (row["topic"], row["date_start"], title)).fetchone()
    if old:
        sets = ",".join(f"{k}=?" for k in row)
        c.execute(f"UPDATE events SET {sets} WHERE id=?", (*row.values(), old["id"]))
        c.commit()
        ident = int(old["id"])
    else:
        cols = ",".join(row)
        c.execute(f"INSERT INTO events ({cols}) VALUES ({','.join('?' * len(row))})", tuple(row.values()))
        c.commit()
        ident = int(c.execute("SELECT last_insert_rowid() AS i").fetchone()["i"])
    _record_dates(c, "event", str(ident), row["date_start"], row["date_end"], row["date_text"],
                  old={**dict(old), "title": title} if old else None,
                  topic=row["topic"], label=title, lat=row["lat"], lon=row["lon"],
                  place=row["place"], bibkey=row["bibkey"])
    return ident


def add_worklog(c, topic: str, done: str, next: str = "", open: str = "", who: str = "") -> int:
    c.execute("INSERT INTO worklog (topic, at, who, done, next, open) VALUES (?,?,?,?,?,?)",
              (slugify(topic), now(), who, done.strip(), next.strip(), open.strip()))
    c.commit()
    return int(c.execute("SELECT last_insert_rowid() AS i").fetchone()["i"])


REQUEST_KINDS = ("download", "api_key", "question", "access", "other")
REQUEST_STATUS = ("open", "approved", "denied", "done")


_STRUCTURAL = re.compile(r"^\s*(?:[-*\u2022]|\d{1,3}[.)]|\(?[a-z0-9]\)|[A-Z][A-Za-z ,/]{0,40}:)(?:\s|$)")
_BARE_URL = re.compile(r"^\s*<?https?://\S+>?\s*$")


def unwrap_hard_wraps(text: str) -> str:
    """Researchers often type a request through a shell heredoc wrapped at
    80 columns, and the review page then shows it as ragged short lines.
    Join the lines of a paragraph back into prose; keep blank-line paragraph
    breaks, list items, 'Label:' lines, salutations and bare URLs on their
    own lines."""
    if not text or "\n" not in text:
        return text
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    paras = []
    for para in re.split(r"\n[ \t]*\n", text):
        joined: list[str] = []
        for line in para.split("\n"):
            line = line.rstrip()
            if not line.strip():
                continue
            prev = joined[-1] if joined else None
            structural = bool(_STRUCTURAL.match(line)) or _BARE_URL.match(line)
            can_join = (prev is not None and not structural and len(prev) >= 50
                        and not prev.rstrip().endswith(":") and not _BARE_URL.match(prev))
            if can_join:
                joined[-1] = prev + " " + line.strip()
            else:
                joined.append(line)
        paras.append("\n".join(joined))
    return "\n\n".join(p for p in paras if p)


def add_request(c, topic: str, kind: str, what: str, **kw) -> int:
    """File a request for a person and carry on: requests are asynchronous by
    design. The person acts on it alone, from the review page, possibly days
    later — so a request must carry everything they need: what to do, where
    (the exact URL, title, edition, volume), why the topic needs it, why it
    needs a person at all (what was tried, and what only a person can do),
    and what will be done with the answer. A person who has to ask a
    follow-up question is answering a bad request."""
    if kind not in REQUEST_KINDS:
        raise ValueError(f"kind must be one of {', '.join(REQUEST_KINDS)}")
    # a literal backslash-n typed inside a shell argument is the line break
    # the researcher meant; the review page showed a lot of them
    def _nl(v):
        if not isinstance(v, str):
            return v
        return unwrap_hard_wraps(v.replace("\\r\\n", "\n").replace("\\n", "\n"))
    what = _nl(what)
    kw = {k: _nl(v) for k, v in kw.items()}
    if len(kw.get("why", "").strip()) < 40:
        raise ValueError(
            "a request needs a real `why`: the person acting on it works alone, later, "
            "from the review page. Say why the topic needs it, why it needs a person at "
            "all (what you tried and what only they can do), exactly where to get it "
            "(URL, title, edition, volume, account to create, the request form), and "
            "what you will do with the answer — not 'get me an API key' but which key, "
            "from which page, and what it unlocks. If they must write to someone, find "
            "the address on the holder's own pages and draft the email for them")
    if kind in ("download", "access") and not kw.get("url", "").strip():
        raise ValueError(f"a {kind} request needs --url: the exact page the person should start from")
    size = kw.get("size_mb")
    c.execute("INSERT INTO requests (topic, kind, what, why, url, size_mb, dest, who, created) "
              "VALUES (?,?,?,?,?,?,?,?,?)",
              (slugify(topic), kind, what.strip(), kw.get("why", ""), kw.get("url", ""),
               None if size in (None, "") else float(size), kw.get("dest", ""), kw.get("who", ""), now()))
    c.commit()
    return int(c.execute("SELECT last_insert_rowid() AS i").fetchone()["i"])


def answer_request(c, ident: int, status: str, answer: str = "") -> dict:
    if status not in REQUEST_STATUS:
        raise ValueError(f"status must be one of {', '.join(REQUEST_STATUS)}")
    c.execute("UPDATE requests SET status=?, answer=?, resolved=? WHERE id=?",
              (status, answer.strip(), now() if status != "open" else "", int(ident)))
    c.commit()
    r = c.execute("SELECT * FROM requests WHERE id=?", (int(ident),)).fetchone()
    if not r:
        raise ValueError(f"no request {ident}")
    return dict(r)


def list_requests(c, status: str | None = None, topic: str | None = None) -> list[dict]:
    q, args = "SELECT * FROM requests WHERE 1=1", []
    if status:
        q += " AND status=?"
        args.append(status)
    if topic:
        q += " AND topic=?"
        args.append(slugify(topic))
    return [dict(r) for r in c.execute(q + " ORDER BY id DESC", tuple(args))]


def resume_state(c, topic: str) -> dict:
    """Everything a run needs to carry a topic on: what the database holds for
    it, the files on disk, the links it owes, and the worklog's last word."""
    t = slugify(topic)
    row = c.execute("SELECT * FROM topics WHERE slug=?", (t,)).fetchone()
    counts = {}
    for table in ("sources", "artifacts", "pages", "people", "places", "events", "subjects", "observations"):
        counts[table] = c.execute(f"SELECT COUNT(*) AS n FROM {table} WHERE topic=?", (t,)).fetchone()["n"]
    counts["tracks"] = c.execute("SELECT COUNT(*) AS n FROM artifacts WHERE topic=? AND type='track'", (t,)).fetchone()["n"]
    counts["dates"] = c.execute("SELECT COUNT(*) AS n FROM dates WHERE topic=?", (t,)).fetchone()["n"]
    files_dir = HISTORY_DIR / t / "files"
    files = sorted(p.name for p in files_dir.iterdir()) if files_dir.is_dir() else []
    registered = {Path(r["local_file"]).name for r in c.execute(
        "SELECT local_file FROM artifacts WHERE topic=? AND local_file<>''", (t,))}
    registered |= {Path(r["local_file"]).name for r in c.execute(
        "SELECT local_file FROM sources WHERE topic=? AND local_file<>''", (t,))}
    registered |= {Path(r["view_file"]).name for r in c.execute(
        "SELECT view_file FROM artifacts WHERE topic=? AND view_file<>''", (t,))}
    log = [dict(r) for r in c.execute("SELECT * FROM worklog WHERE topic=? ORDER BY id DESC LIMIT 12", (t,))]
    reindex_links(c)
    wanted = [dict(r) for r in c.execute(
        "SELECT l.kind, l.name, l.src FROM links l JOIN pages p ON p.slug=l.src "
        "WHERE p.topic=? AND l.target='' ORDER BY l.kind, l.name", (t,))]
    own = {r["bibkey"] for r in c.execute("SELECT bibkey FROM sources WHERE topic=?", (t,))}
    own |= {r["name"] for r in c.execute("SELECT name FROM subjects WHERE topic=?", (t,))}
    problems = [p for p in validate(c)["problems"] if p["what"].startswith(t) or p["what"] in own]
    return {"topic": dict(row) if row else None, "counts": counts, "files": files,
            "requests": list_requests(c, topic=t),
            "unregistered_files": [f for f in files if f not in registered],
            "worklog": log, "wanted": wanted, "problems": problems,
            "artifacts": [dict(r) for r in c.execute(
                "SELECT id, type, date_text, title FROM artifacts WHERE topic=? ORDER BY id", (t,))],
            "pages": [dict(r) for r in c.execute(
                "SELECT slug, title, ordering, status, length(body) AS words FROM pages WHERE topic=? ORDER BY ordering", (t,))],
            "sources": [dict(r) for r in c.execute(
                "SELECT bibkey, year, title FROM sources WHERE topic=? ORDER BY bibkey", (t,))],
            "subjects": [dict(r) for r in c.execute(
                "SELECT s.name, s.kind, s.english, (SELECT COUNT(*) FROM observations o WHERE o.subject=s.name) AS n "
                "FROM subjects s WHERE s.topic=? ORDER BY s.name", (t,))]}


# ---------------------------------------------------------------- BibTeX
BIB_FIELDS = {"author": "author", "title": "title", "year": "year", "journal": "container",
              "booktitle": "container", "publisher": "publisher", "address": "address",
              "volume": "volume", "pages": "pages", "url": "url", "urldate": "urldate",
              "doi": "doi", "note": "note", "institution": "publisher", "school": "publisher",
              "organization": "publisher", "howpublished": "note", "series": "container",
              "archive": "archive", "library": "archive"}


def parse_bib(text: str) -> list[dict]:
    """Entries out of a BibTeX file. Tolerant on purpose: the crew hand-writes
    these, and a missing comma should not cost a source."""
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        start = m.end()
        depth, i = 1, start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[start:i - 1]
        row = {"entry_type": m.group(1).lower(), "bibkey": m.group(2)}
        for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|[^,\n]+)", body):
            name, val = fm.group(1).lower(), fm.group(2).strip().strip(",").strip()
            if val[:1] in "{\"":
                val = val[1:-1]
            val = re.sub(r"\s+", " ", val.replace("{", "").replace("}", "")).strip()
            if name == "keywords":
                row["primary"] = "primary" in val.lower()
            elif name in BIB_FIELDS:
                key = BIB_FIELDS[name]
                row[key] = f"{row[key]}; {val}" if row.get(key) and key == "note" else val
        out.append(row)
    return out


def import_bib(c, text: str, topic: str = "") -> list[str]:
    keys = []
    for row in parse_bib(text):
        if not row.get("title"):
            continue
        keys.append(add_source(c, row.pop("bibkey"), row.pop("title"), topic=topic, **row))
    return keys


def to_bibtex(rows) -> str:
    """The bibliography, for export from the History tab."""
    out = []
    for r in rows:
        fields = [("author", r["author"]), ("title", r["title"]), ("year", r["year"])]
        et = r["entry_type"] or "misc"
        # the container of an article or a web page is a periodical, never a book
        fields.append(("journal" if et in ("article", "online") else "booktitle", r["container"]))
        for name, col in (("publisher", "publisher"), ("address", "address"), ("volume", "volume"),
                          ("pages", "pages"), ("doi", "doi"), ("url", "url"), ("urldate", "urldate")):
            fields.append((name, r[col]))
        # the licence's phrase travels with the citation; the rights note is for the crew
        note = "; ".join(x for x in (r["archive"], r["callno"], licence_label(r["licence"] or ""), r["note"]) if x)
        fields.append(("note", note))
        fields.append(("keywords", "primary" if r["primary_src"] else "secondary"))
        body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
        out.append(f"@{et}{{{r['bibkey']},\n{body}\n}}")
    return "\n\n".join(out) + "\n"


# ---------------------------------------------------------------- wiki
LINK_RX = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")


def link_parts(raw: str) -> tuple[str, str]:
    """``artifact:frobisher-004`` -> ('artifact', 'frobisher-004');
    a bare title -> ('', title), resolved by title later."""
    s = raw.strip()
    if ":" in s:
        head, rest = s.split(":", 1)
        if head.strip().lower() in KINDS:
            return head.strip().lower(), rest.strip()
    return "", s


def index_targets(c) -> dict:
    """Every linkable thing, by kind and by title, so a link can be resolved
    either way."""
    idx: dict[tuple[str, str], str] = {}
    titles: dict[str, str] = {}
    names: dict[str, str] = {}          # slug -> the label a bare link should show

    def put(kind, name, slug, title=None):
        idx[(kind, name.lower())] = slug
        idx[(kind, slugify(name))] = slug
        titles.setdefault((title or name).lower(), slug)
        names.setdefault(slug, title or name)

    for r in c.execute("SELECT id, title FROM artifacts"):
        put("artifact", r["id"], page_slug("artifact", r["id"]), r["title"])
        titles.setdefault(r["title"].lower(), page_slug("artifact", r["id"]))
    for r in c.execute("SELECT bibkey, title FROM sources"):
        put("source", r["bibkey"], page_slug("source", r["bibkey"]), r["title"])
    for r in c.execute("SELECT name, also FROM people"):
        slug = page_slug("person", r["name"])
        put("person", r["name"], slug)
        for alt in (r["also"] or "").split(";"):
            if alt.strip():
                put("person", alt.strip(), slug, r["name"])
    for table, kind in (("animals", "animal"), ("vessels", "vessel")):
        for r in c.execute(f"SELECT name, also FROM {table}"):
            slug = page_slug(kind, r["name"])
            put(kind, r["name"], slug)
            for alt in (r["also"] or "").split(";"):
                if alt.strip():
                    put(kind, alt.strip(), slug, r["name"])
    for r in c.execute("SELECT name, historic, inuktitut FROM places"):
        slug = page_slug("place", r["name"])
        put("place", r["name"], slug)
        for alt in (r["historic"], r["inuktitut"]):
            if alt:
                put("place", alt, slug)
    for r in c.execute("SELECT name, english, french, inuktitut, kalaallisut, also FROM subjects"):
        slug = page_slug("subject", r["name"])
        put("subject", r["name"], slug)
        for alt in [r["english"], r["french"], r["inuktitut"], r["kalaallisut"]] + (r["also"] or "").split(";"):
            if alt and alt.strip():
                put("subject", alt.strip(), slug, r["name"])
    for r in c.execute("SELECT slug, kind, title FROM pages"):
        put(r["kind"] or "page", r["slug"].split("/")[-1], r["slug"], r["title"])
        titles.setdefault(r["title"].lower(), r["slug"])
    for r in c.execute("SELECT id, title FROM events"):
        put("event", str(r["id"]), page_slug("event", str(r["id"])), r["title"])
        titles.setdefault(r["title"].lower(), page_slug("event", str(r["id"])))
    for r in c.execute("SELECT slug, title FROM topics"):
        put("topic", slug_last(slug := page_slug("topic", r["slug"])), slug, r["title"])
        idx[("topic", r["slug"].lower())] = slug
    return {"idx": idx, "titles": titles, "names": names}


def slug_last(slug: str) -> str:
    return slug.split("/")[-1]


def resolve(targets: dict, kind: str, name: str) -> str:
    idx, titles = targets["idx"], targets["titles"]
    if kind:
        return idx.get((kind, name.lower())) or idx.get((kind, slugify(name)), "")
    hit = titles.get(name.lower())
    if hit:
        return hit
    for k in KINDS:
        if (k, name.lower()) in idx:
            return idx[(k, name.lower())]
        if (k, slugify(name)) in idx:
            return idx[(k, slugify(name))]
    return ""


def _mention_index(c) -> tuple[dict, "re.Pattern | None"]:
    """Names the ship's pane auto-links on first mention — people, places
    (historic and Inuktitut forms too), animals and vessels — so the links
    table can index the same mentions. Longest name wins a nested match."""
    mention: dict[str, tuple[str, str]] = {}
    for r in c.execute("SELECT name, also FROM people"):
        slug = page_slug("person", r["name"])
        mention.setdefault(r["name"], ("person", slug))
        for alt in (r["also"] or "").split(";"):
            if alt.strip():
                mention.setdefault(alt.strip(), ("person", slug))
    for r in c.execute("SELECT name, historic, inuktitut FROM places"):
        slug = page_slug("place", r["name"])
        for nm in (r["name"], r["historic"], r["inuktitut"]):
            if nm:
                mention.setdefault(nm, ("place", slug))
    for table, kind in (("animals", "animal"), ("vessels", "vessel")):
        for r in c.execute(f"SELECT name, also FROM {table}"):
            slug = page_slug(kind, r["name"])
            mention.setdefault(r["name"], (kind, slug))
            for alt in (r["also"] or "").split(";"):
                if alt.strip():
                    mention.setdefault(alt.strip(), (kind, slug))
    # a subject links on first mention by its scientific name and its
    # capitalised names (Ovibos moschatus, North Magnetic Pole, Eureka Sound
    # Group); a common noun (fog, wind, muskox, sea ice, air temperature)
    # would link half the wiki to the weather, so those resolve only as
    # explicit [[subject:]] links
    for r in c.execute("SELECT name, english, french, inuktitut, kalaallisut, also FROM subjects"):
        slug = page_slug("subject", r["name"])
        for nm in [r["name"], r["english"], r["french"], r["inuktitut"], r["kalaallisut"]] + (r["also"] or "").split(";"):
            nm = (nm or "").strip()
            if nm and nm[:1].isupper():
                mention.setdefault(nm, ("subject", slug))
    mention = {k: v for k, v in mention.items() if len(k) >= 3}
    # a single word that also occurs inside a longer known name ("Arctic" in
    # C.G.S. Arctic and Arctic Bay, "Baffin" in William Baffin and Baffin Bay,
    # "Erebus" the dog vs HMS Erebus) is too ambiguous to link as a bare
    # mention: hundreds of pages would back-link a dog. Explicit
    # [[kind:name]] links still resolve through every alias.
    inside = set()
    for k in mention:
        parts = [w.strip("()") for w in k.split()]
        if len(parts) > 1:
            inside.update(parts)
    # and a bare toponym that happens to be a vessel or animal name (the
    # schooner Alaska) would link half the wiki to the wrong thing
    geo = {"Alaska", "America", "Canada", "Greenland", "Atlantic", "Pacific",
           "Siberia", "Europe", "Boothia", "Hudson", "Churchill"}
    for k in [k for k in mention if " " not in k and (k in inside or k in geo)]:
        del mention[k]
    if not mention:
        return mention, None
    rx = re.compile(r"\b(" + "|".join(re.escape(n) for n in
                                      sorted(mention, key=len, reverse=True)) + r")\b")
    return mention, rx


def reindex_links(c) -> dict:
    """Re-read every page's links: explicit wikilinks, the people the page
    names in its people field, and bare first mentions of known people,
    places, animals and vessels — the same mentions the ship's pane links
    when it renders, so backlinks see them and `wanted` shrinks to the real
    gaps. Only explicit wikilinks can be wanted; a mention only ever points
    at something that exists."""
    targets = index_targets(c)
    mention, rx = _mention_index(c)
    c.execute("DELETE FROM links")
    wanted: dict[str, list[str]] = {}
    rows = c.execute("SELECT slug, body, summary, people FROM pages").fetchall()
    n = 0
    for r in rows:
        seen = set()
        targeted = set()
        text = (r["body"] or "") + "\n" + (r["summary"] or "")
        for m in LINK_RX.finditer(text):
            kind, name = link_parts(m.group(1))
            if (kind, name) in seen:
                continue
            seen.add((kind, name))
            slug = resolve(targets, kind, name)
            c.execute("INSERT OR REPLACE INTO links (src, kind, name, target) VALUES (?,?,?,?)",
                      (r["slug"], kind, name, slug))
            n += 1
            if slug:
                targeted.add(slug)
            else:
                wanted.setdefault(f"{kind}:{name}" if kind else name, []).append(r["slug"])
        for name in json.loads(r["people"] or "[]"):
            slug = page_slug("person", name)
            if slug not in targeted:
                targeted.add(slug)
                c.execute("INSERT OR REPLACE INTO links (src, kind, name, target) VALUES (?,?,?,?)",
                          (r["slug"], "person", name, slug))
                n += 1
        if rx:
            for m in rx.finditer(LINK_RX.sub(" ", text)):
                kind, slug = mention[m.group(1)]
                if slug in targeted:
                    continue
                targeted.add(slug)
                c.execute("INSERT OR REPLACE INTO links (src, kind, name, target) VALUES (?,?,?,?)",
                          (r["slug"], kind, m.group(1), slug))
                n += 1
    n += _row_links(c, targets)
    c.commit()
    return {"links": n, "pages": len(rows), "wanted": wanted}


def _row_links(c, targets: dict) -> int:
    """The links a generated page carries by virtue of its row: the source it
    cites, the people it names, the place an event happened at. These are the
    backlinks a person, source or place page shows as "Mentioned in" from the
    artifacts and events, and they come from the fields, not the body, which
    is prose alone. A topic is not linked this way: every artifact points at
    its topic already, and thousands of backlinks would bury the topic page.
    A bibkey that names no source is `check`'s problem, not a wanted link."""
    n = 0

    def put(src: str, kind: str, name: str, slug: str, seen: set) -> None:
        nonlocal n
        if slug and slug not in seen:
            seen.add(slug)
            c.execute("INSERT OR REPLACE INTO links (src, kind, name, target) VALUES (?,?,?,?)",
                      (src, kind, name, slug))
            n += 1

    for r in c.execute("SELECT id, bibkey, people FROM artifacts"):
        src, seen = page_slug("artifact", r["id"]), set()
        put(src, "source", r["bibkey"], resolve(targets, "source", r["bibkey"]) if r["bibkey"] else "", seen)
        for p in json.loads(r["people"] or "[]"):
            put(src, "person", p, page_slug("person", p), seen)
    for r in c.execute("SELECT id, bibkey, people, place FROM events"):
        src, seen = page_slug("event", str(r["id"])), set()
        put(src, "source", r["bibkey"], resolve(targets, "source", r["bibkey"]) if r["bibkey"] else "", seen)
        for p in json.loads(r["people"] or "[]"):
            put(src, "person", p, page_slug("person", p), seen)
        if r["place"]:
            put(src, "place", r["place"], resolve(targets, "place", r["place"]), seen)
    for table, kind in (("people", "person"), ("places", "place"), ("animals", "animal"), ("vessels", "vessel"),
                        ("subjects", "subject")):
        for r in c.execute(f"SELECT name, bibkey FROM {table} WHERE bibkey<>''"):
            put(page_slug(kind, r["name"]), "source", r["bibkey"], resolve(targets, "source", r["bibkey"]), set())
    # an observation has no page of its own: its subject's page carries the
    # record, so the subject page is where its source, observer, place,
    # evidence and event are linked from
    seen_by_subject: dict[str, set] = {}
    for r in c.execute("SELECT subject, bibkey, observer, place, artifact_id, event_id, vessel FROM observations"):
        src = page_slug("subject", r["subject"])
        seen = seen_by_subject.setdefault(src, set())
        put(src, "source", r["bibkey"], resolve(targets, "source", r["bibkey"]) if r["bibkey"] else "", seen)
        if r["observer"]:
            put(src, "person", r["observer"], resolve(targets, "person", r["observer"]), seen)
        if r["place"]:
            put(src, "place", r["place"], resolve(targets, "place", r["place"]), seen)
        if r["artifact_id"]:
            put(src, "artifact", r["artifact_id"], resolve(targets, "artifact", r["artifact_id"]), seen)
        if r["event_id"]:
            put(src, "event", str(r["event_id"]), resolve(targets, "event", str(r["event_id"])), seen)
        if r["vessel"]:
            put(src, "vessel", r["vessel"], resolve(targets, "vessel", r["vessel"]), seen)
    for r in c.execute("SELECT name, subject FROM animals WHERE subject<>''"):
        put(page_slug("animal", r["name"]), "subject", r["subject"], resolve(targets, "subject", r["subject"]), set())
    return n


def render_markdown(body: str, targets: dict, base: str = "") -> str:
    """Wikilinks become ordinary Markdown links; everything else is left for
    the page to render. A wanted link is marked so it reads as a gap."""
    def sub(m):
        kind, name = link_parts(m.group(1))
        slug = resolve(targets, kind, name)
        label = m.group(2)
        if not label:
            # an artifact id, a bibkey, a topic slug and an event number are
            # opaque, so a link without a label of its own shows the thing's
            # title instead (issue #9)
            label = targets["names"].get(slug, name) if kind in ("artifact", "source", "topic", "event") \
                else (name if kind else m.group(1))
        if not slug:
            return f'<span class="wanted" title="no page yet">{label}</span>'
        return f'[{label}]({base}{slug})'
    return LINK_RX.sub(sub, body or "")


# ---------------------------------------------------------------- generated pages
# A generated page carries the row's prose alone. The row's fields (date,
# creator, position, licence, credit, source, people, the holding institution,
# a place's kind, a vessel's build and fate) stay in the row and the ship's
# front end lays them out beside the picture and the map; writing them into
# the body showed a reader every fact twice. The rights note is for the crew
# and is never part of a page.
def artifact_body(r: sqlite3.Row) -> str:
    """The generated page for one artifact: its description."""
    return (r["description"] or "").strip()


def source_body(r: sqlite3.Row) -> str:
    return (r["note"] or "").strip()


def person_body(r: sqlite3.Row) -> str:
    return (r["note"] or "").strip()


def place_body(r: sqlite3.Row) -> str:
    return (r["note"] or "").strip()


def animal_body(r: sqlite3.Row) -> str:
    return (r["note"] or "").strip()


def vessel_body(r: sqlite3.Row) -> str:
    return (r["note"] or "").strip()


def event_body(r: sqlite3.Row) -> str:
    return (r["detail"] or "").strip()


def subject_body(r: sqlite3.Row) -> str:
    return (r["note"] or "").strip()


def subject_summary(r) -> str:
    names = " · ".join(x for x in (r["english"], r["inuktitut"]) if x)
    return " · ".join(x for x in (r["kind"], r["domain"], names) if x)


def generated_pages(c) -> list[dict]:
    """A page for every artifact, source, person, place and event. These are
    derived, so they are rebuilt on every publish rather than stored."""
    out = []
    for r in c.execute("SELECT * FROM events ORDER BY id"):
        out.append({"slug": page_slug("event", str(r["id"])), "kind": "event", "title": r["title"],
                    "topic": r["topic"], "summary": r["date_text"] or r["date_start"],
                    "body": event_body(r), "ref": str(r["id"])})
    for r in c.execute("SELECT * FROM artifacts ORDER BY id"):
        out.append({"slug": page_slug("artifact", r["id"]), "kind": "artifact", "title": r["title"],
                    "topic": r["topic"], "summary": (r["description"] or "")[:300],
                    "body": artifact_body(r), "ref": r["id"]})
    for r in c.execute("SELECT * FROM sources ORDER BY bibkey"):
        out.append({"slug": page_slug("source", r["bibkey"]), "kind": "source", "title": r["title"],
                    "topic": r["topic"], "summary": ", ".join(x for x in (r["author"], r["year"]) if x),
                    "body": source_body(r), "ref": r["bibkey"]})
    for r in c.execute("SELECT * FROM people ORDER BY name"):
        out.append({"slug": page_slug("person", r["name"]), "kind": "person", "title": r["name"],
                    "topic": r["topic"], "summary": r["role"] or "", "body": person_body(r), "ref": r["name"]})
    for r in c.execute("SELECT * FROM places ORDER BY name"):
        out.append({"slug": page_slug("place", r["name"]), "kind": "place", "title": r["name"],
                    "topic": r["topic"], "summary": r["kind"] or "", "body": place_body(r), "ref": r["name"]})
    for r in c.execute("SELECT * FROM animals ORDER BY name"):
        out.append({"slug": page_slug("animal", r["name"]), "kind": "animal", "title": r["name"],
                    "topic": r["topic"], "summary": " · ".join(x for x in (r["kind"], r["role"]) if x),
                    "body": animal_body(r), "ref": r["name"]})
    for r in c.execute("SELECT * FROM vessels ORDER BY name"):
        out.append({"slug": page_slug("vessel", r["name"]), "kind": "vessel", "title": r["name"],
                    "topic": r["topic"], "summary": " · ".join(x for x in (r["kind"], r["role"]) if x),
                    "body": vessel_body(r), "ref": r["name"]})
    for r in c.execute("SELECT * FROM subjects ORDER BY name"):
        out.append({"slug": page_slug("subject", r["name"]), "kind": "subject", "title": r["name"],
                    "topic": r["topic"], "summary": subject_summary(r), "body": subject_body(r), "ref": r["name"]})
    return out


# ---------------------------------------------------------------- checks
IMAGE_MAGIC = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"GIF87a", b"GIF89a")


def _small_real_image(f: Path) -> bool:
    """A file under 4 kB is usually an error page, but a line cut from a
    scanned book (Boas's figure 542 is 3.8 kB) is a real image: accept it when
    the bytes begin with a PNG, JPEG or GIF signature."""
    try:
        head = f.read_bytes()[:8]
    except OSError:
        return False
    return any(head.startswith(m) for m in IMAGE_MAGIC)


def _off_map(lat, lon, east_ok: bool = False) -> str | None:
    """A coordinate nothing in this history can honestly carry. Pins may sit
    well south of the Arctic — the voyages sailed from London and New York,
    Munk from Copenhagen, Kane died in Havana — but nothing lies south of 20
    or east of 40, and a longitude in the mirror band east of 40 is almost
    always a dropped minus sign. The one exception is the far side of the
    dateline, 160-180 east: the Karluk's people and Bartlett's walk reached
    the Siberian coast, and those positions are honestly east. A topic whose
    own positions lie largely in the east (Franz Josef Land, the Siberian
    shelf) passes `east_ok`, and so does a row tagged east-verified."""
    if lat is not None and not 20 <= lat <= 90:
        return f"latitude {lat} is south of anywhere this history reaches"
    if lon is not None and not (-180 <= lon <= 180):
        return f"longitude {lon} is off the globe"
    if lon is not None and not east_ok and not (-180 <= lon <= 40 or 160 <= lon <= 180):
        return f"longitude {lon} is east of 40: almost always a dropped minus sign"
    return None


def _points(coords):
    """Every [lon, lat] pair in a GeoJSON coordinates value, any nesting."""
    if isinstance(coords, list):
        if len(coords) >= 2 and all(isinstance(x, (int, float)) for x in coords[:2]):
            yield coords
        else:
            for v in coords:
                yield from _points(v)


# ------------------------------------------------ faces, keywords, ontology
def add_face(c, artifact_id: str, n: int, file: str, **kw) -> int:
    """One face cut from an image artifact. ``file`` is relative to
    db/history/ and should sit under <topic>/files/faces/ so the ship's pull
    brings it. ``person`` is a name in people or '' when unidentified."""
    if not c.execute("SELECT 1 FROM artifacts WHERE id=?", (artifact_id,)).fetchone():
        raise ValueError(f"no artifact {artifact_id!r}")
    box = kw.get("box")
    if box not in (None, ""):
        box = box if isinstance(box, str) else json.dumps(box)
        if len(json.loads(box)) != 4:
            raise ValueError("box must be [x, y, w, h]")
    kind = (kw.get("kind") or "person").strip()
    table = {"person": "people", "animal": "animals", "vessel": "vessels"}.get(kind)
    if not table:
        raise ValueError("a face's kind is person, animal or vessel")
    person = (kw.get("person") or "").strip()
    if person and not c.execute(f"SELECT 1 FROM {table} WHERE name=?", (person,)).fetchone():
        raise ValueError(f"{kind} {person!r} is not in {table}; enter it first or leave the crop unidentified")
    row = {"artifact_id": artifact_id, "n": int(n), "file": file, "box": box or "", "kind": kind,
           "person": person, "confidence": kw.get("confidence"), "method": kw.get("method", ""),
           "updated": now()}
    cols = ",".join(row); marks = ",".join("?" * len(row))
    sets = ",".join(f"{k}=excluded.{k}" for k in row if k not in ("artifact_id", "n"))
    c.execute(f"INSERT INTO faces ({cols}) VALUES ({marks}) ON CONFLICT(artifact_id, n) DO UPDATE SET {sets}",
              tuple(row.values()))
    c.commit()
    return int(c.execute("SELECT id FROM faces WHERE artifact_id=? AND n=?", (artifact_id, int(n))).fetchone()["id"])


def forget_faces(c, artifact_id: str) -> int:
    n = c.execute("DELETE FROM faces WHERE artifact_id=?", (artifact_id,)).rowcount
    c.commit()
    return n


def add_keywords(c, artifact_id: str, paths: list, source: str = "crew", replace: bool = True) -> int:
    """Subject paths on an artifact, e.g. 'Ships & boats > Whalers > Dundee
    fleet'. ``replace`` drops that source's earlier paths first, so a re-run
    of the model does not pile up. A crew path outranks the model's."""
    if not c.execute("SELECT 1 FROM artifacts WHERE id=?", (artifact_id,)).fetchone():
        raise ValueError(f"no artifact {artifact_id!r}")
    if not (source == "crew" or source.startswith("llm:")):
        raise ValueError("source must be 'crew' or 'llm:<model>'")
    clean = []
    for p in paths:
        p = " > ".join(part.strip() for part in str(p).split(">") if part.strip())
        if p and p not in clean:
            clean.append(p)
    if replace:
        c.execute("DELETE FROM keywords WHERE artifact_id=? AND source=?", (artifact_id, source))
    for i, p in enumerate(clean[:3]):
        c.execute("INSERT OR REPLACE INTO keywords (artifact_id, path, ordinal, source, updated) VALUES (?,?,?,?,?)",
                  (artifact_id, p, i, source, now()))
    c.commit()
    return len(clean[:3])


def artifact_keywords(c, artifact_id: str) -> list:
    """The paths to publish: the crew's first, then the model's, three at most."""
    rows = c.execute("SELECT path, source, ordinal FROM keywords WHERE artifact_id=? "
                     "ORDER BY CASE WHEN source='crew' THEN 0 ELSE 1 END, ordinal", (artifact_id,)).fetchall()
    out = []
    for r in rows:
        if r["path"] not in out:
            out.append(r["path"])
    return out[:3]


def set_ontology(c, tree: dict, model: str = "") -> None:
    """The one tree every keyword path belongs to. Kept stable between runs:
    a later run extends it rather than replacing it, so pages do not reshuffle."""
    if not isinstance(tree, dict):
        raise ValueError("the ontology is a dict of level-1 -> {level-2: [level-3, ...]}")
    c.execute("INSERT INTO ontology (id, tree, model, generated) VALUES (1, ?, ?, ?) "
              "ON CONFLICT(id) DO UPDATE SET tree=excluded.tree, model=excluded.model, generated=excluded.generated",
              (json.dumps(tree, ensure_ascii=False), model, now()))
    c.commit()


def get_ontology(c) -> dict | None:
    r = c.execute("SELECT tree, model, generated FROM ontology WHERE id=1").fetchone()
    if not r:
        return None
    return {"generated": r["generated"], "model": r["model"], "tree": json.loads(r["tree"] or "{}")}


def validate(c) -> dict:
    """Everything wrong that a reader would notice: an artifact with no
    credit or no source, a bibkey that resolves to nothing, a coordinate on
    dry land in the wrong hemisphere, a page that links nowhere.

    ``notes`` carries what is worth a look but is not wrong: the tags used
    only once, which are where a near-copy of an established tag hides."""
    problems: list[dict] = []
    notes: list[dict] = []

    def bad(kind, what, detail):
        problems.append({"kind": kind, "what": what, "detail": detail})

    def note(kind, what, detail):
        """Worth a researcher's eye, but nothing a reader would notice."""
        notes.append({"kind": kind, "what": what, "detail": detail})

    keys = {r["bibkey"] for r in c.execute("SELECT bibkey FROM sources")}
    # the eastern topics: three or more of their pinned rows lie between 40
    # and 160 east, so an eastern position there is the rule; a dropped minus
    # sign is a single slip in a topic that otherwise lies west
    band: dict[str, list[int]] = {}
    for t in ("artifacts", "places", "events"):
        for r in c.execute(f"SELECT topic, lon FROM {t} WHERE lon IS NOT NULL"):
            n = band.setdefault(r["topic"], [0, 0])
            n[0] += 40 < r["lon"] < 160
            n[1] += 1
    east_topics = {t for t, (e, n) in band.items() if e >= 3}
    for r in c.execute("SELECT * FROM artifacts"):
        if not r["credit"]:
            bad("artifact", r["id"], "no credit line")
        if r["type"] in ("map", "image") and not r["view_file"]:
            # the ship thumbnails a raster; a PDF, a zip or a page shows as "no picture yet"
            if r["local_file"] and not is_raster(r["local_file"]):
                bad("artifact", r["id"], f"{r['type']} has no raster to show: render one and set --view-file "
                                         f"(pdftoppm for a PDF, a screenshot for a page)")
            elif r["type"] == "map" and not r["local_file"] and not r["download_url"]:
                bad("artifact", r["id"], "map has no file at all: render its geometry or chart to a raster and set --view-file")
        if not r["bibkey"]:
            bad("artifact", r["id"], "no bibkey")
        elif r["bibkey"] not in keys:
            bad("artifact", r["id"], f"bibkey {r['bibkey']} is in no source entry")
        if not r["licence"]:
            bad("artifact", r["id"], "no licence stated")
        elif not is_licence_code(r["licence"]):
            bad("artifact", r["id"], f"licence is not a code: {r['licence'][:60]!r}")
        if r["lat"] is None and not r["geometry"]:
            bad("artifact", r["id"], "neither a position nor a geometry")
        ppl = json.loads(r["people"] or "[]")
        if ppl and (r["description"] or "").strip():
            d = r["description"] + " " + r["title"]
            named = [p2 for p2 in ppl if p2 in r["description"] or
                     (p2.split() and p2.split()[-1] in r["description"])]
            if not named:
                bad("artifact", r["id"], "its people appear only in the title or list; "
                                         "the description must name who it is about")
        # a documented, genuinely eastern position (Novaya Zemlya, the far
        # side of the dateline) is vouched for with the east-verified tag
        east_ok = "east-verified" in (r["tags"] or "") or r["topic"] in east_topics
        msg = _off_map(r["lat"], r["lon"], east_ok)
        if msg:
            bad("artifact", r["id"], msg)
        if r["local_file"]:
            f = HISTORY_DIR / r["local_file"]
            if not f.is_file():
                bad("artifact", r["id"], f"local_file missing: {r['local_file']}")
            elif f.stat().st_size < 4096 and not _small_real_image(f):
                bad("artifact", r["id"], f"local_file suspiciously small ({f.stat().st_size} bytes)")
        if r["geometry"]:
            try:
                g = json.loads(r["geometry"])
                if not isinstance(g, dict) or "coordinates" not in g:
                    bad("artifact", r["id"], "geometry is not a GeoJSON geometry")
                else:
                    for pt in _points(g["coordinates"]):
                        msg = _off_map(pt[1], pt[0], east_ok)
                        if msg:
                            bad("artifact", r["id"], f"geometry point {pt[:2]}: {msg}")
                            break
            except json.JSONDecodeError:
                bad("artifact", r["id"], "geometry is not valid JSON")
        if r["waypoints"]:
            try:
                w = json.loads(r["waypoints"])
                if not isinstance(w, list):
                    raise ValueError
                for i, p in enumerate(w):
                    if isinstance(p, dict):
                        msg = _off_map(p.get("lat"), p.get("lon"), east_ok)
                        if msg:
                            bad("artifact", r["id"], f"waypoint {i} ({p.get('date', 'undated')}): {msg}")
                            break
            except (json.JSONDecodeError, ValueError):
                bad("artifact", r["id"], "waypoints is not a JSON array")
    held: dict[str, list[str]] = {}
    still_misc: list[str] = []
    for r in c.execute("SELECT bibkey, title, licence, url, archive, entry_type FROM sources"):
        if not r["licence"]:
            bad("source", r["bibkey"], "no copyright status")
        elif not is_licence_code(r["licence"]):
            bad("source", r["bibkey"], f"licence is not a code: {r['licence'][:60]!r}")
        if not r["url"]:
            bad("source", r["bibkey"], "no URL")
        if r["archive"]:
            name, callno, detail = normalise_archive(r["archive"])
            held.setdefault(name, []).append(r["bibkey"])
            if name != r["archive"]:
                bad("source", r["bibkey"], f"archive {r['archive'][:60]!r} is a variant of {name!r}"
                                           + (f"; {callno or detail} belongs in callno or the note" if callno or detail else ""))
        if r["entry_type"] == "misc":
            still_misc.append(r["bibkey"])
    if still_misc:
        note("sources", f"{len(still_misc)} of entry_type misc",
             "give each the type that fits: " + ", ".join(k for k in ENTRY_TYPES if k != "misc")
             + "; " + ", ".join(still_misc[:6]) + ("..." if len(still_misc) > 6 else ""))
    for name, keys in sorted(held.items()):
        if len(keys) == 1:
            note("archive", name[:60], f"held by one source only ({keys[0]}): check it is not another "
                                       f"spelling of an archive already in use")
    # tags: a spelling the writers no longer accept is a legacy row to mend,
    # and a tag used once is the long tail, reported as a note
    where: dict = {}
    for kind, sql in (("artifact", "SELECT id AS what, tags FROM artifacts"),
                      ("event", "SELECT id AS what, tags FROM events")):
        for r in c.execute(sql):
            ident = str(r["what"])
            for raw in stored_tags(r["tags"]):
                fixed = normalise_tags(raw)
                if fixed != [raw]:
                    if raw in TAG_ALIASES:
                        bad(kind, ident, f"tag {raw!r} is a variant of {TAG_ALIASES[raw]!r}")
                    else:
                        bad(kind, ident, f"tag {raw[:60]!r} is not in the canonical form: "
                                         f"{', '.join(fixed) or '(nothing)'}")
                for t in fixed:
                    where.setdefault(t, []).append(f"{kind} {ident}")
    for t, used in sorted(where.items()):
        if len(used) == 1:
            note("tag", t, f"used once, on {used[0]}")

    for r in c.execute("SELECT name, kind FROM vessels WHERE kind<>''"):
        if not is_vessel_kind(r["kind"]):
            bad("vessel", r["name"], f"kind is not a code: {r['kind'][:60]!r}")
    # the natural half: a subject resolves in its backbone or says why not;
    # an observation has its subject, its date, its position and its source
    # `keys` was rebound by the archive loop above; the source set again
    source_keys = {r["bibkey"] for r in c.execute("SELECT bibkey FROM sources")}
    subjects = {r["name"]: dict(r) for r in c.execute("SELECT * FROM subjects")}
    for name, r in subjects.items():
        if r["kind"] not in SUBJECT_KINDS:
            bad("subject", name, f"kind is not a code: {r['kind'][:40]!r}")
        if r["domain"] not in DOMAINS:
            bad("subject", name, f"domain is not a code: {r['domain'][:40]!r}")
        if r["parent"] and r["parent"] not in subjects:
            bad("subject", name, f"parent {r['parent']!r} is no subject")
        if not r["backbone_id"] and not (r["note"] or "").strip():
            bad("subject", name, "no backbone id (GBIF, WoRMS, WEBLEX, IAU) and no note saying why")
        if r["bibkey"] and r["bibkey"] not in source_keys:
            bad("subject", name, f"bibkey {r['bibkey']} is in no source entry")
        # the names in the languages of the region are half the record: a
        # living thing, a kind of ice, a weather, a thing in the sky without
        # its Inuktitut or Kalaallisut name is worth a researcher's eye
        if r["kind"] in ("taxon", "ice", "weather", "sky", "water", "landform", "phenomenon") \
                and not r["inuktitut"] and not r["kalaallisut"] and r["rank"] not in ("family", "order", "class", "phylum", "kingdom"):
            note("subject", name, "no Inuktitut or Kalaallisut name: look in Rasmussen's and Boas's vocabularies, "
                                  "the NWMB species lists and the IQ studies, or say in the note that none is recorded")
    for r in c.execute("SELECT * FROM observations"):
        if r["subject"] not in subjects:
            bad("observation", r["id"], f"subject {r['subject']!r} is no subject")
        if not r["date_start"]:
            bad("observation", r["id"], "no date")
        if r["lat"] is None or r["lon"] is None:
            bad("observation", r["id"], "no position, and its place gives none")
        else:
            # the magnetic pole has crossed into the eastern hemisphere; an
            # observation vouches for an eastern position with the same tag
            msg = _off_map(r["lat"], r["lon"], "east-verified" in (r["tags"] or "") or r["topic"] in east_topics)
            if msg:
                bad("observation", r["id"], msg)
        if not r["bibkey"]:
            bad("observation", r["id"], "no bibkey")
        elif r["bibkey"] not in source_keys:
            bad("observation", r["id"], f"bibkey {r['bibkey']} is in no source entry")
        if r["method"] in ("transect", "catch-record", "aerial-survey") and not r["count"] and r["value"] is None:
            bad("observation", r["id"], f"a {r['method']} wants a count")
        if r["method"] == "sounding" and r["depth"] is None and r["value"] is None:
            bad("observation", r["id"], "a sounding wants a depth or a value")
        if r["value"] is not None and not r["unit"]:
            bad("observation", r["id"], "a value without its unit")
        if r["place"] and not c.execute("SELECT 1 FROM places WHERE name=?", (r["place"],)).fetchone():
            bad("observation", r["id"], f"place {r['place']!r} is no place row")
        if r["observer"] and " " in r["observer"] and not c.execute(
                "SELECT 1 FROM people WHERE name=?", (r["observer"],)).fetchone():
            note("observation", r["id"], f"observer {r['observer']!r} has no person row (fine for a party or a watch)")
        if r["artifact_id"] and not c.execute("SELECT 1 FROM artifacts WHERE id=?", (r["artifact_id"],)).fetchone():
            bad("observation", r["id"], f"artifact {r['artifact_id']!r} does not exist")
        if r["sensitive"] and r["place"]:
            note("observation", r["id"], "sensitive: the place is published blank and the position coarsened")
    for r in c.execute("SELECT slug, domain FROM topics"):
        if r["domain"] not in TOPIC_DOMAINS:
            bad("topic", r["slug"], f"domain is not history or nature: {r['domain']!r}")
    for r in c.execute("SELECT kind, COUNT(*) AS n FROM places WHERE kind<>'' GROUP BY kind"):
        if r["kind"] not in PLACE_KINDS:
            note("place-kind", r["kind"], f"used on {r['n']} place(s) and not in the vocabulary: "
                                         + ", ".join(PLACE_KINDS))
    for r in c.execute("SELECT name, topic, lat, lon FROM places WHERE lat IS NOT NULL"):
        msg = _off_map(r["lat"], r["lon"], r["topic"] in east_topics)
        if msg:
            bad("place", r["name"], msg)
    for r in c.execute("SELECT id, topic, title, lat, lon, tags FROM events WHERE lat IS NOT NULL"):
        msg = _off_map(r["lat"], r["lon"], r["topic"] in east_topics or "east-verified" in (r["tags"] or ""))
        if msg:
            bad("event", str(r["id"]), f"{r['title']}: {msg}")
    # a span with only one end cannot be drawn as a bar
    for r in c.execute("SELECT span, COUNT(*) AS n, MIN(role) AS a, MAX(role) AS b "
                       "FROM dates WHERE span<>'' GROUP BY span HAVING n<2 OR a=b"):
        bad("dates", r["span"], f"span has {r['n']} endpoint(s), roles {r['a']}..{r['b']}; "
                                "a time-limited activity needs one start and one end")
    def chrono(d):
        # ISO strings sort chronologically except BCE years, whose string
        # order inverts: -2400 comes before -1900
        neg = d.startswith("-")
        y = d.lstrip("-").split("-")[0]
        return (-int(y) if neg else int(y), d.lstrip("-"))
    for r in c.execute("SELECT d1.span AS span, d1.date AS a, d2.date AS b FROM dates d1 "
                       "JOIN dates d2 ON d1.span=d2.span AND d1.role='start' AND d2.role='end' "
                       "WHERE d1.span<>''"):
        if chrono(r["b"]) < chrono(r["a"]):
            bad("dates", r["span"], f"ends {r['b']} before it starts {r['a']}")
    stats = {t: c.execute(f"SELECT COUNT(*) AS n FROM {t}").fetchone()["n"]
             for t in ("topics", "sources", "artifacts", "pages", "people", "places", "events", "dates",
                       "subjects", "observations")}
    return {"problems": problems, "notes": notes, "stats": stats}


# ---------------------------------------------------------------- publish
# licences whose files never leave the research copy: a file held under a
# library or publisher licence, a work cited but not reproduced, and a whole
# work kept under fair dealing (only a figure, an image or a map is shown)
WITHHELD_LICENCES = ("in-copyright-licensed", "in-copyright-cited")


def withheld(r) -> bool:
    """Whether an artifact's file stays off the published copy."""
    if r["licence"] in WITHHELD_LICENCES:
        return True
    return r["licence"] == "fair-dealing" and r["type"] not in ("image", "map")


def display_line(coords: list, step: float = 1.0) -> list:
    """A track's line as the map should draw it: every leg follows the great
    circle, cut into pieces of at most `step` degrees of arc, and each longitude
    continues from the one before (it may pass 180 or -180), so a leg across the
    date line or near the Pole never sweeps the long way round the globe. A
    point on a pole has no longitude of its own: it takes its neighbour's, so
    the line comes up one meridian and leaves down the next."""
    import math
    pts = [[float(p[0]), float(p[1])] + list(p[2:]) for p in coords if len(p) >= 2]
    for i, p in enumerate(pts):
        if abs(p[1]) >= 89.9999:
            nb = pts[i - 1] if i else (pts[i + 1] if i + 1 < len(pts) else None)
            if nb is not None and abs(nb[1]) < 89.9999:
                p[0] = nb[0]

    def vec(lon, lat):
        lo, la = math.radians(lon), math.radians(lat)
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))

    out: list = []
    for i, p in enumerate(pts):
        if i:
            a, b = pts[i - 1], p
            va, vb = vec(a[0], a[1]), vec(b[0], b[1])
            ang = math.acos(max(-1.0, min(1.0, sum(x * y for x, y in zip(va, vb)))))
            n = int(math.ceil(math.degrees(ang) / step)) if ang > 1e-9 else 1
            if n > 1 and math.sin(ang) > 1e-9:
                for k in range(1, n):
                    t = k / n
                    s1, s2 = math.sin((1 - t) * ang) / math.sin(ang), math.sin(t * ang) / math.sin(ang)
                    x, y, z = (s1 * u + s2 * v for u, v in zip(va, vb))
                    lat = math.degrees(math.atan2(z, math.hypot(x, y)))
                    lon = math.degrees(math.atan2(y, x)) if math.hypot(x, y) > 1e-12 else b[0]
                    out.append([round(lon, 5), round(lat, 5)])
        out.append([p[0], p[1]] + p[2:])
    for i in range(1, len(out)):
        prev = out[i - 1][0]
        lon = out[i][0]
        lon += 360.0 * round((prev - lon) / 360.0)
        out[i][0] = round(lon, 5)
    return out


def display_geometry(g: dict) -> dict:
    """`display_line` over a LineString or each line of a MultiLineString."""
    if not isinstance(g, dict):
        return g
    if g.get("type") == "LineString":
        return {**g, "coordinates": display_line(g.get("coordinates") or [])}
    if g.get("type") == "MultiLineString":
        return {**g, "coordinates": [display_line(ln) for ln in g.get("coordinates") or []]}
    return g


def publish(root: Path, db: Path | None = None) -> dict | None:
    """Publish English and explicitly selected, reviewed locale variants."""
    from .localization import publish_locales
    return publish_locales(Path(root), Path(db or HISTORY_DB), _publish,
                           Path(os.environ.get('ARCTIC_HISTORY_TRANSLATIONS', HISTORY_DIR / 'translations.sqlite')))


def _publish(root: Path, db: Path | None = None, *, _out=None, _link_context=None) -> dict | None:
    """Render the wiki and the map layer into ``root/data/history/`` for the
    History tab, and copy the artifact files people can open. Returns the
    manifest entry, or None when there is no history database yet."""
    import shutil
    p = Path(db or HISTORY_DB)
    if not p.exists():
        return None
    c = connect(p, create=False)
    try:
        info, targets = _link_context if _link_context is not None else (reindex_links(c), index_targets(c))
        out = Path(_out) if _out is not None else root / "data" / "history"
        (out / "pages").mkdir(parents=True, exist_ok=True)

        # 1. the wiki: hand-written narrative pages and the generated ones
        pages, index = [], []
        written = [dict(r, ref="") for r in (dict(x) for x in c.execute(
            "SELECT slug, kind, title, topic, summary, body, ordering, status, people FROM pages ORDER BY ordering, title"))]
        for pg in written + generated_pages(c):
            back = [r["src"] for r in c.execute(
                "SELECT DISTINCT src FROM links WHERE target=? ORDER BY src", (pg["slug"],))]
            doc = {"slug": pg["slug"], "kind": pg["kind"], "title": pg["title"], "topic": pg.get("topic", ""),
                   "summary": pg.get("summary", ""), "ref": pg.get("ref", ""),
                   "status": pg.get("status", ""),
                   "people": json.loads(pg.get("people") or "[]"),
                   "html": render_markdown(pg["body"], targets), "backlinks": back}
            pages.append(doc)
            index.append({k: doc[k] for k in ("slug", "kind", "title", "topic", "summary", "status")})
        for doc in pages:
            atomic(out / "pages" / f"{doc['slug'].replace('/', '__')}.json", json.dumps(doc, ensure_ascii=False))

        # 2. the map layer: artifacts with a position or a geometry
        arts = []
        # the natural domain of an artifact: its topic's domain, and for the
        # natural half the domains of the subjects whose observations cite it
        # as evidence or whose names are among its tags, so a hub topic's
        # pictures fall into the domains they belong to rather than all of them
        topic_domain = {r["slug"]: r["domain"] or "history" for r in c.execute("SELECT slug, domain FROM topics")}
        subj_domain = {r["name"]: r["domain"] for r in c.execute("SELECT name, domain FROM subjects")}
        subj_by_tag = {slugify(r["name"]): r["domain"] for r in c.execute("SELECT name, domain FROM subjects")}
        obs_domains: dict[str, set] = {}
        for r in c.execute("SELECT artifact_id, subject FROM observations WHERE artifact_id<>''"):
            d = subj_domain.get(r["subject"])
            if d:
                obs_domains.setdefault(r["artifact_id"], set()).add(d)
        for r in c.execute(f"SELECT * FROM artifacts ORDER BY {date_order('date_start')}, id"):
            a = {k: r[k] for k in ("id", "topic", "type", "title", "date_text", "date_start", "creator",
                                   "description", "lat", "lon", "credit", "bibkey", "licence",
                                   "rights_note", "source_url", "local_file", "pages")}
            a["licence_label"] = licence_label(r["licence"])
            a["people"] = json.loads(r["people"] or "[]")
            a["tags"] = normalise_tags(r["tags"])
            for f in ("geometry", "waypoints"):
                if r[f]:
                    try:
                        a[f] = json.loads(r[f])
                    except json.JSONDecodeError:
                        log.warning("artifact %s has unreadable %s", r["id"], f)
            if a.get("geometry"):
                a["geometry"] = display_geometry(a["geometry"])
            a["page"] = page_slug("artifact", r["id"])
            a["routing"] = r["routing"] or ""
            a["keywords"] = artifact_keywords(c, r["id"])
            a["domain"] = topic_domain.get(r["topic"], "history")
            nat = set(obs_domains.get(r["id"], ()))
            nat |= {subj_by_tag[t] for t in a["tags"] if t in subj_by_tag}
            a["domains"] = sorted(nat)

            def ship(rel: str) -> str | None:
                src = HISTORY_DIR / rel
                if not src.is_file():
                    return None
                dest = root / "data" / "history" / "files" / Path(rel).name
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
                    shutil.copy2(src, dest)
                return f"data/history/files/{dest.name}"

            if withheld(r):
                # held for research under licence, or a whole work kept under
                # fair dealing: the record is published, the file is not, and a
                # copy left by an earlier publish is taken back
                for rel in (r["local_file"], r["view_file"]):
                    if rel:
                        (root / "data" / "history" / "files" / Path(rel).name).unlink(missing_ok=True)
            elif r["local_file"]:
                url = ship(r["local_file"])
                if url:
                    a["url"] = url
            if r["view_file"] and not withheld(r):
                # a raster view of a PDF, a page or a zipped GeoTIFF: the ship
                # thumbnails `url`; the original stays reachable as original_url
                view = ship(r["view_file"])
                if view:
                    if a.get("url"):
                        a["original_url"] = a["url"]
                    a["url"] = view
            arts.append(a)

        # 3. the timeline, and the topics that own everything
        events = [{**{k: r[k] for k in ("id", "topic", "date_text", "date_start", "date_end",
                                        "title", "detail", "lat", "lon", "place", "bibkey")},
                   "people": json.loads(r["people"] or "[]"), "tags": normalise_tags(r["tags"])}
                  for r in c.execute(f"SELECT * FROM events ORDER BY {date_order('date_start')}, id")]
        topics = [dict(r) for r in c.execute("SELECT slug, title, summary, status, domain FROM topics ORDER BY title")]
        for t in topics:
            t["artifacts"] = c.execute("SELECT COUNT(*) AS n FROM artifacts WHERE topic=?", (t["slug"],)).fetchone()["n"]
            t["pages"] = c.execute("SELECT COUNT(*) AS n FROM pages WHERE topic=?", (t["slug"],)).fetchone()["n"]
            t["observations"] = c.execute("SELECT COUNT(*) AS n FROM observations WHERE topic=?", (t["slug"],)).fetchone()["n"]

        # the timeline: every atomic date, with the spans of the time-limited
        # activities resolved into one row carrying both endpoints
        rows = [dict(r) for r in c.execute(
            f"SELECT * FROM dates ORDER BY {date_order('date')}, role DESC, id")]
        hidden = {r["id"] for r in c.execute("SELECT id FROM observations WHERE sensitive=1")}
        for r in rows:
            if r["entity_kind"] == "observation" and r["entity_id"] in hidden:
                r["lat"], r["lon"] = coarsen(r["lat"], r["lon"])
                r["place"] = ""
        spans: dict[str, dict] = {}
        timeline = []
        for r in rows:
            item = {k: r[k] for k in ("entity_kind", "entity_id", "topic", "date", "precision",
                                      "qualifier", "role", "span", "label", "lat", "lon",
                                      "place", "bibkey")}
            if r["span"] and r["role"] in ("start", "end"):
                held = spans.get(r["span"])
                if held is None:
                    item["date_end"] = ""
                    spans[r["span"]] = item
                    timeline.append(item)
                else:
                    held["date_end"] = r["date"]
                    held["precision_end"] = r["precision"]
                    continue
            else:
                timeline.append(item)
        for item in timeline:
            if item["date"].startswith("-"):
                item["display"] = date_display(item["date"])
                if item.get("date_end", "").startswith("-"):
                    item["display_end"] = date_display(item["date_end"])
        atomic(out / "timeline.json", json.dumps({"timeline": timeline}, ensure_ascii=False))
        atomic(out / "artifacts.json", json.dumps({"artifacts": arts}, ensure_ascii=False))

        # faces cut from the photographs, for the People page; unknown sitters last
        faces = []
        for r in c.execute("SELECT f.*, a.title FROM faces f JOIN artifacts a ON a.id=f.artifact_id "
                           "ORDER BY CASE WHEN f.person='' THEN 1 ELSE 0 END, f.person, f.artifact_id, f.n"):
            src = HISTORY_DIR / r["file"]
            if not src.is_file():
                continue
            dest = root / "data" / "history" / "files" / "faces" / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
                shutil.copy2(src, dest)
            faces.append({"artifact": r["artifact_id"], "page": page_slug("artifact", r["artifact_id"]),
                          "title": r["title"], "file": f"data/history/files/faces/{dest.name}",
                          "box": json.loads(r["box"]) if r["box"] else [],
                          "kind": r["kind"] or "person",
                          "person": r["person"] or "",
                          "person_page": page_slug(r["kind"] or "person", r["person"]) if r["person"] else "",
                          "confidence": r["confidence"], "method": r["method"] or ""})
        if faces:
            atomic(out / "faces.json", json.dumps({"faces": faces}, ensure_ascii=False))
        onto = get_ontology(c)
        if onto:
            atomic(out / "ontology.json", json.dumps(onto, ensure_ascii=False))
        atomic(out / "events.json", json.dumps({"events": events}, ensure_ascii=False))
        # the named places with their positions, machine-readable — an "in this
        # place" vignette wants coordinates, not just the generated wiki pages
        places = [{**{k: r[k] for k in ("name", "historic", "inuktitut", "lat", "lon",
                                        "kind", "note", "bibkey", "topic")},
                   "page": page_slug("place", r["name"])}
                  for r in c.execute("SELECT * FROM places ORDER BY name")]
        atomic(out / "places.json", json.dumps({"places": places}, ensure_ascii=False))
        people_rows = [{**{k: r[k] for k in ("name", "also", "role", "born", "died",
                                             "affiliation", "note", "topic")},
                        "indigenous": bool(r["indigenous"]),
                        "page": page_slug("person", r["name"])}
                       for r in c.execute("SELECT * FROM people ORDER BY name")]
        atomic(out / "people.json", json.dumps({"people": people_rows}, ensure_ascii=False))
        animal_rows = [{**{k: r[k] for k in ("name", "kind", "also", "role", "born", "died",
                                             "affiliation", "note", "topic")},
                        "page": page_slug("animal", r["name"])}
                       for r in c.execute("SELECT * FROM animals ORDER BY name")]
        atomic(out / "animals.json", json.dumps({"animals": animal_rows}, ensure_ascii=False))
        vessel_rows = [{**{k: r[k] for k in ("name", "kind", "kind_note", "also", "role", "built",
                                             "lost", "affiliation", "tonnage", "note", "topic")},
                        "kind_label": vessel_kind_label(r["kind"]),
                        "page": page_slug("vessel", r["name"])}
                       for r in c.execute("SELECT * FROM vessels ORDER BY name")]
        atomic(out / "vessels.json", json.dumps({"vessels": vessel_rows}, ensure_ascii=False))
        subject_rows, observation_rows = publish_nature(c, out)
        atomic(out / "index.json", json.dumps({"pages": index, "topics": topics,
                                               "wanted": info["wanted"]}, ensure_ascii=False))
        atomic(out / "references.bib", to_bibtex(c.execute("SELECT * FROM sources ORDER BY bibkey")))
        stamp = max([r["updated"] or "" for r in c.execute(
            "SELECT MAX(updated) AS updated FROM artifacts")] + [""]) or now()
        return {"file": "data/history/index.json", "stamp": stamp, "artifacts": len(arts), "faces": len(faces),
                "pages": len(pages), "events": len(events), "topics": len(topics),
                "places": len(places), "people": len(people_rows),
                "animals": len(animal_rows), "vessels": len(vessel_rows),
                "subjects": len(subject_rows), "observations": len(observation_rows),
                "dates": len(rows), "timeline": len(timeline),
                "sources": c.execute("SELECT COUNT(*) AS n FROM sources").fetchone()["n"],
                "wanted": len(info["wanted"])}
    finally:
        c.close()


def publish_nature(c, out: Path) -> tuple[list, list]:
    """The natural half's published files: ``subjects.json`` (every subject
    with its names and its record's size), ``observations.json`` (a map
    layer: points by subject and domain with the date and the number, so the
    map can play the season, the century and the value; sensitive rows
    coarsened to half a degree with the place blank), and the excerpts a
    small model aboard reads: one text per subject (the page body followed
    by its record as dated lines) and one per place with observations."""
    subjects = [dict(r) for r in c.execute("SELECT * FROM subjects ORDER BY name")]
    by_name = {s["name"]: s for s in subjects}
    obs_all = [dict(r) for r in c.execute(
        f"SELECT * FROM observations ORDER BY {date_order('date_start')}, id")]
    record: dict[str, list] = {}
    published = []
    for o in obs_all:
        o["tags"] = normalise_tags(o["tags"])
        s = by_name.get(o["subject"], {})
        o["domain"] = s.get("domain", "")
        o["kind"] = s.get("kind", "")
        o["subject_page"] = page_slug("subject", o["subject"])
        o["label"] = _observation_label(o)
        pub = dict(o)
        if o["sensitive"]:
            pub["lat"], pub["lon"] = coarsen(o["lat"], o["lon"])
            pub["place"] = ""
        published.append(pub)
        record.setdefault(o["subject"], []).append(pub)
    for s in subjects:
        s["page"] = page_slug("subject", s["name"])
        s["observations"] = len(record.get(s["name"], []))
        s["children"] = [x["name"] for x in subjects if x["parent"] == s["name"]]
    atomic(out / "subjects.json", json.dumps({"subjects": subjects}, ensure_ascii=False))
    atomic(out / "observations.json", json.dumps({"observations": published}, ensure_ascii=False))

    def line(o: dict) -> str:
        who = o["observer"] or o["vessel"] or ""
        where = o["place"] or (f"{o['lat']:.2f} {o['lon']:.2f}" if o["lat"] is not None else "")
        cite = o["bibkey"] + (f" {o['pages']}" if o["pages"] else "")
        return f"- {o['date_text'] or o['date_start']}: {o['label']}" + (f", {where}" if where else "") \
               + (f" ({who})" if who else "") + f". {o['detail']} [{cite}]"

    exc = out / "excerpts"
    exc.mkdir(parents=True, exist_ok=True)
    for s in subjects:
        names = "; ".join(x for x in (s["english"], s["french"], s["inuktitut"], s["kalaallisut"], s["also"]) if x)
        head = f"# {s['name']}" + (f" ({names})" if names else "") + f"\n{s['kind']}, {s['domain']}" \
               + (f", {s['unit']}" if s["unit"] else "") + (f"; status {s['status']}" if s["status"] else "") + "\n\n"
        body = (s["note"] or "").strip()
        rec = record.get(s["name"], [])
        text = head + body + ("\n\n## The record\n" + "\n".join(line(o) for o in rec) if rec else "") + "\n"
        atomic(exc / f"subject__{slugify(s['name'])}.txt", text)
    # one text per place: every observation placed there or within 25 km of it
    places = [dict(r) for r in c.execute("SELECT name, lat, lon, kind, note FROM places")]
    placed = [o for o in published if o["lat"] is not None]
    for p in places:
        near = [o for o in placed if o["place"] == p["name"]]
        if p["lat"] is not None:
            near += [o for o in placed if o["place"] != p["name"] and _near(p["lat"], p["lon"], o["lat"], o["lon"], 25)]
        if not near:
            continue
        near.sort(key=lambda o: (o["date_start"], o["id"]))
        text = f"# {p['name']}" + (f" ({p['kind']})" if p["kind"] else "") + "\n\n" + (p["note"] or "").strip() \
               + "\n\n## Observations here\n" + "\n".join(line(o) for o in near) + "\n"
        atomic(exc / f"place__{slugify(p['name'])}.txt", text)
    return subjects, published


def _near(lat1, lon1, lat2, lon2, km: float) -> bool:
    """Within km of each other, on the sphere."""
    from math import radians, sin, cos, asin, sqrt
    if None in (lat1, lon1, lat2, lon2):
        return False
    a = sin(radians(lat2 - lat1) / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371 * asin(sqrt(a)) <= km


def atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
