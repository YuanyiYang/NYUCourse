/*
 * LRU.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef LRU_H_
#define LRU_H_

#include "Page_Picker.h"

class LRU: public PagePicker {

public:

	LRU() {

	}

	~LRU() {

	}

	int getVictim() {
		int index = LRU_List.back();
		LRU_List.pop_back();
		return index;
	}
};

#endif /* LRU_H_ */
