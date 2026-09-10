# Display note: walrus and seals

For the operator and the front end. Not a wiki page. It says, for every series
in this topic worth showing, what the figure or widget should be, which fields
of `observations.json` drive it, the units, what a scientist aboard would
compare it with, and which static figure stands in for it now.

## The shape of this topic's record

Five hundred and thirty-three observations, five species and a subspecies row, 1822
to the present day. It divides into three records of quite different kinds, and
a display that mixes them without saying so will mislead:

1. **The narrative record, about 240 rows, 1822 to 1946.** Dated encounters
   from Parry and Lyon, Kane, Hall, Tyson, Nares and Feilden, Greely, Peary,
   Sverdrup, Cook, Amundsen at Uqsuqtuuq, Bernier, Low, Boas, Rasmussen,
   Stefansson, Jenness among the Copper Inuit, Birket-Smith and the RCMP annual reports of 1921 to 1935. Its
   thickness follows the observers, not the animals: the August peak in it is
   half ships' phenology. It also carries the testimony rows, in which the
   observer is an Inuk or Inughuit hunter or a community.
2. **The modern survey, management and community record, about 40 rows, 1950 to
   2017.** The DFO aerial-survey estimates by stock and the COSEWIC catch
   table, which are the only rows in the topic that are a real time series;
   and the Qikiqtani Truth Commission community histories, whose rows carry
   each community's own sealing year, the sealskin prices and trade volumes of
   1955 to 1964, and what the relocations did to a sealing season. Filter these
   apart on `method` `testimony` with a `qtc2013` bibkey where you want the
   community record alone.
3. **The occurrence-photograph record, 249 rows, 1900 to 2026.** GBIF
   occurrences with images, overwhelmingly research-grade iNaturalist
   photographs of the last fifteen years, plus fourteen museum specimens whose
   date and position are those of the collection, not of the photograph. Its
   density follows where people with cameras go, which is the settlements, the
   cruise tracks and the Labrador coast.

A fourth series is latent in the community rows and worth a plate when a run
has time for it: the sealskin price and the skins traded, 1955 to 1964, against
the 1984 boycott that ended the trade. It wants `value` with `unit` `dollars`
and `sealskins`, and it is four rows so far — an argument for entering the rest
of the trade figures rather than for drawing it yet.

Any widget that pools these should say which rows it is drawing on, or
filter on `method`: `sighting`, `hunt`, `catch-record` and `testimony` are the
narrative record; `aerial-survey` and `survey` are the modern one; `camera` and
`specimen` are the photograph record.

Three fields carry most of the information: `subject`, `date_start`, and
`lat`/`lon`. `count` is free text on purpose (*a large number*, *about 200*,
*eighteen*, *12*) and must never be coerced to a number silently: a widget that
needs a number should use only the rows where `count` parses, and should show
how many rows it dropped. `value` with `unit` carries the numbers that are
numbers: body masses in pounds, a bearded seal's length in feet, the survey
estimates in walrus, the catch totals in walrus.

## 1. The walrus layer on the map — the first thing to build

A map layer of every walrus record, filtered by date, is the single most useful
thing this topic can give the ship, because the animal is tied to shallow banks
and the ship crosses them.

```json
{"kind": "layer", "subject": "Odobenus rosmarus", "since": "1820", "until": "2026",
 "title": "Walrus recorded in the archipelago and Baffin Bay, 1822 to now"}
```

Notes for the implementation: `sensitive` rows publish at half-degree rounding
with `place` blank, and eleven of the walrus rows are marked sensitive because
they name a haul-out or an ugli. The layer must respect that and must not draw
a haul-out label. Colour by the era, not by `method`. The static figure
`walrus-and-seals-fig-walrus-map.png` stands in for this now.

## 2. The season strip — for the bridge watch

```json
{"kind": "strip", "subject": "Odobenus rosmarus", "x": "date_start", "group_by": "subject",
 "since": "1820", "until": "2026", "title": "The months in which each pinniped is recorded here"}
```

One row per species, one mark per dated record, month on the x axis. The
comparison a scientist wants beside it is the ship's own season: the
*Amundsen* is here in the same months the ships of this record were, so the
strip should be able to shade the ship's current window. Static figure:
`walrus-and-seals-fig-season.png`. Draw the narrative rows and the camera rows
in different marks: the camera rows are summer-biased for a different reason.

## 3. Body mass by species

```json
{"kind": "bars", "subject": "Erignathus barbatus", "y": "value", "unit": "pounds",
 "display_unit": "kg", "group_by": "subject",
 "title": "Recorded body masses, in the pounds the observers wrote"}
```

Eight rows only, so this is a dot plot rather than bars in practice; the `bars`
kind with one bar per animal is the closest thing in the fixed vocabulary. The
conversion is pounds to kilograms, 0.4536. A scientist aboard would compare it
with modern published masses (a bearded seal of 250-300 kg, a ringed seal of
50-70 kg, an Atlantic walrus bull of 800-1,200 kg) and would find the
nineteenth-century walrus figures low, because they are hoist reckonings of
butchered animals. Static figure: `walrus-and-seals-fig-body-mass.png`.

## 4. The catch by year, 1980 to 2015 — now buildable

The one genuine annual series the topic holds. It is not in the observation
rows year by year, because a published table is a dataset and the layer enters
its milestones rather than re-keying it: the rows are
`walrus-and-seals-244` to `-247` (the 1982 maximum, the 2013 minimum, the
thirty-six-year total, the 2010-15 annual mean by population), and the whole
table stands behind them in the source `cosewic2017walrus`, Table 2, and in the
plate drawn from it.

```json
{"kind": "bars", "subject": "Odobenus rosmarus rosmarus", "y": "value", "unit": "walrus",
 "group_by": "place", "since": "1980", "until": "2015",
 "title": "Walrus landed in the eastern Canadian Arctic, by year and population"}
```

Static figure, and the thing to show until the front end can read the table
itself: `walrus-and-seals-fig-catch-1980-2015.png`, stacked by Central-Low
Arctic subsistence, sport hunt and High Arctic. What a scientist aboard would
put beside it is the ship's own position against the Foxe Basin and northern
Hudson Bay grounds, which supply over half the Canadian catch.

## 5. The survey estimates by stock

```json
{"kind": "bars", "subject": "Odobenus rosmarus rosmarus", "y": "value", "unit": "walrus",
 "group_by": "place", "since": "2005", "until": "2015",
 "title": "What the aerial surveys counted, stock by stock"}
```

Nine rows, `method` `aerial-survey`, drawn from the 2017 COSEWIC report: 727 in
Penny Strait-Lancaster Sound, 503 in western Jones Sound and 1,251 in Baffin
Bay in August 2009; 10,379 at the Foxe Basin uglit in September 2011; 5,500 in
northern and western Hudson Bay in September 2014; 2,100 to 2,500 at Hoare Bay;
6,020 wintering in Hudson Strait in April 2012; 200 in the Low Arctic. Three of
those rows are `sensitive` because they count animals at named haul-outs, so
the bars must be labelled by stock and never by ugli. Static figure:
`walrus-and-seals-fig-surveys.png`, which also sets the 6,020 wintering animals
of Hudson Strait apart from the rest, because they belong to several stocks and
would otherwise be counted twice. The comparison worth
offering is the ship's transit against the stock boundaries: the High Arctic
stocks total 2,481 animals, which is the order of a single Foxe Basin count.

## 6. The record beside the ship's position

The most useful widget of all, and the one that needs nothing new: given the
ship's own latitude and longitude, the nearest observations of any pinniped in
date order. That is the per-place excerpt the design already calls for
(NATURE-DESIGN section 7a), and it wants no spec of its own beyond the map
layer above. With the occurrence photographs in, most positions in Baffin Bay
and Hudson Strait now return a picture as well as a sentence.

## The diagrams

Two are drawn and registered, and both are drawn rather than photographed
because no plate in the held texts shows the thing in section:

- `walrus-and-seals-fig-aglu.png`, the ringed seal's breathing hole through the
  fast ice, with the chamber, the snow lair, the ice thickness the animal will
  keep open, and the hunter's indicator across the opening, from Kane 1856
  v. 1 pp. 261-262, Boas 1888 and Rasmussen 1931.
- `walrus-and-seals-fig-spears.png`, the three spears of the Iglulingmiut as
  Parry had them described in 1822-23: the oonak for the small seal, the uklaik
  or akleega for the large seal with its blown bladder, the katleelik for the
  walrus and the whale, and the siatko, the bone head that comes free of the
  point and turns across the wound like a toggle on its allek of ugjuk skin.
  Parry 1824 pp. 507-509.

A third worth drawing when there is time is the walrus's tie to the bottom: a
section from the ugli out across a bank, with the depth the animal will dive to
for clams (about eighty metres) marked against the soundings the narratives
give, which would show at a glance why the grounds are where they are.

## Units, everywhere

Masses are in pounds as written; the page converts (x 0.4536). Lengths are in
feet as written (x 0.3048). Depths, where they appear, are in fathoms as
written (x 1.8288 for metres). Survey estimates and catch totals are counts of
animals and convert to nothing. Nothing in this topic is converted in the row.
