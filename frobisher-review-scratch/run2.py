import sys
sys.path.insert(0, '/data/dev/arctic-history/frobisher-review-scratch')
from verify2 import check

Q = [
 # --- page frobisher-1576-first-voyage
 ('1576 gaynes', "sure, certayne, and present gaynes", ['coll','best']),
 ('1576 gutte', "greate gutte, bay or passage", ['coll','best']),
 ('1576 commission', "only for the searching of the Gold Ore, and to deferre the further discoverie of the passage untill another tyme", ['coll','best']),
 ('1576 lok wonder', "such a wonder onto the whole city and to the rest of the realm", ['coll']),
 ('1576 wonder2', "as seemed never to have happened the like great matter to any man's knowledge", ['coll']),
 # --- page gold-that-was-not
 ('gold example sake', "for example sake", ['coll','best']),
 ('gold house', "artificially framed and cunningly devised by a notable learned man", ['coll','best']),
 ('gold flatter', "flatter nature", ['coll']),
 # --- page kodlunarn: Hall's list
 ('kod hall list', "Coal; flint-stone; fragments of tile, glass, and pottery; an excavation which I have called an abandoned mine; a trench made by the shore on an inclined plane, such as is used in building a ship on the stocks; the ruins of three stone houses, one of which was twelve feet in diameter, with palpable evidence of its having been erected on a foundation of stone cemented together with lime and sand; and some chips of wood which I found on digging at the base of the ship's trench.", ['hall2','rgs']),
 ('kod karping soft', "Soft - very soft - same as wood all falling in pieces; the tarrio - sea - came up into the trench where the wood was.", ['hall2']),
 ('kod moss of ages', "the moss of ages", ['coll','hall2']),
 ('kod best bulwark', "Best's Bulwark", ['coll','hall2']),
 # --- page first-contact
 ('fc rejoyce', "seemed greatly to rejoyce, skipping, laughing, and dancing for joy", ['coll','best']),
 ('fc trade protocol', "they doe use to laye down of their marchandise uppon the ground, so much as they meane to parte withall, and so looking that the other partie, with whome they make trade, shoulde doe the like, they themselves doe departe, and then, if they doe like of their marte, they come againe, and take in exchange the others marchandise, otherwise, if they like not, they take their owne and departe.", ['coll','best']),
 ('fc canibales', "least perhaps their enemies shoulde receive glory or praye of their dead carcasses; for they supposed us be like to be canibales", ['coll','best']),
 ('fc fyersnes', "geven to fyersnes and rapyne", ['coll','best']),
 ('fc docible', "pleasaunt, and docible amongst us in a verye short time", ['coll','best']),
 # --- page the-captives
 ('cap sides ake', "made his sides ake against the grounde for a moneth after", ['coll','best']),
 ('cap tears', "fell so out into tears that he could not speake a word in a great space", ['coll','best','chesh']),
 ('cap linen', "no linen or woolle at all", ['chesh']),
 ('cap ducke', "he would hit a ducke at a good distance of and not misse", ['chesh']),
 ('cap god be with you', "God be with you", ['chesh']),
 # --- page strait-on-the-map
 ('map frobussher', "Frobusshers Straightes", ['coll','best']),
 ('map penny money', "My knowledge is money", ['rgs']),
 ('map president', "it was quite clear, therefore, that the natives were not bad geographers, and were acquainted with the coast-line of their country", ['rgs']),
 ('map coast as disc', "Coast as discovered by Queen Elizabeth", ['hall2','rgs']),
 ('map title', "Frobisher Strait proved to be a Bay", ['rgs']),
 ('map neatby east greenland', "it was supposed that Frobisher Bay was on the east shore of Greenland", ['neatby']),
 ('map tinnujok', "Tin-nu-jok-ping-oo-se-ong", ['hall2','rgs']),
]
for lab, ph, keys in Q:
    check(lab, ph, keys)
