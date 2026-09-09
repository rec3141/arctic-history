import sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from updev import evupd
F=(69.9783,-92.0183); S=(70.0167,-91.90)

# Felix Harbour positions
for eid in (267,268,302,303,305,304,306,307):
    evupd(eid, lat=F[0], lon=F[1])
# Sheriff's Harbour positions
for eid in (294,308,314):
    evupd(eid, lat=S[0], lon=S[1])

evupd(384, detail="Four years and nearly five months, of which the ship spent four winters beset on one stretch of the Boothia coast and the crew a fifth in a hut at Fury Beach. The ship's company was twenty-three: twenty paid hands and three officers - John Ross, his nephew James Clark Ross and the purser William Thom - who served without pay. Three died on the voyage and twenty came home; the Commons committee that examined the accounts put it that only one man in twenty-three was lost in consequence of the expedition. It is the longest that any beset crew has survived in the Arctic.")

evupd(294, detail="The summer of 1830 never opened. Warping and sawing through September and October recovered four miles of northing; on 31 October, with two hundred yards still to go and the ice sixteen feet thick, John Ross gave the order to stop and lie where they were. The whole month's gain was 850 feet. They called the berth Sheriff's Harbour, after Felix Booth, Sheriff of London; Ross notes that those fond of puns thought the name well chosen. James Clark Ross wintered here taking the magnetic observations that fixed the direction of the pole, and his mean position for the berth is 70 deg 01 min N, 91 deg 54 min W. She got out on 29 August 1831. Ross's later dispatch says the ship was cut in about the middle of November 1830, which the journal does not bear out; the journal is followed here.")

evupd(308, detail="A party of six left the ship at Sheriff's Harbour - not at Victoria Harbour, which the Victory did not reach until the end of that August - accompanied part of the way by John Ross's own party, which turned back at the western sea. A winter of magnetic observations at Sheriff's Harbour had given a dip above 89 degrees and a calculated position for the pole; the journey was made for that purpose alone. Thomas Blanky and Thomas Abernethy were the two mates in the party.",
      people="James Clark Ross; Thomas Abernethy; Thomas Blanky")

evupd(313, detail="The whole of the 1831 season gained about fourteen miles of northing. The ship got out of Sheriff's Harbour on 29 August and made four miles to a bay John Ross had named Mundy Harbour in 1829; by 15 and 16 October, with the anchors carried ashore and the boats turned over on the ice, 'it was very certain that we had now settled ourselves for the winter'. Ross named the berth Victory Harbour after his ship; it was renamed Victoria Harbour by permission of the Duchess of Kent and the Princess Victoria. The stoker James Dixon died here on 10 January 1832 and is buried on the west shore. With provisions running only to June 1832, the decision to walk out was taken here. Position from James Clark Ross's magnetic table (lat 70 deg 09 min 18 sec N, long 91 deg 30 min 33 sec W); the narrative gives the latitude of the harbour reached on 29 August as 70 deg 18 min 11 sec, and the two do not agree.")

evupd(330, detail="A frame of spars 32 feet by 16 covered in canvas, banked in November with four to seven feet of snow and then flooded with water at 15 degrees below zero so that the whole set as ice: John Ross wrote that they 'actually became the inhabitants of an iceberg'. Twenty-one men wintered in it, all that were left of the twenty-three who had sailed. Bedding, clothing and fresh meat were all short, Christmas 1832 was the first they had spent without wine or spirits, and scurvy took hold. Chimham Thomas the carpenter died here on 16 February 1833.")

evupd(376, detail="Only thirteen of the party had been fit enough to carry provisions forward in seven journeys of sixty-two miles each to Batty Bay; three others were in the last stage of debility and one man had lost a foot. The twenty who were left of the ship's company left Fury Beach on 8 July carrying three men who could not walk, and reached the boats in six days; the sick began to recover as soon as they got there.")
