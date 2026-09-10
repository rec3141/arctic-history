# Display note: glaciers and ice caps

For the operator and the front end. Not a wiki page.

What this topic's rows are shaped like, what should be drawn from them, and which static plate stands in for each widget until the front end can render it. The seven plates already registered are `glaciers-and-ice-caps-f01` to `f07` — six figures drawn from the rows and one conceptual diagram, `f07`, the zones of a high-arctic accumulation area, which is not a figure at all and should never be shown as one; each is 1600 px wide, drawn with `tools/atlas.py`, and cited from the pages. Sections 5 and 6 below were open questions in run 1 and are now answered: the World Glacier Monitoring Service data are in, and both plates are drawn.

---

## 1. The Agassiz melt record — the single most important series here

**What it is.** The fraction of each half-century's ice on the Agassiz Ice Cap that is clear refrozen meltwater rather than bubbly snow ice, from about 8300 BC to 1961, from the combined 1984 and 1987 cores. It is the most sensitive summer thermometer the Canadian Arctic has and it needs no calibration to be legible: nil means the summers did not melt, a hundred means they melted through.

**Why a scientist aboard wants it.** It is the baseline. Any statement about how fast the Arctic is warming is measured against something, and thirty years of station record is not enough. This is ten thousand years, at 80 degrees north, from the ice itself. It is also the thing that reframes the expedition record: Kane, Hayes and Greely arrived in the coldest summers of the Holocene, and what they described is the ice at its greatest recent extent.

**The rows.** Subject `melt-layer percentage`, place `Agassiz ice-core site`, `value` in `%`, `unit` `%`, `date_text` the year of the half-century, `bibkey` `noaa2431agassiz`, `artifact_id` `glaciers-and-ice-caps-d01`. Only eight milestone values are entered as observations, per the brief's rule that a time series is not re-entered; the whole series is in the artifact file, which is 207 rows of `year<TAB>percent`.

**The widget.** A series against time, but a very long one, so the x axis wants a log-like or broken treatment rather than a linear one if the front end can manage it; otherwise linear, as the plate does it.

```json
{"kind": "series", "subject": "melt-layer percentage", "place": "Agassiz ice-core site",
 "x": "date_start", "y": "value", "unit": "%", "display_unit": "%",
 "since": "-8339", "until": "1961",
 "title": "Ten thousand years of Ellesmere summers, from the Agassiz Ice Cap"}
```

**Stands in for now:** `glaciers-and-ice-caps-f01`.

**Note for whoever implements it.** The observation rows alone will draw eight points, not a curve. Either the front end reads the artifact file `glaciers-and-ice-caps-agassiz-pcmeltco_50yr.txt` (three header blocks then `year<TAB>value`, tab separated, years negative for BC), or a later run enters the whole series as observations. Reading the file is better: it keeps the row count honest.

---

## 2. Ice thickness across northern Ellesmere, April 1966

**What it is.** The greatest ice depth the Scott Polar Research Institute's radio echo sounder returned over each glacier and ice cap on four days of flying. Fourteen places, 135 m to 900 m.

**Why aboard.** It is the answer to "how much ice is up there", and it shows the thing that matters for the future: several of these glaciers rest on beds below sea level, so their retreat can go marine and run away.

**The rows.** Subject `glacier ice thickness`, `place` the glacier, `value` in metres, `method` `sounding`, `instrument` the sounder, `bibkey` `hattersleysmith1969glacier`, all dated April 1966.

```json
{"kind": "bars", "subject": "glacier ice thickness", "group_by": "place",
 "y": "value", "unit": "m", "display_unit": "m",
 "since": "1966-04", "until": "1966-04",
 "title": "How thick the ice is: the airborne sounding of April 1966"}
```

**Stands in for now:** `glaciers-and-ice-caps-f03`. Ordered by value, horizontal, with the value printed beside each point — a lollipop, not a bar, because the numbers are single measurements not totals.

---

## 3. The ablation stakes on the Gilman Glacier, 1957 and 1958

**What it is.** Ice lost at each of nine stakes by 15 August 1958, three at the meteorological mast at 1,030 m and six half a mile down glacier, with the 1957 and 1958 means at the mast as reference lines.

**Why aboard.** It shows the two facts about high-arctic ablation that a number alone hides: loss rises steeply down a glacier, and two consecutive summers at the same place can differ by a factor of two. Anybody reading a single season's melt figure should see this first.

**The rows.** Subject `ablation`, place `Gilman Glacier`, `value` in `cm`, `qualifier` naming the stake, `bibkey` `lotz1958operation` or `hattersleysmith1959research`.

```json
{"kind": "bars", "subject": "ablation", "place": "Gilman Glacier",
 "group_by": "qualifier", "y": "value", "unit": "cm", "display_unit": "cm",
 "since": "1957", "until": "1959",
 "title": "Two summers on the Gilman Glacier: what the ablation stakes read"}
```

**Stands in for now:** `glaciers-and-ice-caps-f04`, which converts to inches on the right axis because the reports print both.

---

## 4. The land ice as a map layer

**What it is.** Forty-seven place rows of kind `glacier`, `ice-cap` and `ice-core-site`, with positions from the Canadian Geographical Names Database, plus White, Thompson, Baby and Müller from the science-stations topic. Run 2 added the Melville South Ice Cap, John Evans Glacier, the Penny and Meighen ice-core sites, and the Mittie, Airdrop and Good Friday Bay glaciers of the surge inventory.

**Why aboard.** It is the index. A scientist who wants to know what the ice is called on the coast the ship is passing wants this, filtered to the map view, with each point opening its place page and its observations.

```json
{"kind": "layer", "subject": "glacier", "place": "",
 "since": "1854", "until": "2026",
 "title": "The land ice of the archipelago, glacier by glacier"}
```

**Stands in for now:** `glaciers-and-ice-caps-f02`, which was drawn from the forty places the topic held in run 1 and does not yet show the seven added since — the Melville South Ice Cap in particular lies west of its extent. Redrawing it is a small job for a later run and would be worth doing once the place list settles. In the live map this should be a filter on `places.kind in (glacier, ice-cap, ice-core-site)` rather than on the observations layer, because many of these places carry no observation of their own yet.

---

## 5. Glacier front change, White against Thompson — DRAWN

**What it is.** The one comparison in this topic that a scientist will ask about unprompted: two glaciers a few kilometres apart, at the head of the same fiord, in the same weather, one going back and the other coming forward for half a century.

**What the rows now support.** The World Glacier Monitoring Service's front-variation table, extracted for this archipelago as `glaciers-and-ice-caps-d05`: twenty-five surveyed front positions on White, Thompson and Crusoe glaciers between 1960 and 1977, with the survey and reference dates and the change in **metres** (the WGMS column is metres, not millimetres — the released CSV header in this topic says `front_variation_m` for that reason). Cumulatively over those surveys Thompson came forward 293 m, Crusoe 34 m, White went back 93 m. Five of the individual surveys are entered as observations, 167 to 171; the rest live in the file.

**The widget.** Two series against time, cumulative from the first survey, on one axis — this is the exception to the rule at the foot of this note, because both series are the *same quantity* measured the same way, and the comparison is the whole point.

```json
{"kind": "series", "subject": "glacier retreat", "place": "White Glacier",
 "x": "date_start", "y": "value", "unit": "m", "display_unit": "feet",
 "since": "1959", "until": "1978",
 "compare": {"subject": "glacier advance", "place": "Thompson Glacier", "since": "1959", "until": "1978"},
 "title": "Two glaciers, one fiord: Thompson coming forward while White goes back"}
```

**Stands in for now:** `glaciers-and-ice-caps-f06`. The front end should plot the *cumulative* sum from the first survey, not the per-survey increments, and should mark each survey with a dot so that the long straight segments — 1969 to 1976 on White, 1968 to 1971 on Thompson — read as gaps in the record rather than as steady motion.

**Still wanting.** The annual terminus positions after 1977 are in Cogley, Ecclestone and Adams 1996 (Eastern Snow Conference 53: 83–94) and Hember, Cogley and Ecclestone 2003 (ESC 60: 214–224), neither of which is held. With those the plate could run to the present and show Thompson's advance ending about 2008.

---

## 6. The mass-balance series — DRAWN

**What it is.** The annual mass balance of every Canadian Arctic glacier the World Glacier Monitoring Service holds, from `glaciers-and-ice-caps-d04`: 296 whole-glacier balance years, 1960 to 2023, for eleven glaciers, of which five are long series — White, Baby, Meighen, the northwest basin of Devon, and Melville South — and the sixth, Barnes south dome, ran ten years and stopped.

**Why aboard.** This is the ground truth that satellite gravimetry estimates of Canadian Arctic ice loss are checked against, and one of the few long in-situ series anywhere above 75 degrees. It is also the plainest possible statement of when the change happened: the five cumulative curves are nearly flat for thirty years and then bend down together after about 1990.

**The rows.** Subject `mass balance`, `place` the glacier or ice cap, `value` in `mm w.e.`, `method` `survey`, `bibkey` `wgms2026fog`, `artifact_id` `glaciers-and-ice-caps-d04`. Thirty-one milestone observations are entered, 141 to 171: for each long series its first year, its most negative year, its most positive year, its last year and its cumulative. The 296 annual values are in the artifact file, per the brief's rule that a time series is not re-entered.

**The widget.** Bars about zero for one glacier, or cumulative lines for the comparison. Both are worth having; the bars answer "how bad was that year" and the lines answer "when did it change".

```json
{"kind": "bars", "subject": "mass balance", "place": "White Glacier",
 "group_by": "date_start", "y": "value", "unit": "mm w.e.", "display_unit": "m w.e.",
 "since": "1959", "until": "2026",
 "compare": {"subject": "mass balance", "place": "Baby Glacier", "since": "1959", "until": "2026"},
 "title": "Sixty years of weighing White Glacier"}
```

```json
{"kind": "series", "subject": "mass balance", "place": "Melville South Ice Cap",
 "x": "date_start", "y": "value", "unit": "mm w.e.", "display_unit": "m w.e.",
 "since": "1960", "until": "2026",
 "compare": {"subject": "mass balance", "place": "Meighen Island ice cap", "since": "1960", "until": "2026"},
 "title": "Cumulative mass balance of the Canadian Arctic reference glaciers"}
```

**Stands in for now:** `glaciers-and-ice-caps-f05`, which plots all five cumulatively. **The front end must read the file, not the observation rows**, for either widget: the rows are milestones and would draw five points, not a curve. `glaciers-and-ice-caps-wgms-caa-mass-balance.csv` is plain CSV with a header row, `glacier,wgms_id,year,area_km2,winter_balance_mm_we,summer_balance_mm_we,annual_balance_mm_we,remarks`; empty cells are genuinely missing, not zero. For the `series` form, sum `annual_balance_mm_we` from each glacier's own first year.

---

## 6a. The four deep cores, as a profile

**What it is.** Four ice caps in this archipelago have been drilled to bedrock, and the four holes are not comparable in depth but are comparable in what they reach: Meighen 1965, 121.2 m, bottoming in ice younger than the climatic optimum; Devon 1971–73, 299 m, with late Wisconsinan ice in the last 1.7 m; Agassiz, four holes 1977–1989; Penny P95 1995, 333.78 m to the bed, dated to 7,900 years at 319 m and tied to the Younger Dryas at 326.

**Why aboard.** The depth of the hole is not the interesting number; the age at the bottom is. A scientist asking "how far back does the ice here go" should get all four answers at once and see that the southernmost ice cap, Penny, holds the oldest ice.

**The rows.** Subject `ice core`, `place` the ice-core site, `value` the depth in `m`, `date` the drilling year or the age of the layer, `method` `core`. Observations 125, 126, 172 to 176, 178, 201.

```json
{"kind": "profile", "subject": "ice core", "place": "",
 "x": "value", "y": "date_start", "unit": "m", "display_unit": "m",
 "group_by": "place", "since": "-9550", "until": "1996",
 "title": "How deep and how old: the four cores drilled to bedrock"}
```

**Stands in for now:** nothing. It wants either a small multiple — one column per ice cap, depth downward, with the dated horizons marked — or a table. A table would be honest and is cheap; this is a case where the front end should not reach for a chart.

---

## 7. The record itself, as a strip

**What it should be.** Every observation in this topic by date and by method — testimony, sighting, survey, sounding, core, sample — so that the shape of the record is visible: a scatter of eyewitness description from 1854 to 1938, then a dense block of measurement from 1953, then the cores reaching back ten thousand years off the left-hand edge.

**Why aboard.** It answers "how well is this known, and since when", which is the question behind most questions about Arctic change.

```json
{"kind": "strip", "subject": "", "place": "",
 "x": "date_start", "group_by": "method",
 "since": "1854", "until": "2026",
 "title": "How the land ice came to be recorded"}
```

**Stands in for now:** nothing. It is cheap to draw once the front end has `strip`, and it would work for every nature topic without modification, which is why it is written as a spec rather than drawn.

---

## 8. The diagram, and what it is for

`glaciers-and-ice-caps-f07` is the topic's only conceptual diagram: the five zones of a high-arctic accumulation area on a schematic long profile, drawn from Müller 1962. **It is not derived from a series and there is no widget for it.** It exists because the single most misleading thing a reader can do with this topic is take a snow line off a photograph and call it an equilibrium line, and because no plate in the layer shows the zones. The front end should treat it as an illustration: show it beside the [[subject:superimposed ice]] and [[subject:accumulation]] subject pages and on page 50, and never regenerate or animate it.

If a later run wants a second diagram, the one the topic still lacks is the surge cycle drawn as a reservoir emptying: the upper basin thickening through the quiescent decades and the ice moving bodily down to the front in the active phase. The rows to draw it from are in place — Otto Glacier's 1959-64 height changes by elevation band, and the fifty-one glaciers of the Copland inventory with their advances and their one clear case of post-surge retreat.

---

## Units, and the conversion rule

Every value in this topic is stored as the source printed it. That means the same quantity appears in several units and the page, or the widget, does the arithmetic:

- **Ablation and accumulation**: `cm` and `m` in the Operation Hazen reports, `inches` (water equivalent) in Baird 1955 and Hattersley-Smith 1955. Display in cm; the conversion is 1 in = 2.54 cm, and a water-equivalent figure is *not* the same quantity as a depth of ice — do not convert between them (ice to water is roughly ×0.9 and the reports usually give both).
- **Ice thickness**: `m` from 1966 onward, `feet` in Baird 1955. Display in m; 1 ft = 0.3048 m.
- **Glacier front heights and altitudes**: `feet` throughout the nineteenth century and into the 1950s. Display in m.
- **Velocity**: `cm/day` and `m/day` in the Hazen reports, `feet` per interval in Hayes, `m/a` on the subject row. Display in m/a; a daily rate is not simply ×365 for a glacier whose movement is seasonal, so label a converted annual rate as an extrapolation.
- **Mass balance**: `mm w.e.` per year in the WGMS rows, already the standard unit. Display in metres water equivalent when the number is cumulative, because thirteen and a half metres reads and minus 13,499 millimetres does not.
- **Front variation**: `m`, positive forward and negative back, as the WGMS gives it. Feet on the right axis where the plate has room.
- **Melt percentage and oxygen isotopes**: dimensionless and per mil. No conversion.

## Two things the front end should not do

**Do not draw a trend line through the melt record.** It is not a linear series and the shape is the point.

**Do not put glacier front positions and mass balance on the same axis.** A front position responds to the bed and to the glacier's size as much as to climate, and Thompson Glacier is the standing proof of it. Where both are shown, they belong in stacked panels with the caveat in the subtitle. Two *front* series together are a different matter and section 5 asks for them: there the quantity is the same and the comparison is the point.
