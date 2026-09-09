import sys
sys.path.insert(0, '/data/dev/arctic-history/frobisher-review-scratch')
from verify2 import check

ALL = ['best', 'coll', 'hall2', 'rgs', 'chesh', 'neatby']

Q = [
 # artifact quotes
 ('020 five men', "they rowed furder beyond that poynt of the land owt of his sight, and there landed iij of them, and the other twayn rested in the bote a little from the land so as he saw them agayn, to whom owt of the ship they made signes and noyse as well as they could to call them to the ship. And immediately these two men with the bote rowed into the land agayn to their fellowes owt of his sight, and after that hower he never saw them.", ['coll']),
 ('021 plucked', "the capitayn called for an other bell which allso he reached to him with a short arme, and in that reache he caught holde on the man's hand, and with his other hand he caught holde on his wrest; and suddenly by mayn force of strength plucked both the man and his light bote owt of the sea into the ship in a tryse.", ['coll']),
 ('022 arrow', "the other being yong, and combred with a sucking childe at hir backe, hiding herselfe behinde the rocks, was espied by one of oure men, who, supposing she had bin a man, shot through the heare of hir head, and pierced hir through the child's arme, whereupon she cried out, and was taken.", ['coll','best']),
 ('023 healed', "our surgeon, meaning to heale hir child's arme, applyed salves therunto. But, she not acquainted with such kinde of surgerie, plucked those salves away, and, by continuall licking with hir own tongue, not much unlike our dogges, healed uppe the child's arme.", ['coll','best']),
 ('024 register a', "Collichang a heathen man buried the 8th of November", ['chesh']),
 ('024 register b', "Egnock a heathen woman buried the 13th of November", ['chesh']),
 ('024 heading', "Burials in Anno 1577", ['chesh']),
 ('025 koojesse', "The men who built the ship, and started with it, all died - died with the cold.", ['hall2']),
 ('025 hall adds', "This agreed precisely with what old Ookijoxy Ninoo told me the previous winter", ['hall2']),
 ('025 hall adds2', "She said that the five men built a ship, and found so much ice that they could not proceed, and finally all froze to death.", ['hall2']),
 ('026 ebierbing', "When our baby boy gets old enough, we tell him all about you, and about all those kodlunas who brought brick, iron, and coal to where you have been, and of the kodlunas who built a ship on Kodlunarn Island. When boy gets to be an old Innuit he tell it to other Innuits, and so all Innuits will know what we now know.", ['hall2']),
 ('026 hall comment', "Thus, by the simple unadorned statement of Ebierbing may be known how it is that oral history is preserved among the Innuit people of the North.", ['hall2']),
 ('027 petato', "A long, long, long, long time ago, a great many ships came here. A northerly gale prevailed, and broke - or smashed - some of the ships.", ['hall2']),
 ('027 petato2', "My mother's grandmother's grandfather knew a good deal about it.", ['hall2']),
 ('028 rae', "He fully concurred in all he had said as to the truthfulness of the Esquimaux. When he first brought home information he had gained from them, they were called liars and story-tellers. He knew better. He never in his life found an Esquimaux tell a falsehood unless it was to gain some particular object.", ['rgs']),
 ('029 best mistaken', "The Generall, albeit with the fyrste perchance he found out the error, and that this was not the old straytes, yet he persuaded the fleete alwayes that they were in theyr righte course and knowne straytes.", ['coll','best']),
 ('038 ingots', "two ingots of fine gold, weighing 9 pennyweights 8 grains, and two ingots of fine silver, weighing 7 ounces 18 pennyweights", ['coll']),
 ('039 neatby', "the sea must needs at last have an ending", ['neatby']),
 ('039 best orig', "knowing that the Sea at length must needes have an endyng, and that some lande shoulde have a beginning that way", ['best','coll']),
 ('031 karping soft', "same as wood all falling in pieces", ['hall2']),
]
for lab, ph, keys in Q:
    check(lab, ph, keys)
