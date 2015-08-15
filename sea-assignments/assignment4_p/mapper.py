import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import json
import urlparse
import urllib
from collections import defaultdict
import os
import subprocess
import hashlib
import time

import logging
import os

class RetrieveMapOutput(web.RequestHandler):
	def head(self):
		self.finish()

	def get(self):
		partition = self.get_argument('reducerIx', None)
		mapTaskID = self.get_argument('mapTaskID', None)
		pairs = []
		for key, values in Map.mapOutputs[mapTaskID][int(partition)]:
			for value in values:
				pairs.append((key, value))
		self.write(json.dumps(pairs))

class Map(web.RequestHandler):
	mapOutputs = defaultdict(lambda: defaultdict(list))

	def head(self):
		self.finish()
		
	def get(self):		
		mapperPath = self.get_argument('mapperPath', None)
		numReducers = self.get_argument('numReducers', None)
		inputFile = self.get_argument('inputFile', None)
		if mapperPath is None or numReducers is None or inputFile is None:
			self.write(json.dumps({"status": "error"}))
			return

		numReducers = int(numReducers)
		partitioner = HashPartitioner(numReducers)
		mapTaskID = hashlib.md5(mapperPath + inputFile + str(time.time())).hexdigest()
		outByPartition = defaultdict(lambda: defaultdict(list))
		if not os.path.exists(inputFile):
			self.write(json.dumps({"status": "no input"}))
			return

		mapGen = mapper(mapperPath, inputFile)			
		for kOut, vOut in mapGen:
			outByPartition[partitioner(kOut)][kOut].append(vOut)		
		for p in outByPartition.keys():
			Map.mapOutputs[mapTaskID][p] = [(k, outByPartition[p][k]) for k in sorted(outByPartition[p].keys())]
		self.write(json.dumps({"status": "success", "mapTaskID": mapTaskID}))

def mapper(mapperPath, inputFile):
	#mapperPath = os.path.abspath(mapperPath)
	#logging.info("Input file %s" % inputFile)
	#logging.info("Mapper path: %s" % mapperPath)	
	p = subprocess.Popen(['python', mapperPath], stdin=open(inputFile), stdout=subprocess.PIPE)
	(out, err) = p.communicate()
	for line in out.split("\n"):
		line = line.strip()
		if len(line) == 0:
			continue
		kOut, vOut = line.strip().split("\t", 1)
		yield kOut, vOut

class HashPartitioner:
	def __init__(self, numReducers):
		self.numReducers = numReducers

	def __call__(self, key):
		return int(hashlib.md5(key).hexdigest()[:8], 16) % self.numReducers
