/*
 * NRU.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef NRU_H_
#define NRU_H_

#include <vector>
#include "Page_Picker.h"
#include "variable.h"

class NRU: public PagePicker {

	int timeCount;
	vector<int> class0;
	vector<int> class1;
	vector<int> class2;
	vector<int> class3;

public:
	NRU() {
		timeCount = 0;
	}
	~NRU() {

	}
	int getVictim() {
		int res  = 0;
		refreshClass();
		timeCount++;
		if (timeCount % 10 == 0) {
			resetReferenceBit();
		}
		if(!class0.empty()){
			int index = _r->next(class0.size());
			res = class0[index];
		}else if(!class1.empty()){
			int index = _r->next(class1.size());
			res = class1[index];
		}else if(!class2.empty()){
			int index = _r->next(class2.size());
			res = class2[index];
		}else{
			int index = _r->next(class3.size());
			res = class3[index];
		}
		res = _page_table[res].index_phy_frame;
		return res;
	}

	void refreshClass() {
		class0.clear();
		class1.clear();
		class2.clear();
		class3.clear();

		for (int i = 0; i < NUM_VIRTUAL_PAGE; i++) {
			if (_page_table[i].present) {
				bool R = _page_table[i].referenced;
				bool M = _page_table[i].modified;
				if (R && M) {
					class3.push_back(i);
				} else if (R && !M) {
					class2.push_back(i);
				} else if (!R && M) {
					class1.push_back(i);
				} else {
					class0.push_back(i);
				}
			}
		}
	}

	void resetReferenceBit() {
		for (int i = 0; i < NUM_VIRTUAL_PAGE; i++) {
			if (_page_table[i].present) {
				_page_table[i].referenced = 0;
			}
		}
	}
};

#endif /* NRU_H_ */
