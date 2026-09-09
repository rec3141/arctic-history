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
KINDS = ("page", "artifact", "source", "person", "place", "event", "topic", "animal", "vessel")
ARTIFACT_TYPES = ("image", "text", "track", "place", "event", "map", "quote", "object")
LICENCE_HINT = ("public domain", "crown copyright expired", "cc0", "cc by", "cc by-sa",
                "fair dealing", "all rights reserved", "unknown")

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
  entry_type  TEXT NOT NULL DEFAULT 'misc',
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
  archive     TEXT DEFAULT '',            -- holding institution
  language    TEXT DEFAULT '',            -- of the text as held (ISO 639-1: en, fr, da, no, de, iu...)
  orig_language TEXT DEFAULT '',          -- when the work is a translation
  translator  TEXT DEFAULT '',
  callno      TEXT DEFAULT '',            -- accession or catalogue number
  licence     TEXT DEFAULT '',
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
  licence     TEXT DEFAULT '',
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
  kind        TEXT DEFAULT '',             -- bomb vessel, steam whaler, schooner, icebreaker, Lancaster bomber
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

RASTER_SUFFIXES = (".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp")
ROUTING = ("", "water", "as-given")       # how a track's line is drawn: routed through water, or as its waypoints


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
        if "kind" not in {r[1] for r in c.execute("PRAGMA table_info(faces)")}:
            c.execute("ALTER TABLE faces ADD COLUMN kind TEXT NOT NULL DEFAULT 'person'")
        if "status" not in {r[1] for r in c.execute("PRAGMA table_info(pages)")}:
            c.execute("ALTER TABLE pages ADD COLUMN status TEXT NOT NULL DEFAULT 'draft'")
        for table, col, default in (("sources", "language", "''"), ("sources", "orig_language", "''"),
                                    ("sources", "translator", "''"), ("artifacts", "language", "''"),
                                    ("pages", "language", "'en'"),
                                    ("artifacts", "view_file", "''"), ("artifacts", "routing", "''"),
                                    ("pages", "people", "'[]'")):
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


def _iso(v: str) -> str:
    """The sortable form of a date written as a year, a month or a full date.
    A range ("1845/1848") yields its first date; anything unparseable is ''."""
    s = str(v or "").strip().split("/")[0].strip()
    m = re.match(r"^(-?\d{1,4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?$", s)
    if not m:
        m2 = re.search(r"\b(\d{3,4})\b", s)
        return f"{int(m2.group(1)):04d}" if m2 else ""
    y, mo, d = m.group(1), m.group(2), m.group(3)
    out = f"{int(y):04d}" if not y.startswith("-") else y
    if mo:
        out += f"-{int(mo):02d}"
        if d:
            out += f"-{int(d):02d}"
    return out


def date_order(col: str) -> str:
    """An ORDER BY expression that puts ISO dates in calendar order even when
    some are BC: '-2500' before '-1900' before '0001'. Text order alone gets
    BC backwards, which the thule-dorset run noticed in its timeline."""
    return (f"CASE WHEN substr({col},1,1)='-' THEN -CAST(substr({col},2,4) AS INTEGER) "
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
    for f in ("summary", "researcher", "status"):
        if kw.get(f) not in (None, ""):
            row[f] = kw[f]
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
    return _upsert(c, "topics", "slug", row)


def add_source(c, bibkey: str, title: str, **kw) -> str:
    key = re.sub(r"[^a-z0-9]", "", str(bibkey).lower()) or slugify(title).replace("-", "")
    row = {"bibkey": key, "title": title, "entry_type": kw.get("entry_type", "misc")}
    for f in ("author", "year", "container", "publisher", "address", "volume", "pages", "url",
              "urldate", "doi", "archive", "callno", "licence", "note", "local_file", "topic",
              "language", "orig_language", "translator"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
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
           "people": _json_list(kw.get("people")), "tags": _json_list(kw.get("tags")),
           "lat": None if kw.get("lat") in (None, "") else float(kw["lat"]),
           "lon": None if kw.get("lon") in (None, "") else float(kw["lon"])}
    for f in ("creator", "description", "source_url", "download_url", "local_file",
              "licence", "credit", "bibkey", "pages", "language", "view_file", "routing"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
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
    if row["lat"] is None and not row.get("geometry"):
        raise ValueError("an artifact needs a lat/lon, or a geometry if it is a track")
    prev = c.execute("SELECT date_start, date_end, title FROM artifacts WHERE id=?", (row["id"],)).fetchone()
    out = _upsert(c, "artifacts", "id", row)
    _record_dates(c, "artifact", out, row["date_start"], row["date_end"], date_text,
                  old=dict(prev) if prev else None,
                  topic=row["topic"], label=title, lat=row["lat"], lon=row["lon"],
                  bibkey=row.get("bibkey", ""))
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
              "source": ("sources", "bibkey")}
    if kind not in tables:
        raise ValueError(f"kind must be date or one of {', '.join(tables)}")
    table, key = tables[kind]
    r = c.execute(f"SELECT * FROM {table} WHERE {key}=?", (ident,)).fetchone()
    if not r:
        raise ValueError(f"no {kind} {ident!r}")
    if kind == "source":
        users = [t for t in ("artifacts", "events", "people", "places")
                 if c.execute(f"SELECT 1 FROM {t} WHERE bibkey=? LIMIT 1", (ident,)).fetchone()]
        if users:
            raise ValueError(f"source {ident!r} is still cited by rows in {', '.join(users)}; re-point them first")
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
    summary = kw.get("summary", "")
    if old and (old["body"] != body or old["title"] != title or old["summary"] != summary):
        c.execute("INSERT INTO page_history (slug, title, summary, body, status, saved) "
                  "VALUES (?,?,?,?,?,?)",
                  (s, old["title"], old["summary"], old["body"], old["status"], now()))
    row = {"slug": s, "kind": kind if kind in KINDS else "page", "title": title, "body": body,
           "topic": slugify(kw["topic"]) if kw.get("topic") else "",
           "summary": summary, "ordering": int(kw.get("ordering", 100)), "status": status,
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
           "indigenous": 1 if kw.get("indigenous") or (old and old["indigenous"]) else 0}
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
    for f in ("kind", "also", "role", "born", "died", "affiliation", "note", "bibkey", "topic"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    return _upsert(c, "animals", "name", row)


def add_vessel(c, name: str, **kw) -> str:
    """A ship, boat or aircraft, by the name it is usually written under."""
    kw = _keep_home_topic(c, "vessels", name, kw)
    row = {"name": name.strip()}
    for f in ("kind", "also", "role", "built", "lost", "affiliation", "tonnage", "note", "bibkey", "topic"):
        if kw.get(f) is not None:
            row[f] = str(kw[f])
    return _upsert(c, "vessels", "name", row)


def add_event(c, topic: str, date: str, title: str, **kw) -> int:
    row = {"topic": slugify(topic), "date_text": str(date), "date_start": _iso(date),
           "date_end": _iso(kw.get("date_end", "")), "title": title,
           "detail": kw.get("detail", ""), "place": kw.get("place", ""),
           "bibkey": kw.get("bibkey", ""), "people": _json_list(kw.get("people")),
           "tags": _json_list(kw.get("tags")), "updated": now(),
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
    for table in ("sources", "artifacts", "pages", "people", "places", "events"):
        counts[table] = c.execute(f"SELECT COUNT(*) AS n FROM {table} WHERE topic=?", (t,)).fetchone()["n"]
    counts["tracks"] = c.execute("SELECT COUNT(*) AS n FROM artifacts WHERE topic=? AND type='track'", (t,)).fetchone()["n"]
    counts["dates"] = c.execute("SELECT COUNT(*) AS n FROM dates WHERE topic=?", (t,)).fetchone()["n"]
    files_dir = HISTORY_DIR / t / "files"
    files = sorted(p.name for p in files_dir.iterdir()) if files_dir.is_dir() else []
    registered = {Path(r["local_file"]).name for r in c.execute(
        "SELECT local_file FROM artifacts WHERE topic=? AND local_file<>''", (t,))}
    registered |= {Path(r["local_file"]).name for r in c.execute(
        "SELECT local_file FROM sources WHERE topic=? AND local_file<>''", (t,))}
    log = [dict(r) for r in c.execute("SELECT * FROM worklog WHERE topic=? ORDER BY id DESC LIMIT 12", (t,))]
    reindex_links(c)
    wanted = [dict(r) for r in c.execute(
        "SELECT l.kind, l.name, l.src FROM links l JOIN pages p ON p.slug=l.src "
        "WHERE p.topic=? AND l.target='' ORDER BY l.kind, l.name", (t,))]
    problems = [p for p in validate(c)["problems"]
                if p["what"].startswith(t) or p["what"] in {r["bibkey"] for r in c.execute(
                    "SELECT bibkey FROM sources WHERE topic=?", (t,))}]
    return {"topic": dict(row) if row else None, "counts": counts, "files": files,
            "requests": list_requests(c, topic=t),
            "unregistered_files": [f for f in files if f not in registered],
            "worklog": log, "wanted": wanted, "problems": problems,
            "artifacts": [dict(r) for r in c.execute(
                "SELECT id, type, date_text, title FROM artifacts WHERE topic=? ORDER BY id", (t,))],
            "pages": [dict(r) for r in c.execute(
                "SELECT slug, title, ordering, status, length(body) AS words FROM pages WHERE topic=? ORDER BY ordering", (t,))],
            "sources": [dict(r) for r in c.execute(
                "SELECT bibkey, year, title FROM sources WHERE topic=? ORDER BY bibkey", (t,))]}


# ---------------------------------------------------------------- BibTeX
BIB_FIELDS = {"author": "author", "title": "title", "year": "year", "journal": "container",
              "booktitle": "container", "publisher": "publisher", "address": "address",
              "volume": "volume", "pages": "pages", "url": "url", "urldate": "urldate",
              "doi": "doi", "note": "note", "institution": "publisher", "school": "publisher",
              "organization": "publisher", "howpublished": "note", "series": "container"}


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
        fields.append(("journal" if et == "article" else "booktitle", r["container"]))
        for name, col in (("publisher", "publisher"), ("address", "address"), ("volume", "volume"),
                          ("pages", "pages"), ("doi", "doi"), ("url", "url"), ("urldate", "urldate")):
            fields.append((name, r[col]))
        note = "; ".join(x for x in (r["archive"], r["callno"], r["licence"], r["note"]) if x)
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
    for k in [k for k in mention if " " not in k and k in inside]:
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
    c.commit()
    return {"links": n, "pages": len(rows), "wanted": wanted}


def render_markdown(body: str, targets: dict, base: str = "") -> str:
    """Wikilinks become ordinary Markdown links; everything else is left for
    the page to render. A wanted link is marked so it reads as a gap."""
    def sub(m):
        kind, name = link_parts(m.group(1))
        slug = resolve(targets, kind, name)
        label = m.group(2)
        if not label:
            # an artifact id and a bibkey are opaque, so a link without a label
            # of its own shows the thing's title instead
            label = targets["names"].get(slug, name) if kind in ("artifact", "source") else (name if kind else m.group(1))
        if not slug:
            return f'<span class="wanted" title="no page yet">{label}</span>'
        return f'[{label}]({base}{slug})'
    return LINK_RX.sub(sub, body or "")


# ---------------------------------------------------------------- generated pages
def artifact_body(r: sqlite3.Row) -> str:
    """The generated page for one artifact: what it is, where it is, who to
    credit, and the source to follow."""
    lines = [r["description"] or ""]
    facts = []
    if r["date_text"]:
        facts.append(f"**Date** {r['date_text']}")
    if r["creator"]:
        facts.append(f"**Creator** {r['creator']}")
    if r["lat"] is not None:
        facts.append(f"**Position** {r['lat']:.4f}, {r['lon']:.4f}")
    if r["licence"]:
        facts.append(f"**Licence** {r['licence']}")
    if facts:
        lines += ["", " · ".join(facts)]
    if r["credit"]:
        lines += ["", f"**Credit** {r['credit']}"]
    if r["bibkey"]:
        pages = f", {r['pages']}" if r["pages"] else ""
        lines += ["", f"**Source** [[source:{r['bibkey']}]]{pages}"]
    people = json.loads(r["people"] or "[]")
    if people:
        lines += ["", "**People** " + ", ".join(f"[[person:{p}]]" for p in people)]
    if r["source_url"]:
        lines += ["", f"[At the holding institution]({r['source_url']})"]
    return "\n".join(lines).strip()


def source_body(r: sqlite3.Row) -> str:
    lines = []
    cite = ", ".join(x for x in (r["author"], f"*{r['title']}*", r["container"], r["publisher"], r["year"]) if x)
    lines.append(cite + ".")
    if r["archive"] or r["callno"]:
        lines += ["", "**Held at** " + ", ".join(x for x in (r["archive"], r["callno"]) if x)]
    if r["licence"]:
        lines += ["", f"**Copyright** {r['licence']}"]
    if r["note"]:
        lines += ["", r["note"]]
    lines += ["", "**Kind** " + ("primary source" if r["primary_src"] else "secondary source")]
    if r["url"]:
        lines += ["", f"[Read it]({r['url']})"]
    return "\n".join(lines).strip()


def person_body(r: sqlite3.Row) -> str:
    lines = []
    head = " · ".join(x for x in (r["role"], r["affiliation"],
                                  f"{r['born']}–{r['died']}" if (r["born"] or r["died"]) else "") if x)
    if head:
        lines.append(head)
    if r["also"]:
        lines += ["", f"Also written {r['also']}."]
    if r["note"]:
        lines += ["", r["note"]]
    if r["bibkey"]:
        lines += ["", f"**Source** [[source:{r['bibkey']}]]"]
    return "\n".join(lines).strip()


def place_body(r: sqlite3.Row) -> str:
    lines = []
    names = [x for x in (r["inuktitut"], r["historic"]) if x]
    if names:
        lines.append("Also " + ", ".join(names) + ".")
    if r["lat"] is not None:
        lines += ["", f"**Position** {r['lat']:.4f}, {r['lon']:.4f}"]
    if r["kind"]:
        lines += ["", f"**Kind** {r['kind']}"]
    if r["note"]:
        lines += ["", r["note"]]
    if r["bibkey"]:
        lines += ["", f"**Source** [[source:{r['bibkey']}]]"]
    return "\n".join(lines).strip()


def animal_body(r: sqlite3.Row) -> str:
    lines = []
    head = " · ".join(x for x in (r["kind"], r["role"], r["affiliation"],
                                  f"{r['born']}–{r['died']}" if (r["born"] or r["died"]) else "") if x)
    if head:
        lines.append(head)
    if r["also"]:
        lines += ["", f"Also called {r['also']}."]
    if r["note"]:
        lines += ["", r["note"]]
    if r["bibkey"]:
        lines += ["", f"**Source** [[source:{r['bibkey']}]]"]
    return "\n".join(lines).strip()


def vessel_body(r: sqlite3.Row) -> str:
    lines = []
    head = " · ".join(x for x in (r["kind"], r["affiliation"], r["tonnage"]) if x)
    if head:
        lines.append(head)
    if r["role"]:
        lines += ["", r["role"]]
    if r["built"]:
        lines += ["", f"**Built** {r['built']}"]
    if r["lost"]:
        lines += ["", f"**Fate** {r['lost']}"]
    if r["also"]:
        lines += ["", f"Also {r['also']}."]
    if r["note"]:
        lines += ["", r["note"]]
    if r["bibkey"]:
        lines += ["", f"**Source** [[source:{r['bibkey']}]]"]
    return "\n".join(lines).strip()


def event_body(r: sqlite3.Row) -> str:
    lines = []
    when = r["date_text"] or (r["date_start"] + (f" to {r['date_end']}" if r["date_end"] else ""))
    head = " \u00b7 ".join(x for x in (when, r["place"]) if x)
    if head:
        lines.append(head)
    if r["detail"]:
        lines += ["", r["detail"]]
    people = json.loads(r["people"] or "[]")
    if people:
        lines += ["", "People: " + ", ".join(f"[[person:{x}]]" for x in people) + "."]
    if r["place"]:
        lines += ["", f"Place: [[place:{r['place']}]]."]
    if r["bibkey"]:
        lines += ["", f"Source: [[source:{r['bibkey']}]]."]
    if r["topic"]:
        lines += ["", f"Topic: [[topic:{r['topic']}]]."]
    return "\n".join(lines)


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


def _off_map(lat, lon) -> str | None:
    """A coordinate nothing in this history can honestly carry. Pins may sit
    well south of the Arctic — the voyages sailed from London and New York,
    Munk from Copenhagen, Kane died in Havana — but nothing lies south of 20
    or east of 40, and a longitude in the mirror band east of 40 is almost
    always a dropped minus sign. The one exception is the far side of the
    dateline, 160-180 east: the Karluk's people and Bartlett's walk reached
    the Siberian coast, and those positions are honestly east."""
    if lat is not None and not 20 <= lat <= 90:
        return f"latitude {lat} is south of anywhere this history reaches"
    if lon is not None and not (-180 <= lon <= 40 or 160 <= lon <= 180):
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
    dry land in the wrong hemisphere, a page that links nowhere."""
    problems: list[dict] = []

    def bad(kind, what, detail):
        problems.append({"kind": kind, "what": what, "detail": detail})

    keys = {r["bibkey"] for r in c.execute("SELECT bibkey FROM sources")}
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
        msg = None if "east-verified" in (r["tags"] or "") else _off_map(r["lat"], r["lon"])
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
                        msg = _off_map(pt[1], pt[0])
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
                        msg = _off_map(p.get("lat"), p.get("lon"))
                        if msg:
                            bad("artifact", r["id"], f"waypoint {i} ({p.get('date', 'undated')}): {msg}")
                            break
            except (json.JSONDecodeError, ValueError):
                bad("artifact", r["id"], "waypoints is not a JSON array")
    for r in c.execute("SELECT bibkey, title, licence, url FROM sources"):
        if not r["licence"]:
            bad("source", r["bibkey"], "no copyright status")
        if not r["url"]:
            bad("source", r["bibkey"], "no URL")
    for r in c.execute("SELECT name, lat, lon FROM places WHERE lat IS NOT NULL"):
        msg = _off_map(r["lat"], r["lon"])
        if msg:
            bad("place", r["name"], msg)
    for r in c.execute("SELECT id, title, lat, lon FROM events WHERE lat IS NOT NULL"):
        msg = _off_map(r["lat"], r["lon"])
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
             for t in ("topics", "sources", "artifacts", "pages", "people", "places", "events", "dates")}
    return {"problems": problems, "stats": stats}


# ---------------------------------------------------------------- publish
def publish(root: Path, db: Path | None = None) -> dict | None:
    """Render the wiki and the map layer into ``root/data/history/`` for the
    History tab, and copy the artifact files people can open. Returns the
    manifest entry, or None when there is no history database yet."""
    import shutil
    p = Path(db or HISTORY_DB)
    if not p.exists():
        return None
    c = connect(p, create=False)
    try:
        info = reindex_links(c)
        targets = index_targets(c)
        out = root / "data" / "history"
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
        for r in c.execute(f"SELECT * FROM artifacts ORDER BY {date_order('date_start')}, id"):
            a = {k: r[k] for k in ("id", "topic", "type", "title", "date_text", "date_start", "creator",
                                   "description", "lat", "lon", "credit", "bibkey", "licence",
                                   "source_url", "local_file", "pages")}
            a["people"] = json.loads(r["people"] or "[]")
            a["tags"] = json.loads(r["tags"] or "[]")
            for f in ("geometry", "waypoints"):
                if r[f]:
                    try:
                        a[f] = json.loads(r[f])
                    except json.JSONDecodeError:
                        log.warning("artifact %s has unreadable %s", r["id"], f)
            a["page"] = page_slug("artifact", r["id"])
            a["routing"] = r["routing"] or ""
            a["keywords"] = artifact_keywords(c, r["id"])

            def ship(rel: str) -> str | None:
                src = HISTORY_DIR / rel
                if not src.is_file():
                    return None
                dest = out / "files" / Path(rel).name
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
                    shutil.copy2(src, dest)
                return f"data/history/files/{dest.name}"

            if r["local_file"]:
                url = ship(r["local_file"])
                if url:
                    a["url"] = url
            if r["view_file"]:
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
                   "people": json.loads(r["people"] or "[]"), "tags": json.loads(r["tags"] or "[]")}
                  for r in c.execute(f"SELECT * FROM events ORDER BY {date_order('date_start')}, id")]
        topics = [dict(r) for r in c.execute("SELECT slug, title, summary, status FROM topics ORDER BY title")]
        for t in topics:
            t["artifacts"] = c.execute("SELECT COUNT(*) AS n FROM artifacts WHERE topic=?", (t["slug"],)).fetchone()["n"]
            t["pages"] = c.execute("SELECT COUNT(*) AS n FROM pages WHERE topic=?", (t["slug"],)).fetchone()["n"]

        # the timeline: every atomic date, with the spans of the time-limited
        # activities resolved into one row carrying both endpoints
        rows = [dict(r) for r in c.execute(
            f"SELECT * FROM dates ORDER BY {date_order('date')}, role DESC, id")]
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
            dest = out / "files" / "faces" / src.name
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
        vessel_rows = [{**{k: r[k] for k in ("name", "kind", "also", "role", "built", "lost",
                                             "affiliation", "tonnage", "note", "topic")},
                        "page": page_slug("vessel", r["name"])}
                       for r in c.execute("SELECT * FROM vessels ORDER BY name")]
        atomic(out / "vessels.json", json.dumps({"vessels": vessel_rows}, ensure_ascii=False))
        atomic(out / "index.json", json.dumps({"pages": index, "topics": topics,
                                               "wanted": info["wanted"]}, ensure_ascii=False))
        atomic(out / "references.bib", to_bibtex(c.execute("SELECT * FROM sources ORDER BY bibkey")))
        stamp = max([r["updated"] for r in c.execute(
            "SELECT MAX(updated) AS updated FROM artifacts")] + [""]) or now()
        return {"file": "data/history/index.json", "stamp": stamp, "artifacts": len(arts), "faces": len(faces),
                "pages": len(pages), "events": len(events), "topics": len(topics),
                "places": len(places), "people": len(people_rows),
                "animals": len(animal_rows), "vessels": len(vessel_rows),
                "dates": len(rows), "timeline": len(timeline),
                "sources": c.execute("SELECT COUNT(*) AS n FROM sources").fetchone()["n"],
                "wanted": len(info["wanted"])}
    finally:
        c.close()


def atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
