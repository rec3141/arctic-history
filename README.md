# Arctic history: the Amundsen's History and Nature wiki

The research behind the CCGS *Amundsen* dashboard's History and Nature tabs:
a database of the High Arctic's human past and natural record, written by
research agents on grid, and the code that publishes it as the wiki, map
layer, timeline and bibliography the ship shows, and that the ship's chat
crew reads.

## How it is made and used aboard

1. **Research (grid).** Grid, on the university network where publishers
   see a campus address, owns the database. Research agents, one per topic,
   work from `db/history/BRIEF.md`, fetch sources through the library proxy
   (`tools/history-fetch.py`) and write every source, artifact (image, map,
   quote), person, place, event, date, voyage track and wiki page through
   `tools/history-db.py`, the only writer. Topics are in two domains:
   history (voyages, Inuit oral history, stations, place names…) and nature
   (birds, polar bear, the sea ice, the water column, the sky…), where
   subjects and dated observations are recorded too.
2. **To the ship.** `tools/history-sync.sh pull` copies a snapshot of the
   database and rsyncs the fetched files to the ship (daily, by cron;
   objects over 100 MB are listed and fetched by name). The ship writes
   nothing to the database.
3. **Published.** The dashboard build calls `arctic_history.publish()`
   (through underway's `dashboard/history.py`), which exports the wiki, the
   map layer, the timeline, the bibliography and the natural record to
   `data/history/`, in English and in each reviewed translation. The History
   and Nature tabs render them.
4. **Read by the chat.** The ship's chat crew are personas of one local model
   (`dashboard/chatbot.py`): Ada, the Librarian, answers from the history
   half; Doc from the natural half and the ship's own measurements. Their
   prompts carry excerpts of the published pages most relevant to the
   question, and their answers cite those pages.
5. **Back to grid.** The Nature tab lets the ship record observations (and
   its photo import adds more) in an append-only journal,
   `db/history/_journal/`. `history-sync.sh push-journal` sends it to grid,
   where `history-db.py ingest --journal` writes it into the database. This
   is the one thing the ship sends.

Code moves through this repository; the database and the fetched files move
by rsync and are not committed.

## Layout

    arctic_history/            the schema, the writers and publish(); no dependencies
    arctic_history/localization.py   reviewed translations, published as frozen snapshots
    tools/history-db.py        the only way anything is written; also stats, check, resume, requests, ingest
    tools/history-fetch.py     the only way anything is downloaded: EZproxy, Scholars Portal, file checks
    tools/history-sync.sh      pull (grid -> ship), push-journal (ship -> grid), status
    tools/history-translations.py    review and release of translations (docs-localization.md)
    tools/faces.py, animal-crops.py  cut faces and animals out of the pictures
    tools/keywords.py          subject keywords for images, maps and quotes
    tools/digitize-tracks.py, route-tracks.py   voyage tracks from printed maps, routed through water and terrain
    tools/atlas.py, plates.py  figures in the layer's house style
    tools/library-search.py, mail-draft.py, requests-sync.py   the person's part (below)
    tools/usage.py             plan usage, as /usage shows it
    tools/ocr.sh               GPU OCR of scans (below)
    tests/                     test_history.py, test_localization.py
    db/history/BRIEF.md        the brief every researcher works from: read it first
    db/history/NATURE-DESIGN.md, KNOWLEDGE-TERMS.md   the nature half's design and vocabulary
    db/history/JOURNAL.md      the ship's journal format and ingest
    db/history/PROVENANCE.md   how the layer was made: the model's part, the review pass, the figures
    db/history/history.sqlite  the database (not committed)
    db/history/<topic>/        files/ (downloads), notes/ (extractions)
    db/history/_staging/       primary texts and cached lookups; MANIFEST.md lists them
    db/history/_ledger/        the EZproxy cookie jar and routing data

Python 3.8 is enough (`/usr/bin/python3`). `curl`, `file` and `rsync` are the
only other tools.

## Where things stand

    python3 tools/history-db.py stats                        counts of every kind of row
    python3 tools/history-db.py check                        problems to fix
    python3 tools/history-db.py wanted                       wikilinks to pages not yet written
    python3 tools/history-db.py requests --status open       what researchers are waiting on
    python3 tools/history-db.py resume --topic franklin-1845 one topic: counts, sources, artifacts,
                                                             pages, unregistered files, links owed,
                                                             problems, requests and its worklog

A topic is `open` until a researcher's run finishes it; the brief's last step
sets it to `drafted`, and `done` is set explicitly
(`history-db.py topic --slug <slug> --status done`). A new run on a topic
starts from `resume`.

## Running the researchers

Each researcher is a Claude Code subagent given the brief and one topic. It
writes everything to the database as it is found, with a worklog line after
every milestone, because runs get cut off. The prompt shape that works:

> Read db/history/BRIEF.md in full and follow it exactly. Your topic slug is
> `<slug>`. Run `tools/history-db.py resume --topic <slug>` and continue from
> the worklog. Write to the database as you go. Topic: <two paragraphs of
> scope, the named people to enter, which activities are spans, which
> voyages are tracks, what deserves its own page>.

Launch researchers with `model: opus`; Sonnet is fine for fetch-and-register
work. Five to eight at a time is comfortable: more hit Wikimedia's rate limit
and the API session limit. In a wave, mix image-heavy topics with text-heavy
ones (Commons rate-limits the shared campus address), and run hub topics that
others link to (inuit-oral-history above all) early, so wikilinks resolve
instead of piling up in `wanted`.

A wave may use no more than 80% of the five-hour usage window.
`python3 tools/usage.py` prints the same figures as `/usage` and exits 1 once
the five-hour window is past 80%: check it before each batch of launches and
as researchers finish, and stop launching until the window resets. The
weekly figure is the one to watch across days.

The brief's "Helpers and the web" section holds for every agent: each
launches only agents smaller than itself (Opus to Sonnet to Haiku; Haiku
launches nothing), Sonnet helpers are capped at 2 at once and 6 per run,
Haiku readers are uncapped, and pages are downloaded once and read from the
local copy, by Haiku if long, never re-read through WebFetch.

## The person's part

Researchers file requests for what they cannot do alone: API keys, titles the
library does not license, judgement calls. Before an access request they run
`tools/library-search.py` (UM catalogue: shelf copies and licensed platforms)
and, where the platform is Scholars Portal, pull the needed pages with
`tools/history-fetch.py --scholarsportal` under a crew-wide one-session-per-hour
gate. Hard copies to fetch by hand queue in `db/history/PICKUP-QUEUE.md`. The
review page lives at https://cryomics.org/amundsen/requests/ (basic auth; the
password hash is in `~/.amundsen-htpasswd` on dreamhost). Grid pushes the
queue there and collects the decisions every minute with
`tools/requests-sync.py pull` (cron), and `tools/backup.sh` snapshots the
database hourly to `db/history/_backups/` and to dreamhost:backups/amundsen/
(also cron). The CLI works too:

    python3 tools/history-db.py requests --status open
    python3 tools/history-db.py answer --id 7 --status approved --answer "fetched to franklin-1845/files/..."

## Access

The EZproxy signs in from this machine's address with no password, so
`history-fetch.py` reaches JSTOR, Cambridge Core, Wiley, Taylor and Francis
and the rest directly. Wikimedia rate-limits the campus address: send Commons
queries one at a time, and check the cached lookups in `_staging/` before
querying.

## Development

The tests run with the standard library alone:

    python3 -m unittest discover -s tests

or, in a virtualenv with the test extra (`pip install -e '.[test]'`):

    python3 -m pytest tests/

## OCR on grid

Raw scans get real OCR on this machine's GPU: `tools/ocr.sh <file.pdf|image>
[outdir]` (marker + surya in `.ocr-venv/`, a uv-managed Python 3.11). To
rebuild the environment:

    ~/.local/bin/uv venv .ocr-venv --python 3.11
    ~/.local/bin/uv pip install --python .ocr-venv/bin/python \
        "torch==2.5.1" --index-url https://download.pytorch.org/whl/cu121
    ~/.local/bin/uv pip install --python .ocr-venv/bin/python "marker-pdf==1.6.2"
    ~/.local/bin/uv pip install --python .ocr-venv/bin/python \
        "torch==2.5.1+cu121" "torchvision==0.20.1+cu121" \
        --index-url https://download.pytorch.org/whl/cu121   # again: marker's deps bump both

The pins matter: the GV100 is Volta, so torch must be a cu121 build (newer
wheels want a newer driver), and marker 1.6.x is the last torch-native
generation — marker 2 / surya 2 OCR through a vllm Docker server that does
not run on this card.
