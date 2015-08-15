import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import json
import uuid
import logging
logging.basicConfig(level=logging.INFO)
BASE_URL = "http://linserv2.cims.nyu.edu:"

class dataStore():
	def __init__(self):
		self.data = {}

class testHandler(web.RequestHandler):
	
	class_wide = str(uuid.uuid4().hex)
	
	def initialize(self,data):
		self.data = data
		logging.info("init testHandler")

	def get(self):
		self.instance_wide = str(uuid.uuid4().hex)
		resp = {}
		resp['class'] = testHandler.class_wide
		resp['instance'] = self.instance_wide
		self.data.data = resp
		logging.info(json.dumps(resp))
			
class getDataHandler(web.RequestHandler):
	def initialize(self, data):
		self.data = data
		logging.info("init getDataHandler")
	def get(self):
		#logging.info(json.dumps(self.data.data))
		self.write(json.dumps(self.data.data))
		self.finish()
		
class retrieveHandler(web.RequestHandler):
		
	@gen.coroutine
	def get(self):
		http = httpclient.AsyncHTTPClient()
		futures = []
		for i in range(5):
			url = "%s%d/test" % (BASE_URL,25800+i)
			logging.info("Fetching %s" % url)
			futures.append(http.fetch(url))
		futures = []
		for i in range(5):
			url = "%s%d/result" % (BASE_URL,25800+i)
			logging.info("Fetching %s" % url)
			futures.append(http.fetch(url))
		responses = yield futures
		result = {}
		for idx,resp in enumerate(responses):
			result[idx] = json.loads(resp.body)
		self.write(json.dumps(result))
		self.finish()

def makeEnd(index):
	port = 25800 + index
	data = dataStore()
	app = web.Application([web.url(r"/test", testHandler, dict(data=data)),web.url(r"/result", getDataHandler, dict(data=data)), web.url(r"/rrrr", retrieveHandler)])
	app.listen(port)
	logging.info("No. %d worker is listening on %d" % (index, port))


if __name__ == "__main__":
	taskID = process.fork_processes(5)
	makeEnd(taskID)
	IOLoop.instance().start()
	
	
