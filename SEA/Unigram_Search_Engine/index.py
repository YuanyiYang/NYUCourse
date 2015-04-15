import os
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_DYNAMIC'] = 'FALSE'
import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import json
import urlparse
import urllib
from collections import defaultdict
import numpy as np
from sklearn.metrics.pairwise import linear_kernel

class Index(web.RequestHandler):
    def initialize(self, data):
        self._postingsList, self._logIDF = data

    def head(self):
        self.finish()

    def get(self):
        query = self.get_argument('q', None)
        if query is None:
            return
        queryTerms = query.split()
        # let's say we have N documents and M terms in query
        # Apparently we assume unique term in query
        # queryVector is a 1 * M dimension array
        queryVector = np.array([self._logIDF[term] for term in queryTerms])
        # docVectoDict is a N * M vector, with default value np.array([0] * M)
        docVectorDict = defaultdict(lambda: np.array([0]*len(queryTerms)))

        for i in range(len(queryTerms)):
            term = queryTerms[i].lower()
            newList = self._postingsList[term]
            for item in newList:  # newList is [(docID,tf)]
                docVectorDict[item[0]][i] = item[1] * self._logIDF[term]
        docMatrix = np.zeros((len(docVectoDict)), len(queryTerms)))
        docIx = 0
        docIxToDocID = {}
        for docID in docVectorDict.keys():
            docMatrix[docIx][:] = docVectorDict[docID][:]
            docIxToDocID[docIx] = docID
            docIx += 1
        # linear_kernel is used to compute the similarity
        sims = linear_kernel(queryVector,docMatrix).flatten()
        # argsort return the index 
        bestDocIxes = sims.argsort()[::-1]
        bestDocSims = sims[bestDocIxes]
        bestDocIDs = [docIxToDocID[docIx] for docIx in bestDocIxes]
        postings = zip(bestDocIDs, bestDocSims)
        self.write(json.dumps({"postings":postings}))


