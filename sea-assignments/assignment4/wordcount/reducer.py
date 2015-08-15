#!/usr/bin/env python 
# python reducer.py -i(index) -o(output.path)
from itertools import groupby, imap
from operator import itemgetter
import sys, getopt
import logging
import os, os.path

logging.basicConfig(level=logging.INFO)

def main(argv):
    #logging.info("Number of argument: %d" % len(sys.argv))
    #logging.info("Arguments list: %s" % str(sys.argv))
    intput_index = ""
    output_path = ""
    try:
        opts, args = getopt.getopt(argv,"i:o:")
    except getopt.GetoptError:
        logging.error("python reducer.py -i <index> -o <outputPath>")
        sys.exit(2)
    for opt, arg in opts:
        #print "opt: %s, arg: %s" %(opt, arg)
        if opt=="-i":
            intput_index = arg
        elif opt=="-o":
            output_path = arg
 
    output_path = output_path + "/" + intput_index.strip() + ".out"
    output_path = output_path.strip()
    if os.path.exists(output_path):
        os.remove(output_path)

    out_file = open(output_path, 'w')
    sys.stdout = out_file
		
    logging.debug("Index %s" % intput_index)
    logging.info("output_path %s" % output_path)
    data = imap(lambda x: x.strip().split("\t"), sys.stdin)
    for word, group in groupby(data, itemgetter(0)):
        total = sum(int(count) for _, count in group)
        print "%s\t%d" % (word, total)

if __name__ == "__main__":
    main(sys.argv[1:])


