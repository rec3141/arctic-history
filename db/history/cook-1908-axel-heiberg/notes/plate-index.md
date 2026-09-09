# Plate / table index — Cook, *My Attainment of the Pole* (1911), and Crocker Land photo-lists (1913)

Method as in the Amundsen-Gjøa index: `pdfinfo` for page counts; `pdftotext
-layout` split on form-feed into per-PDF-page text (helper scripts in
`/tmp/sweepb-helper/`); pages under ~45 OCR words flagged as plate/blank
candidates; cross-checked against the front-matter "List of Illustrations"
(Cook, pdf pp. 29–30) and each plate's own OCR caption where legible. For
Cook, the cross-check was strongly corroborated by a set of plate images
already extracted to this document's `files/` directory in an earlier
session (`cook-1908-axel-heiberg-plate-nNNN.jpg`); those filenames use
`N = pdf page − 1` (0-indexed), and every one of them lines up with a
plate identified independently below.

**Format check** (`pdfimages -list`): both PDFs are **page-scan** Internet
Archive / archival PDFs — Cook's book is one full-bleed colour raster
(`jpx`) plus mask per page, same as the Amundsen volumes. The Crocker Land
photo-list PDF likewise shows exactly 3 image objects per page (2 raster
images + 1 mask) across all 266 pages, i.e. it too is a straight scan of
physical leaves, not a digital layout with separate embedded figures.
`pdfimages -f N -l N` pulls the whole page as a single image in both cases.

---

## C. Cook, *My Attainment of the Pole* — `cook-1908-axel-heiberg-cook1911-attainment.pdf`

`pdfinfo`: **702 pages**. Page-scan (see above).

### Front matter (not plates)

| pdf page | subject | kind |
|---|---|---|
| 1–8 | blank flyleaves / IA insert pages | blank |
| 9–14 | title page, "Other Books by Dr. Cook," half-title | text |
| 12 | **Frontispiece** — "Frederick A. Cook" portrait, facing the title page. Caption verbatim in OCR: *"FREDERICK A.COOK"* | photo |
| 16 | blank leaf | blank |
| 23–28 | **Table of Contents** (6 pages, printed pp. xiii–xviii) | table |
| 29–30 | **List of Illustrations** (printed plate list used for cross-checking below) | table |
| 31–32 | running title only ("MY ATTAINMENT OF THE POLE"), no image caption — looks like a repeated half-title leaf rather than a plate | text |

### Plates

Every caption below marked "verbatim in OCR" was read directly off the
plate page itself, not copied from the front-matter list — the printed
captions on Cook's plates OCR unusually cleanly for a page-scan.

| pdf page | printed/facing page | caption or subject | kind |
|---|---|---|---|
| 111–112 | facing 78 | "On the Chase for Bear" and/or "The Box-House at Annoatok and Its Winter Environment" (both entries share facing p.78 in the list; only one distinct plate leaf located here) — no caption in OCR | photo |
| 123–124 | facing 88 | "Man's Prey of the Arctic Sea — Walrus Asleep" — no caption in OCR | photo |
| 127 | facing 90 | "The Helpers — Northernmost Man and His Wife" — caption verbatim in OCR: *"THE HELPERS NORTHERNMOST MAN AND HIS WIFE"* | photo |
| 128 | (verso of p.127) | blank | blank |
| 153 | facing 114 | "Rudolph Francke in Arctic Costume" — caption verbatim in OCR: *"RUDOLPH FRANCKE IN ARCTIC COSTUME"* | photo |
| 154 | (verso of p.153) | blank | blank |
| 171 | facing 130 | "Midnight" / "'A Panorama of Black Lacquer and Silver'" (both facing p.130) — caption verbatim in OCR: *"MIDNIGHT A PANORAMA OF BLACK LACQUER AND SILVER."* | photo |
| 172 | (verso of p.171) | blank | blank |
| 195 | facing 162 | "A Mecca of Musk Ox Along Eureka Sound" — caption verbatim in OCR (lower case as scanned): *"a mecca of musk ox along eureka sound"* — list also has "A Native Helper" and "Ah-We-Lah's Prospective Wife," both facing 162, not separately located | photo |
| 196 | (verso of p.195) | blank | blank |
| 229 | facing 184 | "The Capture of a Bear" — caption verbatim in OCR: *"THE CAPTURE OF A BEAR"* — list also has "Rounding Up a Herd of Musk Oxen," facing 184, not separately located | photo |
| 230 | (verso of p.229) | blank | blank |
| 237 | facing 190 | "Along the Edge of the Polar Sea — Last Land's End" — caption verbatim in OCR: *"ALONG THE EDGE OF THE POLAE SEA LOST LAND S END"* | photo |
| 238 | (verso of p.237) | blank | blank |
| 243–244 | facing 194 | "Svartevoeg — Camping 500 Miles From the Pole" — no caption in OCR (already extracted as `plate-n242.jpg`) | photo |
| 251–252 | facing 202 | "Dashing Forward en Route to the Pole" — no caption in OCR (already extracted as `plate-n250.jpg`) | photo |
| 259–260 | facing ~206 | "Departure of Supporting Party" / "A Breathing Spell" / "Poleward!" (three list entries share facing p.206; only one distinct plate leaf located here, already extracted as `plate-n258.jpg`) — no caption in OCR | photo |
| 293–294 | facing 238 | "'The Igloo Built, We Prepare for Our Daily Camp'" — no caption in OCR | photo |
| 301 | facing 244 | "Bradley Land Discovered" — caption verbatim in OCR: *"BRADLEY LAND DISCOVERED"* — list also has "Submerged Island of Polar Sea" and "Going Beyond the Bounds of Life," both facing 244, not separately located | photo |
| 302 | (verso of p.301) | blank | blank |
| 315 | facing 256 | "Camping to Eat and Take Observations" — caption verbatim in OCR: *"CAMPING TO EAT AND TAKE OBSERVATIONS"* — list also has "On Again!," facing 256, not separately located | photo |
| 316 | (verso of p.315) | blank | blank |
| 325 | facing 264 | "Swift Progress Over Smooth Ice" — caption verbatim in OCR: *"SWIFT PROGRESS OVER SMOOTH ICE"* — list also has "Building an Igloo" and "A Lifeless World of Cold and Ice," both facing 264, not separately located | photo |
| 326 | (verso of p.325) | blank | blank |
| 341 | facing 278 | "'Too Weary to Build Igloos, We Used the Silk Tent'" — caption verbatim in OCR: *"TOO WEARY TO BUILD IGLOOS WE USED THE SILK TENT"* — list also has "'Across Seas of Crystal Glory to the Boreal Centre,'" facing 278, not separately located | photo |
| 342 | (verso of p.341) | blank | blank |
| 347–348 | facing 282 | "Mending Near the Pole" — no caption in OCR | photo |
| 351 | **not in printed list** | "Route to the Pole and Return" — caption verbatim in OCR: *"ROUTE TO THE POLE AND RETURN"*. Not itemized in the front-matter List of Illustrations; appears to be a separate route-map insert | map |
| 353 | facing 286 | "At the Pole — 'We Were the Only Pulsating Creatures in a Dead World of Ice'" — caption partly legible in OCR: *"AT THE POLE WE WERE THE ONLY PULSATING CREATURES IN A [...]"* | photo |
| 354 | (verso of p.353) | blank | blank |
| 361 | facing 292 | "Observation Determining the Pole — Photograph From Original Note" — caption partly legible in OCR: *"OBSERVATION DETERMINING THE POLE PHOTOGRAPH FROM [...]"* | photo |
| 362 | (verso of p.361) | blank | blank |
| 369–370 | facing 298 | "First Camp at the Pole, April 21, 1908" — no caption in OCR | photo |
| 384 | facing 310 | "'With Eager Eyes We Searched the Dusky Plains of Crystal, but There was No Land, No Life, to Relieve the Purple Run of Death'" — no caption in OCR | photo |
| 387–388 | facing 312 | "Record Left in Brass Tube at North Pole" — this is a facsimile of a handwritten field note; OCR renders it as illegible noise rather than a caption, consistent with reproduced handwriting | photo (facsimile) |
| 401 | facing 324 | "'Miles and Miles of Desolation'" — caption verbatim in OCR: *"MILES AND MILES OK DESOLATION."* — list also has "Homeward Bound," facing 324, not separately located | photo |
| 402 | (verso of p.401) | blank | blank |
| 411–412 | facing 332 | "Back to Land and Back to Life — Awakened by a Winged Harbinger" — no caption in OCR (already extracted as `plate-n410.jpg`) | photo |
| 417–418 | facing 336 | "Saved From Starvation — The Result of One of Our Last Cartridges" — no caption in OCR (already extracted as `plate-n416.jpg`) | photo |
| 439 | facing 356 | "E-Tuk-I-Shook Waiting for a Seal at a Blow-Hole" — caption verbatim in OCR: *"E-TUK-I-SHOOK WAITING FOR A SEAL AT A BLOW-HOLE"* | photo |
| 440 | (verso of p.439) | blank | blank |
| 455 | facing 370 | "Toward Cape Sparbo in Canvas Boat" — caption verbatim in OCR: *"TOWARD CAPE SPARBO IN CANVAS BOAT"* — list also has "Food and Fuel — Prize of a 15-Hour Battle," facing 370, not separately located | photo |
| 456 | (verso of p.455) | blank | blank |
| 467 | facing 380 | "Punctured Canvas Boat in Which We Paddled 1,000 Miles" — caption verbatim in OCR: *"PUNCTURED CANVAS BOAT IN WHICH WE PADDLED 1,000 MILE[S]"* — list also has "Famine Days..." and "Den in Which Were Spent 100 Double Nights," both facing 380, not separately located | photo |
| 468 | (verso of p.467) | blank | blank |
| 473 | facing 384 | "Bull Fights With the Musk Ox About Cape Sparbo" — caption verbatim in OCR: *"BULL FIGHTS WITH THE MUSK OX ABOUT CAPE SPARBO"* | photo |
| 474 | (verso of p.473) | blank | blank |
| 514 | **uncertain** | page shows only a running header (OCR: *"4S4 MY ATTAINMENT OF THE POLE"*, i.e. printed p.~454), no image caption. Could be a plate with an untranscribed caption, or a text page that was misflagged as low-text — recommend a visual check | photo? |
| 549 | facing 458 | "Governor Kraul in His Study" — caption verbatim in OCR: *"GOVERNOR KRAUL IX HIS STUDY"* — list also has "Arrival at Upernavik," facing 458, not separately located | photo |
| 550 | (verso of p.549) | blank | blank |
| 613 | facing 520 | "'The Mother of Seals' and Her Deserted Child" — caption verbatim in OCR: *"THE MOTHER OF SEALS AXI) HER DESERTED CHILD"* | photo |
| 614 | (verso of p.613) | blank | blank |

### Tables

| pdf page | subject | kind |
|---|---|---|
| 23–28 | Table of Contents | table |
| 29–30 | List of Illustrations | table |
| 661 | Appendix half-title | text |
| 663–671 | **"Observations, Etc. (Exact copy from original Field Papers)"** — a 9-page verbatim reproduction of Cook's field-journal entries: date, weather, temperature, barometer readings, ice/travel conditions | table |
| 672–679 | Appendix essay, "Questions That Enter Calculations for Position of the North Pole" (prose, not tabular) | text |
| 680 | "The Land-Divided Ice-Pack Reported by Peary Proves Cook's Attainment of the Pole" — caption verbatim in OCR | map |
| 681–688 | Appendix essay continues (prose rebuttal of Peary claims) | text |
| 689–696 | **Index** (8 pages, printed pp. ~595–602) | table |
| 697–699 | blank | blank |
| 700 | library loan/return-date slip (modern library artifact) | text |
| 701–702 | blank | blank |

No separate provisioning or sledge-ration list was found; the only
structured/tabular material in this volume is the field-observations log
(pdf 663–671) and the Index.

---

## D. Crocker Land Expedition photograph lists (MacMillan, 1913) — `crocker-land-1913-macmillan1913-photolists.pdf`

`pdfinfo`: **266 pages**. Page-scan, 3 image objects/page (see above).

### Nature of this document

This PDF is **not** a printed narrative book with occasional inserted
plates — its own title is "[Lists of Photographs of the Crocker Land
Expedition]," and the content bears that out: it is MacMillan's own
photograph register/log, largely in **cursive handwriting** (negative
numbers, dates, brief subject descriptions), alternating through most of
the document with tipped-in photographic prints. `pdftotext` OCR on
handwritten pages is almost entirely illegible noise rather than real
words — it still produces enough token "noise" to often clear the
45-word low-text threshold even though it is not readable prose, so the
low-text flag here should be read as "probable photograph page," and
non-flagged pages as "probable handwritten log page," **not** as any
guarantee of legibility either way.

Effectively the **whole PDF is one large table**: a running catalogue of
photographs, each with (illegible, handwritten) metadata and often a
facing print. It is presented here as one block rather than page-by-page
prose because that is what it structurally is.

### Front matter (not photographs)

| pdf page | subject | kind |
|---|---|---|
| 1 | Cornell/library ownership bookplate: "CROCKER LAND EXPEDITION" | text |
| 2 | illegible stamp/bookplate remnants | text |
| 3 | "Library of the ... for the People / for Education / for Science" bookplate | text |
| 4 | handwritten ledger fragment ("M 0 5," "H 0 4," etc. — possibly early negative numbers) | table |
| 5–6 | blank | blank |

### Photograph pages (candidate plates — low-text/blank, i.e. probable photographic prints)

No caption is recoverable in OCR for any of these (handwritten log,
described above); where a short legible fragment survived it is quoted
below, otherwise treated as a blank plate page. Facing/printed page
numbers do not apply — this is an unpaginated working register, not a
paginated book.

| pdf page(s) | caption / legible fragment | kind |
|---|---|---|
| 8 | none | photo |
| 46 | none | photo |
| 50–76 (every 2nd page, 14 pages) | none | photo |
| 79–87 (9 consecutive pages) | none — a run of 9 pages in a row with no handwritten text between them, i.e. a block of tipped-in prints not interleaved with log entries | photo |
| 90–94 (every 2nd page, 3 pages) | none | photo |
| 98–102 (every 2nd page, 3 pages) | none | photo |
| 106–108 (every 2nd page, 2 pages) | none | photo |
| 109–113 (5 consecutive pages) | none — another consecutive block | photo |
| 116 | none | photo |
| 120–124 (every 2nd page, 3 pages) | none | photo |
| 125 | none | photo |
| 128–138 (every 2nd page, 6 pages) | none | photo |
| 139–144 (6 consecutive pages) | none — consecutive block | photo |
| 146–150 (every 2nd page, 3 pages) | none | photo |
| 162–176 (every 2nd page, 8 pages) | none | photo |
| 177–178 (2 consecutive pages) | none | photo |
| 180–250 (every 2nd page, 36 pages) | none | photo |
| 254–256 (every 2nd page, 2 pages) | none | photo |
| 257–266 (10 consecutive pages) | none — a final consecutive block, likely a closing set of prints | photo |

### Pages with a legible OCR fragment (log entries or numbers worth a manual look)

| pdf page | fragment | likely reading |
|---|---|---|
| 7 | garbled cursive | handwritten log entry, illegible |
| 20–21 | garbled cursive | handwritten log entries, illegible |
| 25 | "17" | possibly a negative/catalogue number |
| 42 | garbled cursive | handwritten log entry, illegible |
| 65 | "57" | possibly a negative/catalogue number |
| 67 | "59" | possibly a negative/catalogue number |
| 78 | garbled cursive | handwritten log entry, illegible |
| 104 | "v\i" | illegible fragment |
| 114 | "120" | possibly a negative/catalogue number |
| 118 | garbled | illegible fragment |
| 126 | garbled | illegible fragment |
| 151 | garbled | illegible fragment |
| 227 | "IS" | illegible fragment / possible number |
| 229 | garbled cursive | handwritten log entry, illegible |
| 252 | "m" | illegible fragment |

### Table pages (the log itself)

The remaining ~110 pdf pages not listed above (interleaved with the
photograph pages, mostly odd-numbered in the pp. 9–177 stretch) carry
handwritten log/register text — dates, negative numbers, and photo
descriptions in MacMillan's hand — that clears the low-text threshold as
noise but is not machine-readable. Structurally these are the "list of
photographs" the PDF's title promises: **kind = table** throughout. None
of it could be transcribed here; a researcher wanting the actual
descriptions will need to read the handwriting directly from the page
images (`pdftoppm`/`pdfimages` per page, not OCR).

**Bottom line for cut-and-register purposes**: this PDF should be treated
as ~130 individual candidate photograph pages (listed above by pdf page
number) each needing a full-page image pull and manual inspection, paired
with an equal number of handwritten log pages that carry whatever caption
information exists — there is no separate front-matter "List of
Illustrations" to cross-check against, unlike documents A/B/C.
