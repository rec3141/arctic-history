#!/usr/bin/env python3
"""Apply the review's artifact corrections through history-db.py."""
import json, re, sqlite3, subprocess, sys

DB = 'db/history/history.sqlite'
FIELDS = [
    ('title', '--title'), ('type', '--type'), ('bibkey', '--bibkey'),
    ('credit', '--credit'), ('date_text', '--date'), ('creator', '--creator'),
    ('description', '--description'), ('lat', '--lat'), ('lon', '--lon'),
    ('source_url', '--source-url'), ('download_url', '--download-url'),
    ('local_file', '--local-file'), ('licence', '--licence'), ('pages', '--pages'),
    ('language', '--language'), ('people', '--people'), ('tags', '--tags'),
    ('view_file', '--view-file'), ('routing', '--routing'),
]

D = {}   # id -> {field: value}

def set(aid, **kw):
    D.setdefault(aid, {}).update(kw)

P = 'davis-baffin-hudson-%03d'

# --- descriptions rewritten so the people are named in the prose itself ---
set(P % 28, description=(
    "John Davis wrote this to his backer William Sanderson from Exeter a fortnight after the "
    "second voyage came home, with two men killed in Labrador and the Northstarre missing with "
    "all hands. \"I have now full experience of much of the Northwest part of the world, and have "
    "brought the passage to that certainty, as that I am sure it must be in one of foure places, "
    "or els not at all.\" Davis offered to spend his whole portion of Sandridge on a third "
    "voyage, and did."))
set(P % 30, description=(
    "John Davis to William Sanderson, written the day after he landed at Dartmouth from the third "
    "voyage. \"With Gods great mercy I have made my safe returne in health, with all my companie, "
    "and have sailed threescore leagues farther then my determination at my departure. I have bene "
    "in 73 degrees, finding the Sea all open, and forty leagues betweene land and land. The passage "
    "is most probable, the execution easie... Yesterday, the 15 of September, I landed all wearie, "
    "therefore I pray you pardon my shortnesse.\" Davis's journal gives 72° 12′; 73 is the "
    "letter's round figure. Nobody funded a fourth voyage: the Armada came the next summer."))
set(P % 33, description=(
    "Jens Munk on the death of Erich Hansen Li at the winter harbour, 19 May 1620, \"who, "
    "throughout the voyage, had been very industrious and willing, and had neither offended anyone "
    "nor deserved any punishment. He had dug many graves for others, but now there was nobody that "
    "could dig his, and his body had to remain unburied.\" After 12 May the ground could no longer "
    "be worked by the men still alive; the dead were dragged on deck or put over the side."))
set(P % 34, description=(
    "Whit Sunday, 4 June 1620. Jens Munk wrote that of sixty-four men only three besides himself "
    "were still alive, all of them lying down and unable to help one another, and that he expected "
    "to be dead within days: \"INASMUCH as I have now no more hope of life in this world, I "
    "request, for the sake of God, if any Christian men should happen to come here, that they will "
    "bury in the earth my poor body, together with the others which are found here, expecting their "
    "reward from God in Heaven: and, furthermore, that this my journal may be forwarded to my most "
    "gracious Lord and King.\" The margin of the manuscript at this entry reads 61 dead. Munk lived, "
    "sailed the sloop home with two companions, and delivered the journal himself."))
set(P % 38, description=(
    "Abacuk Pricket's account of the moment the shallop was cast off. It had been towed astern "
    "while the Discovery cleared the ice. Then: \"they cut her head fast from the sterne of our "
    "ship, then out with their top-sayles, and towards the east they stood in a cleere sea.\" Henry "
    "Hudson, his son John, and seven others were in it: an open boat in James Bay at midsummer, with "
    "a fowling piece, some meal and an iron pot. Nothing further is known. Thomas Button looked for "
    "them in 1612-13 and later expeditions found nothing."))
set(P % 47, title="You are out of the way to Iapon, for this is not it")
set(P % 51, description=(
    "Half a board and a cross, found by Luke Foxe standing at Port Nelson in August 1631, nineteen "
    "years after Thomas Button wintered there. One side had carried the royal arms and the names of "
    "James I and Prince Henry; the other carried Button's own record. The board had been broken and "
    "half of it was gone, so what follows is Christy's 1894 reconstruction, with the words he "
    "supplied set in square brackets and the rest as Foxe copied it: \"[To this Pl]ace, I came the "
    "27th of August, 1612, [by foul] weather, where I wintered the [before] written time, and then, "
    "by reason o[f] [wants] and sickness amongst my Company, [I] [was] forst to leave my owen Ship, "
    "[and with the] [Pinnas to] procecute my discovery [for the North] [West] the day and yeare "
    "afores[aid]. Per me Thomas Button, Gentleman.\" Button's journal was taken from him on his "
    "return and has never been found, so only the unbracketed words are certainly his. They confirm "
    "independently that he had to abandon the Resolution."))
set(P % 15, description=(
    "Printed in Purchas his Pilgrimes. Henry Briggs was a mathematician, not a sailor, and drew the "
    "north from the reports and charts of Henry Hudson, Thomas Button, Robert Bylot and William "
    "Baffin. It shows Hudson Bay open to the west and California as an island: the map that kept the "
    "search alive for another century."))
set(P % 53, description=(
    "A page of the traverse book kept on John Davis's third voyage, ruled in columns for month, day, "
    "course, leagues run, latitude by observation, the wind, and remarks. This is the working "
    "navigational record behind Davis's survey of the strait that now carries his name, printed by "
    "the Hakluyt Society from the original."))
set(P % 55, description=(
    "Traverse book columns kept on John Davis's third voyage for late July 1587: courses, leagues, "
    "latitude, wind, and remarks noting Mount Raleigh, the ice, and the fishing. A rare survival of "
    "an Elizabethan navigator's working table."))
set(P % 56, description=(
    "Traverse book columns from John Davis's third voyage for the crossing westward, with the "
    "remarks column recording the passage among the ice and the sighting of land."))
set(P % 57, description=(
    "The last traverse book pages of John Davis's 1587 voyage, running south towards the Labrador "
    "coast and home."))
set(P % 62, description=(
    "A ring diagram for computing the Epact, from John Davis's The Seaman's Secrets, worked through "
    "in the text with the example of the year 1590 — part of the calendar arithmetic an "
    "Elizabethan navigator had to carry in his head."))
set(P % 63, description=(
    "John Davis's scale showing how many leagues are sailed upon each compass point to raise or lay "
    "a degree of latitude — the traverse table in geometric form, from The Seaman's Secrets."))
set(P % 64, description=(
    "Facsimile of the divisional title page of the second part of John Davis's navigation manual: "
    "\"The Second Parte of this Treatise of Navigation, wherein is taught the most excellent "
    "instrumen[t]s...\"."))
set(P % 65, description=(
    "Armillary diagram of the sphere with its poles, axis, equinoctial and zodiac, from the passage "
    "on the poles of the zodiac in John Davis's The Seaman's Secrets."))
set(P % 66, description=(
    "The companion armillary figure in John Davis's The Seaman's Secrets, showing the circles of the "
    "sphere as they stand to the horizon."))
set(P % 67, description=(
    "The geometric construction by which the degrees are projected on the transversary of the "
    "cross-staff, from John Davis's The Seaman's Secrets."))
set(P % 68, description=(
    "A second construction in John Davis's The Seaman's Secrets, laying down the degrees from the "
    "intersections upon the staff."))
set(P % 70, description=(
    "Figure of an observer with the quadrant, near the close of the Second Book of John Davis's The "
    "Seaman's Secrets."))
set(P % 71, description=(
    "The final circular demonstration of the staff in John Davis's The Seaman's Secrets, with the "
    "colophon \"Imprinted at London by Thomas Dawson, dwelling neere the three Cranes in the "
    "Vintree, 1607\"."))
set(P % 76, description=(
    "A table page from William Baffin's journal of the 1615 voyage, recording the working through "
    "the ice towards the island of Resolution at the eastern mouth of Hudson Strait, with the daily "
    "latitude and the compass variation."))
set(P % 77, description=(
    "A table page from William Baffin's journal of the 1615 voyage, for the passage through Hudson "
    "Strait past the Savage Islands, with a note of eight days' stay and a longitude reckoned five "
    "degrees west from London — among the earliest longitude estimates from these waters."))
set(P % 78, description=(
    "A table page from William Baffin's journal of the 1615 voyage, for the western end of the "
    "strait: Cape Comfort, Nottingham and Salisbury islands, the north shore within Resolution "
    "Island, and the ice the Discovery worked through under Robert Bylot."))
set(P % 80, description=(
    "The Hakluyt Society's 1860 lithographic facsimile of Hessel Gerritsz's chart drawn from Henry "
    "Hudson's own papers, folded as a frontispiece to Asher's volume. It labels the new inland sea "
    "\"Mare Magnum de M. Hudson\", names Fretum Davis and Groenlandia, and carries the royal arms "
    "with the motto DIEU EST MON DROIT, four compass roses and a fleet under sail. This is the map "
    "that first put Hudson Bay before European readers."))
set(P % 81, description=(
    "A north polar projection with the pole at the centre and the meridians radiating from it, "
    "showing Groenlandia, Nova Zembla, Europe and the north-west. Asher reproduced it in his volume "
    "of the Henry Hudson documents, at the head of the section of Divers Voyages and Northerne "
    "Discoveries."))


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    # strip research-process leaf numbers from every artifact's pages field
    for r in db.execute("select id, pages from artifacts where topic='davis-baffin-hudson'"):
        if r['pages'] and 'scan leaf' in r['pages']:
            clean = re.sub(r',?\s*scan leaf\s*\d+', '', r['pages']).strip().rstrip(',')
            D.setdefault(r['id'], {})['pages'] = clean
    for aid in sorted(D):
        r = db.execute("select * from artifacts where id=?", (aid,)).fetchone()
        if r is None:
            sys.exit('missing ' + aid)
        cmd = ['/usr/bin/python3', 'tools/history-db.py', 'artifact',
               '--id', aid, '--topic', r['topic']]
        for col, flag in FIELDS:
            val = D[aid].get(col, r[col])
            if col in ('people', 'tags') and val and str(val).startswith('['):
                v = json.loads(val)
                val = ';'.join(v) if col == 'people' else ','.join(v)
            if val is None or val == '':
                continue
            cmd += [flag, str(val)]
        subprocess.run(cmd, check=True)

main()
