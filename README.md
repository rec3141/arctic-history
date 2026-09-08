# Arctic history: the CCGS Amundsen's History tab

This repository holds both halves of the Amundsen dashboard's History tab: the
research backend described below, and the front end that renders the database
into a map, a timeline and a wiki that a local model reads. The front end is
developed on the ship and lands in its own directory alongside these.

The research runs on grid, on the university network, where publishers see a
campus address. Grid owns the database; the ship is read-only toward grid and
pulls the database and files with `tools/history-sync.sh pull` for the
dashboard build. Code moves through this repository; the database and the
fetched files are not committed — they move by rsync.

## The research backend

    arctic_history/            the schema and the writers; standalone, no dependencies
    tools/history-db.py        the only way anything is written: topics, sources, artifacts,
                               tracks, people, places, events, spans, dates, wiki pages,
                               worklog, requests
    tools/history-fetch.py     the only way anything is downloaded: EZproxy, file checks
    tools/history-sync.sh      grid -> ship, pull only
    tests/test_history.py      python3 -m unittest tests.test_history
    db/history/BRIEF.md        the brief every researcher works from: READ THIS FIRST
    db/history/history.sqlite  the database
    db/history/<topic>/        files/ (downloads), notes/ (extractions), RESUME.md (first-run leftovers)
    db/history/_staging/       primary texts fetched by the first runs; MANIFEST.md lists them
    db/history/_ledger/        the EZproxy cookie jar

Python 3.8 is enough (`/usr/bin/python3`). `curl`, `file` and `rsync` are the
only other tools.

## How the work is organised

Twenty-three topics, one researcher each, all writing into the one database
through the CLI. The brief is the contract: it says what to enter, in what
form, and above all that everything is written to the database as it is
found, with a worklog line after every milestone, because runs get cut off.
This is the third attempt: the first two lost hours of research by writing
nothing until the end.

To see where a topic stands:

    python3 tools/history-db.py resume --topic franklin-1845

It prints the counts, the sources, the artifacts, the pages, the unregistered
files, the links owed, the problems, the requests, and the worklog. A new run
starts from that.

To see the whole:

    python3 tools/history-db.py stats
    python3 tools/history-db.py check
    python3 tools/history-db.py wanted
    python3 tools/history-db.py requests --status open

## Starting the researchers

Each researcher is a Claude Code subagent given the brief and one topic. The
prompt shape that works:

> Read db/history/BRIEF.md in full and follow it exactly. Your topic slug is
> `<slug>`. Run `tools/history-db.py resume --topic <slug>` and continue from
> the worklog. Write to the database as you go. Topic: <two paragraphs of
> scope, the named people to enter, which activities are spans, which
> voyages are tracks, what deserves its own page>.

Opus handles a topic well; Sonnet is fine for the fetch-and-register parts.
Twenty at once hit Wikimedia's rate limit and the API session limit; five to
eight at a time is comfortable. When picking a wave, mix image-heavy topics
with text-heavy ones (Commons rate-limits the shared campus address), and run
hub topics that everyone links to — inuit-oral-history above all — early, so
other topics' wikilinks resolve instead of piling up in `wanted`.

The topics and the status of each:

| slug | status |
| --- | --- |
| davis-baffin-hudson, ross-parry, kane-hall-polaris, amundsen-gjoa, franklin-1845 | researched on the ship; rows in, no wiki pages yet; each topic's last worklog line says what its next run should do |
| inuit-oral-history | 13 files (Boas, Inuit-drawn charts), nothing in the database |
| frobisher | 14 files (Best, White portraits, maps), nothing in the database |
| nares-greely | 20 files, nothing in the database |
| sverdrup-bernier-peary | 21 files, nothing in the database |
| norse-helluland | 6 texts, nothing in the database |
| ross-victory | 3 texts (Ross 1835 and Huish), nothing in the database |
| relocations-qtc | 9 QTC reports and RCAP 1994 staged, nothing in the database |
| posts-rcmp-missions | RCMP reports 1921-25, Nascopie, staged; nothing in the database |
| franklin-search, mcclure-investigator, karluk-cae, whaling, thule-dorset, wrecks-disasters, greenland-inughuit, science-stations, st-roch-modern, hudson-strait-south-baffin | topic rows only |

## The person's part

Researchers file requests for what they cannot do alone: API keys, titles the
library does not license, judgement calls. The review page lives at
https://cryomics.org/amundsen/requests/ (basic auth; the password hash is in
`~/.amundsen-htpasswd` on dreamhost). Grid pushes the queue there and collects
the decisions every minute with `tools/requests-sync.py pull` (cron), and
`tools/backup.sh` snapshots the database hourly to `db/history/_backups/` and
to dreamhost:backups/amundsen/ (also cron). The CLI works too:

    python3 tools/history-db.py requests --status open
    python3 tools/history-db.py answer --id 7 --status approved --answer "fetched to franklin-1845/files/..."

## Sending it back

From the ship, `tools/history-sync.sh pull` takes a consistent snapshot of
this database, installs it, and rsyncs the files — compressed, resumable,
and gated at 100 MB per object (Starlink-sized; `HISTORY_SYNC_MAX` overrides).
Anything larger is held on grid and listed at the end of the pull, to be
fetched by name: `history-sync.sh pull <topic>/files/<name>`. Run it from
cron daily aboard. The dashboard build then publishes the wiki, the map
layer, the timeline and the bibliography under `data/history/`. Nothing here
needs to know about the dashboard.

## Access

The EZproxy signs in from this machine's address with no password, so
`history-fetch.py` reaches JSTOR, Cambridge Core, Wiley, Taylor and Francis
and the rest directly. Wikimedia rate-limits the campus address: send Commons
queries one at a time, and check the cached lookups in `_staging/` before
querying.

## Development

The tests run with the standard library alone:

    python3 -m unittest tests.test_history

or, in a virtualenv with the test extra (`pip install -e '.[test]'`):

    python3 -m pytest tests/test_history.py

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
