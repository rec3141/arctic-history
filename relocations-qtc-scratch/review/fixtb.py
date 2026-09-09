import sqlite3
c = sqlite3.connect('db/history/history.sqlite')
b = c.execute("select body from pages where slug='relocations-the-ships-that-took-people-south'").fetchone()[0]
old = ('[[person:Walter Rudnicki]], a federal social\n'
       'worker who was aboard, told the QTC in 2008 that the rule was applied through\n'
       'nursing mothers: "The baby was sent to the person [standing closest] to the\n'
       'mother and she was sent off. No concern was given to who would take care of the\n'
       'child. I saw this going on" ([[artifact:relocations-qtc-026]]). He also\n'
       'described patients discharged in mid-winter in the summer clothes they had left\n'
       'in — ')
new = ('[[person:Walter Rudnicki]], a retired social\n'
       'worker, told the QTC in 2008 that the policy was applied even to nursing\n'
       'mothers: "The baby was sent to the person [standing closest] to the mother and\n'
       'she was sent off," he explained, "no concern was given to who would take care of\n'
       'the child. I saw this going on" ([[artifact:relocations-qtc-026]]). He also\n'
       'described patients discharged in winter in the summer clothing they had left in\n'
       '— ')
assert old in b, 'no match'
open('relocations-qtc-scratch/review/bodies/relocations-the-ships-that-took-people-south.md', 'w').write(b.replace(old, new))
print('ok')
