import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import logging
import socket
import hashlib
import getpass

# Pick a base port based on username
MAX_PORT = 49152
MIN_PORT = 10000
BASE_PORT = int(hashlib.md5(getpass.getuser()).hexdigest()[:8], 16) % \
    (MAX_PORT - MIN_PORT) + MIN_PORT

# Static backend configuration
NUM_BACKENDS = 3
BACKENDS = [socket.gethostname() + ":" + str(BASE_PORT + i + 1) for i in range(NUM_BACKENDS)]

# Frontend
class FrontendHandler(web.RequestHandler):
    nextBackendIx = 0 # class-scope variable

    @gen.coroutine
    def get(self):
        http = httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://" + BACKENDS[self.nextBackendIx])
        if response.error: raise web.HTTPError(500)
        FrontendHandler.nextBackendIx += 1
        FrontendHandler.nextBackendIx %= len(BACKENDS)
        self.write(response.body)
        self.finish()

def makeFrontend():
    return web.Application([
            web.url(r"/", FrontendHandler),
        ])

# Backend
class BackendHandler(web.RequestHandler):
    def initialize(self, port):
        self.port = port

    def get(self):
        self.write(socket.gethostname() + ":" + str(self.port))

def makeBackend(port):
    return web.Application([
            web.url(r"/", BackendHandler, dict(port=port)),
        ])

def main(): 
    taskID = process.fork_processes(4)
    if taskID == 0:
        app = httpserver.HTTPServer(makeFrontend())
        app.add_sockets(netutil.bind_sockets(BASE_PORT))
        logging.info("Front end is listening on " + str(BASE_PORT))
    else:
        port = BASE_PORT + taskID
        app = httpserver.HTTPServer(makeBackend(port))
        app.add_sockets(netutil.bind_sockets(port))
        logging.info("Back end %d listening on %d" % (taskID, port))
    IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    main()
