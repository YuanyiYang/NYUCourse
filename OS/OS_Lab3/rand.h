/*
 * rand.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef RAND_H_
#define RAND_H_

#include "stddef.h"
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

class Rand {
	int num;
	int ofs;
	int * randvals;

public:
	Rand(char * file) {
		this->num = 0;
		this->ofs = 0;
		this->randvals = NULL;
		ifstream infile;
		infile.open(file);
		string str;
		if (infile.is_open()) {
			getline(infile, str);
			num = atoi(str.c_str());
			randvals = new int[num];
			int count = 0;
			while (getline(infile, str)) {
				randvals[count] = atoi(str.c_str());
				count++;
			}
		}
		infile.close();
	}

	int next(int range) {
		int rand = randvals[ofs] % range;
		ofs++;
		if (ofs == num) {
			ofs = 0;
		}
		return rand;
	}
};

#endif /* RAND_H_ */
