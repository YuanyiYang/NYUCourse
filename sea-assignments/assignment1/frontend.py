import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import logging
import socket

FRONTEND_PORT=80

class FrontendHandler(web.RequestHandler):
    
    @gen.coroutine
    def get(self):
        http = httpclient.AsyncHTTPClient()
        response = yield http.fetch("/")  # new url here 
        if response.error:
            raise web.HTTPError(500)
        self.write(response.body)
        self.finish()

def makeFrontend():
    return web.Application([
            web.url(r"/", FrontendHandler),
        ])


def main():
    app = httpserver.HTTPServer(makeFrontend())
    app.add_sockets(netutil.bind_sockets(FRONTEND_PORT))
    logging.info("Front end is listening on " + str(FRONTEND_PORT))
    IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    main()