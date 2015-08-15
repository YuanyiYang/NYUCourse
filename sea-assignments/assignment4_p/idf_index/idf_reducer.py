#!/use/bin/env python

import sys
import pickle
import json
from collections import defaultdict 
import math

# input: %s\t%s\n % (term, docID)

result = defaultdict(float)
documentCount = defaultdict(int)
docIDs = set()

for line in sys.stdin:
    term, docID = line.strip().split("\t", 1)
    docID = int(docID)
    docIDs.add(docID)
    documentCount[term] = documentCount[term] + 1
    
for term in documentCount:
	idf = math.log(len(docIDs) / documentCount[term])
	result[term] = idf
  
print pickle.dump(result,sys.stdout)
