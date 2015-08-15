from bs4 import BeautifulSoup
import codecs
from nltk.stem.porter import * 
from nltk.tokenize import RegexpTokenizer
import pickle
import math
import os, errno
    
def main():
    f = codecs.open("info_ret.xml", encoding="utf-8")
    xml_soup = BeautifulSoup(f, "xml")
    docID = 0
    IndexServerSize = 3
    DocServerSize = 3
    allPages = xml_soup.find_all("page")
    term_IDF = {}
    #print(len(allPages))
    #index = {term: {docID: TF}, IDF: term_IDF, Dictionary: Set}
    docIndexes = [ {} for i in range(DocServerSize)]
    # docIndex = { docID : {title:XXX, url:XXX, docBody:XXX}}
    invertedIndexes = [ {} for i in range(IndexServerSize)]
    stemmer = PorterStemmer()
    for page in allPages:
        serverIndex = docID % IndexServerSize
        docServerIndex = docID % DocServerSize
        index = invertedIndexes[serverIndex]
        docIndex = docIndexes[docServerIndex]
        title = page.title.string
        #print type(page)
        #print type(page.text)
        #print type(page.find("text"))
        bodies = page.find("text").string
        docIndex[docID] = {}
        docIndex[docID]["title"] = unicode(title)
        docIndex[docID]['URL'] = unicode(title)
        docIndex[docID]['docBody'] = unicode(bodies)
        removePunc = preprocess(bodies)
        for word in removePunc.split():
			word = stemmer.stem(word)
			if word not in term_IDF:
				term_IDF[word] = 1
			if word not in index:
				index[word] = {}
			postingList_map = index[word]
			if docID not in postingList_map:
				postingList_map[docID] = 1
			else:
				postingList_map[docID] += 1
			index[word] = postingList_map
		# give high weight for word in title
        for word in unicode(title).split():
			word = stemmer.stem(word)
			if word not in term_IDF:
				term_IDF[word] = 1
			if word not in index:
				index[word] = {}
			postingList_map = index[word]
			if docID not in postingList_map:
				postingList_map[docID] = 50
			else:
				postingList_map[docID] += 50
			index[word] = postingList_map
        docID += 1
        
    for term, IDF in term_IDF.iteritems():
		DF = float(0)
		for index in invertedIndexes:
			if term in index:
				DF += len(index[term])
		IDF = math.log((docID+1)/DF)
		term_IDF[term] = IDF
		
    for index in invertedIndexes:
		index["IDF"] = term_IDF
		index["Dictionary"] = set(term_IDF.keys())
		
    for i in range(len(invertedIndexes)):
		file_name = "Index" + str(i) + ".idx"
		slientRemove(file_name)
		pickle.dump(invertedIndexes[i],open(file_name,"wb"))
		print "Dump to " + file_name
	
    for i in range(len(docIndexes)):
		file_name = "doc_index" + str(i) + ".idx"
		slientRemove(file_name)
		pickle.dump(docIndexes[i], open(file_name, "wb"))
		print "Dump Doc Index to %s" % file_name

def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	return " ".join(tokens)
	
def slientRemove(path):
	try:
		os.remove(path)
		print "Remove " + path
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

if __name__ == "__main__":
    main()
