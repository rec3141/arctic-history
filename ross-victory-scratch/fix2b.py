import sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from upd import upd
F=(69.9783,-92.0183); S=(70.0167,-91.90); V=(70.155,-91.509); P=(70.0881,-96.7792)

upd('ross-victory-070', title="Shullanina, Tulluahiu and Tirikshiu", pages="plate 16, facing p. 272",
    people="Tulluahiu; Tirikshiu; Shullanina; Chimham Thomas",
    lat=F[0], lon=F[1],
    description="The plate John Ross's binder's list calls Tulluachiu and Family: three Netsilingmiut standing on the ice in winter clothing, named on the plate itself as SHULANINA, TULLUACHIU and TIRIKSHIU - the hunter Tulluahiu, his wife Tirikshiu and his daughter Shullanina. Tulluahiu stands on the wooden leg the ship's carpenter Chimham Thomas made for him in January 1830, and the lettering VICTORY can be read on its shaft. Put on stone by J. Brandard from Ross's own drawing, printed by Graf and Soret. The appendix calls them the most remarkable family the expedition met.")

upd('ross-victory-071', title="Felix Harbour (Chart)", pages="plate 17, facing p. 300",
    lat=F[0], lon=F[1],
    description="John Ross's surveyed plan of Felix Harbour, where the Victory lay through the first winter, with the ship's berth marked and the soundings taken round her.")

upd('ross-victory-072', title="Umingmak: Commander Ross killing a musk bull",
    pages="plate 18, facing p. 350", people="James Clark Ross",
    lat=69.9, lon=-93.0,
    description="Hand-coloured plate captioned UMINGMAK (COMMANDER J. C. ROSS KILLING A MUSK BULL), put on stone by J. Brandard from John Ross's original drawing. Umingmak is the Inuktitut word for the musk ox. It shows James Clark Ross's sledge party on one of the 1830 journeys inland from Felix Harbour, the dogs holding the animal at bay in a gully while the shot is taken; the narrative describes the dogs seizing it by the heels and dodging as it turned. Position approximate.")

upd('ross-victory-073', title="Lady Melville's Lake", pages="plate 19, facing p. 390",
    lat=69.7, lon=-93.5,
    description="Plate 19 of John Ross's narrative: the lake on the Boothia isthmus crossed by the sledge parties, with a party and their dogs on the shore. From the height above it James Clark Ross could count hundreds of caribou on the flat land on either side. Position approximate.")

upd('ross-victory-074', title="Graham's Valley", pages="plate 20, facing p. 401",
    people="James Clark Ross; George Macdiarmid",
    lat=69.9, lon=-92.6,
    description="Plate 20 of John Ross's narrative: a valley between rock walls with a flag on the bluff above and a sledge party halted below. Graham's Valley is on the route west from Felix Harbour, and it is the place as far as which the surgeon George Macdiarmid went with James Clark Ross in May 1830 to mark a spot where provisions could be laid up against the party's return. Position approximate; Ross prints no observation for it.")

upd('ross-victory-075', title="Sheriff's Harbour and Copeland Islands",
    pages="plate 21, facing p. 518", people="John Ross; James Clark Ross",
    lat=S[0], lon=S[1],
    description="The Victory in her second winter quarters at Sheriff's Harbour, with a dog team on the ice. James Clark Ross's mean observed position for the berth is 70 deg 01 min N, 91 deg 54 min W. It was from here, not from the later berth at Victoria Harbour, that he set out for the North Magnetic Pole on 27 May 1831, after a winter of magnetic observations that had already given a dip above 89 degrees.")

upd('ross-victory-076', title="Saumarez River", pages="plate 22, facing p. 531",
    people="James Clark Ross",
    lat=70.2, lon=-93.0,
    description="Plate 22 of John Ross's narrative: a sledge party hauling up a deep frozen stream bed between rock walls on one of James Clark Ross's Boothia journeys. Position approximate.")

upd('ross-victory-077', title="Tilson's Islands", pages="plate 23, facing p. 542",
    people="John Ross",
    lat=70.2, lon=-92.6,
    description="Plate 23 of John Ross's narrative: a great isolated rock with sledges and dogs halted beneath it, on the coast Ross named Tilson's Islands. Position approximate.")

upd('ross-victory-078', title="River Lindsay", pages="plate 24, facing p. 581",
    people="John Ross",
    lat=70.1, lon=-93.2,
    description="Plate 24 of John Ross's narrative: a Netsilingmiut camp of skin tents beside the River Lindsay, with people and dogs. It was at Lindsay river that Ross met Tulluahiu's whole family again in the summer of 1831. Position approximate.")

upd('ross-victory-079', title="Victory under sail for the last time",
    pages="plate 25, facing p. 595", people="John Ross",
    lat=S[0], lon=S[1],
    description="Plate 25 of John Ross's narrative, and the last time the Victory ever moved under her own sails: 29 August 1831, casting off from Sheriff's Harbour under a reefed topsail with a strong west wind. She ran four miles, took the ground once, broke the lower rudder iron, and was warped into the bay Ross had named Mundy Harbour in 1829 and now renamed for his ship. She was abandoned there on 29 May 1832.")

upd('ross-victory-080', title="Victoria Harbour (Chart)", pages="plate 26, facing p. 608",
    people="John Ross; James Dixon",
    lat=V[0], lon=V[1],
    description="John Ross's surveyed plan of the harbour where the Victory was abandoned, captioned VICTORIA HARBOUR, with the compass rose, a scale of 1200 yards and soundings from 3 to 23 fathoms. It is the most exact record of the wreck site there is: the ship's berth is drawn in about 10 fathoms on the eastern side, a note marks where the stores were landed at the head of the harbour, and on the western shore is lettered J. Dixon's grave - the stoker James Dixon, who died aboard on 10 January 1832 and was buried here on the 16th.")
