/*
 * rand.h
 *
 *  Created on: Feb 28, 2015
 *      Author: yuanyiyang
 */

#ifndef RAND_H_
#define RAND_H_

#include "stddef.h"
#include <iostream>
#include <fstream>
#include <string>
using namespace std;
/*
 * Random number generator
 */
class Rand {
	int num;
	int ofs;
	int * randvals;
public:
	Rand(){
		this->num = 0;
		this->ofs = 0;
		this->randvals = NULL;
	}

	void init(char * file){
		ifstream infile;
		infile.open(file);
		string str;
		if(infile.is_open()){
			getline(infile, str);  // first line is the count of random number
			num = atoi(str.c_str());
			randvals = new int[num];
			int count = 0;
			while(getline(infile,str)){
				randvals[count] = atoi(str.c_str());
				count++;
			}
		}
		infile.close();
	}

	int myrandom(int burst){
		return 1 + (randvals[ofs] % burst);
	}

	int next(int burst){
		int rand = myrandom(burst);
		ofs++;
		if(ofs==num){
			ofs = 0;
		}
		return rand;
	}
};

#endif /* RAND_H_ */
