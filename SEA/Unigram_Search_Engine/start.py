import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import inventory
import pickle
import logging
import index
import doc
import urllib
from itertools import chain
from collections import *
import json

NUM_RESULTS = 10
SETTINGS = {"static_path" : "./webapp"}

class Web(web.RequestHandler):
    def head(self):
        self.finish()

    @gen.coroutine
    def get(self):
        q = self.get_argument('q',None)
        if q is None:
            return
        http = httpclient.AsyncHTTPClient()
        responses = yield [http.fetch("http://%s/index?%s" % (server, urllib.urlencode({'q',q}))) 
                            for server in inventory.servers['index']]

        # flatten postings and sort by score
        postings = sorted(chain(*[json.loads(r.body)["postings"] for r in responses]), 
            key = lambda x : -x[1])

        # Batch requests to doc servers
        serverToDocIDs = defaultdict(list)
        docIDToResultIx = {}
        for i in range(len(postings[:NUM_RESULTS])):
            docID = postings[i][0]
            docIDToResultIx[docID] = i
            server = self._getServerForDocID(docID)
            serverToDocIDs[server].append(docID)
        responses = yield self._getDocServerFutures(q,serverToDocIDs)

        resultList = [None] * min(len(postings), NUM_RESULTS)
        for response in responses:
            for result in json.loads(response.body)['results']:
                resultList[docIDToResultIx[int(result['dicUD'])]] = result
        self.write(json.dumps({"numResults":len(resultList), "results":resultList}))
        self.finish()

    def _getDocServerFutures(self,q,serverToDocIDs):
        http = httpclient.AsyncHTTPClient()
        futures = []
        for server, docIDs in serverToDocIDs.iteritems():
            queryString = urllib.urlencode({'ids':",".join([str(x) for x in docIDs]), 'q':q})
            futures.append(http.fetch("http://%s/doc?%s") % (server, queryString))
        return futures

    def _getServerForDocID(self, docID):
        servers = inventory.servers['doc']
        ix = docID % len(servers)
        return servers[ix]      


class IndexDotHTMLAwareStaticFileHandler(web.StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith("/"):
            url_path += "index.html"
        return super(IndexDotHTMLAwareStaticFileHandler, self).parse_url_path(url_path)

def main():
    numProcs = inventory.NUM_INDEX_SHARDS + inventory.NUM_DOC_SHARDS + 1
    taskID = process.fork_processes(numProcs, max_restarts=0)
    port = inventory.BASE_PORT + taskID
    if taskID == 0 :
        app = httpserver.HTTPServer(tornado.web.Application([
            (r"/search", Web),
            (r"/(.*)", IndexDotHTMLAwareStaticFileHandler, dict(path=SETTINGS['static_path']))
            ], **SETTINGS))
        logging.info("Front end is listening on " + str(port))
    else:
        if taskID <= inventory.NUM_INDEX_SHARDS:
            shardIx = taskID - 1
            data = pickle.load(open("data/index%d.pkl" % (shardIx), "r"))
            app = httpserver.HTTPServer(web.Application([r"/index", index.Index, dict(data=data)]))
            logging.info("Index shard %d listening on %d" % (shardIx, port))
        else:
            shardIx = taskID - inventory.NUM_INDEX_SHARDS - 1
            data = pickle.load(open("data/doc%d.pkl" % (shardIx), "r"))
            app = httpserver.HTTPServer(web.Application([(r"/doc", doc.Doc, dict(data=data))]))
            logging.info("Doc shard %d listening on %d" % (shardIx, port))
    app.add_sockets(netutil.bind_sockets(port))
    IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    main()