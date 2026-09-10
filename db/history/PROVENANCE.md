# How this history layer was made

The History tab of the CCGS *Amundsen*'s dashboard is a research database — a
wiki, a map layer, a timeline and a bibliography covering the human history of
the Canadian Arctic Archipelago and Baffin Bay, from the Paleo-Inuit arrival
some 4,500 years ago to the ship this dashboard runs on. This file explains
how it was built, what part artificial intelligence played, how the work was
checked, and where its limits are. It is meant to be read by anyone who uses
the layer and wants to know how far to trust a given line.

## The short version

The layer was researched and written by AI agents — instances of Anthropic's
Claude, running as Claude Code — working from a human-authored brief, writing
every fact through a single validated command-line tool into one shared
database, and filing requests to a person whenever a task needed a human. Every
narrative page was then checked, line by line, against the primary sources on
disk by a second AI pass, and only pages a reviewer could stand behind were
marked `good`. A human (R. Eric Collins, University of Manitoba) set the brief,
answered the requests, made the judgement calls, and owns the result.

Nothing here is a substitute for the primary sources. Every artifact carries
its citation; every quotation was checked against the text it came from; and
where the sources disagree, the pages say so rather than choosing silently.

## The record, in numbers

*(a snapshot; the database is maintained over time and these grow)*

| | |
| --- | --- |
| Topics | 35 |
| Wiki pages (hand-written narrative) | 273 |
| Artifacts (map items: images, maps, quotes, tracks, objects) | 3,267 |
| — of which historical images and maps | 1,714 |
| — of which pinned primary-source quotations | 629 |
| — of which reconstructed voyage/sledge tracks | 147, with 2,135 waypoints |
| Sources in the bibliography | 474, in 6 languages (en, fr, da, de, la, iu) |
| People recorded | 1,368, of whom 521 are Indigenous |
| Places | 563 |
| Dated events / atomic date records | 1,955 / 5,957 |
| Cross-links between pages | ~11,500 |
| Requests filed to a person, and answered | 50 |

## Who did what

**The human** wrote the brief that every agent works from (`BRIEF.md`), chose
the topics, answered every request, made the judgement calls the agents
referred up (permissions, sensitive framing, what to buy or borrow), and is the
named author and owner of the layer.

**The AI research agents** did the reading and the writing. Each was given one
topic and the brief, and worked to two rules the brief puts above all others:
start from what the database already holds, and *write to the database as you
go, never at the end* — because a run can be cut off at any moment, and a run
that ends with sixty rows saved and an honest note of where it stopped is a
success where a run that ends with a plan in its head and nothing written is a
failure. They entered sources, artifacts, people, places, dated events and
voyage tracks, and wrote the narrative pages that tie them together. They could
not do everything: downloads a library gate, permissions from a rights holder,
a scan of a book held only on a shelf, a question of sensitive framing — those
they filed as requests for a person, and carried on with other work.

**The AI review agents** were a separate pass. Once a topic's pages were
drafted, a reviewer re-read every one against the primary texts held on disk —
checking every quotation word for word (against the page image itself where the
scanned text was unreliable), every date and coordinate against the sources,
every cross-link, and the licence on every image — and rewrote what was wrong
before marking a page `good`. A page a reviewer could not stand behind stayed
`draft`, with the reason recorded. The review pass wrote 68 of the layer's 693
running worklog entries.

## What the review caught

The review pass was not a formality. Among the errors it found and corrected
against the sources:

- **Two fabricated quotations** — passages attributed to real authors that
  appear nowhere in their work — were removed and replaced with what the source
  actually says.
- **Misattributed testimony** — including a passage of Inuit survivor testimony
  credited to the wrong person, and several expedition quotations given to the
  wrong speaker or the wrong year — was corrected against the record.
- **A claim the source never made** (a stated cause of death, a suicide inferred
  where the narrative pointedly does not say) was withdrawn.
- **Coordinates** wrong by tens to hundreds of kilometres, and **plate captions**
  misread by the image-harvesting pass, were fixed against each book's own list
  of illustrations and against georeferenced page images.
- **A death not in the modern record** (a stoker who died in 1853, found lettered
  on a surveyed harbour plan) and **Inuit personal names preserved in oral
  history and in no European record** were recovered and entered.

These are noted here not to alarm but to be honest: an unreviewed AI draft
contains mistakes of exactly this kind, which is why the review pass exists and
why a page's status is worth checking.

## The standards the work was held to

The brief sets out standards that matter especially for a history of the
Canadian Arctic, whose communities are living and whose past includes violence,
relocation and epidemics:

- **Indigenous knowledge and presence are the narrative, not an appendix.** Every
  named Inuit, Inughuit and other Indigenous participant the record preserves is
  entered as a person; oral history is treated as evidence, cited and weighed
  like any other source.
- **Epistemic humility about "discovery."** Most of what these expeditions
  "discovered" was inhabited or long known. The pages say what happened —
  sighted, charted, reached, mapped, rediscovered — and keep the word "discovery"
  only inside a direct quotation, a proper name, or an explorer's own reported
  claim.
- **Living communities are named as they are now** — current Inuktitut place
  names first, the historic English name in parentheses — and hard history is
  reported factually, in the terms the communities and the Qikiqtani Truth
  Commission use. Testimony from the QTC and similar sources is quoted exactly as
  published, never softened or sharpened.
- **Disagreement is shown, not hidden.** Where sources conflict on a date, a
  position or a fact, the page presents the conflict and says which it follows.

## The human-in-the-loop

The layer was not built by AI acting alone. A live request queue connected the
agents to a person throughout: when an agent hit something only a human could
do or decide, it filed a request — with the exact source, a drafted email where
one was needed, and everything the person needed to act — and a person reviewed
each on a web page and answered it. All 50 such requests were answered. This is
how the permissions, the sensitive judgement calls, and the material behind a
library login entered the record.

## Reading the layer honestly

- **A page marked `good`** has been checked against its sources by a reviewer. A
  page still marked `draft` has been researched but not yet fully verified —
  treat its specifics with more caution.
- **Every artifact carries a credit and a source key**; follow them to the
  original. Quotations are verbatim from the cited text and page.
- **A track is a reconstruction** of a route from a published narrative, log or
  the explorer's own sketch-map, accurate to about 10 kilometres, with inferred
  segments labelled as such — not a survey or GPS record.
- **Coordinates sit on a map beside the ship's own position** and were entered
  with that in mind, but they carry the coarseness of their sources; a wreck
  position may be a protected-area centre rather than a surveyed point, and the
  artifact says so where that is true.

## Tooling

The database is one SQLite file, written only through `tools/history-db.py`,
whose schema and writers (`arctic_history/`) enforce the rules above — every
artifact must have a credit and a source, coordinates are range-checked, dates
are stored atomically so the timeline can be read back and sanity-checked, and
the validator (`history-db.py check`) refuses inconsistencies. Full texts and
images were fetched through `tools/history-fetch.py`; scanned books without
usable text were run through OCR on the research machine's GPU. The code, the
brief, and this file are version-controlled; the database and the fetched files
are synced to the ship separately. Every change is attributed in the git
history, which records the human author and the AI model as co-author on each
commit.

*Maintained on the University of Manitoba research network and synced to the
ship. Questions to the layer's author.*
