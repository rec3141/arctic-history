import sys
sys.path.insert(0, '/data/dev/arctic-history/frobisher-review-scratch')
from verify2 import check

Q = [
 ('lok fyersnes', "of countenance and conversation proceding of a nature geven to fyersnes and rapyne", ['coll']),
 ('best column', "made a columne or crosse of stones", ['coll']),
 ('best devoured', "it is to be thoughte that they had slaine and devoured oure men", ['coll']),
 ('best sullen', "desperate in their fight, sullen of nature, and ravenous in their manner of feedinge", ['coll']),
 ('best kinde harted', "exceedingly friendly and kinde harted, one to the other", ['coll']),
 ('best dirges', "a mournefull song, and Dirges", ['coll']),
 ('best chaste', "verye chaste in y-e maner of their living", ['coll']),
 ('best musicke', "They delight in musicke above measure", ['coll']),
 ('best horses', "wondred muche at all our things, and were afraide of our horses, and other beastes, out of measure", ['coll']),
 ('best docible', "beganne to grow more civill, familiar, pleasant, and docible amongst us in a verye shorte time", ['coll']),
 ('best teares', "fell so out into teares, that he could not speake a worde in a greate space", ['coll']),
 ('best bellie', "dangerouslie hurt in the bellie with one of their arrowes", ['coll']),
 ('best wolves', "he was slain with wolves and wilde beastes", ['coll']),
 ('lok xij houses', "the walls of xij olde houses", ['coll']),
 ('parks quote', "have preserved an account of this first European attempt to exploit the natural resources of the Arctic", []),
 ('karping captains', "all same as captains", ['hall2']),
 ('hall britmus', "quantities of timber, carried out for the purpose of building a fort, were buried at the bottom of one of his mines", ['hall2']),
 ('hall haircord', "Small piece of cord, apparently of hair, found deeply embedded in the coal deposit", ['coll']),
 ('hall ekke', "Ek-ke-lu-zhun is a bay on the east side of Countess of Warwick's Sound", ['coll']),
 ('dcb abuses', "the abuses of Captain Furbisher against the Companye", ['coll']),
]
for lab, ph, keys in Q:
    if not keys:
        print('SKIP    %-28s (checked against the Parks Canada page)' % lab)
        continue
    check(lab, ph, keys)
