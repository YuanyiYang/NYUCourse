#!/usr/bin/env python
import json
from operator import itemgetter
from itertools import groupby
import heapq

data1 = "[[\"fish\", \"1\"], [\"fish\", \"1\"], [\"one\", \"1\"], [\"two\", \"1\"]]"
data2 = "[[\"blue\", \"1\"], [\"fish\", \"1\"], [\"fish\", \"1\"], [\"red\", \"1\"]]"
data = [data1, data2]

def linear_merge():
		result = []
		response_body = [[] for x in range(len(data))]
		getKey = itemgetter(0)
		for i in range(len(data)):
			temp_List = []
			temp_List = json.loads(data[i])
			for word,group in groupby(temp_List,getKey):
				total = sum(int(count) for _, count in group)
				new_list = []
				new_list.append(word)
				new_list.append(total)
				response_body[i].append(new_list)
		return linear_merge_helper(response_body)
		#return result
		#print response_body
			
''' This method takes input as a list of sorted lists'''
def linear_merge_helper(body):
		return heapq.merge(*body)
	
def main():
	results = linear_merge()
	for result in results:
		print result

if __name__ == "__main__":
	main()
		
		
			
			
		
		
