import sys
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from upd import upd
F=(69.9783,-92.0183); S=(70.0167,-91.90); V=(70.155,-91.509); P=(70.0881,-96.7792)

upd('ross-victory-020', pages="pp. 9-10", lat=51.44, lon=0.37)

upd('ross-victory-021', lat=F[0], lon=F[1])
upd('ross-victory-022', lat=F[0], lon=F[1])

upd('ross-victory-023', lat=F[0], lon=F[1],
    description="John Ross's account of the first meeting with the Netsilingmiut of Boothia, at Felix Harbour on 9 January 1830: 'Proceeding then alone, to within a hundred yards, I found that each was armed with a spear and a knife, but saw no bows and arrows. Knowing that the word of salutation between meeting tribes was Tima tima, I hailed them in their own language, and was answered by a general shout of the same kind.' Both parties then threw down their weapons. It was the first meeting between this community and any European, and James Clark Ross was among the party that walked out from the observatory with him.")

upd('ross-victory-024', lat=F[0], lon=F[1])

upd('ross-victory-025', lat=F[0], lon=F[1],
    description="John Ross on the Victory under sail again after eleven and a half months fast at Felix Harbour: 'what seaman could feel this as we did, when this creature, which used to carry us buoyantly over the ocean, had been during an entire year immovable as the ice and the rocks around it, helpless, disobedient, dead.' She made three miles that day, and in the whole of 1830 gained four.")

upd('ross-victory-026', lat=V[0], lon=V[1],
    description="John Ross, in the third autumn at Victoria Harbour, from the long tirade against ice and snow: 'when snow was our decks, snow our awnings, snow our observatories, snow our larders, snow our salt; and, when all the other uses of snow should be at last of no more avail, our coffins and our graves were to be graves and coffins of snow.'")

upd('ross-victory-027', lat=P[0], lon=P[1],
    description="James Clark Ross at the North Magnetic Pole, 1 June 1831: 'As soon as I had satisfied my own mind on this subject, I made known to the party this gratifying result of all our joint labours; and it was then, that amidst mutual congratulations, we fixed the British flag on the spot, and took possession of the North Magnetic Pole and its adjoining territory, in the name of Great Britain and King William the Fourth.' He and his party then built a limestone cairn over a canister holding a record of the fact.")

upd('ross-victory-028', lat=P[0], lon=P[1],
    description="James Clark Ross correcting his own legend in print: 'as far as our instruments can be trusted, we had placed ourselves within one minute of the magnetic pole, but had not fixed on the precise spot... if popular conversation gives to this voyage the credit of having placed its flag on the very point, on the summit of that mysterious pole which it perhaps views as a visible and tangible reality, it can now correct itself as it may please.' He adds that a precise determination would need several observers at different distances and bearings, which is how the wandering pole is tracked today.")

upd('ross-victory-029', lat=P[0], lon=P[1],
    description="James Clark Ross on arriving at the magnetic pole: 'We could have wished that a place so important had possessed more of mark or note... But Nature had here erected no monument to denote the spot which she had chosen as the centre of one of her great and dark powers.' He and his party found instead some recently abandoned Netsilingmiut snow houses, took possession of them, and made the observations from there.")

upd('ross-victory-030', lat=V[0], lon=V[1],
    description="John Ross leaving the Victory at Victoria Harbour on 29 May 1832: 'The colours were therefore hoisted and nailed to the mast, we drank a parting glass to our poor ship, and having seen every man out, in the evening, I took my own adieu of the Victory, which had deserved a better fate. It was the first vessel that I had ever been obliged to abandon, after having served in thirty-six, during a period of forty-two years.'")

upd('ross-victory-035', lat=S[0], lon=S[1],
    description="Recorded here because it is what the record actually says. In the third summer at Sheriff's Harbour, twenty-three Netsilingmiut came to the ship and were given dinner, and John Ross wrote that 'we found a relief from the self-converse of our own minds... in the converse of these greasy gormandizing specimens of humanity, whose language we could scarcely comprehend'; and, of a season with nothing in it, 'is it wonderful that even the visits of barbarians were welcome, or can any thing more strongly show the nature of our pleasures'. The people Ross wrote of in these terms had already kept his crew in fresh meat, taught them the country, drawn its chart, and would be the reason several of them came home.")

upd('ross-victory-039', people="John Ross; William Thom; George Macdiarmid; James Marslin; James Dixon; Chimham Thomas",
    description="John Ross to the Admiralty on how the crew of the Victory survived, crediting the purser William Thom: 'the distribution and economy of provisions, and to his judicious plans and suggestions must be attributed the uncommon degree of health which our crew enjoyed; and as two out of the three who died the four and a half years, were cut off early in the voyage by diseases not peculiar to the climate, only one man can be said to have perished.' The three were James Marslin, who died of consumption in January 1830; James Dixon, who died of a long illness in January 1832; and the carpenter Chimham Thomas, dead of scurvy at Fury Beach in February 1833 - the one Ross allowed. The surgeon was George Macdiarmid. Three of twenty-three did not come home from four winters beset and a fifth ashore.")

upd('ross-victory-040', lat=69.9, lon=-92.4,
    description="John Ross on the one moment in four years when it nearly went wrong between the expedition and the Netsilingmiut, in April 1830: 'we were relieved by the courage or confidence of one of the women, who came out of a hut just as I was again raising my gun, and called to me not to fire, advancing up to our party immediately, without showing the least mark of fear. From her, we soon learned the cause of all this hubbub.' Her name is not recorded. An adopted son of Pow-weet-yah, a boy of seven or eight, had been killed in the night by a falling stone and the death laid to the ship's people; James Clark Ross and the surgeon had had a weapon raised at them minutes before.")
