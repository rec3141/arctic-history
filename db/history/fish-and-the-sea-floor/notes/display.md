# Display note: fish and the sea floor

For the operator and the front end. What in this topic is worth showing, what shape it should take,
which fields of `observations.json` drive it, and which static figure stands in for it now.

## 1. The stations, as a map layer

**The series.** Every observation in this topic with `method` in (`dredge`, `trawl`, `sounding`) — 107 rows
at the time of writing, from 1818 to 1935. Each carries `lat`, `lon`, `date_start`, `value` (the depth) and
`unit` (almost always `fathoms`, four rows in `feet`).

**Why a widget beats the figure.** The static plate has to collapse repeat visits to one point and cannot
show the century passing. A `layer` widget with a date slider shows the record filling in: Baffin Bay in
1818-20, Barrow Strait and Wellington Channel in the 1850s, Smith Sound in 1875-76, the Parry Channel after
1906. A scientist aboard wants to know whether anyone has ever put an instrument on the bottom where the
ship is now, and that is a spatial question, not a temporal one.

**Units.** Depth is in fathoms as written. Convert on the axis and in the tooltip at 1 fathom = 1.8288 m.
Do not convert in the row.

**What to compare it with.** The ship's own multibeam coverage and CTD stations, and GEBCO/IBCAO
bathymetry, so a historical sounding can be read against the modern depth at the same place. Where the two
disagree by more than about twenty per cent the historical row is worth flagging; several of these figures
are wire-out readings with no correction for line drift.

**Stands in for it now:** [[artifact:fish-and-the-sea-floor-001]].

```json
{"kind": "layer", "subject": "sea-floor sediment", "place": "the archipelago and Baffin Bay",
 "since": "1818", "until": "1935",
 "title": "Where the sea floor of the archipelago was sampled"}
```

## 2. Depth worked against year

**The series.** The same rows, plotted as `value` against `date_start`. Log scale on the depth axis: the
range is 5 to 1,900 fathoms and a linear axis loses everything shallow.

**What it is for.** It shows what the instruments could reach and when, and it puts the doubtful readings
where a reader can see them: Kane's 1,900 fathoms on the axis of Baffin Bay sits far above everything else
and is entered with `confidence` `doubtful`, which the widget should render as an open or hollow mark.

**Units.** fathoms on the left, metres on the right.

**Stands in for it now:** [[artifact:fish-and-the-sea-floor-002]].

```json
{"kind": "series", "subject": "sea-floor sediment", "place": "the archipelago and Baffin Bay",
 "x": "date_start", "y": "value", "unit": "fathoms", "display_unit": "m",
 "since": "1818", "until": "1935",
 "title": "How deep the record goes: every sounding and dredge haul"}
```

## 3. The char catches

**The series.** Observations of `Salvelinus alpinus` and of `the char fishery` whose `count` parses to a
number of fish — nine rows, 1823 to 1958, from a single fish at Lake Alexandra to a thousand at the Salmon
River. Group by `observer` so that catches by ships' parties and catches by Inuit and Inughuit fishers can
be distinguished, which is the point of the plate.

**Caution.** These are not a time series of abundance and must never be drawn as one. They are nine
occasions on which somebody wrote a number down. The plate is a `bars` by occasion, not by year.

**What to compare it with.** The modern licensed char landings for Nunavut, if the layer ever holds them,
and Ojuvainath's twenty-year run count in South Greenland, which is the only actual series in the topic and
is presently held as one observation with the range in `count`.

**Stands in for it now:** [[artifact:fish-and-the-sea-floor-004]].

```json
{"kind": "bars", "subject": "Salvelinus alpinus", "y": "count", "group_by": "observer",
 "since": "1823", "until": "1958",
 "title": "The char catches the record puts a number to"}
```

## 4. The Camp Clay shrimping

**The series.** Six observations of `Amphipoda` at `Camp Clay`, March to May 1884, with the weight in the
`count` field as the journal gives it (a pint; 27 pounds; 40 pounds in two trips; 450 pounds for the month
of April). This is the one place in the topic where the sea floor is a survival record rather than a
natural-history one, and it should be shown as a `strip` of dated events on a spring calendar rather than a
bar chart, so that 15 May — the day sea kelp and shrimps became the only food — falls in its place.

**Units.** pounds as written; kilogrammes at 0.4536 on the second axis.

**Stands in for it now:** [[artifact:fish-and-the-sea-floor-003]].

```json
{"kind": "strip", "subject": "Amphipoda", "place": "Camp Clay", "x": "date_start",
 "since": "1884-03", "until": "1884-06",
 "title": "What the sea floor gave the Greely party at Camp Clay"}
```

## 5. A subject's own record

Every taxon subject in this topic already generates a page whose second half is its observations in date
order. Three of them are worth a widget of their own because the record is long enough to read as a
distribution rather than a list:

- **`Boreogadus saida`** — a `layer` filtered to the subject, showing every place the Arctic cod has been
  recorded from Parry's 1820 fish in a hole in the ice to the OBIS count. The OBIS row is a single
  observation carrying a total, not 14,629 points; the widget must not draw it as a point of equal weight
  with a nineteenth-century sighting. Mark rows whose `method` is `survey` distinctly.
- **`Salvelinus alpinus`** — a `strip` by month across all years, which shows the run: the record clusters
  hard in July and August at the river mouths and in the winter at the lakes.
- **`the benthos`** and **`sea-floor sediment`** — a `profile` of what came up against the depth it came
  from, using `value` as the depth and the `detail` text as the label. This is the plate that would most
  repay building and that a static figure cannot carry, because the interest is in reading the individual
  hauls.

```json
{"kind": "profile", "subject": "the benthos", "place": "the archipelago and Baffin Bay",
 "x": "value", "y": "value", "unit": "fathoms", "display_unit": "m",
 "since": "1818", "until": "1935",
 "title": "What came up, and from how deep"}
```

## 6. What the front end should not do

- Do not convert any depth, weight or count in the row. Every number in this topic is as written.
- Do not aggregate the OBIS totals with the historical observations in any count or density calculation.
  They are a different kind of row and are marked `method` `survey`, `observer` "the contributing surveys
  and museums".
- Do not draw the nine char catches as a trend.
- Sensitive rows: none in this topic at present. If a spawning river or a weir site is ever entered as a
  place, it should be marked `--sensitive` at entry and the prose must not name it.
