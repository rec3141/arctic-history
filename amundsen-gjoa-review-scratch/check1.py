import sys; sys.path.insert(0,'amundsen-gjoa-review-scratch')
from q import find
QS = [
("027","I was sitting on one of the chain lockers looking towards the land with a deep, solemn feeling that I was on holy ground, Franklin's last safe winter harbour. My thought wandered back"),
("028a","She was lifted up high and flung bodily on to the bare rocks, bump, bump"),
("028b","In my distress I sent up (I honestly confess it) an ardent prayer to the Almighty"),
("028c","Yet another thump, worse than ever, then one more, and we slid off"),
("029a","Lieutenant Hansen came rushing down into the cabin and called out the ever memorable words"),
("029b","Vessel in sight, sir"),
("029c","The North West Passage had been accomplished"),
("029d","my dream from childhood. This very moment it was fulfilled. I had a peculiar sensation in my throat"),
("029e","I was somewhat overworked and tired, and I suppose it was weakness on my part, but I could feel tears coming to my eyes"),
("030a","Are you Captain Amundsen"),
("030b","Is this the first vessel you have met"),
("030c","his countenance brightened up. We shook hands long and heartily"),
("030d","I am exceedingly pleased to be the first one to welcome you on getting through the North West Passage"),
("031a","the bell rang very loudly, all of a sudden. There was something in the ring that spelt disaster, and I ran off at full speed"),
("031b","But I was only just in time to see our dear friend breathe his last. It was an inexpressibly sad moment. I closed the eyes of our late comrade"),
("031c","we remained sitting there for a while in silence and sorrow"),
("032a","My experience is that the Eskimo dress in winter in these regions is far superior to our European clothes"),
("032b","But one must either wear it all or not at all; any mixture is bad"),
("032c","Woollen underclothing absorbs all the perspiration and soon becomes wet through and through"),
("033a","Atikleura is a veritable prodigy at this work"),
("033b","Just a cut here and there, then a kick, and the thin neat block stands separated from the mass of snow"),
("033c","All the blocks from Atikleura's hand are so exactly equal in size that they look as if they had been accurately measured"),
("034a","But I had my scruples about this, as I had already had evidence that nothing either in the Eskimo's clothing or other arrangements was, in fact, without meaning or purpose"),
("034b","so I kept my fringe and put up with the ridicule"),
("035a","My sincerest wish for our friends the Nechilli Eskimo is, that civilisation may never reach them"),
("035b","Eskimo living absolutely isolated from civilisation of any kind, are undoubtedly the happiest, healthiest, most honourable and most contented"),
("035c","children of Nature up at the Pole"),
]
for tag,text in QS:
    r=find(text,40)
    if r: print(f"OK   {tag}: " + ", ".join(k for k,_,_ in r))
    else: print(f"MISS {tag}: {text[:80]}")
