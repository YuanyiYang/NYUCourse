#!/use/bin/env python

import sys
import pickle
import json

doc_to_content = pickle.load(sys.stdin)

for docID in doc_to_content:
    result_v = (doc_to_content[docID]['title'], doc_to_content[docID]['docBody'])
    print "%s\t%s" % (docID, json.dumps(result_v))
