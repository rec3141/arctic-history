#!/usr/bin/env python3
import sys
sys.path.insert(0, '/data/dev/arctic-history/mcclure-investigator-review-scratch')
from reartifact import rerun

D = {}

# ---- the 22 check flags: name the people in the description itself ----

D['002'] = dict(description=(
 "Plate II of Lieutenant Samuel Gurney Cresswell's series of eight, drawn aboard the ship. "
 "Nelson Head, the cliff at the southern end of Banks Island that Robert McClure's Investigator "
 "rounded in September 1850 on her way into Prince of Wales Strait."))

D['003'] = dict(description=(
 "Plate III of Samuel Gurney Cresswell's series. Robert McClure's ship fast in the moving pack at "
 "the head of Prince of Wales Strait in October 1850, drifting with the floe. It was from this "
 "besetment that McClure's sledge party set out on 21 October and, five days later, saw the coast "
 "of Melville Island across Viscount Melville Sound."))

D['004'] = dict(description=(
 "Plate IV, the best known of the series, drawn by Samuel Gurney Cresswell, who was aboard. In "
 "August 1851 Robert McClure's Investigator, working north along the exposed west coast of Banks "
 "Island, was squeezed between the grounded ice and the cliffs; the crew had provisions and boats "
 "on the floe ready to abandon her. Position approximate."))

D['008'] = dict(description=(
 "This is the walk that completed the first passage from ocean to ocean: Robert McClure's people, "
 "among them the surgeon Alexander Armstrong and the Moravian interpreter Johann August "
 "Miertsching, many of them scorbutic, dragging themselves and their sledges over the ice of "
 "Viscount Melville Sound from a ship that had come in from the Pacific to Henry Kellett's two "
 "ships, which had come in from the Atlantic. They left on 3 June 1853 and were aboard the "
 "Resolute at Dealy Island on 17 June. Only the ends are fixed positions; the intervening course "
 "follows the direct line and the Melville Island coast."))

D['012'] = dict(description=(
 "Henry Kellett's HMS Resolute and her steam tender Intrepid, under Francis Leopold McClintock, "
 "were blown out of Dealy Island by a gale on 17 August 1853 after eleven months. They got only as "
 "far east as Point Griffiths before the young ice caught them on 10 September, drifted 180 miles "
 "in the pack, mostly south and east, and stopped for the winter 28 miles south-west of Cape "
 "Cockburn. The positions are observed ones from the drift table the Resolute's master George "
 "Frederick M'Dougall kept and later printed, so the line is good to a mile or two."))

D['022'] = dict(description=(
 "The last four sledges left Henry Kellett's abandoned Resolute and Intrepid at seven in the "
 "evening on 15 May 1854, Francis Leopold McClintock among the officers walking away: \"After "
 "advancing about a quarter of a mile, the crews of the various sledges halted simultaneously; "
 "unharnessed, and gave three hearty cheers for the 'Resolute' and 'Intrepid;' but though the ice "
 "is a good conductor of sound, we heard no response.\" Sixteen months later the Resolute answered "
 "by turning up in Davis Strait."))

D['025'] = dict(description=(
 "Alexander Armstrong, the Investigator's surgeon, explaining what was killing his patients, "
 "written before vitamin C was known: \"If the supply is not equal to the demand, the body wastes, "
 "and debility and disease of a scorbutic character ultimately ensue. I am, therefore, of opinion "
 "that one pound of animal food daily is not sufficient for men employed on Polar service.\" He "
 "also wanted salt meat proscribed from any Arctic dietary. He was wrong about the mechanism and "
 "right that only fresh meat was holding the disease off."))

D['028'] = dict(description=(
 "Alexander Armstrong on the walk from Mercy Bay to Dealy Island: \"It is impossible to convey a "
 "truthful idea of the labour of dragging a sledge over rough ice; at times it can only be moved a "
 "few feet, until it be again arrested by a ragged or almost precipitous wall of rough, broken up "
 "floe ice.\" This is the surface Robert McClure's scorbutic crew crossed for a fortnight in June "
 "1853."))

D['029'] = dict(description=(
 "The last sentence of Alexander Armstrong's Personal Narrative: \"We landed off Ramsgate on the "
 "6th of October, 1854, after an absence of four years and ten months.\" The Investigator was "
 "commissioned at Woolwich on 18 December 1849 and sailed from Plymouth on 20 January 1850; the "
 "surgeon is counting from the commissioning, not from the sailing."))

D['033'] = dict(description=(
 "Robert McClure, writing to the Admiralty from Henry Kellett's Resolute after his crew's march "
 "across the sound: \"in the march across the straits the health of the crew appeared to revive, "
 "and under the present bountiful issue of fresh meat and other invigorating food... they are "
 "rapidly regaining the loss of flesh which nineteen months on two-thirds rations had considerably "
 "reduced.\""))

D['034'] = dict(description=(
 "The complete text of the 1856 edition in which Sherard Osborn set Robert McClure's journals "
 "before the public, from the ship's sailing to the abandonment in the Bay of Mercy. The scan's "
 "machine reading doubles the spaces between words, so any wording taken from it has to be checked "
 "against the printed page."))

D['035'] = dict(description=(
 "The whole of Alexander Armstrong's book: the surgeon's own narrative of the Investigator's four "
 "years, and the fullest account there is of the rations, the scurvy and the five deaths. It "
 "disagrees with Robert McClure's published journals at several points, and where it does, both "
 "readings are given here. The page numbers over the last sixty pages of the scan are reconstructed "
 "from the running heads."))

D['045'] = dict(description=(
 "Plate V of Samuel Gurney Cresswell's series. Robert McClure's ship driving between grounded and "
 "packed ice in a snowstorm on the north coast of Banks Land, the night before she went aground and "
 "then took shelter in the Bay of Mercy. Position approximate."))

D['047'] = dict(description=(
 "Robert McClure's HMS Investigator, abandoned here on 3 June 1853, stands upright in about eleven "
 "metres of water, the upper deck about eight metres down, sheltered inside the bay and preserved "
 "by the cold. Sonar found her within about fifteen minutes of the 2010 survey starting; divers "
 "recorded her in 2011; in May 2026 a Parks Canada team landed a ski-equipped aircraft on the sea "
 "ice, cut a hole through two metres of it, and flew a remotely operated vehicle with a stereo "
 "imaging system over the site, finding her still upright and still being worked on by the ice. She "
 "lies in Inuvialuit waters, just outside the boundary of Aulavik National Park."))

D['052'] = dict(description=(
 "Johann August Miertsching on the Copper Inuit of Prince Albert Land, 3 June 1851. German: \"Ihre "
 "Harpunen, Messer, Beile, Pfeilspitzen, Nähnadeln u. s. w. sind alle von Kupfer verfertigt, "
 "welches sie gediegen von den weiter östlich wohnenden Eskimos gegen Seehundsthran, "
 "Narvalhörner u. dergl. mehr eintauschen.\" English: their harpoons, knives, axes, arrowheads "
 "and sewing needles are all made of copper, which they obtain native, by trading seal oil and "
 "narwhal horn with the people living further east. A working description of the Coppermine trade, "
 "written down by a Saxon missionary on Victoria Island in 1851. The long s of the Fraktur is set "
 "here as s."))

D['055'] = dict(description=(
 "Robert McClure, in the portrait engraved for the published edition of his journals. A small "
 "reproduction, 371 by 480 pixels; no larger copy of this plate is to hand."))

D['057'] = dict(description=(
 "What Henry Kellett's officers saw from the summit of Fife Point on 7 September 1852: six miles of "
 "fast ice between the Resolute and Parry's anchorage at Winter Harbour. \"The practicability of "
 "getting into Winter Harbour was first discussed; but the idea of cutting through six miles of "
 "solid floe, was too absurd to be long entertained.\" Kellett turned back east and wintered at "
 "Dealy Island instead - and so did not learn of Robert McClure's record until Mecham walked back "
 "to the rock in October."))

D['061'] = dict(description=(
 "Bedford Pim crossing Viscount Melville Sound in March 1853 to reach the Investigator: \"The floe, "
 "if floe it can be called, proved bad indeed: hummocks after hummocks followed each other in "
 "apparently endless succession, sometimes composed of very old, then young ice; on the former the "
 "surface was so glassy and uneven that the men could scarcely stand.\" This is the ice his rescue "
 "party crossed in twenty-eight days."))

D['062'] = dict(description=(
 "Bedford Pim's own flat account of the most famous meeting in the Franklin search, written up for "
 "Kellett: \"Arrived within 100 yards without being observed; then, however, two persons taking "
 "exercise on the ice discovered that I did not belong to their ship. Upon beckoning, they quickly "
 "approached, and proved to be Capt. M'Clure and Lieut. Haswell.\" The two men were Robert McClure "
 "and Lieutenant Haswell; Pim gives the time as five in the afternoon. M'Dougall's version, written "
 "from hearsay three years later, is the one everybody quotes."))

D['063'] = dict(description=(
 "Francis Leopold McClintock on the spring 1853 outfit from Dealy Island: \"Each person was "
 "supplied with a pair of canvas boots and two pair of mocassins. The load amounted to 184lbs. a "
 "man.\" That is what each man dragged at the start of a journey of a hundred days. By 1854 the "
 "march to Beechey Island was being made at 215 lb a man."))

D['064'] = dict(description=(
 "George Frederick Mecham on the outer, Beaufort Sea side of Prince Patrick Island, at the northern "
 "limit of the 1853 survey: \"The pack here is much heavier than any yet seen, being almost "
 "entirely composed of very old broken up floes.\" The day before, he had written that his men "
 "\"are very much fagged, and are all snoring before supper is ready.\" This is the edge of the "
 "thick multi-year ice of the Beaufort gyre, described from a sledge in 1853."))

D['067'] = dict(description=(
 "A full instrumental winter from mid-Barrow Strait, kept on board Henry Kellett's HMS Resolute "
 "while she lay beset about 28 miles S.W. by S. of Cape Cockburn at 74 deg 41.5 min N, 101 deg 22 "
 "min W, from her besetment on 10 September 1853 to April 1854: daily maximum, minimum and mean air "
 "temperature, barometer, two interior temperatures, wind direction and force, weather letters and "
 "a remarks column that is mostly aurora. The Resolute's master George Frederick M'Dougall printed "
 "the monthly journals in the appendix to his own narrative of 1857. The ship moved barely a mile "
 "all winter. On 9 December 1853, with the mean at -37.9 F, the remark is \"1 a.m., mercury "
 "frozen\". There is no page for January 1854 in the printed appendix."))

# ---- corrections found on checking ----

# the ration figures were wrong: the page reads 1/2 lb. meat and 2/3 lb. flour
D['065'] = dict(description=(
 "What Bedford Pim was told on arriving at Robert McClure's ship: \"the unfortunate loss of a large "
 "portion of beef compelled the captain to put the ship's company, during the second winter, upon "
 "short allowance, 1/2 lb. meat and 2/3 lb. flour daily, being the principal rations - a miserable "
 "pittance for hearty men in these bleak regions.\" Alexander Armstrong's book records a further "
 "cut on 6 September 1852, to eight ounces of meat gross and ten of flour."))

D['049'] = dict(description=(
 "Johann August Miertsching at the mouth of the Colville, 11 August 1850. German: \"Der Häuptling, "
 "ein sehr schöner und verständiger Mann, hieß Attua. Er hatte 3 Frauen und 13 Kinder.\" "
 "English: \"The chief, a very handsome and sensible man, was named Attua. He had three wives and "
 "thirteen children.\" Alexander Armstrong, writing in English, spells the same name Aitawa and "
 "Attawaa. The diary is set in Fraktur; the long s is given here as s."))

D['050'] = dict(description=(
 "Kenalualik explaining the stars to Johann August Miertsching at Cape Bathurst. German: \"Ueber "
 "uns ist ein sehr großer, blauer Kasten, das Haus der Sonne.\" English: \"Above us is a very "
 "large, blue box, the house of the sun\" - the stars being light coming through small holes in it, "
 "and the sun leaving the house by day. Miertsching had come to teach and spent much of his time "
 "being taught."))

D['051'] = dict(description=(
 "The Copper Inuit camp on Prince Albert Land at the sight of Robert McClure's party, 3 June 1851. "
 "German: \"Da erhoben sie Alle ein Geschrei: sivoravogut! erksidlarpogut! (Wir fürchten uns!)\" - "
 "\"Then they all raised a cry: sivoravogut! erksidlarpogut! (We are afraid!)\" They had never seen "
 "an outsider and had no weapons to hand. It was Johann August Miertsching's Labrador Inuttitut, "
 "understood well enough here, that changed the meeting."))

D['053'] = dict(description=(
 "Kenalualik had already offered Johann August Miertsching a sledge, dogs and a tent if he would "
 "stay the winter at Nuvuak. German: \"stellte mir nun auch seine Tochter vor mit den Worten: takka "
 "unna! (Nimm diese!)\" - \"he now also presented his daughter to me with the words: takka unna! "
 "(Take this one!)\" Miertsching declined, saying he owed duty to his own angajuga, his captain. He "
 "records the girl as about sixteen and does not give her name."))

D['024'] = dict(description=(
 "The Investigator's first meeting with Inupiat, near Point Drew on the Alaskan coast, in Alexander "
 "Armstrong's words: \"We at once landed, and having called out to them words of peace in their own "
 "language, we approached; they timidly met us, and in a few minutes we were rubbing noses - the "
 "customary mode of friendly salutation with them.\" The words of peace were Johann August "
 "Miertsching's. Armstrong's own sentence runs on to call his hosts \"about the most filthy race on "
 "the face of the globe\", which is the register of most of what he writes about them."))

D['001'] = dict(description=(
 "Plate I of Samuel Gurney Cresswell's series, under its own printed title. Robert McClure's "
 "Investigator, six weeks through Bering Strait, raises the high land of Baring Island (Banks "
 "Island) on 6 September 1850 in what is now Amundsen Gulf. It was new to the Navy's charts, not to "
 "the country: Inuvialuit and Copper Inuit knew and used these coasts. The position is approximate, "
 "taken from the ship's track for that day rather than from the plate."))

D['010'] = dict(description=(
 "Lieutenant George Frederick Mecham and the sledge Discovery, with Mr G. S. Nares and the "
 "Perseverance as auxiliary, from Dealy Island west along the south shore of Melville Island, "
 "across to the land he sighted on 29 April and named Eglinton Island, and thence round Prince "
 "Patrick's Land to the pack edge. The route is built day by day from his own printed journal. Two "
 "of his printed observations are legible (Lat. 75 02 N on 14 April; Lat. 77 00 00 N, Long. about "
 "121 45 W in the last week of May); every other point is pinned to the modern coordinates of the "
 "landmarks he names, from the Canadian Geographical Names Database, with the points marked "
 "'position inferred' interpolated along his stated courses. The volume's own heading dates the "
 "journey 4 April to 6 July 1853."))

D['030'] = dict(description=(
 "Ten numbered letters from Robert McClure as laid before Parliament: No. 1 written in the Bay of "
 "Mercy on 1 June 1853 describing Bedford Pim's arrival and the call for volunteers; No. 2 from "
 "Dealy Island on 25 June reporting the abandonment; No. 3 from the North Star at Beechey Island on "
 "27 April 1854. These are McClure's own words to his employers, written on the spot, and they "
 "differ in detail from the edited narrative Sherard Osborn published in 1856. Henry Kellett's and "
 "William Thomas Domville's letters on the state of the crew are printed with them."))

D['037'] = dict(description=(
 "Johann August Miertsching's diary as published at Gnadau in 1855, in the original German and in "
 "Fraktur. It is the only substantial record the expedition made of the Inuvialuit and Copper Inuit "
 "it met, because Miertsching was the only man aboard who could hold a conversation. Fraktur reads "
 "badly by machine, so the page scan is the authority for any wording taken from it."))

D['040'] = dict(description=(
 "The 1,038-page scan of the January 1855 blue book, in which the sledge journals of Mecham, "
 "M'Clintock, Hamilton, Pim and Domville can be read exactly as they were printed for Parliament."))

D['066'] = dict(description=(
 "The officers' day-by-day travelling journals as laid before Parliament: George Frederick Mecham "
 "from p. 498, Francis Leopold McClintock from p. 541, Richard Vesey Hamilton from p. 627, Bedford "
 "Pim's spring journey to the Bay of Mercy from p. 650, William Thomas Domville's from p. 664. They "
 "give the dates, the ice, the loads and the namings at first hand, and they correct the published "
 "narratives in several places - Pim's arrival at five in the afternoon on 6 April, the "
 "Hamilton-Richards meeting dated 18 May rather than 17, and McClintock's own abstract of 105 days "
 "and 1,030 geographical miles against M'Dougall's 106 days and 1,328 statute."))

D['069'] = dict(description=(
 "The scanned pages of George Frederick M'Dougall's narrative, in which the appendix tables - the "
 "meteorological journals of the Resolute's drift winter above all - can be read as printed."))

D['070'] = dict(description=(
 "Every dated entry of the western division's spring 1853 sledge journals - Mecham, M'Clintock, "
 "Nares, de Bray, Domville twice, Pim twice, Roche - and of Krabbe's 1854 journey back to the "
 "abandoned Investigator, set out day by day with the places each day names and the marginal wind "
 "and temperature notes; and a companion gazetteer of 111 Melville and Prince Patrick Island names "
 "with their modern official coordinates, which is what allows the officers' routes to be drawn on "
 "a modern chart."))

D['111'] = dict(
 title="M'Dougall's table of \"Land discovered and searched from 1848 to 1854\"",
 description=(
 "George Frederick M'Dougall's tally, expedition by expedition, of the coastline each commander "
 "claimed as newly charted and the coastline actually searched on foot in the seven years of the "
 "Franklin search; the wording of the heading is his. Henry Kellett's two ships stand at 9,432 "
 "geographical miles searched on foot and 1,618 geographical (1,870 statute) miles of new coast, "
 "against Austin's 6,087 and Robert McClure's 2,350 searched. The totals for the whole search are "
 "21,589 geographical miles searched on foot and 5,782 of new coast."))

D['060'] = dict(description=(
 "What Henry Kellett's spring 1853 sledge parties added to the chart, drawn from their own routes: "
 "Francis Leopold McClintock across Melville Island to Hecla and Griper Bay and then north-west "
 "over Prince Patrick Island; George Frederick Mecham west along the south coast of Melville "
 "Island, round Eglinton Island and up the Beaufort Sea side of Prince Patrick Island; Richard "
 "Vesey Hamilton north-east up Byam Martin Channel towards Bathurst Island. M'Dougall's appendix "
 "credits them with 768, 680 and 170 geographical miles of new coast - 1,618 geographical, or "
 "1,870 statute, in a single season. Set against the whole Franklin search from 1848 to 1854, "
 "Kellett's two ships searched 9,432 geographical miles on foot, against Austin's 6,087 and Robert "
 "McClure's 2,350. The ground they added was Prince Patrick Island, Eglinton Island and the north "
 "and west coasts of Melville Island. The view plots the three officers' routes on a one-degree "
 "graticule from their shared starting point at Dealy Island; there is no coastline drawn under "
 "them, so it shows the shape and reach of the season's work rather than the coast itself."))

D['114'] = dict(description=(
 "Party by party, the sledge, the flag and the motto, the object, the dates of leaving and "
 "returning, the days absent, the distance marched and the new coast covered in the spring of "
 "1853. Francis Leopold McClintock in the Star of the North, 'Lead thou us on', 4 April to 18 "
 "July, 105 days, 1,328 statute miles, furthest Point M'Clintock on Prince Patrick Island at 77 "
 "deg 23 min N, 118 deg 20 min W on 17 and 18 June; George Frederick Mecham in the Discovery, 'Per "
 "Mare, per Terram, per Glaciem', 4 April to 6 July, 94 days, 1,163 statute miles, furthest 77 deg "
 "6 min N, 120 deg 30 min W on 29 May; Emile de Bray in the Hero, 'By Faith and Courage', 4 April "
 "to 18 May as McClintock's auxiliary; George Strong Nares in the Perseverance, 'Dum spiro spero', "
 "4 April to 1 June as Mecham's depot sledge; Richard Vesey Hamilton in the Hope, 'I watch for "
 "your return'; Bedford Pim in the John Barrow, 'Hope on, Hope ever', 10 March to 19 April to the "
 "Bay of Mercy; William Thomas Domville in the James Fitzjames, 'Deo Volente'; Richard Roche in "
 "the Beauty, 'Mon Dieu est ma Roche'. The remarks column carries the season's losses and oddities "
 "as well: against de Bray's row stands the note that on 12 May 1853 John Coombes, stoker, fell "
 "dead upon the floe. The table runs over four spreads; the page held here is the first of them."),
 pages="pp. 520-527")

D['115'] = dict(description=(
 "The summary abstract of every sledge journey from Henry Kellett's Resolute and Intrepid in "
 "autumn 1852 and spring 1853: days absent, statute miles travelled, new coast line explored, game "
 "shot, pounds of meat procured and cairns built, officer by officer. The totals are 8,634 statute "
 "miles travelled and 1,867 statute miles of new coast. It is also where the smaller journeys are "
 "recorded - George Frederick M'Dougall's 19 days, William Thomas Domville's 76 and a half, "
 "Richard Roche's 78 and a half, William H. Richards's five and a half - beside McClintock's 105 "
 "days and Mecham's 94."),
 pages="p. 528")

for k, v in sorted(D.items()):
    rerun('mcclure-investigator-' + k, **v)
