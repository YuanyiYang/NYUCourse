#!/use/bin/env python

import sys
import pickle
import json
import nltk
from nltk.corpus import stopwords
from collections import *
from bs4 import BeautifulSoup 

TITLE_BONUS = 50
REMOVE_PUNCT_MAP = dict((ord(char), None) for char in "=[]\\")
UGLY_TEXT_MAP = dict((ord(char), ord(" ")) for char in "|=[]{}*\\#")
stop = stopwords.words('english')

doc_to_content = pickle.load(sys.stdin)

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

for docID in doc_to_content:
	title = doc_to_content[docID]['title']
	docBody = doc_to_content[docID]['docBody']
	title = cleanText(title)
	docBody = cleanText(docBody)
	tf = getCounter(title, docBody)
	for term in tf.keys():
		result_list = []
		result_list.append(term)
		result_list.append(tf[term])
		print "%s\t%s" % (docID, json.dumps(result_list))


