import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil 
import json
import urllib
import subprocess
import logging
from operator import itemgetter
from itertools import groupby
import heapq
from os.path import abspath, dirname, join
import uuid
import sys

logging.basicConfig(level=logging.INFO)

getKey = itemgetter(0)
MY_BASE_PORT = 25800
MAX_WORKER = 5
WORKERS_PORT = [MY_BASE_PORT+x for x in range(MAX_WORKER)]
BASE_URL = "http://linserv2.cims.nyu.edu:"

# used for each worked to share data between MapHandler and RetrieveMap Handler
class MyDataStore():
	def __init__(self):
		self.data = {}

class ReduceHandler(web.RequestHandler):
	
	@gen.coroutine
	def get(self):
		reducerIx = self.get_argument("reducerIx",None)
		reducerPath = self.get_argument("reducerPath", None)
		mapTaskIDs = self.get_argument("mapTaskIDs", None)
		jobPath = self.get_argument("jobPath", None)
		listOfMapTasks = mapTaskIDs.split(",")
		numMapper = len(listOfMapTasks)
		
		http = httpclient.AsyncHTTPClient()
		futures = []
		for i in range(numMapper):	
			server_port = WORKERS_PORT[i % MAX_WORKER]
			params = urllib.urlencode({ 
				'reducerIx' : reducerIx,
				'mapTaskID' : listOfMapTasks[i]
			})
			url = "%s%d/retrieveMapOutput?%s" % (BASE_URL, server_port, params)
			logging.debug("Fetching %s" % url)
			futures.append(http.fetch(url))
		responses = yield futures
		merged_result = self.linear_merge(responses)
	    # merged_result is a generator object
	    # for pair in merged_result: pair[0] is unicode, pair[1] is an int
		kvString = "\n".join(str(pair[0]) + "\t" + str(pair[1]) for pair in merged_result)
		path = abspath(join(dirname(__file__),reducerPath))
		reducerIndex = "-i %d" % int(reducerIx)
		output_path = "-o %s" % jobPath
		p = subprocess.Popen([path, reducerIndex, output_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		(out, err) = p.communicate(kvString)
		rc = p.returncode
		if err or rc!=0:
			logging.error("Reducer.py error: %s" %err)
			logging.error("Error code: %d" %rc)		
		else:
			#print out
			resp = {"status":"success"}
			self.write(json.dumps(resp))
			self.finish()
		
		
	def linear_merge(self, responses):
		response_body = [[] for x in range(len(responses))]
		for i in range(len(responses)):
			temp_List = []
			temp_List = json.loads(responses[i].body)
			if len(temp_List[0]) == 0:
				continue
			#logging.warn(json.dumps(temp_List))
			for word,group in groupby(temp_List,getKey):
				total = sum(int(count) for _, count in group)
				new_list = []
				new_list.append(word)
				new_list.append(total)
				response_body[i].append(new_list)
		return self.linear_merge_helper(response_body)
			
	''' This method takes input as a list of sorted lists'''
	def linear_merge_helper(self, body):
		return heapq.merge(*body)
		
class MapHandler(web.RequestHandler):
	
	def initialize(self, dataStore, port):
		self.dataStore = dataStore
		self.MAPPER_IN_MEM_RESULT = self.dataStore.data
		self.port = port
	
	@gen.coroutine
	def get(self):
		mapperPath = self.get_argument("mapperPath",None)
		inputFile = self.get_argument("inputFile", None)
		numReducers = self.get_argument("numReducers", None)
		path = abspath(join(dirname(__file__), mapperPath))
		input_path = "-i %s" % inputFile
		numToHash = int(numReducers)
		p = subprocess.Popen([path, input_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		(out, err) = p.communicate()
		rc = p.returncode
		if err or rc!=0:
			logging.error("Mapper.py error: %s %s %s" %(path, input_path, err))
			logging.error("Error code: %d" %rc)
		else:
			unique_id = str(uuid.uuid4().hex)		
			#logging.info(type(out))	
			temp_output_list = json.loads(unicode(out,errors='ignore'))
			output_list = [item for item in temp_output_list if getKey(item)!=""]
			#output_list = json.loads(out)
			if unique_id in self.MAPPER_IN_MEM_RESULT:
				logging.error("Mapper task is in memeory %s" %unique_id)
			else:
				output_dict = {}
				for result in output_list:
					idx = hash(result[0])  % numToHash
					if idx not in output_dict:
						bucket_list = []
						bucket_list.append(result)
						output_dict[idx] = bucket_list
					else:
						bucket_list = output_dict[idx]
						bucket_list.append(result)
				self.MAPPER_IN_MEM_RESULT[unique_id] = output_dict
			# hash the key to correspongind bucket
			logging.info("Finish processing mapperID %s on port %d" % (unique_id, self.port))
			resp = {"status":"success", "mapTaskID":unique_id.strip()}
			self.write(json.dumps(resp))
			self.finish()
			
	
class RetrieveMapOutputHandler(web.RequestHandler):
	def initialize(self, dataStore):
		self.dataStore = dataStore
	
	def get(self):
		reducerIx = self.get_argument("reducerIx", None)
		mapTaskID = self.get_argument("mapTaskID", None)
		if mapTaskID not in self.dataStore.data:
			logging.error("The %s reducer % d try to fetch is not in memory" %(mapTaskID, reducerIx))
			sys.exit(2)
		reducerIx = int(reducerIx)
		resp = [[]]
		if reducerIx in self.dataStore.data[mapTaskID]:
			resp = self.dataStore.data[mapTaskID][reducerIx]
		self.write(json.dumps(resp))
		self.finish()


def makeWorker(index):
	port = WORKERS_PORT[index]
	myDataStore = MyDataStore()
	app = web.Application([web.url(r"/reduce", ReduceHandler),web.url(r"/map", MapHandler, dict(dataStore=myDataStore, port=port)),web.url(r"/retrieveMapOutput", RetrieveMapOutputHandler, dict(dataStore=myDataStore))])
	app.listen(port)
	logging.info("No. %d worker is listening on %d" % (index, port))
	

def main():
	taskID = process.fork_processes(MAX_WORKER)
	makeWorker(taskID)
	IOLoop.instance().start()
	
if __name__ == "__main__":
	main()
