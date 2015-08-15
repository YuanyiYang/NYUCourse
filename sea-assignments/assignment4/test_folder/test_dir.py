#!/usr/bin/env python

import os


def main():
	print os.getcwd()
	print os.path.dirname(os.path.abspath(__file__))
	working_dir = os.getcwd()
	filename_list = []
	for root, dirs, files in os.walk(working_dir):
		for file in files:
			if file.endswith(".in"):
				file_path = os.path.join(root,file)
				filename_list.append(file_path)
	print filename_list
	
if __name__ == "__main__":
	main()
