#!/usr/bin/env python3
import sys
sys.path.insert(0, 'relocations-qtc-scratch/review')
from find import find, NORM, norm

CASES = [
 # (label, expected-file-substring, phrase)
 ('001a','qtc-grise','When we got near'),
 ('001b','qtc-grise','I remember we were all on the deck of the ship, the C. D. Howe, and all the women started to cry. And when women start to cry, the dogs join in. It was eerie.'),
 ('002','qtc-grise','One man had a flashlight and he used his flashlight when they were having a meal. Then the flashlight was passed from shelter to shelter so that people could eat.'),
 ('003','qtc-grise','you can only catch one caribou per year for your family'),
 ('003b','qtc-grise','You are liable to a $5,000 fine or be arrested if you kill any musk-ox'),
 ('004','qtc-grise','I was so scared and thought there would never be light again'),
 ('005','qtc-grise','She tried to make formula for him by mixing flour with water'),
 ('006','rcap-1994','The first ten years in Resolute were the most terrible years of our lives'),
 ('006b','rcap-1994','We spent years without mothers, without fathers, without brothers, without sisters, who were all sick in the hospital'),
 ('006c','rcap-1994','We were completely cut off from the world for the first three or four years'),
 ('007','rcap-1994','Where are all the animals that they were promised'),
 ('008','rcap-1994','right away he was turned down'),
 ('010','rcap-1994','the angle of occupation of the country'),
 ('011','qtc-grise','families will be brought home at the end of one year if they so desire'),
 ('011b','qtc-grise','could return to Port Harrison'),
 ('012','resolute','You can\'t forgive someone who doesn\'t acknowledge what happened'),
 ('014','resolute','We didn\'t know any of this'),
 ('015','resolute','perhaps they could be persuaded to come here as well'),
 ('017','qimmiit','performance, appearance, health, and endurance'),
 ('018','qimmiit','to leave their present economy as undisturbed as possible'),
 ('018b','qimmiit','continue to transfer families from unproductive areas to regions where game is more abundant'),
 ('019','qimmiit','if our dogs were tied up'),
 ('020','qimmiit','The RCMP started killing off Inuit dogs way before the dog distemper epidemic'),
 ('021','qimmiit','they were going to shoot his dogs tomorrow'),
 ('022','rcmpsleddog','In place of a conspiracy, the QTC found a series of inter-connected government policies and laws put into effect and enforced by the RCMP, which quickly undermined traditional Inuit ways of living'),
 ('022b','rcmpsleddog','they effectively outlawed traditional Inuit ways of handling dogs'),
 ('023','rcmpsleddog','toward discrediting Inuit memories'),
 ('023b','rcmpsleddog','denying the validity of most Inuit oral evidence yet presenting the views of non-Inuit with little negative comment'),
 ('024','healthcare','I thought I was lost. I thought I would never come back here to my parents when I first went down. I really thought I was lost.'),
 ('025','healthcare','They would leave in July'),
 ('025b','healthcare','My mother finally came back a year later, in the following spring'),
 ('026','healthcare','was sent off. No concern was given to who would take care of the child. I saw this going on'),
 ('026b','healthcare','It never occurred to the medical personnel that you don\'t wear summer clothes in the dead of winter in Pang'),
 ('027','healthcare','Land of No Return'),
 ('029','nuutauniq','They wouldn\'t dare'),
 ('029b','nuutauniq','powerful social fear or inhibition caused by inequality in power'),
 ('030','nuutauniq','Relocation describes the planned movement of people to a location that has been chosen by an external agent'),
 ('030b','nuutauniq','Evacuation refers to the temporary movement of people by government in real or perceived emergencies'),
 ('031','nuutauniq','domicide'),
 ('031b','nuutauniq','It represents the loss of independence and replacement of a way of life'),
 ('032','finalreport','when past opponents get back together, meet in the middle, are at peace'),
 ('033','finalreport','The decision to give up the traditional way of life was almost never an easy one, and once made, it proved to be irreversible'),
 ('043','tb-apology','Today, I am here to say sorry'),
 ('043b','tb-apology','This policy wasn\'t an accident'),
 ('044','tb-apology','let\'s find them'),
 ('046','resolute','The Pond Inlet Inuit thought that the Inukjuak Inuit were speaking English'),
 ('047','resolute','they were laughing at the same time, while putting my puppies in the garbage'),
 ('048','resolute','Now Resolute Bay is our home and we do not want to leave it'),
 ('049','resolute','it is not considered that the conditions they met with there were any more unpleasant than those they left'),
 ('050','resolute','I asked who would protect them against the government'),
 ('052','resolute','We were close to the shore and we are too far from the shore right now'),
 ('053','resolute','was a scourge in our communities then'),
 ('057','nunatsiaq','We were blind hunters'),
 ('057b','nunatsiaq','we had arrived in a dead land'),
 # page-text claims that are quoted in the pages
 ('P-grise-complicated','qtc-grise','the problems they faced were more complicated than that'),
 ('P-grise-dependent','qtc-grise','families who were the most dependent on government assistance were more likely to be relocated'),
 ('P-qtc-neverfully','qtc-grise','Inuit were never fully informed of options or potential consequences'),
 ('P-eckalook','qtc-grise','did not agree to the move but later on they agreed'),
 ('P-simeonie-noother','qtc-grise','It seemed like I had no other choice but to say yes'),
 ('P-afraid','qtc-grise','were afraid of the RCMP officers and felt pressured to move'),
 ('P-health-immediately','healthcare','had to immediately board the ship to be sent south'),
 ('P-health-leasthumane','healthcare','it was also very likely the least humane'),
 ('P-health-sourceofdisease','healthcare','almost as much a source of disease as a method of prevention'),
 ('P-health-waited','healthcare','waited for their children and parents to return'),
 ('P-larsen-notgood','healthcare','the environment to which they belong'),
 ('P-marsh','healthcare','are not concerned with the true meaning of the two words'),
 ('P-qimmiit-surplus','qimmiit','found opportunities to kill qimmiit they considered to be surplus'),
 ('P-nuut-mix','nuutauniq','voluntary, pressured and forced moves'),
 ('P-nuut-officials','nuutauniq','a voluntary'),
 ('P-nuut-kuptana','nuutauniq','almost unthinkable'),
 ('P-nuut-demanding','nuutauniq','appeared to be demanding consent, not asking for it'),
 ('P-nuut-optimistic','nuutauniq','optimistic forecasts that failed to come true'),
 ('P-nuut-rheaume','nuutauniq','subtle pressure, but it was coming at you from everywhere'),
 ('P-nuut-everyinuk','nuutauniq','Every Inuk who appeared before the QTC experienced a long separation'),
 ('P-final-healing','finalreport','Healing and reconciliation are only possible when the party responsible for past wrongs'),
 ('P-final-sincere','finalreport','willingness to work with Inuit in a respectful partnership'),
 ('P-qimmiit-rec','qimmiit','in part symptoms of intergenerational trauma caused by historical wrongs'),
 ('P-final-domination','finalreport','government domination and interference with Inuit decision-making'),
 ('P-itk-poll','finalreport','generally aware of the realities of life for the Inuit in the Canadian Arctic'),
 ('P-res-kalluk','resolute','RCMP were the leaders back then'),
 ('P-res-pudluk-dark','resolute','the dark season frightened me'),
 ('P-res-martha-months','rcap-1994','I remember the men being out for months'),
 ('P-res-idlout-drunk','resolute','the whole town would be drunk for a whole week'),
 ('P-plaque','','dedicated their lives to Canada'),
]

for label, only, phrase in CASES:
    h = find(phrase, only or None)
    if not h:
        h2 = find(phrase, None)
        if h2:
            print(f'{label:22} WRONG-FILE  found in {[p for p,_ in h2]}  :: {phrase[:70]}')
        else:
            print(f'{label:22} NOT FOUND   :: {phrase[:70]}')
    else:
        print(f'{label:22} ok ({len(h)}) {sorted(set(p for p,_ in h))[0]}')
