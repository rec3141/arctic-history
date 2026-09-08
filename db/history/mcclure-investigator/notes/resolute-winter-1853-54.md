# The Resolute's drift winter, 1853-54: M'Dougall's meteorological journals

Source: George Frederick M'Dougall, Master of H.M.S. *Resolute*, *The Eventful Voyage
of H.M. Discovery Ship "Resolute" to the Arctic Regions* (London: Longman, Brown,
Green, Longmans and Roberts, 1857), Appendix, "Meteorological abstracts", from p. 500.
Local copy: `files/mcclure-investigator-mcdougall1857.txt` (Internet Archive OCR of
`eventfulvoyageof00mdou`) and `files/mcclure-investigator-mcdougall1857.pdf`.

**Where the previous run's page reference points.** The last worklog cited
"M'Dougall's meteorological journal, pp. 512-522". That is *not* in the 1855
Parliamentary blue book — pp. 512-522 there are Lieutenant Mecham's sledge journal.
It is in M'Dougall's own book of 1857, and the reference is right: the monthly
meteorological journals for September 1853 onward begin at p. 512 of that book.

## What the appendix contains

A month-by-month register kept on board the Resolute, one printed page per month,
running from September 1852 (Bridport Inlet, Melville Island) to April 1854 (beset in
the pack in Barrow Strait). Each row is one day and carries: aneroid barometer,
a thermometer reading in the fifties Fahrenheit that is the ship's interior
temperature, air temperature maximum, minimum and mean, a second interior figure,
wind direction, wind force, weather letters (b = blue sky, c = cloudy, m = misty,
o = overcast, q = squally, s = snow, z = haze), and a remarks column.

**The drift winter itself is the months below.** These are the printed headings,
verbatim, with the ship's own stated position:

| month | line in the OCR | heading, as printed |
|---|---|---|
| September 1853 | 32456 | "Kept on board H.M.S. 'Resolute,' Capt. H. Kellett, C.B., off Pt. Griffiths until the 10th, and beset in the Pack between that date and the end of the month, in Lat. 75 N., Long. 106 W." |
| October 1853 | 33106 | "wintering in the Pack, in Lat. 74 41 34 N., Long. 101 22 06 W." |
| November 1853 | 33862 | "wintering in the Pack, S.W.S. 28' from C. Cockburn. Lat. 74 41 N., Long. 101 22 W." |
| December 1853 | 34568 | "wintering in the Pack, S.W. by S., 28 miles from C. Cockburn, Lat. 74 41 N., Long. 101 22 W." |
| January 1854 | — | **not printed.** There is no January page: December's table is followed directly by February's. Whether the leaf is missing from this copy or the month was never printed is unresolved. |
| February 1854 | 35305 | "wintering in the Pack, in Lat. 74 41 30 N., Long. 101 22 00 W." |
| March 1854 | 35930 | "wintering in the Pack, in Lat. 74 41 30 N., Long. 101 22 06 W." |
| April 1854 | 36700 | "frozen up in Pack, in Lat. 74 41 30 N., Long. 101 22 06 W." |

So the whole winter was spent within a mile or two of **74 deg 41.5 min N, 101 deg 22 min W**
— about 28 miles S.W. by S. of Cape Cockburn, in mid-Barrow Strait. The ship was
beset on 10 September 1853 near Point Griffiths in about 75 N, 106 W, and by October
had drifted east-south-east to the position she held all winter.

## The daily rows, December 1853

Read directly off the OCR at lines 34568-34700 and checked one by one. In December
every air temperature is below zero Fahrenheit and the printed minus signs are lost by
the OCR; where the "maximum" reads lower than the "minimum" both are negative and are
given here with the sign restored. Interior figures are the two columns in the fifties
and sixties. Weather letters as above.

| date | air max | air min | air mean | interior | wind | force | weather | remarks as printed |
|---|---|---|---|---|---|---|---|---|
| 1853-12-01 | -16 | -23 | -19 | +59 | North | 2 | b. m. c. | faint flashes of aurora |
| 1853-12-02 | -18 | -26 | -21.7 | 62 | [ditto] | | b. m. | |
| 1853-12-03 | -17 | -25 | -21.7 | 62 | [ditto] | 1 | | 7 p.m., fine arch of aurora S.S.E. to W., altitude about 25 deg |
| 1853-12-04 | -24 | -36 | -32.2 | 64 | Calm | 0 | b. | |
| 1853-12-05 | -35 | -38 | -36.7 | 61 | West | [ditto] | b. m. | |
| 1853-12-06 | -30 | -38 | -34.5 | 59 | | 1 | b. c. | faint arch of aurora |
| 1853-12-07 | -37 | -42 | -40.3 | 54 | Calm | 0 | b. | aurora from S.W. to W. |
| 1853-12-08 | -34 | -40 | -36.4 | 54 | N.E. | 1 | b. c. | 8 p.m., a faint arch of aurora passing through the zenith, N.E. to S.E. |
| 1853-12-09 | -36 | -40.5 | -37.9 | 55 | | | b. | 1 a.m., mercury frozen |

Mercury freezes at about -38 F, so the entry for 9 December marks the first day of the
winter cold enough to put the mercurial thermometers out of use.

**Not yet transcribed.** October and November 1853 and February to April 1854 are in
the file and are legible page by page, but the Internet Archive OCR of these tables
breaks every cell onto its own line and drops the minus signs, so a machine parse of
them misaligns the columns. A future run should run `tools/ocr.sh` on pp. 512-518 of
`files/mcclure-investigator-mcdougall1857.pdf` and transcribe them from a proper
table recognition rather than from this text layer. Nothing in this note is a guess:
every row above was read off the OCR by eye.
