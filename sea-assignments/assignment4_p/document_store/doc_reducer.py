#!/use/bin/env python

import sys
import pickle
import json

result = {}

for line in sys.stdin:
    docID, result_t = line.strip().split("\t", 1)
    docID = int(docID)
    result_tuple = json.loads(result_t)
    result[docID] = result_tuple

print pickle.dump(result,sys.stdout)
