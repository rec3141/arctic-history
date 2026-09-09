import sys; sys.path.insert(0,'amundsen-gjoa-review-scratch')
from q import RAW
import re
vol=sys.argv[1]; needle=sys.argv[2]; before=int(sys.argv[3]) if len(sys.argv)>3 else 300; after=int(sys.argv[4]) if len(sys.argv)>4 else 900
t=RAW[vol]
i=t.find(needle)
print(t[max(0,i-before):i+after] if i>=0 else "NOT FOUND")
