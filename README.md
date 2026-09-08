# Arctic history research: the grid copy

This directory is the research half of the CCGS Amundsen dashboard's History
tab. The research runs here, on the university network, where publishers see a
campus address and the ship's satellite link is not in the way. The dashboard
on the ship pulls the database and the files back with `tools/history-sync.sh`
and renders them into a map, a timeline and a wiki that a local model reads.

## What is here

    dashboard/history.py       the schema and the writers; standalone, no other module needed
    tools/history-db.py        the only way anything is written: topics, sources, artifacts,
                               tracks, people, places, events, spans, dates, wiki pages,
                               worklog, requests
    tools/history-fetch.py     the only way anything is downloaded: routes, EZproxy,
                               the 50 MB rule, the 10 GB/day ledger, file checks
    tools/history-sync.sh      ship <-> grid
    tests/test_history.py      python3 -m pytest tests/test_history.py
    db/history/BRIEF.md        the brief every researcher works from: READ THIS FIRST
    db/history/history.sqlite  the database
    db/history/<topic>/        files/ (downloads), notes/ (extractions), RESUME.md (first-run leftovers)
    db/history/_staging/       primary texts fetched by the first runs; MANIFEST.md lists them
    db/history/_ledger/        bytes per day, and the EZproxy cookie jar

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
eight at a time is comfortable. The topics and the status of each:

| slug | status on hand-over |
| --- | --- |
| davis-baffin-hudson | Davis 1585-87 fully extracted into notes/, sources and rows going in |
| ross-parry | 16 files on disk, rows going in |
| kane-hall-polaris | 9 primary texts staged, rows going in |
| amundsen-gjoa | 24 files on disk, rows going in |
| franklin-1845 | 8 files on disk, rows going in |
| inuit-oral-history | 13 files (Boas, Inuit-drawn charts), nothing in the database |
| frobisher | 14 files (Best, White portraits, maps), nothing in the database |
| nares-greely | 20 files, nothing in the database |
| sverdrup-bernier-peary | 21 files, nothing in the database |
| norse-helluland | 6 texts, nothing in the database |
| ross-victory | 3 texts (Ross 1835 and Huish), nothing in the database |
| relocations-qtc | 9 QTC reports and RCAP 1994 staged, nothing in the database |
| posts-rcmp-missions | RCMP reports 1921-25, Nascopie, staged; nothing in the database |
| franklin-search, mcclure-investigator, karluk-cae, whaling, thule-dorset, wrecks-disasters, greenland-inughuit, science-stations, st-roch-modern, hudson-strait-south-baffin | topic rows only |

The five in the first block were live on the ship when the copy was taken;
their last worklog line says where each stopped.

## The person's part

Researchers file requests for what they cannot do alone: downloads over 50 MB,
API keys, titles the library does not license, judgement calls. On the ship the
dashboard serves a review page at `/history/requests`; here, the CLI does the
same:

    python3 tools/history-db.py requests --status open
    python3 tools/history-db.py answer --id 7 --status approved --answer "fetched to franklin-1845/files/..."

## Sending it back

From the ship, `tools/history-sync.sh pull` takes a consistent snapshot of
this database and rsyncs it with the files. The dashboard build then publishes
the wiki, the map layer, the timeline and the bibliography under
`data/history/`. Nothing here needs to know about the dashboard.

## Bandwidth and access

10 GB a day is the working allowance, enforced by the ledger. The EZproxy
signs in from this machine's address with no password, so `history-fetch.py`
reaches JSTOR, Cambridge Core, Wiley, Taylor and Francis and the rest directly.
Wikimedia rate-limits the campus address: the tool sends those direct and one
at a time, and researchers are told to check the cached Commons lookups in
`_staging/` before querying.
