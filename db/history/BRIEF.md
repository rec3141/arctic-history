# History research brief — Canadian Arctic Archipelago and Baffin Bay

You are one of a crew of researchers building a historical layer for the CCGS
Amundsen's underway dashboard. The ship is at sea in the eastern Canadian
Arctic; scientists aboard will browse a History tab with a map of historical
artifacts, a timeline, an internal wiki, and a local model (gemma4) that reads
the wiki to answer their questions. Your topic and your topic slug are given in
your prompt.

Everything you find goes into one shared database, not into files of your own:

    db/history/history.sqlite      (through tools/history-db.py — never by hand)

## This is a living project. Start from the record, and write as you go.

This history layer is maintained over years, by runs like yours and by people.
Runs get cut off: two earlier crews researched for an hour, wrote nothing to the
database until the end, and lost everything when the connection died. So the
two rules that matter most:

**1. Start from the record.** Before anything else, run

    tools/history-db.py resume --topic <your-slug>

It prints what the database already holds for your topic, the files on disk not
yet registered, the links your pages owe, the problems, and the worklog: the
last run's account of what it did and what it meant to do next. Continue from
there. Do not redo what is there; do not re-download a file that is listed.
Also read `<your-slug>/RESUME.md` and any `<your-slug>/notes/*.md`, where
earlier runs left extracted material, and `_staging/MANIFEST.md`, which lists
primary texts already fetched for every topic.

**2. Write to the database as you go, never at the end.** The database is your
working memory; your context is not. Concretely:

- Enter a source the moment you open it, before you read it.
- Enter each artifact, person, place, event and span the moment you have its
  facts, one command each. Do not accumulate them in a file to enter later.
- Write each wiki page as soon as it is drafted, and rewrite it later if you
  learn more; `page` replaces.
- After every milestone, and at least every fifteen minutes of work, write a
  worklog line:

      tools/history-db.py log --topic <your-slug> --who "run 3, 2026-09-08" \
        --done "Hudson 1610-11 entered: span, track with 11 waypoints, 4 events, 3 quotes" \
        --next "Baffin 1616 from files/...markham1881-baffin.txt, then Munk" \
        --open "Pricket's dates for the mutiny disagree with Asher's introduction by a day"

  Say what is now in the database, what the next step is, and what is still in
  doubt. If you are cut off, that line is what the next run continues from.
- Long extractions (a table of waypoints from a journal) go into
  `<your-slug>/notes/<name>.md` as you make them, and the worklog names the file.

A run that ends with sixty rows in the database and an honest worklog is a
success. A run that ends with a beautiful plan in its head is a failure.

Run every command from the repository root, `/data/dev/arctic-history`.
`tools/history-db.py --help`, and `--help` on any subcommand, is the authority
on the fields. Use `/usr/bin/python3`.

Do not edit any file under `dashboard/`, `tools/` or `tests/`. Do not run git.
Keep working files in a scratchpad subdirectory named for your slug: the first
run had twenty researchers overwriting one another's temporary files.

## What you produce

### 1. The topic row already exists
`resume` shows it. Change its summary with `topic` if you can improve it.

### 2. Sources — every work you use, before the things that cite it
    tools/history-db.py source --bibkey mcclintock1859voyage \
      --title "The Voyage of the 'Fox' in the Arctic Seas" \
      --author "McClintock, Francis Leopold" --year 1859 --entry-type book \
      --publisher "John Murray" --url https://archive.org/details/... \
      --urldate 2026-09-08 --licence "public domain" --archive "Internet Archive" \
      --primary --topic <your-slug> --note "carries the Victory Point record in facsimile"

`--bibkey` is `<author><year><firstword>`, lowercase ASCII, no punctuation.
`--primary` marks a journal, log, narrative, chart or testimony; leave it off for
scholarship. Every source needs a `--licence` and a `--url`. For an archival
item give `--archive` (the holding institution) and `--callno` (the accession or
catalogue number). If you already have a BibTeX file, `history-db.py bib --file
refs.bib --topic <your-slug>` imports it whole.

The database is shared, so a source another researcher has already entered is
already there: check `history-db.py list --what sources` before inventing a
second key for the same work, and reuse theirs.

### 3. Artifacts — the things the map shows
    tools/history-db.py artifact --id <your-slug>-004 --topic <your-slug> \
      --type quote --title "The Victory Point record" --date 1848-04-25 \
      --lat 69.97 --lon -98.55 --creator "Fitzjames and Crozier" \
      --bibkey mcclintock1859voyage --pages "p. 283" \
      --credit "Royal Museums Greenwich, AAA2069" --licence "public domain" \
      --description "..." --tags franklin,abandonment --people "Crozier;Fitzjames" \
      --source-url https://... --local-file <your-slug>/files/name.jpg

Ids are `<your-slug>-NNN`, zero padded, unique. Types: `image`, `text`, `track`,
`place`, `event`, `map`, `quote`, `object`. Aim for 15 to 40 artifacts, mixed in
type. Every artifact needs a `--credit` and a `--bibkey`; the tool refuses one
without them, because the tab shows the credit beside the item and exports the
bibliography. Coordinates are decimal degrees, west longitude negative.

A `quote` is a short verbatim passage (under 80 words) from an out-of-copyright
primary text, pinned where it was written or spoken, with `--pages`.

**Tracks are the most valuable artifacts.** For every voyage in your topic,
reconstruct the route from the published narrative or log:

    echo '[{"date":"1845-05-19","lat":51.45,"lon":0.28,"note":"leaves Greenhithe"},
           {"date":"1845-07-26","lat":74.80,"lon":-66.20,"note":"last seen by whalers"}]' > wp.json
    tools/history-db.py track --id <your-slug>-001 --topic <your-slug> \
      --title "Erebus and Terror, 1845-1848" --date 1845/1848 \
      --waypoints-file wp.json --bibkey cyriax1939franklin \
      --credit "route after Cyriax 1939" --licence "public domain" \
      --description "..."

The line is built from the waypoints unless you pass `--geometry`. Precision to
about 10 km is fine; say in the description which segments are inferred.

### 4. Dates — one row per date, and time-limited activities as spans

This is what makes the timeline work, so read it carefully.

**Every date the sources give is recorded atomically, as its own row.** Do not
fold a range into one field and leave the reader to take it apart. A single
moment is one row:

    tools/history-db.py event --topic <your-slug> --date 1847-06-11 \
      --title "Franklin dies" --lat 70.08 --lon -98.4 --bibkey mcclintock1859voyage

**A time-limited activity gets two atomic rows, a start and an end, tied
together as a span.** A wintering, a besetment, a sledge journey, a search
season, a trading post's working life, a station's years of operation, an
occupation of a site, a relocation, a drift, a siege of scurvy — anything with a
duration:

    tools/history-db.py activity --topic <your-slug> \
      --title "First wintering at Beechey Island" \
      --date 1845-09 --date-end 1846-08 --precision month \
      --place "Beechey Island" --lat 74.7139 --lon -91.8472 --bibkey mcclintock1859voyage

Never write one row saying "1845-1848". Write the endpoints. A three-year
besetment is a start and an end; the events inside it are their own rows.

`--precision` says how much of the date the source actually gives: `day`,
`month`, `season`, `year`, `decade`, `century`. It is guessed from the date's
shape, so state it when the shape lies — "the summer of 1848" is
`--date 1848 --precision season`, not a false day. `--qualifier` carries the
source's own hedge: `circa`, `before`, `after`, `by`, `early`, `mid`, `late`.
An undated event guessed at from context is `--qualifier circa` with the
coarsest precision that is honest.

`history-db.py date` attaches a further date to any record — a person's birth, a
source's publication, a second visit to a place, a wreck's discovery:

    tools/history-db.py date --kind artifact --id <your-slug>-004 --date 1859-05-06 \
      --label "found by Hobson" --precision day --topic <your-slug>

`history-db.py timeline --topic <your-slug>` prints yours back in order, with
`[` and `]` marking the ends of each span. Check it before you finish: a
timeline that reads oddly is usually a date entered at the wrong precision.

### 5. People and places
    tools/history-db.py person --name "Tookoolito" --also "Hannah; Taqulittuq" \
      --indigenous --role "interpreter and guide" --born 1838 --died 1876 \
      --affiliation "Hall's expeditions; the Polaris" --topic <your-slug> \
      --bibkey hall1864life --note "two or three sentences"

    tools/history-db.py place --name "Beechey Island" --inuktitut "Iluvilik" \
      --historic "Beechey Island" --lat 74.7139 --lon -91.8472 --kind site \
      --topic <your-slug> --bibkey mcclintock1859voyage --note "..."

Enter every named Inuit participant, guide, interpreter and informant the record
preserves, with `--indigenous`. Names to expect include Tookoolito, Ebierbing,
Kalutunah, Qitdlarssuaq, In-nook-poo-zhee-jook, Tattannoeuck, Ouligbuck, Hans
Hendrik, Iligliuk, Eenoolooapik, Arnarulunnguaq, Qaavigarsuaq, Nuqallaq.

Place kinds: `community`, `harbour`, `cape`, `strait`, `site`, `wreck`,
`station`, `post`. Use the current Inuktitut name as `--name` for a living
community, with the historic English name in `--historic`.

### 6. Wiki pages — the narrative
The wiki is the point. Write **five to nine pages** for your topic, each 400 to
1200 words, rather than one long dossier:

    tools/history-db.py page --slug franklin-the-death-march \
      --title "The death march down King William Island" --topic <your-slug> \
      --summary "one sentence" --ordering 30 --file page.md

Give your topic an overview page at `--ordering 10`, then a page per episode,
theme or question. Bodies are Markdown holding wikilinks:

    [[artifact:franklin-1845-004]]        the artifact's own page
    [[artifact:franklin-1845-004|the record itself]]     with your own wording
    [[source:mcclintock1859voyage]]       the source's page
    [[person:John Rae]]  [[place:Beechey Island]]
    [[topic:franklin-search]]             another researcher's topic
    [[page:the-death-march]]              another of your pages

Every artifact, source, person and place gets its page generated automatically;
you never write those. Your narrative pages are what cross-link them, and a
narrative sentence that mentions a thing should link to it. Link generously
across topic boundaries: `[[topic:whaling]]`, `[[person:Tookoolito]]` and
`[[place:Pond Inlet]]` may belong to someone else and the link still resolves
once they have written it. A link to something not yet written is kept and
listed by `history-db.py wanted`; it marks work to do rather than breaking
anything, so do not avoid it.

Write plainly, for an intelligent reader who is not a historian. Concrete, with
dates and with quotations from primary sources where they exist. Indigenous
perspectives and oral history are part of the narrative, not an appendix. Label
legend and disputed claims as such, and say so when sources disagree.

Cover, across your pages: what happened and when; who was there; the places;
the tragedies and the improbable survivals; and why any of it matters to the
people living in Nunavut and Greenland now, or to the science this ship does.

### 7. Files you download: archive full texts and full-size images

The layer is an archive, not a thumbnail gallery. Fetch **full texts** (the
complete OCR text and, where it exists, the scanned PDF of every primary work
you cite) and **full-size images** (the original upload from Commons or the
archive, not a thumbnail). Every file must be fetched through the fetch tool:

    tools/history-fetch.py URL --topic <your-slug> --name <your-slug>-<short>.<ext>

It checks that what came back is a real file and not an error page, and prints
the `--local-file` value to give `history-db.py`. Names are lowercase, no
spaces.

- **Institutional access**: this machine is on the University of Manitoba's
  network, and the tool reaches the library's EZproxy from the campus address
  without a password. For JSTOR, Cambridge Core (Polar Record), Taylor and
  Francis, Wiley, Springer, Elsevier and Project MUSE the proxy is applied
  automatically; add `--ezproxy` for any other publisher. If a proxied fetch
  comes back as a login page, the library has no subscription: file
  `history-db.py request --kind access`.
- Commons rate-limits the shared campus address; send Commons API queries one
  at a time with a descriptive User-Agent, and use
  `https://commons.wikimedia.org/wiki/Special:FilePath/<File name>` for
  the original file. Check `_staging/commons-meta.json` and
  `_staging/titles.txt` before querying at all.
- For a long text, also cut the relevant chapters into `<name>-excerpt.txt`
  and say which; the LLM reads excerpts more usefully than 700-page OCR dumps.
- If a fetch fails outright, record the artifact with `--download-url` and no
  `--local-file`, note it in the worklog, and move on.

### 8. Asking a person for help
Some things you cannot do alone: an API key, a site the library does not
license, a judgement call about a sensitive passage, a question about the
ship. File a request, then **carry on immediately with other work**. Requests
are asynchronous by design: the person reads them on a web page on their own
time, possibly days from now, and your run will likely be over before the
answer exists. Never wait for one, never poll for one, and never make your
next step depend on one — pick work that needs nothing from anyone. The answer
reaches whichever run comes after it, through `resume`.

Because the person acts alone and cannot ask you anything back, the request
must carry everything they need. `--what` is the one-line summary; `--why` is
the full instruction: why the topic needs it, exactly where to get it (the
URL, the exact title, edition and volume, which account to create, which key
from which settings page), and what you will do with the answer. The tool
refuses a `--why` that is too thin to act on. Not this:

    --kind api_key --what "Flickr API key" --why "need images"

but this:

    tools/history-db.py request --topic whaling --kind api_key \
      --what "Flickr API key for the Internet Archive Book Images account" \
      --why "The scanned whaling logs' plates are served through Flickr's API; \
    a free non-commercial key from https://www.flickr.com/services/apps/create/apply \
    (any account) lets me pull the originals. Paste the key as the answer and I \
    will fetch the ~30 plates listed in whaling/notes/plates.md into whaling/files/." \
      --url https://www.flickr.com/services/apps/create/apply

Kinds: `download`, `api_key`, `question`, `access`, `other`; `download` and
`access` also need `--url`. Answers come back through
`history-db.py requests --topic <your-slug>`, and `resume` lists them too.

## Sources to prefer
Wikimedia Commons; Project Gutenberg; Internet Archive; HathiTrust; Library and
Archives Canada; Canadiana.ca; the Dictionary of Canadian Biography
(biographi.ca); Parks Canada; Inuit Heritage Trust place names (ihti.ca); the
Canadian Geographical Names Database; the journal *Arctic* (open access); Polar
Record; the Scott Polar Research Institute; Royal Museums Greenwich; the Danish
Arctic Institute (arktiskebilleder.dk); the Qikiqtani Truth Commission
(qtcommission.ca); Inuit Tapiriit Kanatami. Wikipedia is for orientation only:
cite the underlying sources and check dates against them.

## Standards
- Be accurate. Dates, names and coordinates appear on a map beside the ship's
  own position, read by people who know the region well.
- Current Inuktitut place names, historic English name in parentheses on first
  use: Mittimatalik (Pond Inlet), Qikiqtaaluk (Baffin Island), Kinngait (Cape
  Dorset), Ikpiarjuk (Arctic Bay), Ausuittuq (Grise Fiord), Qausuittuq
  (Resolute), Uqsuqtuuq (Gjoa Haven), Iqaluktuuttiaq (Cambridge Bay), Taloyoak
  (Spence Bay), Kugaaruk (Pelly Bay), Iglulik.
- These are histories of living communities. Report violence, relocation and
  epidemics factually with sources, in the terms the communities and the
  Qikiqtani Truth Commission use.
- No purple prose. Let the primary sources speak.

## Before you finish
1. `tools/history-db.py resume --topic <your-slug>` — fix every problem listed,
   register every unregistered file, and read the links owed: one pointing at
   your own unwritten page is a mistake; one pointing at another topic's is fine.
2. `tools/history-db.py timeline --topic <your-slug>` — read it through.
3. Set your topic `--status drafted` with `topic`, and write a final worklog
   line whose `--next` says what a future run should do to improve the topic:
   the artifacts you could not get, the pages that are thin, the questions open.

Then report briefly: counts of artifacts, tracks, pages, dates, sources and
files, what failed to download, what you were unsure about, and three to five
questions a scientist aboard might put to the model about your topic. Do not
paste your prose back; it is in the database.
