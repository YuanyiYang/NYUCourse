#!/usr/bin/env python 

import tornado
from tornado.ioloop import IOLoop
from tornado import web, gen, process, httpserver, httpclient, netutil
import urllib
import sys, getopt
import logging
import os, os.path
import uuid
from nltk.tokenize import RegexpTokenizer
import json
from operator import itemgetter

logging.basicConfig(level=logging.INFO)

LOG_FILE = "/home/yy1112/sea-assignments/assignment4/wordcount/unicode_log.log"
my_logger = logging.getLogger('MyLogger')
my_logger.propagate = False
fh = logging.FileHandler(LOG_FILE, mode="w")
fh.setLevel(logging.DEBUG)
my_logger.addHandler(fh)

def main(argv):
	logging.info("Arguments list: %s" %str(sys.argv))
	input_path = ""
	try:
		opts, args = getopt.getopt(argv, "i:")
	except getopt.GetoptError:
		logging.error("python mapper.py -i <input_path>:")
		sys.exit(2)
	for opt, arg in opts:
		if opt=="-i":
			input_path = arg
			
	input_path = input_path.strip()	
	
	if not os.path.exists(input_path):
		logging.error("Input file: %s not exist" %input_path)
		sys.exit(2)
	
	input_file = open(input_path, 'r')
	'''
	# local combine
	result_dict = {}
	for line in input_file:
		tokens = processLine(line)
		for token in tokens:
			if token in result_dict:
				result_dict[token] = result_dict[token]+1
			else:
				result_dict[token] = 1
	result_list = []
	for key, value in result_dict.iteritems():
		temp = []
		temp.append(key)
		temp.append(value)
		result_list.append(temp)
	sorted(result_list)
	'''
	result_list = []
	for line in input_file:
		tokens = processLine(line)
		for token in tokens:
			temp = []
			temp.append(token)
			temp.append(1)
			result_list.append(temp)
	result_list.sort(key=itemgetter(0))
	input_file.close()
	#logging.info("Mapper: len of result_list %d" % len(result_list))
	#for result in result_list:
	#	my_logger.info(result)
	#print json.dumps(result_list) 
	print json.dumps(result_list, ensure_ascii=False) 
	
def processLine(line):
	line = line.strip()
	line = line.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(line)
	return tokens

if __name__ == "__main__":
	main(sys.argv[1:])
	
#for line in sys.stdin:
#		words = line.strip().split()
#		for word in words:
#			print '%s\t%s' % (word, 1)
