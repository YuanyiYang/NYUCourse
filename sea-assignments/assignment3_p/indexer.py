from xml.dom import minidom
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import inventory
import pickle
from collections import *
import math
import sys
import os

TITLE_BONUS = 50

REMOVE_PUNCT_MAP = dict((ord(char), None) for char in "=[]\\")
UGLY_TEXT_MAP = dict((ord(char), ord(" ")) for char in "|=[]{}*\\#")

def cleanText(text):
	text = BeautifulSoup(text).get_text()
	text = text.translate(UGLY_TEXT_MAP)
	text = text.replace("'''", '"')
	return text

def getCounter(title, text):
	chunk = " ".join([title] * TITLE_BONUS) + " " + text
	noPunctChunk = chunk.translate(REMOVE_PUNCT_MAP)
	termList = nltk.word_tokenize(noPunctChunk)
	termList = [word.lower() for word in termList if word.lower() not in stop]
	return Counter(termList)

if __name__ == "__main__":
	filename = sys.argv[1]
	stop = stopwords.words('english')
	xmldoc = minidom.parse(filename)
	docList = xmldoc.getElementsByTagName('page')

	indexShards = [defaultdict(list) for i in range(inventory.NUM_INDEX_SHARDS)]
	docShards = [defaultdict(dict) for i in range(inventory.NUM_DOC_SHARDS)]
	df = defaultdict(int)
	for docID in range(len(docList)):
		page = docList[docID]
		title = page.getElementsByTagName('title')[0].childNodes[0].nodeValue
		if title.startswith("Category:"):
			continue
		text = cleanText(page.getElementsByTagName('text')[0].childNodes[0].nodeValue)
		tf = getCounter(title, text)

		docShards[docID % len(docShards)][docID] = (title, text)
		for term in tf.keys():
			indexShards[docID % len(indexShards)][term].append((docID, tf[term]))
			df[term] += 1

	logIDF = defaultdict(float)
	for term in df.keys():
		logIDF[term] = math.log(len(docList) / float(df[term]))

	if not os.path.exists("data/"):
		os.makedirs("data/")		
	for ix, indexShard in enumerate(indexShards):
		pickle.dump((indexShards[ix], logIDF), open("data/index%d.pkl" % (ix), "w"))
	for ix, docShard in enumerate(docShards):
		pickle.dump(docShards[ix], open("data/doc%d.pkl" % (ix), "w"))
