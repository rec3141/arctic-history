import sys, subprocess
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from updev import evupd
F=(69.9783,-92.0183); S=(70.0167,-91.90); V=(70.155,-91.509)
R='/data/dev/arctic-history'
def run(*a):
    p=subprocess.run(['/usr/bin/python3','tools/history-db.py',*a],cwd=R,capture_output=True,text=True)
    print(('ok  ' if not p.returncode else 'FAIL ')+a[0]+' '+a[2][:40], p.stderr[-300:] if p.returncode else '')

# --- people
run('person','--name','James Dixon','--role','stoker, rated landman, of the Victory',
    '--affiliation',"John Ross's Victory expedition, 1829-1833",'--died','1832',
    '--topic','ross-victory','--bibkey','ross1835narrative',
    '--note',"One of the three men who died on the voyage, and the least remembered of them. Shipped as a stoker for an engine that was landed on the beach at Felix Harbour within five months of sailing, and afterwards rated landman. He was ailing through the autumn of 1831 at Victoria Harbour with what John Ross calls a complication of disorders, and was not expected to live; he died on 10 January 1832. The weather held up the funeral, a sermon was read on Sunday the 15th and he was buried on the 16th, in a grave the men had cut while they were driving a tunnel through the snow. His grave is lettered on Ross's own surveyed plan of Victoria Harbour, which makes it the one marked burial place of the expedition. His wages, 89 pounds 8s, were repaid unclaimed into the hands of the Treasurer.")
run('person','--name','Henry Ayre','--also','Henry Eyre','--role','cook of the Victory',
    '--affiliation',"John Ross's Victory expedition, 1829-1833",'--died','1833',
    '--topic','ross-victory','--bibkey','ross1835narrative',
    '--note',"Cook through four winters beset and a fifth in the hut at Fury Beach. He came home in the Isabella in October 1833 and the Admiralty's payment list of 28 October records his 165 pounds 2s 8d against the note 'Died soon after his return'. Ross's crew list spells him Eyre; the payment list Ayre.")

# --- places
run('place','--name','Felix Harbour','--lat','69.9783','--lon','-92.0183','--kind','harbour',
    '--note',"The Victory's first wintering berth, on the east coast of the Boothia Peninsula near Lord Mayor Bay, where she was stopped by ice on 1 October 1829 and lay for eleven and a half months. Named for Felix Booth. John Ross settled its position at 69 deg 58 min 42 sec N, 92 deg 01 min 06 sec W, and prints 69 deg 59 min 00 sec in the comparative table on p. 209. It was here that the crew met the Netsilingmiut on 9 January 1830, where Chimham Thomas made Tulluahiu's wooden leg, where the steam engine was landed on the beach, and where Ikmallik and Apelagliu drew the chart of Boothia.")
run('place','--name',"Sheriff's Harbour",'--lat','70.0167','--lon','-91.90','--kind','harbour',
    '--note',"The Victory's second wintering berth, about four miles north of Felix Harbour, cut into through October 1830 at a rate of a few dozen feet a day and given up as a project on 31 October with two hundred yards still to go and the ice sixteen feet thick. Named for Felix Booth as Sheriff of London; Ross records that those fond of puns thought the name apt. James Clark Ross's mean magnetic position for the berth is 70 deg 01 min N, 91 deg 54 min W. He wintered here taking the observations that fixed the direction of the magnetic pole, and it was from here that he set out for it on 27 May 1831 and here that he returned. The ship left on 29 August 1831.")
run('place','--name','Somerset House','--lat','72.7','--lon','-91.92','--kind','site',
    '--note',"The hut built at Fury Beach in July 1832 out of the Fury's spars and canvas, 32 feet by 16, banked in November with four to seven feet of snow flooded with water at 15 below so that it set as ice. Twenty-one men wintered in it from 7 October 1832 to 8 July 1833 - all that were left of the twenty-three who had sailed - and the carpenter Chimham Thomas died there of scurvy in February 1833. The name is a joke against the Admiralty's own Somerset House in London, made on Somerset Island.")
