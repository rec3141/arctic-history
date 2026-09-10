# How the rock should be shown

A note for the operator and the front end, not a wiki page.

This is a geology topic, which means most of its record is **not a time series**. A rock unit has an age range, not a date; an outcrop has a place, not a value. The two things that genuinely vary and are worth a widget are the **history of observation** (who read the rock where, and when) and the **earthquake catalogue**. Everything else wants a map layer or a static plate.

## What is in `observations.json` for this topic

- `subject` is a rock unit, a structure (`Sverdrup Basin`, `salt diapir`, `Eurekan Orogeny`) or `earthquake`.
- `date_start` is the date of the **observation**, not of the rock. A row dated 1900-06-10 records Schei on Carboniferous limestone; nothing in the row says 340 million years. The unit's age lives on the subject, not the observation. **The front end must never plot `date_start` as if it were the age of the rock.**
- `value` and `unit` carry, variously: a bed thickness in `feet`, a dip in `degrees`, a terrace height in `feet`, an earthquake magnitude with the magnitude type as the unit (`Mw`, `mb`, `ML`, `MB`). These are not comparable across rows; filter by `subject` before plotting anything.
- `depth` is metres for the earthquake rows only, and is always 18000 (a nominal 18 km, meaning unresolved). Do not draw a depth profile from it.
- `method` separates the kinds of work: `specimen` and `sample` (someone with a hammer), `survey` (a field traverse), `aerial-survey` (Dunbar and Greenaway from the air), `instrument` (the seismographs), `testimony` (Inuit and Inughuit knowledge), `sighting`.

## Widgets worth building

    {"kind": "layer", "subject": null, "place": null, "title": "Where the rock has been read",
     "since": "1875", "until": "2026", "group_by": "method",
     "unit": null, "display_unit": null}

The primary widget for this topic: every observation as a point on the map, coloured by `method`, with the date range scrubbable. A scientist aboard wants to know whether anyone has ever looked at the rock near the ship's position, and who. The static stand-in is `rock-and-the-sverdrup-basin-fig-map.png`.

    {"kind": "bars", "subject": "earthquake", "place": null, "x": "date_start", "y": "value",
     "unit": "Mw", "display_unit": "Mw", "since": "1985", "until": "2026",
     "group_by": "date_start", "title": "Earthquakes catalogued in the archipelago, by year"}

Counts of catalogued events per year. Worth it because the answer is genuinely surprising — a few a year, none felt before 2009 — and because the shape of the series is mostly the shape of the seismograph network, which the title should say. The static stand-in is `rock-and-the-sverdrup-basin-fig-earthquakes.png`, which plots magnitude against date rather than counts and is the better plate; build the widget only if the map layer below is also built.

    {"kind": "layer", "subject": "earthquake", "place": null, "since": "1985", "until": "2026",
     "group_by": "value", "unit": "Mw", "display_unit": "Mw",
     "title": "Every catalogued earthquake, sized by magnitude"}

Epicentres on the map, marker size by magnitude. This is the one a scientist would actually use, because it shows that the seismicity traces the edge of the basin offshore and the rifted margin in Baffin Bay. Pair it with the bathymetry the ship is running over.

    {"kind": "bars", "subject": null, "place": null, "x": "date_start", "y": "value",
     "unit": "feet", "display_unit": "m", "group_by": "observer",
     "since": "1875", "until": "1975",
     "title": "Bed thicknesses measured in the archipelago, by the person who measured them"}

Marginal. Include only if the front end can filter to `unit == "feet"` and to the thickness rows; otherwise it mixes dips and terrace heights and is worse than nothing. The conversion is 1 foot = 0.3048 m.

## What should NOT be a widget

- **The stratigraphic column.** It is a range chart over 540 million years with thirty-five labelled bars and two annotations. No generic `series`, `bars` or `profile` renderer will make it legible, and it is the single most useful picture in the topic. Keep the static plate, `rock-and-the-sverdrup-basin-fig-column.png`, and make it clickable through to the subject pages.
- **The diapir section.** A conceptual diagram; there is nothing to drive it from. `rock-and-the-sverdrup-basin-fig-diapir.png`.
- **Anything with the rock's own age on an axis.** Ages live on `subjects`, not `observations`, and the front end does not read the subject's age. If a future schema puts `age_young` and `age_old` on the subject row, a `bars` widget over those would render the column automatically, and that is worth doing.

## Units, and what to compare with

| what | unit as written | show as | note |
|---|---|---|---|
| bed thickness | feet | feet, with metres beside | Schei, Feilden and Thorsteinsson all wrote feet; never convert in the row |
| dip | degrees | degrees | |
| raised terrace height | feet | feet and metres | compare with the post-glacial rebound curves in `the-land-surface` |
| earthquake magnitude | Mw, mb, ML, MB | as catalogued, with the type shown | the types are not interchangeable; label every point with its type |
| earthquake depth | m | do not show | always the nominal 18 km |

The comparison a scientist aboard actually wants is not within this topic at all: it is **the map sheet against the sea floor**. Twenty-two Geological Survey sheets are registered here as `map` artifacts with their map-area centres. If the front end can overlay a sheet's coverage box on the ship's track, that is worth more than any chart on this page.

## The static plates, and what each stands in for

| file | stands in for |
|---|---|
| `rock-and-the-sverdrup-basin-fig-column.png` | the stratigraphic column; nothing else will do |
| `rock-and-the-sverdrup-basin-fig-map.png` | the `layer` widget above |
| `rock-and-the-sverdrup-basin-fig-diapir.png` | a conceptual diagram; permanent |
| `rock-and-the-sverdrup-basin-fig-earthquakes.png` | both earthquake widgets above |

## The published sheets, and what the front end should do with them

The map count is no longer twenty-two. The topic now holds **fifty `map` artifacts**, and they fall into three groups the front end should treat differently.

1. **Geological map sheets with a real footprint** — the twenty-two 1:250,000 and tectonic-assemblage sheets already here, plus the six 1:500,000 sheets of Memoir 320 (`-840` to `-845`) and the two regional sheets of the 1991 synthesis (`-980`, `-981`). Every one of these covers a defined map area, and the `lat`/`lon` on the row is only its centre. **The overlay described above is the single most valuable thing that could be built for this topic**: a coverage box per sheet, drawn on the ship's map, so that a scientist can see at a glance which published sheet covers the ground the ship is passing and open its raster. The boxes are not in the database yet; they would have to be read off the sheets' own neat lines or from GEOSCAN's NTS fields, and that is a job for a person or a later run, not a widget.

2. **Sections, traverses and columnar sections** — the twelve columnar-section sheets of Memoir 320 (`-851` to `-862`), its traverses and structure sections, and the structural cross-sections of the synthesis (`-982`, `-983`). These are *line* geometries, not areas: a traverse runs from one named place to another, and a columnar section stands at a point. The columnar sections are the closest thing this topic has to a `profile` widget, but they are not driven by `observations` rows and should not be faked: show the raster, and let the reader zoom. Where a traverse's two ends are named in the title, the front end could draw the line.

3. **Correlation charts and time-scale tables** — `-921`, `-922`, `-984` to `-986`. These have no geography at all; the coordinate on the row is a courtesy. Do not put them on the map. They belong beside the stratigraphic column plate, as the reference the column is a simplification of.

## The plate as the subject page's opening picture

Most subjects in this topic now have a picture that is genuinely *of* them, which was not true before:

| subject | opening picture |
|---|---|
| `salt diapir` | `-902`, the Cape Levvel diapir mapped with its collar of upturned beds; then `-906`, the section through the gypsum body west of Mokka Fiord |
| `Otto Fiord Formation` | `-905`, the selenite crystals from the Mokka Fiord body |
| `Canadian Shield` | `-822`, the kersantite dyke cutting the granite-diorite at Kjothaugen, and the thin sections `-823` to `-825` |
| `Strand Fiord Formation` | `-900`, the geology of the south coast of Strand Fiord |
| `Eurekan Orogeny` | `-947`, the Sawtooth Range across Slidre Fiord |
| `Franklinian Basin` | `-807`, Schei's series A resting on the Archaean at Harbour Fiord |
| `earthquake` | no picture exists and none should be invented; the catalogue plate stands |

The front end already lays a subject's observations out as a record; giving each subject one opening image, chosen here rather than by first-registered order, is worth a field on the subject row.

## A fifth static plate

`rock-and-the-sverdrup-basin-fig-thickness.png` (artifact `-305`) is new: fourteen named formations of the Sverdrup Basin against their greatest measured thickness in metres, in stratigraphic order. It is built straight from `observations` rows with `unit == "m"` and `bibkey == "trettin1991geology"`, taking the largest value per subject, so a `bars` widget could render it automatically:

    {"kind": "bars", "subject": null, "place": null, "x": "subject", "y": "value",
     "unit": "m", "display_unit": "m", "group_by": "subject",
     "since": "1974", "until": "1991",
     "title": "The greatest measured thickness of each formation of the Sverdrup Basin"}

The one thing the widget cannot do is put the units in stratigraphic order rather than alphabetical or by value, because the database does not yet know which unit lies on which. Until `subjects` carries an age or an ordinal, the static plate is the better picture, and the ordering is written into the script that draws it.
