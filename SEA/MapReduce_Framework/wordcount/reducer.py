#!/usr/bin/env python

from itertools import groupby, imap
from operator import itemgetter
import sys

data = imap(lambda x: x.strip().split("\t"), sys.stdin)
for word, group in groupby(data, itemgetter(0)):
	total = sum(int(count) for _, count in group)
	print "%s\t%d" % (word, total)