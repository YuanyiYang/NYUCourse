import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import json
import urlparse
import urllib
from collections import defaultdict
import cgi
import nltk
import string
import re
import indexer

class Doc(web.RequestHandler):	
	def initialize(self, data):
		self._documents = data

	def head(self):
		self.finish()

	def get(self):
		did = self.get_argument('id', None)
		if did is not None:
			dids = did
		else:
			dids = self.get_argument('ids', None)
		dq = self.get_argument('q', None)
		if dids is None or dq is None:
			return	
		docIDs = dids.split(',')
		query = unicode(dq)
		results = []
		for docID in docIDs:
			docData = self._documents[int(docID)]
			title = docData[0]
			text = docData[1]				
			result = {'docID': docID, 
				'title': title, 
				'url': self._getURLFromTitle(title), 
				'snippet': self._getSnippet(text, query)}
			results.append(result)
		self.write(json.dumps({"results": results}))		

	def _getSnippet(self, text, query):
		originalText = text
		lowerText = text.lower()
		if query in lowerText:
			term = query
		else:
			term = None
			for pot in query.split():
				if pot in lowerText:
					term = pot
			if term is None: return "..."
		termStart = lowerText.find(term)
		termStop = termStart + len(term)
		asIs = text[termStart:termStop]
		text = text.replace(asIs, "<strong>" + asIs + "</strong>")
		start = max(0, termStart - 200)
		start = text.find(" ", start)
		stop = min(len(text), termStart + len(term) + 200)
		stop = text.rfind(" ", start, stop) + 1
		ret = text[start:stop]
		if start > 0:
			ret = "..." + ret
		if stop < len(text):
			ret = ret + "..."
		return ret
	
	def _getURLFromTitle(self, title):
		return "http://en.wikipedia.org/wiki/" + title.replace(" ", "_")
		
