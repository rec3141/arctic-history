import sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from upd import upd

F=(69.9783,-92.0183)   # Felix Harbour, observed 69 58 42 N / 92 01 06 W
S=(70.0167,-91.90)     # Sheriff's Harbour, observed 70 01 N / 91 54 W
V=(70.155,-91.509)     # Victoria Harbour, magnetic table 70 09 18 N / 91 30 33 W
P=(70.0881,-96.7792)   # magnetic pole, 70 05 17 N / 96 46 45 W

upd('ross-victory-056', title="Comparative chart of the ancient and modern navigators",
    pages="folding chart, facing p. xxv",
    lat=70.0, lon=-95.0,
    description="The folding chart at the front of John Ross's narrative, laying the tracks of the older navigators over those of the modern ones in red across North America, Baffin's Bay, Hudson's Bay and the Pacific. It is Ross's argument for what remained to be charted, and for why the Victory was worth sending.")

upd('ross-victory-057', title="Victory dismasted in a storm",
    pages="plate 3, facing p. 32", lat=55.2, lon=-8.0,
    description="Plate 3 of John Ross's narrative: the Victory, the first steam vessel taken into the Arctic, in a heavy sea on the outward passage of 1829. She lost her fore topmast in a gale off the Irish coast in June and put into Loch Swilly to refit before taking her final departure on 18 June. Drawn from Ross's own sketch.")

upd('ross-victory-058', title="Taking possession",
    pages="plate 4, facing p. 116", lat=70.80, lon=-92.80,
    description="Plate 4 of John Ross's narrative: the landing party taking formal possession of the coast of Boothia, with the ship and boats in the bay behind. Ross records one such ceremony in August 1829 at an observed latitude of 70 deg 48 min N and longitude 92 deg 48 min W, on ground the Netsilingmiut had lived on for centuries; it is pinned there.")

upd('ross-victory-059', title="Elizabeth Harbour", pages="plate 5, facing p. 142",
    lat=70.60, lon=-91.70,
    description="John Ross's surveyed plan of Elizabeth Harbour on the east coast of Boothia, with soundings and the bearings taken from the ship. In 1832 it was the point the retreating party aimed for with the boats; Ross put it about sixteen miles north of the 70 deg 21 min they had reached at the end of May that year, and the position here is that estimate, not an observation.")

upd('ross-victory-060', title="Andrew Ross Island", pages="plate 7, facing p. 169",
    lat=70.20, lon=-91.75,
    description="Hand-coloured plate of the Victory close under the cliffs of Andrew Ross Island among broken floe ice, put on stone by J. Brandard from John Ross's own drawing. Ross moored to the island in late September 1829, built a cairn on it and named it after his son Andrew Ross. He gives no observed position for it; it lies on the Boothia east coast a few miles north of the harbours where the ship afterwards wintered, and the position here is approximate.")

upd('ross-victory-061', title="Cape Margaret", pages="plate 8, facing p. 172",
    lat=70.30, lon=-91.70,
    description="A boat party under the cliffs at Cape Margaret, one of the features John Ross named and charted on the Boothia shore in September 1829. No observed position is printed for the cape; the position here is approximate.")

upd('ross-victory-062', title="Victory finally stopped by ice", pages="plate 9, facing p. 175",
    lat=F[0], lon=F[1],
    description="Plate 9 of John Ross's narrative, and the turning point of the voyage: the Victory brought up by the ice at the head of the Gulf of Boothia on 1 October 1829. She never sailed free of that coast again. The berth became Felix Harbour, whose latitude Ross settled at 69 deg 58 min 42 sec N, longitude 92 deg 01 min 06 sec W.")

upd('ross-victory-063', title="The Victory's position compared with four earlier winterings, p. 209",
    pages="p. 209", lat=F[0], lon=F[1],
    description="A small ruled table John Ross printed in the autumn of 1829 setting the Victory's own position and mean October temperature beside those of four earlier wintering places: the Victory at 69 deg 59 min 00 sec N, 92 deg 01 min 06 sec W, mean October 1829 +8.43 deg; Melville Island 1819, -6.50; Winter Island 1821, +9.51; Iglulik 1822, +9.79; Port Bowen 1824, +10.85. It is the observed position of Felix Harbour and, with it, Ross's argument that his berth was the coldest of the five.")

upd('ross-victory-064', title="Account of the daily proportion of provisions served to 18 men for 14 days",
    pages="p. 215", lat=F[0], lon=F[1],
    description="The Victory's ration table, printed by John Ross for the first winter: what eighteen men were issued, item by item, over a fortnight. The fourteen-day totals are 126 lb of bread, 145.5 lb of flour, 6 lb of suet, 9 lb of raisins, 39.375 lb of sugar, 15.67 lb of cocoa, 3.3 lb of tea, 6 lb of rice, 15.625 lb of lemon juice, 108 lb of preserved meats, 40.5 lb each of salt beef and salt pork, pickled cabbage and onions, and one gallon of spirits. Lemon juice was served every day and spirits twice a fortnight. Ross adds that vinegar was served as required, preserved soups were kept back for the coldest weather, and lemons and tamarinds were reserved for the sick, and that the whole of this duty belonged to the purser William Thom.")
