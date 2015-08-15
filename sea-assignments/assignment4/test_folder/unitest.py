#!/usr/bin/env python


import json

l = [['\xc2', 1] for x in range(10)]
jl = json.dumps(l, ensure_ascii=False)
print l
print jl
x = json.loads(unicode(jl, errors='	'))
print x
