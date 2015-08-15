from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
import socket
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

count = 0

class GenAsyncHandler(RequestHandler):

	def initialize(self, port):
		self.port = port

	@gen.coroutine
	def get(self):
		global count 
		http_client = AsyncHTTPClient()
		redirect_url = "http://" + socket.gethostname() + ":" + str(self.port+1+(count%3))
		count = count + 1
		response = yield http_client.fetch(redirect_url)
		self.write(response.body)

class FirstHandler(RequestHandler):
	def initialize(self, port):
		self.port = port
	
	def get(self):
		new_url = "http://" + socket.gethostname() + ":" + str(self.port)
		self.write(new_url)
		self.write("<br/>")		
		self.flush()		
	

class SecondHandler(RequestHandler):
	def initialize(self, port):
		self.port = port

	def get(self):
		new_url = "http://" + socket.gethostname() + ":" + str(self.port)
		self.write(new_url)
		self.write("<br/>")		
		self.flush()

class ThirdHandler(RequestHandler):
	def initialize(self, port):
		self.port = port

	def get(self):
		new_url = "http://" + socket.gethostname() + ":" + str(self.port)
		self.write(new_url)
		self.write("<br/>")		
		self.flush()

if __name__ == "__main__":
	application1 = Application([(r"/",FirstHandler,dict(port=25802)),])
	application1.listen(25802)
	app2 = Application([url(r"/", SecondHandler, dict(port=25803)),])
	app2.listen(25803)
	app3 = Application([url(r"/", ThirdHandler, dict(port=25804)),])
	app3.listen(25804)
	loadBalancer = Application([(r"/", GenAsyncHandler, dict(port=25801)),])
	loadBalancer.listen(25801)
	IOLoop.instance().start()
