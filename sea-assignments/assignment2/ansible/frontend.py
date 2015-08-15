import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import logging
import socket
import json

FRONTEND_PORT=80
BACKENDS = json.load(open("config.json", "r"))["backends"]

class FrontendHandler(web.RequestHandler):
    nextBackendIx = 0

    @gen.coroutine
    def get(self):
        http = httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://" + BACKENDS[self.nextBackendIx] + ":8080" ) 
        if response.error:
            raise web.HTTPError(500)
        FrontendHandler.nextBackendIx += 1
        FrontendHandler.nextBackendIx %= len(BACKENDS)
        self.write(response.body)
        self.finish()

def makeFrontend():
    return web.Application([
            web.url(r"/", FrontendHandler),
        ])


def main():
    for back in BACKENDS:
        print back
    app = httpserver.HTTPServer(makeFrontend())
    app.add_sockets(netutil.bind_sockets(FRONTEND_PORT))
    logging.info("Front end is listening on " + str(FRONTEND_PORT))
    IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    main()
