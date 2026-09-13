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

**This list is what to produce, not the order to work in.** The first crews
worked it top to bottom, and every one of them ran out of time with rows in
the database and not a single wiki page — and the wiki is the point. Draft
your topic's overview page as soon as your first artifacts and spans are in,
and each episode's page as soon as that episode's rows exist. Pages are
drafts by default and every save keeps the version it replaced, so a rough
page now beats a perfect page never. A run that ends with sixty rows and no
pages has stopped short.

Every writer replaces on a re-run, and re-dating a record replaces its
timeline entry too. A row entered outright in error — a duplicate person, a
stray date — is removed with `forget --kind <kind> --id <id>`; say what you
removed and why in the worklog.

### 1. The topic row already exists
`resume` shows it. Change its summary with `topic` if you can improve it.

### 2. Sources — every work you use, before the things that cite it
    tools/history-db.py source --bibkey mcclintock1859voyage \
      --title "The Voyage of the 'Fox' in the Arctic Seas" \
      --author "McClintock, Francis Leopold" --year 1859 --entry-type book \
      --publisher "John Murray" --url https://archive.org/details/... \
      --urldate 2026-09-08 --licence public-domain --archive "Internet Archive" \
      --primary --topic <your-slug> --note "carries the Victory Point record in facsimile"

`--bibkey` is `<author><year><firstword>`, lowercase ASCII, no punctuation.
Do not stop at English: the record of this region is also Danish, Norwegian,
French, German and Inuktitut, and the original often says more than its
translation. Give every non-English source `--language` (ISO 639-1: da, no,
fr, de, iu, kl...); when you work from a translation, give `--translator` and
`--orig-language` and cite the original edition too where it can be found. A
quote artifact taken from a non-English text carries `--language` as well.
(The wiki will later be translated for the francophone crew, so knowing what
is already French matters.)
`--primary` marks a journal, log, narrative, chart or testimony; leave it off for
scholarship. Every source needs a `--licence` and a `--url`. For an archival
item give `--archive` (the holding institution) and `--callno` (the accession or
catalogue number). If you already have a BibTeX file, `history-db.py bib --file
refs.bib --topic <your-slug>` imports it whole.

`--archive` is the institution's own name, nothing else: `Arctic Institute of
North America`, not `Arctic (AINA)`, `ARCTIC journal` or `Arctic 36(4):
380-381`. Anything in it that identifies the copy (an item, microform,
catalogue or accession number) goes in `--callno`, and the journal, volume and
pages go in `--container`, `--volume` and `--pages`. The tool corrects a
spelling it already knows; `check` flags the rest.

**Choose `--entry-type`. Do not leave it at `misc`.** `book` a standalone work,
`article` a piece in a journal, magazine or newspaper, `incollection` a chapter
or paper in a book or a report series, `report` a government or institutional
report, `thesis` a thesis, `online` a web page or catalogue record, `dataset` a
data file or service. `misc` is only for what none of them fits: an artwork, a
photograph, an object, a manuscript. `article` and `online` print `--container`
as the journal in the bibliography and `incollection` prints it as the book, so
the type and the container must agree.

**`--licence` is a code, not a sentence.** The tool refuses anything else.
Pick the one that describes what this layer may do with the item:

| code | use it for |
|---|---|
| `public-domain` | out of copyright, a US government work, no known restrictions, a route or plot compiled for this project |
| `cc0`, `cc-by-4.0`, `cc-by-sa-2.5`, `cc-by-nc-sa-4.0`, `cc-by-nc-nd-4.0` | Creative Commons, with the version as the holder states it |
| `crown-expired` | Canadian Crown copyright whose fifty-year term has run out |
| `crown-open` | Crown copyright still in force, reproduced under the Open Government Licence, the Reproduction of Federal Law Order, or Government of Canada/Nunavut non-commercial terms |
| `open-access` | free to read at the publisher without a CC licence: *Arctic* before late 2016, Érudit, U of T/Laval journals, UCalgary Press, finding aids |
| `attribution` | reusable with attribution under the holder's own terms (Inuit Heritage Trust, Council of Europe) |
| `permission` | the holder or the project owner approved this use; name the request number in the note |
| `fair-dealing` | in copyright; a short passage quoted or a figure described under fair dealing for research |
| `in-copyright-licensed` | in copyright; a file is held for internal research use under a University of Manitoba or publisher licence, not for republication |
| `in-copyright-cited` | in copyright; cited only, nothing reproduced or held |
| `rights-reserved` | the holder reserves rights and this layer works within their stated terms (Arktisk Institut, AMNH) |
| `not-cleared` | not cleared for reuse: no file is held until a person confirms |
| `unknown` | status not yet established |

Everything the code does not say goes in `--rights-note`, free text: who
holds the rights, why the term is thought expired (and when), the request
that approved the use, what is and is not held. The wiki shows the code's
phrase followed by the note, so write the note as a sentence a reader can
use: `--licence crown-expired --rights-note "Crown copyright of 1961 expired
2011 under the fifty-year term; HathiTrust serves the volume full view"`.
When the code says it all, leave the note off.

The database is shared, so a source another researcher has already entered is
already there: check `history-db.py list --what sources` before inventing a
second key for the same work, and reuse theirs.

### 3. Artifacts — the things the map shows

**Acquire more than you think you need.** Every text you cite is fetched and
registered; every plate, map, chart, sketch and photograph in a source you
have open becomes an image artifact with its position, not a mention; every
dated position in a journal is a waypoint. A page with three artifacts behind
it is thin; ten to twenty is normal for a page built from a primary text. When
a Commons category or an archive's collection holds fifty relevant images,
take them all, a few at a time, and register each one. Storage is not your
concern; a missing original cannot be recovered later.
    tools/history-db.py artifact --id <your-slug>-004 --topic <your-slug> \
      --type quote --title "The Victory Point record" --date 1848-04-25 \
      --lat 69.97 --lon -98.55 --creator "Fitzjames and Crozier" \
      --bibkey mcclintock1859voyage --pages "p. 283" \
      --credit "Royal Museums Greenwich, AAA2069" --licence public-domain \
      --description "..." --tags franklin,abandonment --people "Crozier;Fitzjames" \
      --source-url https://... --local-file <your-slug>/files/name.jpg

**A re-run of `artifact` or `track` merges**: a field you do not pass keeps
what the row holds, and an explicit `""` clears it, so a run that passes only
the id, topic, type, title, credit, bibkey and the one field you are changing
is safe (the required ones must always be given).
Ids are `<your-slug>-NNN`, zero padded, unique. Types: `image`, `text`, `track`,
`place`, `event`, `map`, `quote`, `object`. Aim for 15 to 40 artifacts, mixed in
type. Every artifact needs a `--credit` and a `--bibkey`; the tool refuses one
without them, because the tab shows the credit beside the item and exports the
bibliography. Coordinates are decimal degrees, west longitude negative. A subject genuinely
east of 40 (Novaya Zemlya, the far side of the dateline) carries
`--tags east-verified` so `check` accepts what would otherwise look like a
dropped minus sign.

**`--tags` takes one thing per tag, comma separated**, and the tool stores
them one per tag. Write a tag lowercase, with its words hyphenated at the
boundary: `musk-ox`, `fort-conger`, `ice-shelf`, `st-roch`, `full-text`, never
run together (`muskox`) or spaced (`musk ox`). A tag is singular, because it
names a kind of thing and not a count: `dog`, `wreck`, `grave`, `vessel`,
`relic`. A proper name keeps the form it is written in, plural and all:
`queen-elizabeth-islands`. Known variants are folded to the canonical spelling
as they are written, and `check` names any left in an older row. Reuse a tag
the layer already has rather than coining a near-copy of it; `check` lists
every tag used only once, which is where the near-copies show up.

An entry is about people and things: **name them in the description itself**,
not only in the title or the `--people` list. A reader of the description
alone — and the model reading it as an excerpt — must learn who and what the
entry concerns. `check` flags an artifact or event whose people never appear
in its own prose.

A `quote` is a short verbatim passage (under 80 words) from an out-of-copyright
primary text, pinned where it was written or spoken, with `--pages`.

**Tracks are the most valuable artifacts.** For every voyage in your topic,
reconstruct the route from the published narrative or log:

    echo '[{"date":"1845-05-19","lat":51.45,"lon":0.28,"note":"leaves Greenhithe"},
           {"date":"1845-07-26","lat":74.80,"lon":-66.20,"note":"last seen by whalers"}]' > wp.json
    tools/history-db.py track --id <your-slug>-001 --topic <your-slug> \
      --title "Erebus and Terror, 1845-1848" --date 1845/1848 \
      --waypoints-file wp.json --bibkey cyriax1939franklin \
      --credit "route after Cyriax 1939" --licence public-domain \
      --rights-note "route compiled for this project; Cyriax 1939 is in copyright" \
      --description "..."

The line is built from the waypoints unless you pass `--geometry`. Precision to
about 10 km is fine; say in the description which segments are inferred.

A track also carries a `--routing` code that says how its line was drawn, and
the routing tools own it: `water` for a voyage routed through water by
`tools/route-tracks.py`, `as-given` for a line that follows the waypoints as
they are given (great-circle legs: sea-ice journeys, drifts, flights), and
`terrain` for an overland or mixed journey routed through the valleys and
passes of the elevation model and along the expedition's printed route map by
`tools/digitize-tracks.py`. Leave it unset when you write a track; the waypoints
are the truth whichever way the line is drawn, and a routed line is only ever
written back with the row's every other field as it stands. Only a `terrain`
run may move a waypoint, and then only one whose position was inferred, to
where the printed map and the terrain put it, saying so in its note and in the
description with the position it had before.

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

**Animals and vessels are first-class, like people.** A named dog, pony,
ship's cat or bear cub is an `animal` row (`history-db.py animal --name Mike
--kind dog --role "..." --affiliation "..." --bibkey ...`), a ship, boat or
aircraft is a `vessel` row (`history-db.py vessel --name "HMS Investigator"
--kind barque --kind-note "purchased into the Navy" --built "1848, Greenock"
--lost "..." --affiliation ...`), and pages link them as [[animal:Mike]] and
[[vessel:HMS Investigator]]. Use the name as it is usually written, check
`list --what animals` or `vessels` first, and put the ship's other names in
`--also`. Every vessel a track belongs to should exist as a row.

**A vessel's `--kind` is a code, not a sentence.** The map filters on it, so
the tool refuses anything else. Pick the hull, rig or craft type:

| code | use it for |
|---|---|
| `ship` | full-rigged: a discovery ship, a frigate, an Elizabethan ship of the Queen's navy |
| `barque` | barque or bark, three masts with the mizzen fore-and-aft |
| `brig` | brig, brigantine, gun-brig |
| `schooner` | schooner of any number of masts, with or without an auxiliary |
| `sloop` | single-masted, and the small converted craft rigged that way |
| `yacht` | a private or converted yacht, under sail or screw |
| `bomb-vessel` | the mortar ships taken into the discovery service: Erebus, Terror, Hecla, Fury |
| `boat` | a ship's boat, a pinnace, a steam launch: anything carried, towed or rowed |
| `umiak` | an open skin boat |
| `steamer` | powered and nothing more particular: paddle, screw, tug, gunboat, revenue cutter |
| `tender` | a small steamer attached to a squadron |
| `icebreaker` | built to break ice, from the Wind class to the Polar class |
| `submarine` | a submarine |
| `whaler` | a whaling vessel whose rig no source gives |
| `steam-whaler` | the steam whalers of the last whaling decades |
| `sealer` | a sealing vessel, whether steam, motor or sail |
| `research-vessel` | research and survey work |
| `cruise-ship` | tourist and expedition cruising |
| `transport` | a storeship, a supply or hospital ship, a chartered transport |
| `freighter` | cargo |
| `tanker` | oil |
| `aircraft` | any aeroplane; the type goes in the note |

The code names the rig or the hull where a source gives one, and the work
where that is all it gives: a whaling barque is `--kind barque` with
`--kind-note whaler`, while a whaler whose rig nobody recorded is `--kind
whaler`. Everything the code leaves out goes in `--kind-note`, free text: the
class (`--kind icebreaker --kind-note "Wind class"`), the aircraft type
(`--kind aircraft --kind-note "DHC-3 Otter"`), the trade, a conversion
(`--kind sloop --kind-note "converted herring boat"`), who bought her
(`--kind whaler --kind-note "purchased into the Navy"`). The wiki shows the
code's word and then the note, so write the note as it would be read after a
comma. When the code says it all, leave the note off.

**This is not Wikipedia: there is no notoriety requirement.** Enter every
person a source names — the seamstress, the dog driver, the ship's cook, the
constable, the child born on the floe, the juror — with what the source says
about them, however little. A name with a role and a date is a row. The
people the published narratives leave out are exactly the ones this layer
exists to hold, and a scientist aboard is as likely to ask about the Inughuit
hunter who found the route as about the officer who took the credit. Check
`list` first so one person does not become two rows.
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
`station`, `post`, `island`, `region`, `port`, `bay`, `river`, `lake`, and the
natural kinds of section 9. Use the current Inuktitut name as `--name` for a living
community, with the historic English name in `--historic`.

### 6. Wiki pages — the narrative
The wiki is the point. Write **five to nine pages** for your topic, each 400 to
1200 words, rather than one long dossier:

    tools/history-db.py page --slug franklin-the-death-march \
      --title "The death march down King William Island" --topic <your-slug> \
      --summary "one sentence" --ordering 30 --file page.md

Give your topic an overview page at `--ordering 10`, then a page per episode,
theme or question. Do not wait until the page is polished: a new page is
status `draft` (shown as such in the tab), `page` replaces and keeps every
old version (`versions --slug <slug>` lists them), and a later run or a
person can promote it with `--status good` when it has been checked. Write
rough and early, revise freely. Bodies are Markdown holding wikilinks:

    [[artifact:franklin-1845-004]]        the artifact's own page
    [[artifact:franklin-1845-004|the record itself]]     with your own wording
    [[source:mcclintock1859voyage]]       the source's page
    [[person:John Rae]]  [[place:Beechey Island]]
    [[topic:franklin-search]]             another researcher's topic
    [[page:the-death-march]]              another of your pages

Every artifact, source, person and place gets its page generated automatically;
you never write those. Your narrative pages are what cross-link them, and a
narrative sentence that mentions a thing should link to it. Name the page's
principal people with `--people "A;B"`: the tab's People strip and their
"Mentioned in" backlinks use it exactly. Bare first mentions of known people,
places, animals and vessels are indexed automatically at publish, and events
have pages too — `[[event:<id>]]` links one. Link generously
across topic boundaries: `[[topic:whaling]]`, `[[person:Tookoolito]]` and
`[[place:Pond Inlet]]` may belong to someone else and the link still resolves
once they have written it. A link to something not yet written is kept and
listed by `history-db.py wanted`; it marks work to do rather than breaking
anything, so do not avoid it.

The wiki is self-contained: its reader is a scientist aboard, not the crew.
Never reference the research process — no notes/ files, worklogs, extraction
files, contact sheets, leaf numbers, "a previous run", "this run", or "the
database". If a notes file holds something the reader needs, the place for it
is the page itself or an artifact; the pointer stays in the worklog.

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
archive, not a thumbnail). Always keep the original, whatever its size:
storage and bandwidth downstream are not your concern, and smaller copies can
always be derived later, while a discarded original cannot. Every file must
be fetched through the fetch tool:

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
- **A raw scan with no usable OCR is not a dead end**: `tools/ocr.sh
  <file.pdf|image> [outdir]` runs a modern OCR (marker + surya) on this
  machine's GPU and prints the path of the markdown it wrote. Use it for
  scanned books, plates with captions, and manuscript facsimiles the
  archive's own OCR mangled; quote-check antique typography (the long s)
  against the page image. One document at a time — the GPU is shared.
- If a fetch fails outright, record the artifact with `--download-url` and no
  `--local-file`, note it in the worklog, and move on.
- **Before you file a `request --kind access`, search the library.** Run
  `tools/library-search.py "<title words author>"` (or `--isbn`). It prints
  the shelf copies and the e-book platforms the University of Manitoba
  licenses, each marked reachable from grid, browser-only, or no. Scholars
  Portal is reachable: `tools/history-fetch.py --scholarsportal <uri>
  --pages FROM-TO` pulls up to 53 reader pages, and the tool enforces the
  crew-wide rule of one session per platform per hour — if it says wait,
  wait and do other work; do not look for another way in. Pull the chapters
  the page actually needs, not the book. A browser-only or unlicensed
  platform, or a shelf copy with no e-copy, is what the request is for: say
  in the request what the search showed. **The library is yours alone**: only
  you, the Opus researcher, run `library-search.py` or `--scholarsportal`.
  Helpers and readers never touch either; a Sonnet helper that needs a
  library answer reports the need back to you.

### 8. Asking a person for help

**No request is needed for a Library and Archives Canada image that is already
on Wikimedia Commons.** The person has approved their use as a class and
asserts fair use for them: register the Commons original with the LAC
reference number, the Commons file name and the credit line LAC gives, and
move on. File a request only for LAC material that is not on Commons.
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
the full instruction, and it answers four questions: why the topic needs it;
**why it needs a person at all** — what you tried yourself and what only a
person can do (no digital copy exists anywhere, the form wants a human's
login, the call is one of judgement); exactly where to go (the URL, the exact
title, edition and volume, the catalogue entry, the request form); and what
you will do with the answer. When the action is writing to someone — a
permissions desk, an archive, a rights holder — first look for the dedicated
page: institutions usually have a specific media, permissions or image-request
page with its own address and process (Parks Canada's wreck imagery, for
instance, goes to erebus-terror-images@pc.gc.ca via its filming-and-photos
page, not to the site's general contact). Name that address and process (from
their own pages, never guessed) and include a ready-to-send draft of the
message, introduced with the exact line `Draft, ready to send:`, opening
with `To:` and `Subject:` lines carrying the found address and a subject,
and ending with the signature block in `db/history/SIGNATURE.txt`, verbatim
— so the person's whole job is to read it and send it. In a usage or permission
letter asking for fewer than ten items, name them in a list — title, date,
identifier, and for a digital object its DOI or a direct link (verified on
the holder's own pages, never guessed; say where you saw it if no stable
link exists) — never "a small number of images": a list the recipient can
approve line by line gets a faster and fuller answer. The tool refuses a
`--why` too thin to act on.
Not this:

    --kind download --what "Life with the Esquimaux vol. II" --why "only have vol. I"

but this:

    tools/history-db.py request --topic kane-hall-polaris --kind download \
      --what "Life with the Esquimaux (Hall, 1864), volume II - no digital copy found" \
      --why "Volume I is staged, but I searched Internet Archive, HathiTrust and \
    Google Books and no scan of volume II exists, so a person must ask the library. \
    UM Libraries holds the 1864 Sampson Low set (catalogue: <link>); please request \
    a scan through the document delivery form at <link> and attach or drop the PDF \
    at the --dest path. It carries Tookoolito's and Ebierbing's first years with \
    Hall, which the people and quote rows for both currently cite second-hand." \
      --url https://search.lib.umanitoba.ca/... \
      --dest kane-hall-polaris/files/kane-hall-polaris-hall-esquimaux-v2.pdf

Kinds: `download`, `api_key`, `question`, `access`, `other`; `download` and
`access` also need `--url`. Answers come back through
`history-db.py requests --topic <your-slug>`, and `resume` lists them too.

### 9. Natural history — subjects and observations

The History tab holds what people did in the archipelago. The natural half
holds what the archipelago is and does: the rock and its fossils, the ice on
land and at sea, the water under the ship, the sky above it, the weather, the
magnetic field, and the living things, together with what every one of those
people wrote down about them on the way. A `nature` topic (the topic row says
`domain nature`) produces everything above — sources, artifacts, dates,
people, places, pages — and two more kinds of row: **subjects** and
**observations**. `db/history/NATURE-DESIGN.md` is the design; this section
is the contract.

**Nothing here was discovered.** It was observed, measured, recorded,
sounded, collected, named.

**The subject** is what an observation is of: a species, a rock unit, a
fossil bed, a mineral, a landform, a kind of ice, a variable of the water or
the weather, a thing in the sky, a feature of the magnetic field. One table,
one kind of page, one link form for all of them. `--kind` and `--domain` are
codes (`--help` lists them):

    tools/history-db.py subject --name "Ovibos moschatus" --kind taxon --domain biology \
      --rank species --parent Bovidae --english muskox --french "boeuf musqué" \
      --inuktitut umingmak --kalaallisut umimmak --also "musk-ox; musk ox" \
      --backbone-id gbif:2441090 --status "COSEWIC not at risk 2007" \
      --topic <your-slug> --bibkey <where the names and the note come from> \
      --note "two to five sentences: what it is, where it lives or lies in the region, why it matters here"

    tools/history-db.py subject --name "air temperature" --kind weather --domain meteorology \
      --unit C --topic <your-slug> --note "..."          # a variable: observations of it carry a value

    tools/history-db.py subject --name "North Magnetic Pole" --kind field --domain geomagnetism \
      --backbone-id "nrcan:north-magnetic-pole" --topic <your-slug> --note "..."

- `--name` is the scientific or technical name; the page is generated from
  `--note`, so write the note as the species account, the rock unit's
  description, the phenomenon's explanation, for a scientist aboard. Any of
  the names resolves a link or an observation: `[[subject:Ovibos moschatus]]`,
  `[[subject:muskox]]`, `[[subject:umingmak]]` all reach the one page.
- **Names in the languages of the region are knowledge somebody holds.** Give
  `--english`, `--french`, `--inuktitut` and `--kalaallisut` where the sources
  give them, in the orthography the source uses, with the community's current
  spelling in `--also` when it differs, and cite the source of the names in
  `--bibkey` or the note. The sea-ice vocabulary above all.
- **`--backbone-id` ties the subject to the world's catalogue** so the layer
  can join GBIF, OBIS and the rest: `gbif:<usageKey>` for land and birds
  (`curl -s "https://api.gbif.org/v1/species/match?name=Ovibos%20moschatus"`
  gives `usageKey`), `worms:<AphiaID>` for the sea
  (`curl -s "https://www.marinespecies.org/rest/AphiaIDByName/Balaena%20mysticetus?marine_only=true"`),
  `weblex:<unit id>` for a rock unit (the Lexicon of Canadian Geologic Units,
  weblex.canada.ca), `iau:<name>` for a sky object, `meteoritical:<name>`
  for a meteorite. A variable or a phenomenon has no backbone: leave it blank
  and the note says what it is. `check` flags a subject with neither.
- Genus and family rows exist so the tree can be walked (`--parent`), as
  formation and group rows do for the stratigraphic column. Enter the parent
  before the child. Check `list --what subjects` first: another researcher's
  `Cetacea` is yours too.
- `--status` is the COSEWIC or IUCN code with its year, for a taxon.
- A named individual animal stays an `animal` row; give it `--subject` (its
  species) so the two join.

**The observation** is the atom of the natural half, as the date is of the
timeline: one subject, one date, one position, one source, and where there
is a number, the number in the unit it was written in.

    tools/history-db.py observation --id <your-slug>-001 --topic <your-slug> \
      --subject umingmak --date 1900-04-13 --lat 78.6 --lon -95.2 \
      --count "a herd of 17" --method hunt --observer "Otto Sverdrup" \
      --bibkey sverdrup1904new --pages "v. 1 p. 412" \
      --detail "Sverdrup's party shot four of a herd of seventeen muskoxen at the head of the fiord, to feed the dogs."

    tools/history-db.py observation --id <your-slug>-002 --topic <your-slug> \
      --subject "air temperature" --date 1882-02-04 --place "Fort Conger" \
      --value -58.5 --unit F --qualifier "coldest of the winter" --method station-record \
      --instrument "spirit thermometer" --observer "Adolphus Greely" --bibkey greely1888report \
      --pages "v. 1 appendix" --detail "The minimum of the winter of 1881-82 at Fort Conger, read at the station."

    tools/history-db.py observation --id <your-slug>-003 --topic <your-slug> \
      --subject sounding --date 1871-08-28 --lat 82.1 --lon -60.5 --qualifier "no bottom at" \
      --value 1000 --unit fathoms --method sounding --vessel "USS Polaris" --bibkey davis1876narrative \
      --detail "The Polaris found no bottom at 1,000 fathoms off Cape Union."

    tools/history-db.py observation --id <your-slug>-004 --topic <your-slug> \
      --subject "Ursus maritimus" --date 1924-08 --lat 74.55 --lon -82.4 --sensitive \
      --count 2 --stage "cub" --behaviour "denning" --method sighting --confidence probable \
      --observer "A. H. Joy" --bibkey rcmp1925report --pages "p. 42" \
      --detail "Joy reported a bear den with two cubs on the slope above the harbour."

- `--id` is `<your-slug>-NNN`, stable, so a re-run replaces. `--subject` is
  any of the subject's names, and the subject must exist first. `--date` as
  written (`1900-04-13`, `1882-02`, `1820/1821`). `--lat/--lon`, or a
  `--place` row that has them. `--bibkey` and `--pages` always. `--detail`
  is the sentence that says what was seen, naming the observer. `--method` is
  a code (`--help`). `--observer` is a `people` name where the record names
  one (enter the person), or the party or the watch. `--artifact` points at
  the evidence (the plate, the quote, the specimen); `--event` at the
  human-history event this also is, so the timeline shows one thing, not two.
- **Numbers are entered as written, in the unit written**, never converted:
  Greely's Fahrenheit stays Fahrenheit, a lead-line sounding stays in fathoms.
  The page does the arithmetic and says so. A variable's subject carries the
  unit the page converts to; the observation carries the unit as written.
- **Doubt goes in `--confidence`, not in the subject.** A narrative's "a
  whale" is `Cetacea`, not a guessed species; "a great depth" with no lead is
  a `--qualifier`, not a `--value`; a count the source estimates is
  `--count "about 200"`.
- **Sensitive sites are marked at entry**: a den, a nest, a haul-out, a
  calving ground, a fossil site at risk. `--sensitive` publishes the row with
  its position rounded to half a degree and its place blank; the full row
  stays here; the page prose never names the site.
- **Time series are not re-entered.** A station's daily record, a survey's
  transects, an ice chart series is a source with `--entry-type dataset`, and
  the layer enters the extremes, the firsts and the milestones (the coldest
  day, the first open water, the year the shelf calved) as observations that
  cite it, with a page that says where the whole series lives.
- A specimen, a rock sample, a meteorite, an ice core is an artifact of type
  `object` with the catalogue number in `--credit`; the observation points at
  it with `--artifact`. A photograph of the animal, the outcrop, the aurora
  is an `image` artifact the observation cites.

**Community knowledge documents: the spirit, not just the letter (the owner, 2026-09-10).**
The modern community knowledge projects (the NWMB harvest and IQ studies, the Inuit
Bowhead Knowledge Study, the Igloolik Oral History Project, the Nunavut Arctic
College elders' volumes, the community sea-ice atlases, the Pikialasorsuaq report,
the ITK studies) belong to the communities that made them, and none carries an open
licence (`db/history/KNOWLEDGE-TERMS.md` quotes each one's terms). The rule: the
layer **summarizes** such a document in its own words and enters the facts it
records as observations, each cited to the document with the elder or the community
as `--observer`; every page that draws on one **links to the raw document** and
**credits the elders, the community and the project by name**. The layer does
**not quote** these documents verbatim (no quote artifacts), does not hold or
publish their images or transcripts, and does not publish anything the project
itself withheld (a glossary held back for verification by elders stays held back).
Where a project's terms say ask before reuse, summarizing its published report is
within the spirit; taking its data or its users' content is not. Register such a
source with `--licence in-copyright-cited` and a rights note quoting its own terms
and naming the elders; put the URL in `--url` so the page can link it.

**Natural places.** Enter the glacier, the bird cliff, the haul-out, the
polynya, the fossil site, the weather station as a `place` with a natural
kind: `glacier`, `ice-cap`, `ice-shelf`, `ice-island`, `polynya`,
`bird-cliff`, `haul-out`, `denning-area`, `calving-ground`, `fossil-site`,
`outcrop`, `meteorite-fall`, `hot-spring`, `pingo`, `ice-core-site`,
`tide-station`, `magnetic-station`, `weather-station`, `lake`, `river`,
`range`, `basin`, `sound`, `channel`, `fiord`, beside the human kinds.

**Read inward before outward.** Every primary narrative already on disk
carries natural history of every kind: Parry's appendices, Ross at the
Magnetic Pole, Kane's, Hayes's and Hall's tables, Nares's and Greely's
appendices, Sverdrup's hunting returns and Schei's geology, the whalers'
catches, the RCMP patrol reports, Krüger's geology, the aerial descriptions,
Tener's survey, the oral-history record of animals, ice and weather and
their names. The texts are under `db/history/<topic>/files/*.txt` and
`_staging/` (`grep -ril "musk" db/history/*/files/*.txt` finds them; the
human topic's `list --what artifacts` gives the bibkey and the artifact id
to cite). Their sources are already entered: cite the same bibkey with your
pages, and point `--artifact` at the human topic's quote or plate where one
exists, or add your own quote artifact under your slug. Haiku readers over
the text layers find the passages; you enter them. Only then look outward,
to the open catalogues and series (NATURE-DESIGN.md section 8a): most of
the modern record is open and reachable from grid without the library.

**Pages.** The same five to nine narrative pages as a history topic, with
the overview at `--ordering 10`, and they link the subjects
(`[[subject:...]]`), the places, the people who made the observations and
the history topics where the record came from. The subject pages are
generated from `--note` and the front end lays out the names, the status,
and **the record**: every observation of the subject in date order with
observer, value and source. So the muskox page reads as a species account
followed by a two-hundred-year sighting log. Do not write the record into
the prose; write the note well and enter the observations.

**`check` demands** a subject that exists, a date, a position or a place, and
a bibkey; a value with its unit; a count for a transect or a catch record; a
depth or a value for a sounding; and a backbone id or a note for every
subject. `resume` lists your subjects with their observation counts, and
nags for pages once twenty observations are in.

## Helpers and the web

Three waves of researchers showed where the budget went. Helper agents four
levels deep did two thirds of all web fetching; every WebFetch ran the whole
page through a model and kept nothing; and nearly every helper ran on Opus
because nobody said otherwise. Two rules follow.

**An agent launches only agents smaller than itself.** You run on Opus, so
any helper you launch is `model: sonnet`, and a Sonnet helper may launch only
`model: haiku`. Haiku launches nothing. Put the rule in the helper's prompt so
it knows its place: "You are a Sonnet helper. Launch only Haiku agents, and
only to read files. Do not run tools/library-search.py or
history-fetch.py --scholarsportal; the library is the researcher's." Prefer
doing the work yourself to launching a helper at all; a helper is for a
bounded extraction you can name in one sentence.

**Sonnet helpers are capped; Haiku readers are not.** You (Opus) may have at
most 2 Sonnet helpers running at once and launch at most 6 in a run; wait for
one to finish before starting the next. Haiku readers are cheap: any agent,
you included, may launch as many `model: haiku` readers as the files call for,
in parallel, with no cap. Put the rule in the helper's prompt with the model
rule.

**Cache locally, then read the cache with Haiku.** Do not use WebFetch to read
a page. It downloads the page again on every call, runs the whole page through
a model each time, and keeps nothing. Instead:

1. Download once. Sources and images go through `tools/history-fetch.py` as in
   section 7. Pages that are not part of the record (catalogue entries, finding
   aids, search results) go into your scratchpad subdirectory:
   `curl -sL URL -o <scratch>/<your-slug>/<name>.html`.
2. Ask questions of the file, not of the web. A short file you read yourself.
   For a long one, launch a `model: haiku` agent whose prompt names the file
   and the question: "Read <path> and list every dated position with its page
   number." One download then answers every later question for free.
3. WebSearch is fine for finding things; it runs inside your own turn. Once it
   has found a URL, download and cache the page as above rather than WebFetch it.

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
- Epistemic humility about "discovery". Most of what these expeditions
  "discovered" was inhabited or long known: write what actually happened —
  sighted, reached, charted, mapped, observed, identified, noticed, recorded,
  rediscovered (where knowledge was lost and regained), located (a wreck, a
  cairn), first European sighting of. Keep the word only where it is a proper
  name (HMS Discovery, a book's title, Discovery Harbour), inside a verbatim
  quotation, or reported as the actors' own framing ("what Parry claimed as a
  discovery"). This applies to pages, artifact and event titles, and
  descriptions alike.
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
