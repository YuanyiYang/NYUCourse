#!/usr/bin/env python 
import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import sys, getopt
import logging
import os
import workers
import urllib
import json

logging.basicConfig(level=logging.INFO)

MAX_WORKER = workers.MAX_WORKER
WORKERS_PORT = workers.WORKERS_PORT 

BASE_URL = "http://linserv2.cims.nyu.edu:"
# since base_port has working listen on it, for simplification use one less port
MY_BASE_PORT = workers.MY_BASE_PORT
COOR_BASE_PORT = MY_BASE_PORT - 1

class CoordinatorHandler(web.RequestHandler):
	
	def initialize(self,mapperPath, reducerPath, jobPath, numReducers):
		self.mapperPath = mapperPath
		self.reducerPath = reducerPath
		self.jobPath = jobPath
		self.numReducers = numReducers
		
	@gen.coroutine
	def get(self):
		logging.info("New Job begin!---------------------------------")
		self.mapperPath = self.get_argument("mapperPath", None)
		self.reducerPath = self.get_argument("reducerPath", None)
		self.jobPath = self.get_argument("jobPath", None)
		self.numReducers = int(self.get_argument("numReducers", None))
		'''
		if not mapperPath:
			self.mapperPath = mapperPath
		if not reducerPath:
			self.reducerPath = reducerPath
		if not jobPath:
			self.jobPath = jobPath
		if not numReducers:
			self.numReducers = int(numReducers)
		'''
		# all required parameters are stored in the instance field of this obj
		
		# get all input file ends with '.in' under current directory
		working_dir = os.getcwd()
		filename_list = []
		for root, dirs, files in os.walk(working_dir):
			for file in files:
				if file.endswith(".in"):
					file_path = os.path.join(root,file)
					filename_list.append(file_path)
			
		# handle mapper route
		num_supposed_mapper = len(filename_list)
		map_worker_list = []   
		if MAX_WORKER < num_supposed_mapper:
			n = num_supposed_mapper / MAX_WORKER
			m = num_supposed_mapper % MAX_WORKER
			map_worker_list = WORKERS_PORT * n
			map_worker_list.extend(WORKERS_PORT[:m])				
		else:
			map_worker_list = WORKERS_PORT[:num_supposed_mapper]
		http = httpclient.AsyncHTTPClient()
		futures = []
		for idx, file_path in enumerate(filename_list):
			assigned_port = map_worker_list[idx]
			params = urllib.urlencode({
				'mapperPath' : self.mapperPath,
				'inputFile': file_path,
				'numReducers' : self.numReducers
			})
			url = "%s%d/map?%s" % (BASE_URL, assigned_port, params)
			logging.debug("Coordinator: Sending %s to mapper %d with %d reducers" %(file_path, assigned_port, self.numReducers))
			logging.debug("Fetch url: %s" % url)
			futures.append(http.fetch(url))
		responses = yield futures
		
		# check whether all mapper has finish
		mapper_task_ids = []
		for response in responses:
			response_body = json.loads(response.body)
			# if one mapper fails. simply quit the program
			if "status" not in response_body or "success" != response_body['status']:
				logging.error("Error response from mapper %s" % json.dumps(response_body))
				sys.exit(2)
			mapper_task_ids.append(response_body['mapTaskID'])
		logging.info("Coordinator: fetching %d(should equal to num of mappers) responses" % len(mapper_task_ids))
		
		# handle reducer
		final_mapper_result = ",".join(mapper_task_ids)
		reducer_port_idx = []
		if MAX_WORKER >= self.numReducers:
			reducer_port_idx = WORKERS_PORT[:self.numReducers]
		else:
			n = self.numReducers / MAX_WORKER
			m = self.numReducers % MAX_WORKER
			reducer_port_idx = WORKERS_PORT * n
			reducer_port_idx.extend(WORKERS_PORT[:m])	
		http = httpclient.AsyncHTTPClient()
		futures = []
		for idx, port_num in enumerate(reducer_port_idx):
			assigned_port = port_num
			params = urllib.urlencode({
				'reducerIx' : idx,
				'reducerPath': self.reducerPath,
				'mapTaskIDs' : final_mapper_result,
				'jobPath' : self.jobPath
			})
			url = "%s%d/reduce?%s" % (BASE_URL, assigned_port, params)
			logging.info("Coordinator: reducer % d(on port %d) fetch all mapperTaskID output to %s" %(idx,assigned_port,self.jobPath))
			futures.append(http.fetch(url))
		responses = yield futures
		
		# produce final output
		for response in responses:
			body = json.loads(response.body)
			if "status" not in body or "success" != body['status']:
				logging.error("Error response from reducer %s" % json.dumps(body))
				sys.exit(2)
			response_body = ""
			working_dir = os.getcwd()
			directory_path = os.path.join(os.getcwd(), self.jobPath)
			for i in range(self.numReducers):
				output_file = str(i) + ".out"
				file_path = os.path.join(directory_path, output_file)
				if not os.path.exists(file_path):
					logging.error("Missing reducer output %s" % file_path)
					sys.exit(2)
				else:
					f = open(file_path, 'r')
					response_body += file_path + "<br/>"
					for line in f:
						line += "<br/>"
						response_body += line 
					f.close()
		self.write(response_body)
		logging.info("MapReduce has finished, system exiting......")
		self.finish()

def main(mapperPath, reducerPath, jobPath, numReducers):
	app = web.Application([web.url(r"/coordinator", CoordinatorHandler, dict(mapperPath=mapperPath, reducerPath=reducerPath, jobPath=jobPath, numReducers=numReducers))])
	app.listen(COOR_BASE_PORT)
	logging.info("Coordinator handler is listening on %d" % COOR_BASE_PORT )
	IOLoop.instance().start()


if __name__ == "__main__":
	#logging.info("Arguments list: %s" %str(sys.argv))
	argv = sys.argv[1:]
	mapperPath = ""
	reducerPath = ""
	jobPath = ""
	numReducers = ""
	try:
		opts, args = getopt.getopt(argv, "m:r:j:n:", ["mapperPath=", "reducerPath=", "jobPath=", "numReducers="])
	except getopt.GetoptError:
		logging.error("python coordinator.py --mapperPath=<mapper_path> --reducerPath=<reducer_path> --jobPath=<job_path> --numReducers=<num>")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-m","--mapperPath"):
			mapperPath = arg
			mapperPath = mapperPath.strip()
		elif opt in ("-r", "--reducerPath"):
			reducerPath = arg
			reducerPath = reducerPath.strip()
		elif opt in ("-j", "--jobPath"):
			jobPath = arg
			jobPath = jobPath.strip()
		elif opt in ("-n", "--numReducers"):
			numReducers = arg
			numReducers = int(numReducers.strip())
	main(mapperPath, reducerPath, jobPath, numReducers)
