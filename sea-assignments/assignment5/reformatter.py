#!/usr/bin/env python

from bs4 import BeautifulSoup
import os,sys, getopt
import logging
import shutil
import codecs
import pickle

logging.basicConfig(level=logging.INFO)


def main(input_file, output_file_list, numPartitions):
	docID = 0
	f = codecs.open(input_file, encoding="utf-8")
	xml_soup = BeautifulSoup(f, "xml")
	allPages = xml_soup.find_all("page")
	contents = [ dict() for x in range(numParitition)]
	for page in allPages:
		partition_index = docID % numPartitions
		title = page.title.string
		bodies = page.find("text").string
		page_dict = dict()
		page_dict["docID"] = str(docID)
		page_dict["title"] = unicode(title)
		page_dict["docBody"] = unicode(bodies)
		contents[partition_index][docID] = page_dict
		docID += 1
	for idx, file_name in enumerate(output_file_list):
		pickle.dump(contents[idx], open(file_name,"wb"))
		logging.info("Dump to %s", file_name)
	
if __name__ == "__main__":
	argv = sys.argv[1:]
	jobPath = ""
	numParitition = ""
	input_file = argv[0].strip()
	argv = argv[1:]
	try:
		opts, args = getopt.getopt(argv,'',['jobPath=','numPartitions='])
	except getopt.GetoptError:
		logging.error("python reformatter.py info_ret.xml --jobPath=<job_path> --numPartitions=<num_partition>")
		sys.exit(2)		
	for opt, arg in opts:
		if opt in ("--jobPath"):
			jobPath = arg
			jobPath = jobPath.strip()
		elif opt in ("--numPartitions"):
			numParitition = arg.strip()
			numParitition = int(numParitition)
	if os.path.exists(jobPath):
		shutil.rmtree(jobPath)
	os.makedirs(jobPath)
	all_files_name = [jobPath + "/" + str(x)+".in" for x in range(numParitition)]
	main(input_file,all_files_name,numParitition)
	
