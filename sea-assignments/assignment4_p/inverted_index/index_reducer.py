#!/use/bin/env python

import sys
import pickle
import json
from collections import defaultdict 

result = defaultdict(list)

for line in sys.stdin:
    docID, result_t = line.strip().split("\t", 1)
    docID = int(docID)
    result_list = json.loads(result_t) #[term, tf]
    term = result_list[0]
    tf = result_list[1]
    tf = int(tf)
    tup = (docID, tf)
    result[term].append(tup)

print pickle.dump(result,sys.stdout)
