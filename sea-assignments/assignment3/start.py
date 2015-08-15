import tornado
from tornado.ioloop import IOLoop 
from tornado import web, gen, httpserver, httpclient, netutil, process
import logging
import socket
import json
import heapq
import pickle
import sys, random
import numpy
from nltk.stem.porter import * 

FRONT_END = 25800
#BASE_INDEX = 35315
BASE_INDEX = 25801
BASE_DOC = 25804
#BASE_DOC = 35318
NUM_BACKENDS = 3
INDEX_PREFIX = "Index"
DOC_PREFIX = "doc_index"

INDEX_SERVERS = ["http://" + socket.gethostname() + ":" + str(BASE_INDEX+i) for i in range(NUM_BACKENDS)]
DOC_SERVERS = ["http://" + socket.gethostname() + ":" + str(BASE_DOC+i) for i in range(NUM_BACKENDS)]

stemmer = PorterStemmer()

def makefrontend():
	application = web.Application([
	        (r"/search", FrontendHandler),
	        (r"/js/(.+)", JSHandler),
	        (r"/", StaticPageHandler),
	    ])
	application.listen(FRONT_END)
	logging.info("Front end is listening on %d" % FRONT_END)

class FrontendHandler(web.RequestHandler):
    # parallelism coroutine
    @gen.coroutine
    def get(self):
        query = self.get_argument("q", None)
        http = httpclient.AsyncHTTPClient()
        responses = yield [http.fetch(url + "/index?q=" + query) for url in INDEX_SERVERS]
        bodies = [response.body for response in responses]
        # use of min heap
        # print bodies
        h = [] 
        for body in bodies:
            body = json.loads(body)
            for postingList in body["postings"]:
                if len(h) >= 10:
                    heapq.heapreplace(h, (postingList[1], postingList[0]))
                else:
                    heapq.heappush(h, (postingList[1], postingList[0]))
        #print h
        ordered = [heapq.heappop(h) for i in range(len(h))]
        ordered.sort(key=lambda tup:tup[0], reverse=True)
        frontend_body = []
        for score_docid_tuple in ordered:
            docId = score_docid_tuple[1]
            docServerPortIndex = docId % 3;
            #print type(docId)
            #print "index %s" % type(docServerPortIndex)
            docServer_url = DOC_SERVERS[docServerPortIndex] + "/doc?id=" + str(docId) + "&q=" + query
            #print docServer_url
            response = yield http.fetch(docServer_url)
            response_body = json.loads(response.body)
            frontend_body.extend(response_body["results"])
        frontend_response_body = {}
        frontend_response_body["numResults"] = len(frontend_body)
        frontend_response_body["results"] = frontend_body
        print "server writing back"
        self.write(json.dumps(frontend_response_body))
        self.finish()

class StaticPageHandler(web.RequestHandler):
    def get(self):
        f = open("index.html","r")
        self.write(f.read())
        f.close()
        self.finish()

class JSHandler(web.RequestHandler):
    def get(self, word=None):
        file_name = "js/" + word
        #print file_name
        f = open(file_name,"r")
        self.write(f.read())
        f.close()
        self.finish()

def makeIndexer(indexPos):
	app = web.Application([
	    (r"/index", IndexServer, dict(indexPos=indexPos)),
	])
	app.listen(BASE_INDEX + indexPos)
	logging.info("Indexer end %d listen on %d" % (indexPos, BASE_INDEX + indexPos))
	
	
class IndexServer(web.RequestHandler):
	
	postingList = {}  #  term : postingList[ list of DocID ]
	
	def initialize(self, indexPos):
		self.port = BASE_INDEX + indexPos;
		file_name = INDEX_PREFIX + str(indexPos) + ".idx"
		self.load_index = pickle.load(open(file_name, "rb"))
		self.dictionary = self.load_index["Dictionary"]
		self.IDF = self.load_index["IDF"]
	
	def get(self):
		query = self.get_argument("q", None)
		pre_terms = query.split()
		terms = []
		for term in pre_terms:
			term = stemmer.stem(term)
			terms.append(term)
		docId = self.nextDoc(terms, -1)
		doc_results = []
		postings = []
		query_vector = []
		for term in terms:
			query_vector.append(self.IDF[term])
		while docId!=sys.maxint:
			doc_results.append(docId)
			docId = self.nextDoc(terms, docId)
		for docId in doc_results:
			doc_vector = []
			for term in terms:
				termFreq = self.load_index[term][docId]
				TFIDF = termFreq * self.IDF[term]
				doc_vector.append(TFIDF)
			doc_score = self.computeScore(query_vector, doc_vector)
			result = []
			result.append(docId)
			#print type(docId)
			result.append(doc_score)
			postings.append(result)
		final_result = {}
		final_result["postings"] = postings
		self.write(json.dumps(final_result))
		self.finish()
			
	
	def computeScore(self, query_vector, doc_vector):
		return numpy.inner(query_vector, doc_vector)
				
	def nextDoc(self, terms, docID):
		results = {}
		for term in terms:
			if term not in self.dictionary:
				return sys.maxint
			this_term_next_DocID = self.next(term, docID)
			if this_term_next_DocID == sys.maxint:
			    return sys.maxint
			results[term] = this_term_next_DocID
		maxDocId = results[random.choice(results.keys())]
		hit = True
		for term in results:
			if maxDocId!=results[term]:
				hit = False
				maxDocId = max(maxDocId, results[term])
		if hit:
			return maxDocId
		else:
			return self.nextDoc(terms, maxDocId-1)
		
					
	def next(self, term, currentDocId):
		if term not in self.postingList:
			pList = list(self.load_index[term].keys())
			pList.sort()
			self.postingList[term] = pList
		pList = self.postingList[term]
		if pList[-1] <= currentDocId:
			return sys.maxint
		if pList[0] > currentDocId:
			return pList[0]
		low = 0;
		jump = 1;
		high = low + jump;
		while high<len(pList) and pList[high]<=currentDocId:
			low = high + 1
			jump *= 2
			high = low + jump
		if high >= len(pList):
			high = len(pList) - 1
		offset = self.binarySearch(pList,low,high,currentDocId)
		return pList[offset]
	
	def binarySearch(self, pList, low, high, currentDocId):
		if pList[low] > currentDocId:
			return low
		mid = 0
		while(low<=high):
			mid = (low+high)/2
			if(pList[mid]==currentDocId):
				return mid+1
			elif(pList[mid]<currentDocId):
				low = mid + 1
			else:
				high = mid - 1
		return (high+low)/2 + 1		

def makeDocEnd(indexPos):
	app = web.Application([
	    (r"/doc", DocServer, dict(indexPos=indexPos)),
	])
	app.listen(BASE_DOC + indexPos)
	logging.info("DocServer end %d listen on %d" % (indexPos, BASE_DOC + indexPos))
	        
class DocServer(web.RequestHandler):
    snippet_size = 25
    def initialize(self, indexPos):
		self.indexPos = indexPos
		file_name = DOC_PREFIX + str(indexPos) + ".idx"
		self.load_index = pickle.load(open(file_name, "rb"))
		
    def get(self):
		query = self.get_argument("q", None)
		docID = self.get_argument("id", None)
		docID = int(docID)
		result = {}
		results = {}
		results["results"] = []	
		url = self.load_index[docID]["URL"]
		title = self.load_index[docID]["title"]
		docBody = self.load_index[docID]["docBody"]
		result["url"] = url
		result["docID"] = docID
		result["title"] = title
		term_pos = docBody.find(query)
		result["snippet"] = docBody[term_pos-self.snippet_size:term_pos+self.snippet_size]
		result["snippet"] = result["snippet"].replace(query, "<strong>" + query + "</strong>")
		results["results"].append(result)
		print "doc server writing back"
		self.write(json.dumps(results))
		self.finish()
        
def main():
	taskID = process.fork_processes(7)
	if taskID == 6:
		makefrontend()
	elif taskID<=2:
		#makeIndexer(taskID)	
		makeDocEnd(taskID)
	else:
		makeIndexer(taskID-3)		
	IOLoop.instance().start()
	
if __name__ == "__main__":
	main()
