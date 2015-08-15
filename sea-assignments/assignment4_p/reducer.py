import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import json
import urlparse
import urllib
from collections import defaultdict
import inventory
import heapq
import subprocess
from itertools import chain, groupby, imap, islice

import logging
import os

class RetrieveReduceOutput(web.RequestHandler):
	def head(self):
		self.finish()

	def get(self):
		jobPath = self.get_argument('jobPath', None)
		numReducers = self.get_argument('numReducers', None)
		numReducers = int(numReducers)
		self.write("<pre>")
		for filename in [jobPath + "/%d.out" % i for i in range(numReducers)]:
			self.write(filename + ":\n" + unicode(open(filename, 'r').read(), "utf8") + "\n")
		self.finish()

class Reduce(web.RequestHandler):
	def head(self):
		self.finish()
		
	@gen.coroutine
	def get(self):
		reducerIx = self.get_argument('reducerIx', None)
		reducerPath = self.get_argument('reducerPath', None)
		jobPath = self.get_argument('jobPath', None)
		mapTaskIDs = self.get_argument('mapTaskIDs', None)
		if reducerIx is None or reducerPath is None or jobPath is None or mapTaskIDs is None:
			self.write(json.dumps({"status": "error"}))
			return
			
		reducerIx = int(reducerIx)
		mapTaskIDs = mapTaskIDs.split(",")		
		numMappers = len(mapTaskIDs)

		http = httpclient.AsyncHTTPClient()
		futures = []
		servers = inventory.servers['worker']
		for i in range(numMappers):
			server = servers[i % len(servers)]
			params = urllib.urlencode({'reducerIx': reducerIx,
			                          'mapTaskID': mapTaskIDs[i]})
			url = "http://%s/retrieveMapOutput?%s" % (server, params)	
			print "Fetching", url
			futures.append(http.fetch(url))
		responses = yield futures

		partitions = [json.loads(r.body) for r in responses if not r.error]
		kvPairs = heapq.merge(*partitions)
		outputFile = jobPath + "/%d.out" % (reducerIx)
		reducer(kvPairs, reducerPath, reducerIx, outputFile)
		self.write(json.dumps({"status": "success"}))
		self.finish()

def reducer(kvPairs, reducerPath, reducerIx, outputFile):
	logging.info("reducerPath: %s" % os.path.abspath(reducerPath))
	logging.info("outputFile: %s" % os.path.abspath(outputFile))
	output = open(outputFile, 'w')
	p = subprocess.Popen(['python',reducerPath], stdin=subprocess.PIPE, stdout=output)
	for pair in kvPairs:
		p.stdin.write("%s\t%s\n" % (pair[0].encode("utf8"), pair[1].encode("utf8")))
	p.stdin.close()
	p.wait()
	output.close()


