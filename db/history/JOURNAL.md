# The ship's journal: entry aboard, for the front end

Grid owns the database and the ship pulls. What the ship writes is a
**journal**: an append-only file of observation lines in the CLI's own
vocabulary, one JSON object per line, under `db/history/_journal/` on the
ship, named by month (`2026-09.jsonl`) with pictures beside it under
`_journal/img/`. `tools/history-sync.sh push-journal` is the one ship-to-grid
path: it rsyncs `_journal/` up to grid's `db/history/_journal/incoming/`,
where `tools/history-db.py ingest --journal <file>` turns each line into rows
through the same writers as everything else, so `check` and the brief's rules
apply. Ingest is idempotent on `id`: a corrected line with the same id
replaces the row on the next ingest. A line that fails is reported with its
line number and reason, and the rest go in.

## A line

    {"kind": "observation", "id": "amundsen-2026-09-11-003", "subject": "Balaena mysticetus",
     "date": "2026-09-11T14:22Z", "lat": 76.104, "lon": -92.41, "count": "1",
     "method": "sighting", "observer": "<crew name>", "vessel": "CCGS Amundsen",
     "detail": "A bowhead surfaced twice off the port bow and sounded.",
     "artifact_file": "_journal/img/2026-09-11-003.jpg", "origin": "ship"}

    {"kind": "observation", "id": "amundsen-2026-09-12-004", "subject": "aurora",
     "date": "2026-09-12T03:10Z", "lat": 76.2, "lon": -92.6, "qualifier": "first of the season",
     "method": "sighting", "observer": "<crew name>", "detail": "Three arcs through the zenith, green, for forty minutes."}

    {"kind": "observation", "id": "amundsen-2026-09-12-005", "subject": "water temperature",
     "date": "2026-09-12T09:00Z", "lat": 79.9, "lon": -71.2, "depth": 300, "value": 1.9, "unit": "C",
     "method": "instrument", "instrument": "CTD", "qualifier": "warmest Atlantic water seen this cruise",
     "detail": "Cast 2026-0417, the temperature maximum at 300 m in Nares Strait."}

Fields, all as `history-db.py observation --help` describes them:

| field | required | notes |
|---|---|---|
| `kind` | | `observation` (the default) or `subject` |
| `id` | yes | `amundsen-<YYYY-MM-DD>-<nnn>`; never reused; a corrected line keeps the id |
| `subject` | yes | any of the subject's names in `subjects.json`: the scientific name, English, French, Inuktitut, Kalaallisut, or a synonym |
| `date` | yes | ISO; the ship's clock, UTC |
| `lat`, `lon` | yes | the ship's GPS, or where the thing was |
| `place` | | a place row's name, when it applies |
| `depth`, `height` | | metres below or above the surface |
| `value`, `unit` | | the number and its unit as read; a variable subject wants them |
| `count` | | living things: `"1"`, `"about 200"`, `"a pod"` |
| `qualifier` | | `"first of the season"`, `"no bottom at"` |
| `stage`, `sex`, `behaviour` | | living things |
| `method` | | a code: `sighting`, `instrument`, `sounding`, `camera`, `acoustic`, `edna`, `net`, `trawl`, `dredge`, `core`, `sample`, `station-record` ... |
| `instrument` | | the CTD, the multibeam, the binoculars |
| `observer` | yes in practice | the crew member's name as they want it credited, or `"the bridge watch"` |
| `vessel` | | `CCGS Amundsen` |
| `detail` | yes | the sentence that says what was seen |
| `confidence` | | `certain`, `probable`, `doubtful` |
| `sensitive` | | `1` for a den, a nest, a haul-out, a calving ground: published coarsened |
| `artifact_file` | | a photograph beside the journal, written aboard as `_journal/img/<name>`; ingest resolves it against the journal file's own directory (so it is found under `_journal/incoming/img/` on grid) and registers it as an image artifact credited to the observer; a line whose photograph is not there fails with that reason |
| `licence` | | for the photograph; defaults to `attribution` with the photographer credited |
| `origin` | | `ship` (the default at ingest) or `crew` |
| `topic` | | defaults to `ship-journal`; the ingest declares the topic and the dataset source `amundsenjournal` if they do not exist |
| `bibkey` | | defaults to `amundsenjournal`; a remarkable reading from a ship system may cite its cruise report instead |
| `event_id` | | the human-history event this also is |

A `subject` line adds a subject the picker did not have, and needs the same
fields as `history-db.py subject`: `name`, `kind`, `domain`, and the names.
Prefer asking grid to add one; the ship's line is for the walrus nobody put
in the list before the cruise.

## What the tab does with it

The entry form writes the line: position from the GPS, time from the clock,
the subject picked from the published `subjects.json` (Inuktitut and French
names in the picker, domain as a filter), a photograph attached, sensitive
sightings marked. @doc's model does the same from a sentence in the chat,
fills the position and time, matches the subject by any of its names, and
asks for confirmation before appending. The journal is flat on purpose so a
local model produces it reliably; the writer on grid does the strict
validation, and a line that fails ingest comes back to the ship's log as a
problem to fix, not a silent drop.

What the ship does not journal: the CTD casts, the multibeam, the met
station, the ice radar. Those have their own systems. A remarkable reading
from any of them is journalled as an observation with the cast or file id in
`detail`, so the page can point at it.

## What the ship reads back

After the next pull, `data/history/observations.json` carries the sighting
as a point with its subject, domain, date and value beside Parry's parhelia
of 1820; the subject's page lists it in **the record**; the timeline shows it
as an `observation`; and `data/history/excerpts/subject__<slug>.txt` and
`place__<slug>.txt` hold the subject's and the place's whole record as one
text for @doc and @ada.
