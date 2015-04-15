import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import json
import hashlib
import urllib
import inventory
import glob
import argparse

class Runner(web.RequestHandler):
    def head(self):
        self.finish()

    @gen.coroutine
    def get(self):
        mapperPath = self.get_argument('mapperPath', None)
        reducerPath = self.get_argument('reducerPath', None)
        jobPath = self.get_argument('jobPath', None)
        numReducers = int(self.get_argument('numReducers', 2))
        if mapperPath is None or reducerPath is None or jobPath is None:
            self.write(json.dumps({"status": "error"}))
            self.finish()
            return


class Job:
    def __init__(self, mapper, reducer, numReducers, jobPath):
        self.mapper = mapper
        self.reducer = reducer
        self.numReducers = numReducers
        self.jobPath = jobPath

    def run(self):
        IOLoop.current().run_sync(self.runCoroutine)

    @gen.coroutine
    def runCoroutine(self):
        mapper = self.mapper
        reducer = self.reducer
        numReducers = self.numReducers
        jobPath = self.jobPath

        inputFiles = glob.glob(jobPath+"/*.in")
        numMappers = len(inputFiles)
        http = httpclient.AsyncHTTPClient()
        servers = inventory.servers['worker']
        futures = []
        for i, inputFile in enumerate(inputFiles):
            server = servers[i%len(servers)]
            params = urllib.urlencode({
                'mapperPath':mapper,
                'inputFile': inputFile,
                'numReducers':numReducers
                })
            url = "http://%s/map?%s" % (server,params)
            futures.append(http.fetch(url))
        responses = yield futures

        mapTaskIDs = []
        for r in responses:
            r = json.loads(r.body)
            status = r['status']
            assert status=="noinput" or status=="success"
            mapTaskIDs.append(r["mapTaskID"])

        futures = []
        for i in range(numReducers):
            server = servers[i%len(servers)]
            params = urllib.urlencode({
                'numMappers' : numMappers,
                'reducerIx' : i,
                'reducerPath' : reducer,
                'jobPath' : jobPath,
                'mapTaskIDs': ','.join(mapTaskIDs)
                })
            url = "http://%s/reduce?%s" % (server, params)
            futures.append(http.fetch(url))
        responses = yield futures
        for r in responses:
            status = json.loads(r.body)["status"]
            assert status == "success"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapperPath", required=True)
    parser.add_argument("--reducerPath", required=True)
    parser.add_argument("--jobPath", required=True)
    parser.add_argument("--numReducers", type=int, required=True)
    args = parser.parse_args()
    Job(mapper=args.mapperPath, 
        reducer=args.reducerPath, 
        numReducers=args.numReducers, 
        jobPath=args.jobPath).run()