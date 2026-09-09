import sys, subprocess
sys.path.insert(0,'/data/dev/arctic-history/ross-victory-scratch')
from updev import evupd
R='/data/dev/arctic-history'
def run(*a):
    p=subprocess.run(['/usr/bin/python3','tools/history-db.py',*a],cwd=R,capture_output=True,text=True)
    print(('ok  ' if not p.returncode else 'FAIL ')+' '.join(a[:4])[:60], p.stderr[-400:] if p.returncode else '')

F=('69.9783','-92.0183'); S=('70.0167','-91.90'); V=('70.155','-91.509')

# new events for James Dixon
run('event','--topic','ross-victory','--date','1832-01-10','--title','Death of James Dixon, stoker',
    '--lat',V[0],'--lon',V[1],'--place','Victoria Harbour','--bibkey','ross1835narrative',
    '--people','James Dixon','--tags','death,scurvy,wintering',
    '--detail',"The third winter at Victoria Harbour. James Dixon, shipped as a stoker for the engine that had been landed at Felix Harbour in 1829 and afterwards rated landman, had been failing since December with what John Ross calls a complication of disorders and was not expected to live. He died on 10 January 1832. The men who had been driving a snow tunnel cut his grave; the weather postponed the funeral, a sermon was read for him on Sunday the 15th, and he was buried on the morning of the 16th. He was the second of the three men who died on the voyage, and the only one whose grave is marked on a chart: Ross's surveyed plan of Victoria Harbour letters it on the west shore.")
run('event','--topic','ross-victory','--date','1832-01-16','--title','James Dixon buried at Victoria Harbour',
    '--lat',V[0],'--lon',V[1],'--place','Victoria Harbour','--bibkey','ross1835narrative',
    '--people','James Dixon','--tags','burial,wintering',
    '--detail',"The funeral of the stoker James Dixon, put off from the 15th by the weather and held with the usual solemnities on the morning of Monday 16 January 1832. His grave is lettered on the west shore of John Ross's surveyed plan of Victoria Harbour, a few hundred yards from where the Victory was abandoned four months later.")
