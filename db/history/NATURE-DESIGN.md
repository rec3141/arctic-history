# Natural history: a design for the second half of the layer

The History tab holds what people did in the archipelago. The natural history
half holds what lives there, what the ice and the rock are doing, and what
every one of those people wrote down about it on the way. Both halves sit in
the one database and the one wiki, so a muskox page can cite Sverdrup's diary
and Sverdrup's page can link the muskox, and the model aboard answers a
question about caribou on Melville Island with Tener's 1961 transect and
Parry's 1820 hunting return in the same breath.

This document is the design to argue with before any table is made. Aboard,
the domain belongs to @doc; the entry side is built with him.

## 1. Principles carried over

- **Grid owns the database; the ship pulls.** That holds. The ship's own
  observations reach grid through a journal file, not through a second writer
  (section 6).
- **Everything is written as it is found**, through the one CLI, with a
  worklog line, and the brief is the contract. A natural-history researcher
  gets a second brief that adds to BRIEF.md rather than replacing it.
- **Sources, licences, credits** work exactly as they do now: every
  observation cites a `bibkey` and pages, every image carries a credit and a
  licence code, every dataset is a source with `entry_type dataset`.
- **Names in the languages of the region.** A species carries its scientific
  name, its English and French names, and its Inuktitut and Kalaallisut names
  as first-class fields, the way a place carries `inuktitut` and `historic`.
- **No discovery framing.** Nothing here was discovered; it was observed,
  recorded, counted, collected. The same rule as the human history.

## 2. The atom: an observation

Dates are the atom of the timeline; the **observation** is the atom of the
natural history. One taxon, one date, one position, one source. Everything
else hangs off it.

    a walrus haul-out of about 200 animals, Dundas Harbour, 16 August 1924,
    Joy, RCMP annual report 1925 p. 42

    12 muskoxen shot at De To Kratere, Axel Heiberg, 29 May 1901,
    Isachsen and Hassel, New Land vol. 2 p. 298

    Peary caribou, 7 on transect, Bathurst Island, 24 July 1961,
    Tener, Occasional Paper 4 p. 31

    a bowhead surfacing beside the ship, 76.1 N 92.4 W, 11 September 2026,
    the Amundsen's bridge watch

The first three are already in the texts on disk and are the first wave's
work. The fourth is what @doc enters aboard. They are the same row.

An observation is a fact about nature at a time and place; an **event** stays
a fact about people. Where the two coincide (the muskoxen at De To Kratere fed
the dogs that got Isachsen home) the observation carries `event_id` so the
timeline and the map show one thing, not two.

## 3. Entities and tables

Four additions. Nothing existing changes shape.

### taxa

    taxa
      name          TEXT PRIMARY KEY   -- the accepted scientific name: Ovibos moschatus
      rank          TEXT               -- kingdom .. species, subspecies
      parent        TEXT               -- the next rank up, by name; makes the tree
      group_        TEXT               -- mammal, bird, fish, invertebrate, plant, lichen,
                                          fungus, alga, microbe, protist   (a code)
      english       TEXT               -- muskox
      french        TEXT               -- boeuf musqué
      inuktitut     TEXT               -- umingmak (roman orthography; syllabics in `also`)
      kalaallisut   TEXT               -- umimmak
      also          TEXT               -- other names, synonyms, spellings, semicolon list
      status        TEXT               -- COSEWIC or IUCN code, free text with the year
      backbone_id   TEXT               -- GBIF or WoRMS id, so the name can be checked
      note          TEXT               -- the reader's paragraph
      bibkey, topic, updated

A taxon is a wiki kind: `[[taxon:Ovibos moschatus]]`, and the link resolver
accepts any of its names (`[[taxon:muskox]]`, `[[taxon:umingmak]]`) the way a
place resolves through its historic and Inuktitut names. Genus and family rows
exist so the tree can be walked; most rows are species.

The existing `animals` table is not merged into this: it holds named
individuals (Sverdrup's dog Gammelgulen, the Karluk's cat). An individual gets
a `taxon` column pointing at its species, and that is the whole change.

### observations

    observations
      id            INTEGER PRIMARY KEY
      taxon         TEXT NOT NULL      -- taxa.name; the writer resolves a common name
      date_text, date_start, date_end  -- as artifacts and events; dates table rows follow
      lat, lon, place                  -- required, unless `place` names a place row
      count         TEXT               -- "about 200", "12", "a herd", "present", "absent"
      count_n       REAL               -- the number when there is one
      unit          TEXT               -- individuals, pairs, nests, carcasses, per transect mile
      stage         TEXT               -- adult, calf, cub, pup, juvenile, mixed, unknown
      sex           TEXT
      behaviour     TEXT               -- hauled out, feeding, migrating, denning, killed, ...
      method        TEXT               -- a code: sighting, hunt, specimen, transect, aerial-survey,
                                          camera, acoustic, edna, catch-record, testimony
      observer      TEXT               -- people.name, or a vessel/expedition name
      vessel        TEXT               -- vessels.name when it applies
      detail        TEXT               -- the sentence that says what was seen, naming the observer
      confidence    TEXT               -- certain, probable, doubtful (identification, not the fact)
      artifact_id   TEXT               -- the photograph, quote or object that is the evidence
      event_id      INTEGER            -- the human-history event this also is
      sensitive     INTEGER DEFAULT 0  -- den, nest, haul-out, calving ground: publish coarsened
      origin        TEXT               -- research, ship, crew  (who wrote it; section 6)
      bibkey, pages, topic, updated

`check` demands a taxon that exists, a date, a position or place, and a
bibkey; an observation whose `method` is `catch-record` or `transect` wants a
`count_n`. A `sensitive` observation is published with its position rounded to
0.5 degrees and its place blank; the full row stays on grid.

### Natural places

`places.kind` already carries `polynya`. The vocabulary grows a natural set:
`glacier`, `ice-shelf`, `ice-island`, `polynya`, `bird-cliff`, `haul-out`,
`denning-area`, `calving-ground`, `fossil-site`, `formation`, `hot-spring`,
`lake`, `river`, `range`. The same cleanup that gave vessels a kind vocabulary
gives places one, and the natural kinds are part of it.

### Specimens and datasets

No new table. A museum specimen is an artifact of type `object` with the
catalogue number in `credit` and a `taxon` in its tags; a photograph of an
animal is an `image` whose observation row points at it. A survey or a time
series (Tener's transects, the White Glacier mass balance, the Hell Gate
polynya extent) is a source with `entry_type dataset`, and its per-record
content is observations. Sea-ice, weather and oceanographic records are not
re-entered here: the ship has them, and a page links out.

## 4. Topics and the tab

Topics get a `domain` column, `history` or `nature`, and the front end makes
a tab of each. The natural topics, a first cut, each with a researcher:

| slug | scope |
|---|---|
| muskox-and-caribou | the two land herbivores, the 1961 survey, the crashes and recoveries |
| polar-bear | the bear, the dens, the Lancaster Sound population, the encounters |
| walrus-and-seals | haul-outs, the hunt, ringed and bearded seal, harp seal at the ice edge |
| whales-and-narwhal | bowhead, narwhal, beluga; the whalers' catch as the first census |
| birds | the cliffs (Cape Vera, Coburg, Prince Leopold), ivory gull, eider, the 1876 to 1938 lists |
| fish-and-the-sea-floor | Arctic char, cod, the benthos, the trawls |
| plants-and-lichens | the flora lists from Parry's appendix to the Polar Continental Shelf Project |
| the-small-and-the-microbial | sea-ice algae, the plankton, the microbial mats, the ship's own science |
| rock-and-fossils | the fossil forests of Geodetic Hills, the Strand Fiord volcanics, the salt domes, Franklin 1955 |
| glaciers-and-ice-shelves | the Ward Hunt and Milne shelves, the ice islands, White Glacier, the retreat since 1959 |
| polynyas-and-the-ice | the North Water, Hell Gate, the Dundas polynya, the sea ice year by year |

Each topic writes taxa, observations, places, pages, and the artifacts behind
them, and links into the human topics where the record came from. The
human-history topics do not change; the observations pulled from their texts
carry the natural topic's slug and cite the same sources.

## 5. The wiki

A taxon page is generated like a person page, and its body is the row's
`note`; the front end lays out the names, the status, and two lists the row
gives it: **the record**, every observation of the taxon in date order with
observer and source, drawn from `observations` at publish time, and
**mentioned in**, from the links table as now. So the muskox page reads as a
species account followed by a 200-year sighting log, each line a link to the
narrative page it came from.

Hand-written pages work as they do now, with `[[taxon:...]]` links. Bare
first mentions of a taxon's names in any page body become links the way
person and place names do, so the human-history pages already written link
into the natural half without being touched.

The publish adds `taxa.json`, `observations.json` (a map layer: points by
taxon, with the date so the map can play the season and the century), and
generated `taxon/<slug>` pages; the timeline gains observations as a kind;
the keyword tree gains a taxon branch under "Fauna and Nature", which the
ontology already has.

## 6. Entry aboard: @doc's tab

The ship is read-only toward grid, and stays so. What the ship writes is a
**journal**: an append-only file of observation rows in the CLI's own
vocabulary, one JSON object per line, under `db/history/_journal/` on the
ship:

    {"kind": "observation", "id": "amundsen-2026-09-11-003", "taxon": "Balaena mysticetus",
     "date": "2026-09-11T14:22Z", "lat": 76.104, "lon": -92.41, "count": "1", "count_n": 1,
     "method": "sighting", "observer": "<crew name>", "vessel": "CCGS Amundsen",
     "detail": "...", "artifact_file": "_journal/img/2026-09-11-003.jpg", "origin": "ship"}

The tab's entry form writes that line, takes the position from the ship's
GPS and the time from the clock, lets @doc pick the taxon from the published
`taxa.json` (with the Inuktitut and French names in the picker), attaches a
photograph, and marks sensitive sightings. `history-sync.sh push-journal`
is the one ship-to-grid path: it rsyncs `_journal/` up. On grid,
`history-db.py ingest --journal` turns each line into rows through the same
writers as everything else, so `check` and the brief's rules apply, and it is
idempotent on `id`. Ship ids carry the `amundsen-<date>-` prefix, so there is
never a collision with research ids, and a corrected line with the same id
replaces the row on the next ingest.

The same journal format serves a crew member typing an observation into the
chat: @doc's model turns "two bears on the floe off the port bow" into a
journal line with the position and time filled in and asks for confirmation.
That is the wiring: the persona writes the journal, the journal reaches grid,
grid publishes, the tab shows the sighting on the map an hour later with
Sverdrup's bears beside it.

## 7. The research plan

**Wave 1, the record in the texts we hold.** Every primary narrative on disk
carries natural history: Parry's appendices of 1821 and 1824 (the first
systematic lists), Sverdrup's hunting returns, Greely's and Nares's natural
history reports, the whalers' catches (the whaling topic's logs are a bowhead
census by year), Tener 1961 (already in as text artifacts, to be re-entered
as observations), the RCMP patrol reports (game seen, dogs fed), Boas and the
oral-history record of animals and their names. A researcher per natural
topic reads the held texts first, writes observations and taxa, and only then
looks outward. Haiku readers over the text layers find the passages; the Opus
researcher enters them.

**Wave 2, the modern record.** COSEWIC and IUCN status reports (open),
Canadian Wildlife Service and DFO surveys (Crown, mostly `crown-open`), the
Polar Continental Shelf Project's reports, the McGill glacier record, the
Arctic journal (open access after 2016), the ship's own cruise reports.

**Wave 3, the ship.** The journal, from the first sighting of the season.

## 8. Checks and rules the brief gains

- A taxon name must resolve in the backbone (GBIF for land and birds, WoRMS
  for the sea) or carry `backbone_id` blank and a note saying why; `check`
  flags the rest. An offline list of the archipelago's known taxa, a few
  hundred names, ships with the tool so a researcher off the network can
  still validate.
- An observation without a date, a position and a bibkey is refused, as an
  artifact without a credit is.
- Historical counts are entered as written, in the unit written, and never
  converted in the row; the page does the arithmetic and says so.
- Identification doubt goes in `confidence`, not in the taxon. A narrative's
  "a whale" is `Cetacea` with `confidence certain`, not a guessed species.
- Sensitive sites are marked at entry, published coarsened, and never named
  in page prose.
- Inuktitut names follow the orthography the source uses, with the community's
  current spelling in `also` when it differs, and the source of every name is
  cited, because the names are knowledge somebody holds.

## 9. Open questions, for the ship

1. **Who is @doc?** A person, the model persona in the chat, or both. The
   journal design serves both, but the tab's entry form is built differently
   for a person typing than for a persona confirming.
2. **The backbone.** GBIF plus WoRMS is the default. If the ship's own science
   uses another (the ArcticNet or DFO species lists), it should be that.
3. **Sensitivity.** 0.5 degrees and a blank place is a first cut; @doc should
   set the rule per group (dens, nests, haul-outs, calving grounds).
4. **The ship's samples.** The ship's sample and cast databases stay where they
   are; an observation may carry a sample id in `detail`, but nothing is
   duplicated here. Confirm that is the boundary.
5. **The journal's pictures.** Photographs taken aboard are the crew's; the
   licence code for a journal image defaults to `attribution` with the
   photographer credited, unless the ship wants `cc-by-4.0`.
6. **Topic list.** Eleven is a first cut. Insects and spiders, freshwater
   life and the terrestrial invertebrates have no home yet and could be their
   own topic or fold into plants-and-lichens.

## 10. Order of work on grid

1. Schema and writers: `taxa`, `observations`, the `taxon` kind and its link
   resolution, `topics.domain`, the natural place kinds, `animals.taxon`.
   Tests. One commit.
2. CLI: `history-db.py taxon`, `observation`, `ingest --journal`; the
   published `taxa.json`, `observations.json`, taxon pages, the timeline kind.
3. The natural-history brief: a section appended to BRIEF.md, with the
   observation examples above as the worked commands.
4. The offline taxon list for the archipelago, seeded from the held texts and
   the COSEWIC lists, checked against GBIF and WoRMS once.
5. The journal format written down for the front end, and `push-journal` in
   the sync script. Issue on GitHub for the ship, the way issues 5 and 6 set
   out the animals, vessels and page contracts.
6. Wave 1.
