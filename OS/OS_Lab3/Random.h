/*
 * Random.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef RANDOM_H_
#define RANDOM_H_

#include "Page_Picker.h"
#include "rand.h"

class Random: public PagePicker {

	Rand * _rand;
	int range;
public:
	Random(Rand * _rand, int range) {
		this->_rand = _rand;
		this->range = range;
	}
	~Random() {

	}
	int getVictim() {
		return _rand->next(range);
	}
};

#endif /* RANDOM_H_ */
