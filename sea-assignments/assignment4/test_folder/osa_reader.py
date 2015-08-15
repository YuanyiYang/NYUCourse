#!/usr/bin/env python

def main():
	f = open("../oas_jobs/0.in", 'r')
	i = 1
	for line in f:
		print line
		i = i+1
		if i==100:
			break

if __name__ == "__main__":
	main()
