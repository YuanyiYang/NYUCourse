import tornado
from tornado.ioloop import IOLoop
from tornado import web, httpserver, httpclient, netutil
import logging
import socket

BACKEND_PORT = 8080

class BackendHandler(web.RequestHandler):

    def get(self):
        self.write(socket.gethostname() + ":" + str(self.port))


def makeBackend():
    return web.Application([
            web.url(r"/", BackendHandler),
        ])

def main():
    app = httpserver.HTTPServer(makeBackend())
    app.add_sockets(netutil.bind_sockets(BACKEND_PORT))
    logging.info("Back end listening on %d" % BACKEND_PORT)
    IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    main()