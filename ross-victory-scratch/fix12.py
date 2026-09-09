import sys, subprocess
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from updev import evupd
R='/data/dev/arctic-history'
def run(*a):
    p=subprocess.run(['/usr/bin/python3','tools/history-db.py',*a],cwd=R,capture_output=True,text=True)
    print(('ok  ' if not p.returncode else 'FAIL ')+' '.join(a[:5])[:60], p.stderr[-400:] if p.returncode else '')

run('event','--topic','ross-victory','--date','1830-05-29',
    '--title',"James Clark Ross reaches and names Victory Point on King William's Land",
    '--lat','69.97','--lon','-98.55','--place','Victory Point','--bibkey','ross1835narrative',
    '--people','James Clark Ross; Thomas Abernethy','--tags','sledging,survey,cairn,franklin',
    '--detail',"The far end of James Clark Ross's longest sledge journey, made from Felix Harbour with Thomas Abernethy. From a stranded mass of ice about forty feet high they saw a point of land fifteen miles to the south-west, which Ross named Cape Franklin; the point they stood on he named Victory Point, 'the ne plus ultra of our labour'. They built a cairn of stones six feet high and put in it a canister with an account of the expedition, thinking it would never be read. Eighteen years later Franklin's surviving officers left their own record at that cairn, and it was found there in 1859 - see [[topic:franklin-1845]]. Ross prints the position as latitude 69 deg 37 min 49 sec N, longitude 98 deg 40 min 49 sec W, and the observing station a few miles back as 69 deg 46 min 19 sec N, 98 deg 32 min 49 sec W. His longitude is close to the modern feature but his latitude is some twenty minutes of arc - about forty kilometres - south of it, and the discrepancy has never been explained; the row is pinned at the modern Victory Point, not at Ross's printed latitude.")

evupd(328, title="Stopped by unbroken ice at 73 deg 56 min N")
