import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import inventory
import pickle
import logging
import hashlib
import getpass
import urllib
from collections import *
import json
import mapper
import reducer
import coordinator

def main():
	numProcs = inventory.NUM_WORKERS
	taskID = process.fork_processes(numProcs, max_restarts=0)
	port = inventory.BASE_PORT + taskID
	app = httpserver.HTTPServer(web.Application([
		web.url(r"/map", mapper.Map),
		web.url(r"/retrieveMapOutput", mapper.RetrieveMapOutput),			
		web.url(r"/reduce", reducer.Reduce),
		web.url(r"/retrieveReduceOutput", reducer.RetrieveReduceOutput),
		web.url(r"/coordinator", coordinator.Runner)]))
	logging.info("Worker %d listening on %d" % (taskID, port))

	app.add_sockets(netutil.bind_sockets(port))
	IOLoop.current().start()

if __name__ == "__main__":
	logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
	main()
