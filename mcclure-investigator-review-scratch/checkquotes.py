#!/usr/bin/env python3
import sys
sys.path.insert(0, '/data/dev/arctic-history/mcclure-investigator-review-scratch')
from verify import find

Q = [
 ('015','osborn',"The North-west Passage was discovered! All doubt as to the water-communication between the two great oceans was removed; and it now alone remained for Captain M'Clure, his officers and men, to perfect the work by traversing the few thousand miles of known ground between them and their homes."),
 ('016','osborn',"Thus we launch into this formidable frozen sea. Spes mea in Deo"),
 ('017','osborn',"Happening to inspect more closely than usual the famous mass of sandstone on which Parry had caused his ship's name to be engraved, Lieut. Mecham could hardly credit his senses when he discovered a document upon its summit, detailing the accomplishment of the north-west passage, and the position of H. M. S. 'Investigator' in Banks Land!"),
 ('018','mcdougall',"In the name of God, who are you?"),
 ('018b','mcdougall',"I am Lieut. Pim of the 'Resolute' (Captain Kellett), now at Melville Island"),
 ('019','mcdougall',"the sick vied with the healthy in activity to get on deck. All was haste and confusion; in a moment the lower deck was cleared, the carpenters had dropped their tools (they were making the first coffin), and even the men on shore, digging a grave, seeing that something unusual had occurred, hurried off to share in the astonishment and delight of their excited shipmates."),
 ('020a','osborn',"is such as renders them utterly unfit to undergo the rigour of another winter in this climate"),
 ('020b','osborn',"there exists in all of them at present, with one or two exceptions, well marked evidence of scurvy and debility in various stages of development, with great loss of flesh and strength"),
 ('021','mcdougall',"Captain Kellett replied that he had come to the conclusion, that nothing contained in his orders would justify him in abandoning the ships under his command"),
 ('021b','mcdougall',"final, decided, and most unmistakeable orders"),
 ('022','mcdougall',"After advancing about a quarter of a mile, the crews of the various sledges halted simultaneously; unharnessed, and gave three hearty cheers for the 'Resolute' and 'Intrepid;' but though the ice is a good conductor of sound, we heard no response."),
 ('024','armstrong',"We at once landed, and having called out to them words of peace in their own language, we approached; they timidly met us, and in a few minutes we were rubbing noses - the customary mode of friendly salutation with them."),
 ('025','armstrong',"If the supply is not equal to the demand, the body wastes, and debility and disease of a scorbutic character ultimately ensue. I am, therefore, of opinion that one pound of animal food daily is not sufficient for men employed on Polar service."),
 ('026','armstrong',"I could only view this contemplated hazardous undertaking in the most serious light"),
 ('026b','armstrong',"I could arrive at no other conclusion than that they were utterly unfit for the performance of the service"),
 ('027','armstrong',"Death for the first time made its appearance amongst us, and removed from this world, John Boyle, (A.B.), after a short illness, from the exhausting effects of dysentery, acting on a scorbutic habit"),
 ('027b','armstrong',"He had spoken cheerfully a few minutes before death, but on making a slight exertion in his bed, sudden syncope ensued, and he died without a struggle."),
 ('028','armstrong',"It is impossible to convey a truthful idea of the labour of dragging a sledge over rough ice; at times it can only be moved a few feet, until it be again arrested by a ragged or almost precipitous wall of rough, broken up floe ice."),
 ('029','armstrong',"We landed off Ramsgate on the 6th of October, 1854, after an absence of four years and ten months."),
 ('031','bluebook',"as the news flew throughout the ship with electric rapidity the whole crew were in commotion, the sick, forgetful of their maladies, leaped from their hammocks, the artificers busily engaged making sledges dropped their tools, the despondency left the healthy"),
 ('032','bluebook',"she was left with her colours flying, the hatchways and skylights all covered and battened down, and every precaution taken to prevent moisture from penetrating between decks; she was perfectly water-tight and serviceable"),
 ('033','bluebook',"in the march across the straits the health of the crew appeared to revive"),
 ('033b','bluebook',"they are rapidly regaining the loss of flesh which nineteen months on two-thirds rations had considerably reduced"),
 ('042','collinson',"His name was Ip-pee-ra, and he appeared to be the leading man of this portion of the tribe. Two of the party with him were his sons-in-law, and the fourth was his wife; far from a handsome specimen of her sex, but uncommonly desirous of picking up the wee things about the decks."),
 ('043a','collinson',"a copper hasp for securing the latch of a door, fastened on by three screws, and with the Queen's mark on it"),
 ('043b','collinson',"almost the only article we have met with which could have belonged to the missing ships"),
 ('044','collinson',"The wind continued strong, and the ship, in consequence of the rough state of the copper from collision with the ice, made but little progress to windward, so that it was not until the 5th of May that we got a sight of Old England."),
 ('049','miertsching',"Der Haeuptling, ein sehr schoener und verstaendiger Mann, hiess Attua. Er hatte 3 Frauen und 13 Kinder."),
 ('050','miertsching',"Ueber uns ist ein sehr grosser, blauer Kasten, das Haus der Sonne."),
 ('051','miertsching',"erhoben alle ein Geschrei: sivoravogut! erksidlarpogut!"),
 ('052','miertsching',"Ihre Harpunen, Messer, Beile, Pfeilspitzen, Naehnadeln u.s.w. sind alle von Kupfer verfertigt, welches sie gediegen von den weiter oestlich wohnenden Eskimos gegen Seehundstran, Narwalhoerner u. dergl. mehr eintauschen."),
 ('053','miertsching',"stellte mir nun auch seine Tochter vor mit den Worten: takka unna!"),
 ('057','mcdougall',"The practicability of getting into Winter Harbour was first discussed; but the idea of cutting through six miles of solid floe, was too absurd to be long entertained."),
 ('058','mcdougall',"the whole sea was covered with a thick sludge, which the seamen not inaptly likened to thick pea-soup. This tended considerably to impede the progress of the ship, and had we not been favoured with a strong breeze, she would have been perfectly unmanageable."),
 ('059','mcdougall',"ignorant of the description of labour and exertion required for arctic travelling, which he candidly confessed surpassed everything in the form of hard work he had ever seen"),
 ('061','bluebook',"The floe, if floe it can be called, proved bad indeed: hummocks after hummocks followed each other in apparently endless succession, sometimes composed of very old, then young ice; on the former the surface was so glassy and uneven that the men could scarcely stand."),
 ('062','bluebook',"Arrived within 100 yards without being observed; then, however, two persons taking exercise on the ice discovered that I did not belong to their ship. Upon beckoning, they quickly approached, and proved to be Capt. M'Clure and Lieut. Haswell."),
 ('063','bluebook',"Each person was supplied with a pair of canvas boots and two pair of mocassins. The load amounted to 184lbs. a man."),
 ('064','bluebook',"The pack here is much heavier than any yet seen, being almost entirely composed of very old broken up floes."),
 ('064b','bluebook',"are very much fagged, and are all snoring before supper is ready"),
 ('065','bluebook',"the unfortunate loss of a large portion of beef compelled the captain to put the ship's company, during the second winter, upon short allowance, 3/4 lb. meat and 1 lb. flour daily, being the principal rations - a miserable pittance for hearty men in these bleak regions"),
 # page block quotes
 ('PAGE-hamilton','bluebook',"Soon after supper we were all astonished by hearing foot-steps approaching the tent; this proved to be Commander Richards and three men from his sledge. They had passed our sledge tracks about 3' off and followed them up."),
 ('PAGE-mcclintock13jun','bluebook',"Saw two ivory gulls. Started at a quarter past eight, at half-past ten the fog cleared off and we saw the land, which is evidently an island."),
 ('PAGE-armstrong-feb','armstrong',"a few hours illness would produce the most alarming degree of prostration I have ever witnessed"),
 ('PAGE-armstrong-avidity','armstrong',"with a degree of avidity and relish which must be experienced to be fully understood"),
 ('PAGE-armstrong-noextra','armstrong',"no extra food was allowed for the sick under any circumstances"),
 ('PAGE-mcclure-meritorious','mcdougall',"most meritorious and praiseworthy"),
 ('PAGE-kellett-clothing','mcdougall',"so as to avoid confusion, in the event of re-occupying the ship"),
 ('PAGE-earliest-spring','mcdougall',"the earliest extended spring journey on record"),
]

for tag, key, phrase in Q:
    p, hits, n = find(key, phrase)
    status = 'OK ' if hits else 'MISS'
    print(f'{status} {tag:26s} [{key}] {len(hits)} hit(s)')
    if not hits:
        # try progressively shorter prefixes to locate the divergence
        words = p.split()
        lo, hi = 1, len(words)
        best = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            _, h2, _ = find(key, ' '.join(words[:mid]))
            if h2:
                best = mid; lo = mid + 1
            else:
                hi = mid - 1
        print(f'      longest matching prefix: {best}/{len(words)} words: "{" ".join(words[:best])}"')
        if best:
            _, h3, nn = find(key, ' '.join(words[:best]))
            h = h3[0]
            print(f'      text says: ...{nn[h:h+len(" ".join(words[:best]))+120]}...')
