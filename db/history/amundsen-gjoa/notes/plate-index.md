# Plate / table index — Amundsen, *The North West Passage* (1908), Vols. I & II

Method: `pdfinfo` for page counts; `pdftotext -layout` split on form-feed into
per-PDF-page text (helper scripts in `/tmp/sweepb-helper/`); pages under ~45
OCR words flagged as plate/blank candidates; a pdf-page → printed-page
mapping built by interpolating between real body-text pages that still show
a legible running page number, then cross-checked against the front-matter
"Illustrations" list (Vol. I: pdf pp. 13–15; Vol. II: pdf pp. 15–17) and,
where present, the plate's own OCR caption.

**Format check** (`pdfimages -list`): both PDFs are **page-scan** Internet
Archive PDFs — every page is one full-bleed colour raster (`jpx`) plus a
1-bit mask/soft-mask, i.e. a photograph of the physical leaf, not a digital
text layout with separately embedded figure objects. `pdfimages -f N -l N`
pulls the *whole page* as a single image. For a full-page plate that image
already *is* the plate (crop only to trim the leaf edge). For an
illustration printed inline on a page that also carries body text (see the
"embedded, not a separate leaf" notes below), the extracted raster will
contain the surrounding type as well — those need a manual crop, not just a
page pull.

---

## Volume I — `amundsen-gjoa-northwest-passage-v1.pdf`

`pdfinfo`: **358 pages**. Text extracted as page-scan (see above).

### Front matter (not plates)

| pdf page | printed/facing page | subject | kind |
|---|---|---|---|
| 1–2 | – | blank flyleaves | blank |
| 3 | – | half-title: "The Gjoa Expedition, 1903–1907 / The North West Passage / by Roald Amundsen" | text |
| 4 | facing title (unpaginated) | **Roald Amundsen** — Frontispiece (per printed list, entry 1). No caption in OCR (plain portrait). | photo |
| 5 | – | title page | text |
| 6 | – | "Published November 23rd, 1907" (imprint) | text |
| 7 | – | dedication | text |
| 8, 10, 12, 16 | – | blank leaves interleaved between Preface / Contents / List of Illustrations | blank |
| 9 | – | Preface | text |
| 11 | – | **Contents** (single page) | table |
| 13–15 | – | **List of Illustrations** (printed plate list used for cross-checking below) | table |

### Plates

| pdf page | printed/facing page | caption or subject | kind |
|---|---|---|---|
| 23 | facing 7 | "Deck of the 'Gjoa'" — caption verbatim in OCR: *"Aft Cabin. b. Engine Room. c. Main Hold. d. Fore Cabin. 'GJOA' (47 TONS R.)"* | diagram |
| 24 | facing 7 | "The 'Gjoa'" [ship photograph] — no caption in OCR; per printed list | photo |
| 27 | facing 11 | "Members of the 'Gjoa' Expedition" — caption partly legible: *"Anton Lund. Helmer Hansen."* (crew names) | photo |
| 28 | (verso of p.27) | blank reverse of the plate leaf | blank |
| 43–44 | facing ~27 | "Godhavn, with Disco Island in the Background" — no caption in OCR; nearest printed-list entry | photo |
| 47 | facing 31 | "Eskimo Beauties from Godhavn" — caption verbatim in OCR: *"ESKIMO BEAUTIES FROM GODHAVN."* | photo |
| 48 | (verso of p.47) | blank | blank |
| 81–82 | facing ~65 | "Fire" — no caption in OCR; nearest printed-list entry | photo |
| 87–88 | facing ~71 | "'Gjoa' Aground" — no caption in OCR | photo |
| 97–98 | facing ~81 | "'Gjoa' at Anchor in Gjoahavn (Summer 1904)" — no caption in OCR | photo |
| 101 | facing 84 | "Gjoahavn and its Environs" — caption verbatim in OCR: *"GJOA HAVEN AND ITS ENVIRONS"* | photo |
| 102 | (verso of p.101) | blank | blank |
| 147–148 | facing ~129 | "The First Christmas Eve on Board" — no caption in OCR (best match by position) | photo |
| 165–166 | facing ~147 | "The First Sledge Expedition" — OCR is unreadable noise, not a caption | photo |
| 183–184 | facing ~165 | "Nechilli Eskimo in their Snow Hut" — no caption in OCR | photo |
| 209 | facing 191 | "The 'Owl' as Archer" — caption verbatim in OCR: *"THE OWL AS ARCHER."* | photo |
| 210 | (verso of p.209) | blank | blank |
| 215 | facing 197 | "Talurnakto" — caption verbatim in OCR: *"TALURNAKTO."* | photo |
| 216 | (verso of p.215) | blank | blank |
| 231–232 | facing ~213 | "Umiktuallu Kills his Foster-son" — OCR is unreadable noise | photo |
| 235 | facing 217 | "Adolf Lindstrom with Samples of Fish on King William Land (Autumn 1904)" — caption partly legible: *"ADOLF LINDSTROM"* | photo |
| 236 | (verso of p.235) | blank | blank |
| 257–258 | facing ~239 (**uncertain**) | printed list is badly OCR-garbled in this range; nearest candidates are "Winter in Gjoahavn" or "Nechilli Eskimo on a Visit" (facing roughly pp. 230–234) — flag for manual check | photo |
| 271–272 | facing ~253 | "Akla and Son" — no caption in OCR | photo |
| 283–284 | facing ~265 (**uncertain**) | nearest printed-list entry: "Uranienborg. The Astronomical Observatory in Winter Time" | photo |
| 293–294 | facing ~275 (**uncertain**) | nearest printed-list entry: "Snow Huts in the Lindstrom Valley at Gjoahavn" | photo |
| 297 | facing 279 | "Magito, the Belle of Ogchoktu" — caption verbatim in OCR: *"MAGITO. THE BELLE OF OGCHOKTU."* | photo |
| 298 | (verso of p.297) | blank | blank |
| 313–314 | facing ~295 (**uncertain**) | nearest printed-list entries: "An Eskimo Camp in Winter Time" / "Nalungia and Atikleura outside their Tent" | photo |
| 317–318 | facing ~299 (**uncertain**) | nearest printed-list entry: "Eskimo Implements" | photo |

**Not located as separate plate leaves** (~40 printed-list entries): "An
Iceberg in Baffin's Bay" (21), "Airing Mouldy Bread" (24), "The Danish
Literary Greenland Expedition" (40), "Eskimo from North Greenland" (43),
"Ruins of the Franklin Depot on Beechey Island" (50), "The 'Franklin, Bellot,
and Belcher' Memorial" (52), the magnetic-observation diagrams facing pp.
86–108 (Magnetic Meridian, Magnetic Inclination Lines, Self-registering
Apparatus, Magnetic Variation Curves ×2, "Gjoa" discharging, Store Shed,
Magnetic Variation House, Observatory), Villa "Magnet" (110), Uranienborg in
Summer (112), Ivayarra (114), Festivities among the Nechilli Eskimo (118),
Interior of the Villa "Magnet" (119), Wiik at the Observatory entrance (123),
A Visit to the Cabin (139), Members of the Expedition front/back view
(152–153), Kagoptinner in his son Poieta's Hut (161), Eskimo Removing (175),
Our Tent near the Magnetic North Pole (185), Kabloka (193), Umiktuallu (194),
Onaller and Son (195), Summer Scene on Deck (204), Summer on King William
Land (207), Closed/Open Nechilli Grave (220–221), Boat Expedition (223), G.
and H. Hansen on the Boat Expedition (227), Nechilli Eskimo on a Visit (230),
The "Owl's" Ice Palace (245), A Hunting Party (246), Silla and Pups by the
Provision Shed (261), Kayak Building (304), Oyara and Alo-Alo, A Living
Boot-jack, and The Nechilli in Summer Time (314). These do not show up as
low-text/blank PDF pages, so they are printed as smaller halftones set
directly into running-text pages rather than on dedicated plate leaves. Each
is still identifiable by its printed/facing page number from the List of
Illustrations (pdf pp. 13–15); extracting them will need a crop of the
relevant text-page raster, not a whole-page pull.

**Missing chart**: the printed list's final entry is "The Route of the
'Gjoa' through the North West Passage" (CHART, facing p. 330, marked "At the
end of Volume"). No such page was found — the volume's narrative ends at pdf
353 (printed p. 335, "END OF VOL. I"), followed directly by the printer's
colophon (pdf 354), two blank leaves (355–356), a University of Toronto
Library card-pocket page (357 — a modern library artifact, not part of the
original book), and a blank verso (358). The fold-out route chart does not
appear to have been captured in this digitization.

### Tables

| pdf page | subject | kind |
|---|---|---|
| 11 | Contents | table |
| 13–15 | List of Illustrations (used above; also a table in its own right) | table |

No meteorological/magnetic-observation data tables, provisioning lists, or
index were found as separate pages — the magnetic and meteorological data
in this volume is discussed in running prose, not tabulated on its own
pages.

---

## Volume II — `amundsen-gjoa-northwest-passage-v2.pdf`

`pdfinfo`: **420 pages**. Text extracted as page-scan (see above).

### Front matter (not plates)

| pdf page | subject | kind |
|---|---|---|
| 1–2, 4–6, 8, 10, 12, 14, 18 | blank leaves / flyleaves | blank |
| 3 | "Digitized by the Internet Archive" (modern insert, not original) | text |
| 7 | half-title: "The Gjoa Expedition, 1903–1907" | text |
| 9 | candidate **Frontispiece** — per printed list: *"Gjoa's first meeting with Whalers after completing the North West Passage"* (unpaginated); OCR on this page is a single stray character, consistent with a plain photograph | photo |
| 13 | **Contents** (single page) | table |
| 15–17 | **List of Illustrations** (printed plate list; badly OCR-scrambled in a two-column layout for several entries — treat facing-page numbers below as approximate where flagged) | table |

### Plates

| pdf page | printed/facing page | caption or subject | kind |
|---|---|---|---|
| 39–40 | facing 21 | "Praederik and Wife in their Snow Hut" — no caption in OCR | photo |
| 67–68 | facing 49 | "Tattooed Thigh (Nechilli Eskimo woman)" — no caption in OCR | photo |
| 85–86 | facing 67 | "Nechilli Eskimo equipped for Seal Fishing" — no caption in OCR | photo |
| 89–90 | facing ~71 (**uncertain**) | list garbled here; candidates include "The 'Ilja' and the 'Kiviuchyervi'" or "Tattooed Arm (Utkohikchyallik Eskimo woman)" | photo |
| 91–92 | facing ~73 (**uncertain**) | candidates include "The 'Owl' Trout Fishing" or "Nechilli Eskimo Visitors on Board" | photo |
| 115 | facing 97 | "The 'Gjoa' in Summer. Gjoahaven, King William Land" — caption verbatim in OCR: *"THE GJOA7 IN SUMMER. GJOAHAVN, KING WILLIAM LAND."* | photo |
| 116 | (verso of p.115) | blank | blank |
| 129–130 | facing ~111 (**uncertain**) | nearest printed-list entry: "Rejoicings" | photo |
| 157–158 | facing 139 | "Lieutenant Hansen as Photographer" — no caption in OCR | photo |
| 171–172 | facing 153 | "The wrecked Whaler 'Bonanza' at King Point" — no caption in OCR | photo |
| 175–176 | facing ~157 (**uncertain**) | nearest printed-list entry: "Our Residence at King Point" or "The Register House at King Point" | photo |
| 179–180 | facing ~161 (**uncertain**) | nearest printed-list entry: "In Winter Quarters at King Point" or "The Colony at King Point" | photo |
| 185–186 | facing 167 | "Kunak and his Family. Summer at King Point" — no caption in OCR | photo |
| 189–190 | facing ~171 (**uncertain**) | nearest printed-list entry: "The Land between King Point and Key Point" | photo |
| 211 | facing ~193 (list gives 209) | "Anakto. An Eskimo from Herschel Island" — caption verbatim in OCR: *"ANAKTO. AN ESKIMO FROM HERSCHEE ISLAND."* | photo |
| 212 | (verso of p.211) | blank | blank |
| 221–222 | facing ~203 (**uncertain**) | nearest printed-list entry: "Wiik's Grave at King Point" or "A Coffee Party at King Point" | photo |
| 265–266 | facing ~247 (**uncertain**) | nearest printed-list entry: "The first two Whalers arriving at King Point, July 11th 1906" | photo |
| 281–282 | facing 263 | "Tupsi. Eskimo Woman at Herschel Island" — caption verbatim in OCR: *"TUPSI. ESKIMO WOMAN AT HERSCHEL ISLAND."* | photo |
| 305–306 | facing ~287 (**uncertain**) | nearest printed-list entry: "Manni (Summer, 1906)" | photo |
| 307–308 | facing ~289 (**uncertain**) | nearest printed-list entry: "Anton Lund (Spring, 1906)" | photo |
| 311–312 | facing ~293 (**uncertain**) | nearest printed-list entry: "After our Arrival at Nome" or "Sports at Nome" | photo |
| 319 | facing ~301 (list gives 305) | "Lieutenant Hansen (Spring, 1906)" — caption verbatim in OCR: *"LIEUTENANT HANSEN (SPRING, I906)."* | photo |
| 320 | (verso of p.319) | blank | blank |

**Not located as separate plate leaves**: roughly 20 further printed-list
entries (e.g. "Ahiva and Alo-Alo in Hunting Garb," "Ogluli Eskimo repairing
his Sledge," "Young Nechilli Archers," "Scene on Deck," "Rejoicings"
duplicates, "Gustav Wiik (Winter 1905)," "Helmer Hansen (Spring 1905),"
"Spring at King Point," "A Summer Scene at King Point," "Eskimo Graves/
Whalers' Graves/Eskimo Huts at Herschel Island," "Peder Ristvedt," "Our
faithful Companions," "On the way to Victoria Land," "At Victoria Land," and
others) were not found as distinct low-text pages — same pattern as Vol. I:
smaller halftones set into running text.

**Missing chart**: the printed list's final entry is a CHART, "King Haakon
VII's Coast and Queen Maud's Sea; Lieutenant Hansen and Sergeant Ristvedt's
sledge expedition in 1905" (facing p. 322, "At the end of Volume"). No such
page was found in the trailing pages: narrative pages run continuously to
pdf 415, followed by the colophon (416, "LONDON: ..."), blanks (417–418), a
library card-pocket page (419), and a blank verso (420). The fold-out chart
does not appear to have been captured in this digitization, matching Vol.
I's missing route chart.

### Tables

| pdf page | printed/facing page | subject | kind |
|---|---|---|---|
| 13 | – | Contents | table |
| 15–17 | – | List of Illustrations (also used above) | table |
| 388–415 | ~369–397 | **Index** — the book's full alphabetical subject index (e.g. entries for Victoria Land sledge expedition, Whale hunting, Wiik, Winter, Wood, Zoological collection). Continuous run of ~28 index pages. | table |

No separate meteorological/magnetic-observation register, provisioning, or
sledge-ration table pages were found in Vol. II.
