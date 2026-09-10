# Natural history: a design for the second half of the layer

The History tab holds what people did in the archipelago. The natural half
holds what the archipelago is and does: the rock and its fossils, the ice on
land and at sea, the water under the ship, the sky above it, the weather, the
magnetic field, and the living things, together with what every one of those
people wrote down about them on the way. Both halves sit in the one database
and the one wiki, so the muskox page cites Sverdrup's diary and Sverdrup's
page links the muskox; the North Magnetic Pole's page runs from James Clark
Ross standing on it in 1831 to the observatory's readings this year; and the
model aboard answers a question about ice thickness in McClure Strait with
Seadragon's 1960 soundings and the Amundsen's own.

This document is the design to argue with before any table is made. Aboard,
the domain belongs to @doc, the resident scientist, with @ada, the ship's
library, beside him; the entry side is built with them (section 7a).

## 1. Principles carried over

- **Grid owns the database; the ship pulls.** That holds. The ship's own
  observations reach grid through a journal file, not a second writer
  (section 7).
- **Everything is written as it is found**, through the one CLI, with a
  worklog line, and the brief is the contract. A natural-history researcher
  gets a section added to BRIEF.md, not a different brief.
- **Sources, licences, credits** work exactly as now: every observation cites
  a `bibkey` and pages, every image carries a credit and a licence code, every
  dataset is a source with `entry_type dataset`.
- **Names in the languages of the region.** A species, a rock unit, a wind, a
  kind of ice carries its scientific or technical name, its English and French
  names, and its Inuktitut and Kalaallisut names as first-class fields, the
  way a place carries `inuktitut` and `historic`. The ice vocabulary in
  Inuktitut is knowledge, and it is cited.
- **No discovery framing.** Nothing here was discovered. It was observed,
  measured, recorded, sounded, collected.

## 2. The atom: an observation of nature

Dates are the atom of the timeline; the **observation** is the atom of the
natural half. One subject, one date, one position, one source, and where there
is a number, the number in the unit it was written in.

    a walrus haul-out of about 200, Dundas Harbour, 16 August 1924,
    Joy, RCMP annual report 1925 p. 42                              biology

    the dip needle at 89 deg 59 min, the Victory's party at the Magnetic Pole,
    1 June 1831, J. C. Ross, Narrative p. 556                       geomagnetism

    no bottom at 1,000 fathoms, the Polaris off Cape Union,
    28 August 1871, Davis's Narrative                               oceanography

    minus 58.5 F, the coldest of the winter, Fort Conger,
    4 February 1882, Greely vol. 1 appendix                         meteorology

    a Tertiary forest bed with stumps in place, Stenkul Fiord,
    June 1901, Schei in New Land vol. 2                             geology

    an aurora in three arcs through the zenith, Winter Harbour,
    15 January 1820, Parry's Journal p. 118                         astronomy

    ice shelf front 4 km back from the 1906 position, Ward Hunt,
    August 1962, Hattersley-Smith                                   glaciology

    a bowhead surfacing beside the ship, 76.1 N 92.4 W,
    11 September 2026, the Amundsen's bridge watch                  biology

The first seven are already in the texts on disk and are the first wave's
work. The last is what @doc enters aboard. They are the same row.

An observation is a fact about nature at a time and place; an **event** stays
a fact about people. Where the two coincide (the muskoxen at De To Kratere fed
the dogs that got Isachsen home; Ross's reading at the pole is the point of
his whole journey) the observation carries `event_id` so the timeline and the
map show one thing, not two.

Time series are observations too, but they are not all re-entered. A station's
daily record is a source with `entry_type dataset`, and the layer enters the
extremes, the firsts and the milestones (the coldest day, the first open
water, the year the shelf calved) as observations that cite it, with a page
that links to the whole series where it lives.

## 3. Subjects: what an observation is of

One table for every kind of subject, because the wiki wants one kind of page
and one link form for all of them. The `kind` says how the row is read.

    subjects
      name          TEXT PRIMARY KEY   -- Ovibos moschatus; Eureka Sound Group; aurora;
                                          North Magnetic Pole; air temperature; sea ice; bowhead
      kind          TEXT               -- a code, section 3.1
      domain        TEXT               -- biology, geology, glaciology, oceanography, sea-ice,
                                          meteorology, astronomy, geomagnetism, hydrography
      rank          TEXT               -- for taxa and rock units: species, genus; formation, group
      parent        TEXT               -- the next rank up, by name; makes the tree
      english, french, inuktitut, kalaallisut   -- the names in the region's languages
      also          TEXT               -- other names, synonyms, spellings, semicolon list
      unit          TEXT               -- for a variable: F, C, fathoms, m, deg, hPa, cm
      status        TEXT               -- COSEWIC or IUCN code with the year, for a taxon
      backbone_id   TEXT               -- GBIF or WoRMS id; a Lexicon of Canadian Geologic
                                          Units id; a SIMBAD or IAU name for a sky object
      note          TEXT               -- the reader's paragraph
      bibkey, topic, updated

### 3.1 Kinds

| kind | domain | examples |
|---|---|---|
| `taxon` | biology | Ovibos moschatus, Cetacea, Saxifraga oppositifolia, a sea-ice diatom |
| `unit` | geology | Eureka Sound Group, Strand Fiord Formation, the Sverdrup Basin, a salt diapir |
| `fossil` | geology | the Geodetic Hills forest, a Devonian fish from Ellesmere, a Miocene beaver-pond fauna |
| `mineral` | geology | native iron of Disko, the Cape York meteoritic iron, coal at Bache Peninsula |
| `landform` | geology | pingo, patterned ground, raised beach, ice-wedge polygon, solifluction lobe |
| `ice` | glaciology, sea-ice | ice shelf, ice island, glacier surge, sikuliaq (new ice), multiyear floe, polynya |
| `water` | oceanography, hydrography | sounding, water temperature, salinity, current, tide, wave, a warm layer |
| `weather` | meteorology | air temperature, pressure, wind, fog, blizzard, ice fog, parhelion, halo |
| `sky` | astronomy | aurora, the midnight sun's first appearance, an eclipse, a comet, Venus in daylight |
| `field` | geomagnetism | declination, dip, the North Magnetic Pole, a magnetic storm |
| `phenomenon` | any | mirage and looming, the Novaya Zemlya effect, a rock fall, an earthquake felt |

A `taxon` row is what the earlier draft called a taxon: genus and family rows
exist so the tree can be walked. A `unit` row walks the stratigraphic column
the same way. A `weather` or `water` row with a `unit` is a variable, and an
observation of it carries a value. A `sky`, `field`, `ice` or `phenomenon`
row is a named thing that happens, and an observation of it may or may not
carry a number.

A subject is a wiki kind: `[[subject:Ovibos moschatus]]`, and the resolver
takes any of its names (`[[subject:muskox]]`, `[[subject:umingmak]]`,
`[[subject:aurora]]`, `[[subject:North Magnetic Pole]]`), the way a place
resolves through its historic and Inuktitut names. Bare first mentions in any
page body link the way person and place names do.

The existing `animals` table is not merged into this: it holds named
individuals (Sverdrup's dog Gammelgulen, the Karluk's cat). An individual gets
a `subject` column pointing at its species, and that is the whole change.

## 4. Observations

    observations
      id            INTEGER PRIMARY KEY
      subject       TEXT NOT NULL      -- subjects.name; the writer resolves a common name
      date_text, date_start, date_end  -- as artifacts and events; dates table rows follow
      lat, lon, place                  -- required, unless `place` names a place row
      depth         REAL               -- metres below the surface, for the water column and cores
      height        REAL               -- metres above, for the sky and the air; negative for ice cores
      value         REAL               -- the number, when there is one
      unit          TEXT               -- as written: F, fathoms, feet, deg, cm; never converted in the row
      count         TEXT               -- for living things: "about 200", "12", "a herd", "present", "absent"
      qualifier     TEXT               -- for anything: "first of the season", "coldest of the winter",
                                          "no bottom at", "estimated", "corrected for index error"
      stage, sex, behaviour            -- for living things
      method        TEXT               -- a code: sighting, hunt, specimen, transect, aerial-survey,
                                          camera, acoustic, edna, catch-record, testimony,
                                          instrument, sounding, dredge, core, sample, station-record
      instrument    TEXT               -- the thermometer, the dip circle, the lead line, the CTD
      observer      TEXT               -- people.name, or the party or watch
      vessel        TEXT               -- vessels.name when it applies
      detail        TEXT               -- the sentence that says what was seen, naming the observer
      confidence    TEXT               -- certain, probable, doubtful (the identification or the reading)
      artifact_id   TEXT               -- the photograph, quote, chart or object that is the evidence
      event_id      INTEGER            -- the human-history event this also is
      sensitive     INTEGER DEFAULT 0  -- den, nest, haul-out, calving ground, a fossil site at risk
      origin        TEXT               -- research, ship, crew (who wrote it; section 7)
      bibkey, pages, topic, updated

`check` demands a subject that exists, a date, a position or place, and a
bibkey; an observation of a variable wants a `value` and a `unit`; a
`transect` or `catch-record` wants a `count`; a sounding wants a `depth` or a
`value`. Historical numbers are entered as written, in the unit written; the
page does the arithmetic and says so. A `sensitive` observation is published
with its position rounded to 0.5 degrees and its place blank; the full row
stays on grid.

## 5. Places, specimens, datasets

**Natural places.** `places.kind` already carries `polynya`. The vocabulary
grows a natural set: `glacier`, `ice-cap`, `ice-shelf`, `ice-island`,
`polynya`, `bird-cliff`, `haul-out`, `denning-area`, `calving-ground`,
`fossil-site`, `outcrop`, `meteorite-fall`, `hot-spring`, `pingo`,
`ice-core-site`, `tide-station`, `magnetic-station`, `weather-station`,
`lake`, `river`, `range`, `basin`, `sound`, `channel`. The same cleanup that
gave vessels a kind vocabulary gives places one, and the natural kinds are
part of it.

**Specimens and samples.** No new table. A museum specimen, a rock sample, a
meteorite, an ice core is an artifact of type `object` with the catalogue
number in `credit` and the subject in its tags; the observation row points at
it. A photograph of an animal, a fossil bed, an aurora is an `image` the
observation cites. The ship's own sample and cast databases are not
duplicated: an observation may carry the sample or cast id in `detail`, and a
page links out.

**Datasets.** A survey, a station record, a time series (Tener's transects,
the White Glacier mass balance, the Alert record since 1950, the Eureka
radiosonde, the Resolute magnetic observatory, the Canadian Ice Service charts,
the tide gauge at Alert) is a source with `entry_type dataset`, and the layer
holds its milestones as observations and a page that says where the whole of
it lives.

## 6. Topics, the tab, the wiki

Topics get a `domain` column, `history` or `nature`, and the front end makes
a tab of each. The natural topics, a first cut, one researcher each:

| slug | scope |
|---|---|
| rock-and-the-sverdrup-basin | the geology: the basin, the salt domes, the Strand Fiord volcanics, Franklin 1955, the mapping since |
| fossils-and-deep-time | the Geodetic Hills forest, the Devonian fishes, the Miocene beaver pond, the Cambrian of the Shield edge |
| meteorites-and-minerals | the Cape York irons and their people, the coal seams the expeditions burned, the Ellesmere Island oil and gas |
| the-land-surface | permafrost, pingos, patterned ground, raised beaches and the land's rise since the ice, the Hazen plateau |
| glaciers-and-ice-caps | the Agassiz and Devon ice cores, White Glacier since 1959, the surges, the retreat |
| ice-shelves-and-ice-islands | Ward Hunt and Milne, T-3, WH-5, the calvings of 1961, 2008 and after |
| the-sea-ice | the ice year by year, the ice vocabulary, the North Water, Hell Gate and the polynyas, the ship's own record |
| the-water-column | soundings from Polaris to multibeam, the Lincoln Sea, the Atlantic layer, currents, tides |
| the-weather-and-the-climate | the winters as the expeditions recorded them, the station records since 1947, the trend |
| the-sky | aurora, the polar night and the midnight sun, eclipses and comets seen from the ice, the transit of 1882 at Fort Conger |
| the-magnetic-pole | the pole's wander from Ross 1831 to now, declination, the observatories, the storms |
| muskox-and-caribou | the two land herbivores, the 1961 survey, the crashes and recoveries |
| polar-bear | the bear, the dens, the Lancaster Sound population, the encounters |
| walrus-and-seals | haul-outs, the hunt, ringed and bearded seal, harp seal at the ice edge |
| whales-and-narwhal | bowhead, narwhal, beluga; the whalers' catch as the first census |
| birds | the cliffs (Cape Vera, Coburg, Prince Leopold), ivory gull, eider, the lists from 1820 to 1938 |
| fish-and-the-sea-floor | Arctic char, cod, the benthos, the dredges and trawls |
| plants-and-lichens | the flora lists from Parry's appendix to the Polar Continental Shelf Project |
| the-small-and-the-microbial | sea-ice algae, the plankton, the microbial mats, the ship's own science |

Each topic writes subjects, observations, places, pages, and the artifacts
behind them, and links into the human topics where the record came from. The
human-history topics do not change; the observations pulled from their texts
carry the natural topic's slug and cite the same sources.

**The subject page** is generated like a person page: its body is the row's
`note`, and the front end lays out the names, the unit or status, and two
lists the row gives it: **the record**, every observation of the subject in
date order with observer, value and source, drawn from `observations` at
publish time, and **mentioned in**, from the links table as now. So the
muskox page reads as a species account followed by a two-hundred-year
sighting log; the air-temperature page as a note followed by every recorded
extreme from Parry's winter to the station's; the North Magnetic Pole's page
as the story of the wander, each fix a line with its observer.

**The publish** adds `subjects.json`, `observations.json` (a map layer: points
by subject and domain, with the date and the value so the map can play the
season, the century and the number), and generated `subject/<slug>` pages;
the timeline gains observations as a kind; the keyword tree gains branches
for the domains under the "Fauna and Nature" and "Ice and sea" heads it
already has.

## 7. Entry aboard: @doc's tab

The ship is read-only toward grid, and stays so. What the ship writes is a
**journal**: an append-only file of observation rows in the CLI's own
vocabulary, one JSON object per line, under `db/history/_journal/` on the
ship:

    {"kind": "observation", "id": "amundsen-2026-09-11-003", "subject": "Balaena mysticetus",
     "date": "2026-09-11T14:22Z", "lat": 76.104, "lon": -92.41, "count": "1",
     "method": "sighting", "observer": "<crew name>", "vessel": "CCGS Amundsen",
     "detail": "...", "artifact_file": "_journal/img/2026-09-11-003.jpg", "origin": "ship"}

    {"kind": "observation", "id": "amundsen-2026-09-11-004", "subject": "aurora",
     "date": "2026-09-12T03:10Z", "lat": 76.2, "lon": -92.6, "qualifier": "first of the season",
     "method": "sighting", "observer": "<crew name>", "detail": "...", "origin": "ship"}

The tab's entry form writes that line, takes the position from the ship's
GPS and the time from the clock, lets @doc pick the subject from the
published `subjects.json` (with the Inuktitut and French names in the picker
and the domain as a filter), attaches a photograph, and marks sensitive
sightings. `history-sync.sh push-journal` is the one ship-to-grid path: it
rsyncs `_journal/` up. On grid, `history-db.py ingest --journal` turns each
line into rows through the same writers as everything else, so `check` and
the brief's rules apply, and it is idempotent on `id`. Ship ids carry the
`amundsen-<date>-` prefix, so there is never a collision with research ids,
and a corrected line with the same id replaces the row on the next ingest.

The same journal format serves a crew member typing into the chat: @doc's
model turns "two bears on the floe off the port bow" or "halo with parhelia
all afternoon" into a journal line with the position and time filled in and
asks for confirmation. That is the wiring: the persona writes the journal,
the journal reaches grid, grid publishes, and the tab shows the sighting on
the map an hour later with Parry's parhelia of 1820 beside it.

What the ship does not journal: the CTD casts, the multibeam, the met
station, the ice radar. Those have their own systems. A remarkable reading
from any of them (the warmest Atlantic water yet seen in Nares Strait, no
bottom where the chart says 200 m) is journalled as an observation with the
cast or file id in `detail`, so the page can point at it.

## 7a. @ada and @doc

Aboard, two personas run on a local Gemma model with the wiki as their second
brain: **@ada**, the ship's library, and **@doc**, the resident scientist.
The layer serves both from the same published files, and the design has to
suit a model that reads excerpts rather than a database.

- **@ada** answers from the whole wiki, both halves, and the bibliography:
  who was here, what they wrote, where the copy is. Nothing changes for her
  except that subject pages and observations join the excerpt index.
- **@doc** answers from the natural half first: a subject page with its
  record, the observations near the ship's position and date, the datasets
  behind them. The publish therefore writes, beside `observations.json`, a
  per-subject excerpt (`subject/<slug>` page body followed by its record as
  dated lines) and a per-place excerpt (every observation within a place's
  reach, in date order), so a small model can be handed the muskox record or
  the Eureka Sound record as one text.
- **@doc writes the journal.** A crew member's sentence in the chat becomes a
  journal line: @doc fills the position and time from the ship, matches the
  subject against `subjects.json` by any of its names, and asks for
  confirmation before appending. The journal format is flat on purpose, so
  a local model produces it reliably; the writer on grid does the strict
  validation, and a line that fails ingest comes back to the ship's log as
  a problem to fix, not a silent drop.
- **Both read the same excerpts the historian reads today**, so the front
  end's excerpt builder grows two kinds and no new mechanism.

## 8. The research plan

**Wave 1, the record in the texts we hold.** Every primary narrative on disk
carries natural history of every kind: Parry's appendices of 1821 and 1824
(the first systematic lists of animals, plants and rocks, and the
meteorological and magnetic registers); Ross at the Magnetic Pole; Kane's,
Hayes's and Hall's tide, temperature and sounding tables (Schott reduced them
all for the Smithsonian and those volumes are free); Nares's and Greely's
natural history and physical appendices and the 1882 transit; Sverdrup's
hunting returns and Schei's geology; the whalers' catches (a bowhead census
by year); Peary's meteorites; the RCMP patrol reports (game seen, ice met,
dogs fed); Krüger's geology; Operation Franklin; Dunbar and Greenaway's
aerial descriptions; Tener 1961 (already in as text artifacts, to be
re-entered as observations); Hattersley-Smith's ice shelves; the McGill
glacier reports; Boas and the oral-history record of animals, ice and
weather and their names. A researcher per natural topic reads the held texts
first, writes subjects and observations, and only then looks outward. Haiku
readers over the text layers find the passages; the Opus researcher enters
them.

**Wave 2, the modern record.** COSEWIC and IUCN status reports, Canadian
Wildlife Service and DFO surveys, the Geological Survey's maps and the
Lexicon of Canadian Geologic Units, the Polar Continental Shelf Project's
reports, the ice-core papers, the Canadian Ice Service atlases, the
Meteorological Service's station normals and extremes, the Geomagnetic
Laboratory's pole positions, the Arctic journal (open access after 2016),
ArcticNet and the ship's own cruise reports.

**Wave 3, the ship.** The journal, from the first sighting of the season.

## 8a. Data sources, by domain

The human half was built from narratives and archives. The natural half
needs the record's other shape: catalogues, series, maps and status reports,
most of them open. A first list, with the licence code each falls under and
the route from grid.

| domain | source | what it gives | licence | route |
|---|---|---|---|---|
| biology | GBIF occurrence downloads for the archipelago's bounding box | every georeferenced specimen and sighting the museums and surveys have shared, with dates and collectors | `cc-by-4.0` / `cc0` per dataset | API, no login; cite the download DOI |
| biology | OBIS | the marine occurrences: benthos, fish, plankton, mammals | `cc-by-4.0` | API |
| biology | Canadian Museum of Nature collections | the type specimens and the historical collections from Parry to the PCSP | `attribution` | portal and GBIF |
| biology | COSEWIC and IUCN status reports | population, range, the threats, by species | `crown-open` / `attribution` | open PDFs |
| biology | Canadian Wildlife Service and DFO reports | the surveys since Tener: muskox, caribou, bear, walrus, whale counts | `crown-open` | publications.gc.ca (session cookie, section 8) |
| biology | Nunavut Wildlife Management Board and the co-management boards | harvest studies and Inuit knowledge reports | `attribution`, some `not-cleared` | open PDFs, ask where unclear |
| biology | the Arctic journal and Polar Record | the field papers, a century and a half of them | `open-access` after 2016, `in-copyright-licensed` before | AINA free; Cambridge Core through the library |
| geology | GEOSCAN, the Geological Survey of Canada | memoirs, bulletins, maps, open files, the 1:250,000 sheets | `crown-expired` / `crown-open` | open downloads |
| geology | WEBLEX, the Lexicon of Canadian Geologic Units | every formation with its type section, age and author | `crown-open` | web, per unit |
| geology | Canadian Geochronology Knowledgebase; the Nunavut Geoscience portal | ages and the territory's own maps | `crown-open` | open |
| geology | the Meteoritical Bulletin database | the Cape York irons and every other fall and find | `attribution` | web |
| glaciology | GLIMS and the Randolph Glacier Inventory | every glacier outline with an id | `cc-by-4.0` | download |
| glaciology | the World Glacier Monitoring Service | White Glacier and the other mass-balance series | `attribution` | web, email for map sheets |
| glaciology | the Agassiz and Devon ice-core papers and NOAA paleoclimate | the cores and their records | `public-domain` (NOAA) / `in-copyright-cited` | NOAA open |
| sea ice | the Canadian Ice Service: weekly charts, the climatic atlas, the digital archive since 1968 | the ice year by year, the polynyas, the freeze-up and break-up dates | `crown-open` (Open Government Licence) | open data portal |
| sea ice | NSIDC sea-ice index and the passive-microwave record | the daily concentration since 1978 | `public-domain` | download |
| sea ice | the Inuit sea-ice vocabulary: SIKU, the Igliniit project, community atlases | the words for the ice and the trails across it | `attribution` / `not-cleared` until asked | open PDFs; ask the communities' projects |
| oceanography | GEBCO and IBCAO | the bathymetry, and the older soundings behind it | `public-domain` / `attribution` | download |
| oceanography | DFO's ocean data (Marine Environmental Data Section), the Polar Data Catalogue, ArcticNet | casts, moorings, the ship's own past cruises | `crown-open` / `cc-by-4.0` | portals, some registration |
| oceanography | CHS tide tables and the Alert gauge | the tides | `crown-open` | open |
| meteorology | ECCC historical climate data: Alert, Eureka, Resolute, Isachsen, Mould Bay | the daily record since 1947, the normals and the extremes | `crown-open` (Open Government Licence) | open data, CSV by station |
| meteorology | the JAWS and Operation Hazen reports; the IGY record | the first years, station by station | `crown-expired` / `public-domain` (US) | GEOSCAN, HathiTrust |
| astronomy, geomagnetism | NRCan Geomagnetic Laboratory: the observatories and the pole positions | declination, the storms, the pole's track since 1831 | `crown-open` | open |
| astronomy | the 1882 transit reports (Fort Conger; the international campaign), the eclipse and comet notices in the narratives | the sky as the expeditions saw it | `public-domain` | HathiTrust, IA |
| all | the Smithsonian Contributions to Knowledge: Schott's reductions of Kane, Hayes and Hall | the tides, temperatures, magnetics and soundings of 1853 to 1873, reduced | `public-domain` | IA, Biodiversity Heritage Library |
| all | the Biodiversity Heritage Library | the natural-history appendices of every narrative, as page images with OCR | `public-domain` | API, no login |
| all | the Polar Data Catalogue (CCIN) | the metadata of every Canadian Arctic dataset, with contacts | `cc-by-4.0` | API |
| all | Wikidata and Wikimedia Commons | the ids that tie a subject to GBIF, the Lexicon and the rest; the pictures | `cc0` / per file | API, one query at a time from this address |

The route column matters as much as the source: most of this is open and
reachable from grid without the library, which is a different world from the
human half.

## 9. Checks and rules the brief gains

- A subject name must resolve in its backbone (GBIF for land and birds,
  WoRMS for the sea, the Lexicon of Canadian Geologic Units for rock units,
  the WMO vocabulary for weather, the IAU for sky objects) or carry a blank
  `backbone_id` and a note saying why; `check` flags the rest. An offline list
  of the archipelago's known subjects, a few hundred names across the
  domains, ships with the tool so a researcher off the network can still
  validate.
- An observation without a date, a position and a bibkey is refused, as an
  artifact without a credit is.
- Numbers are entered as written, in the unit written, and never converted in
  the row; the page does the arithmetic and says so. Fahrenheit stays
  Fahrenheit in Greely's row.
- Doubt goes in `confidence`, not in the subject. A narrative's "a whale" is
  `Cetacea`, not a guessed species; a "great depth" with no lead is a
  `qualifier`, not a `value`.
- Sensitive sites are marked at entry, published coarsened, and never named
  in page prose.
- Inuktitut and Kalaallisut names follow the orthography the source uses,
  with the community's current spelling in `also` when it differs, and the
  source of every name is cited, because the names are knowledge somebody
  holds. The sea-ice vocabulary above all.

## 10. Open questions, for the ship

1. **The entry form.** @doc is the persona; the question is whether the crew
   also get a form to type into directly, or only the chat. The journal
   serves both.
2. **The backbones.** GBIF plus WoRMS for life and the Lexicon for rock units
   are the defaults; the ship's own species and station lists may be better.
3. **Sensitivity.** 0.5 degrees and a blank place is a first cut; @doc sets
   the rule per kind (dens, nests, haul-outs, calving grounds, fossil sites).
4. **The boundary with the ship's systems.** Casts, multibeam, met and ice
   radar stay where they are; the layer holds the remarkable reading and the
   pointer. Confirm that is the line.
5. **The journal's pictures.** Photographs taken aboard are the crew's; the
   licence code for a journal image defaults to `attribution` with the
   photographer credited, unless the ship wants `cc-by-4.0`.
6. **The topic list.** Nineteen is a first cut. Insects, freshwater life and
   the terrestrial invertebrates have no home yet; seismology and the
   earthquakes felt in the narratives could fold into the land-surface topic.
7. **Units on the page.** Whether the page shows the original unit with a
   conversion beside it, or the converted value with the original in a
   tooltip. The row is fixed either way.

## 11. Order of work on grid

1. Schema and writers: `subjects`, `observations`, the `subject` kind and its
   link resolution, `topics.domain`, the natural place kinds,
   `animals.subject`. Tests. One commit.
2. CLI: `history-db.py subject`, `observation`, `ingest --journal`; the
   published `subjects.json`, `observations.json`, subject pages, the
   timeline kind.
3. The natural-history section of BRIEF.md, with the observation examples
   above as the worked commands.
4. The offline subject list for the archipelago, seeded from the held texts
   and the status and lexicon lists, checked against the backbones once.
5. The journal format written down for the front end, and `push-journal` in
   the sync script. Issue on GitHub for the ship, the way issues 5 and 6 set
   out the animals, vessels and page contracts.
6. Wave 1.
