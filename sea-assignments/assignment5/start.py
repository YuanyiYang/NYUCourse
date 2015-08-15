#!/use/bin/env python
import shlex, subprocess
import logging

logging.basicConfig(level=logging.DEBUG)
NUM_REDUCERS = 3

def main():
	doc_process_args = "python assignment4_p/coordinator.py --mapperPath=assignment4_p/document_store/doc_mapper.py --reducerPath=assignment4_p/document_store/doc_reducer.py --jobPath=assignment5/df_jobs --numReducers=%d" % NUM_REDUCERS
	logging.debug("Doc_Server mapReduce param: %s" % doc_process_args)
	doc_process_args = shlex.split(doc_process_args)	
	doc_process = subprocess.Popen(doc_process_args)
	doc_return_code = doc_process.wait()
	if doc_return_code is not 0:
		logging.error("MapReduce Doc return code %d" % doc_return_code)
		sys.exit(2)
	
	inverted_process_args = "python assignment4_p/coordinator.py --mapperPath=assignment4_p/inverted_index/index_mapper.py --reducerPath=assignment4_p/inverted_index/index_reducer.py --jobPath=assignment5/i_df_jobs --numReducers=%d" % NUM_REDUCERS
	logging.debug("Inverted_Server mapReduce param: %s" % inverted_process_args)
	inverted_process_args = shlex.split(inverted_process_args)
	inverted_process = subprocess.Popen(inverted_process_args)
	inverted_return_code = inverted_process.wait()
	if inverted_return_code is not 0:
		logging.error("MapReduce Inverted return code %d" % inverted_return_code)
		sys.exit(2)
	
	tf_idf_args = "python assignment4_p/coordinator.py --mapperPath=assignment4_p/idf_index/idf_mapper.py --reducerPath=assignment4_p/idf_index/idf_reducer.py --jobPath=assignment5/idf_jobs --numReducers=1" 
	logging.debug("IDF mapReduce param: %s" % tf_idf_args)
	tf_idf_args = shlex.split(tf_idf_args)
	idf_process = subprocess.Popen(tf_idf_args)
	idf_return_code = idf_process.wait()
	if idf_return_code is not 0:
		logging.error("MapReduce IDF return code %d" % idf_return_code)
		sys.exit(2)
		
if __name__ == "__main__":
	main()
	


