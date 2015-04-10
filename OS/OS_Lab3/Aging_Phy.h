/*
 * Aging_Phy.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef AGING_PHY_H_
#define AGING_PHY_H_

#include <vector>
#include <iostream>
#include <limits>
#include "Page_Picker.h"
#include "variable.h"

class Aging_Phy: public PagePicker {

	vector<unsigned int> _ages;

public:
	Aging_Phy() {
		for (int i = 0; i < _num_phy_frame; i++) {
			_ages.push_back(0);
		}
	}
	~Aging_Phy() {

	}
	int getVictim() {
		updateAges();
		unsigned int min = _ages.front();
		int result = 0;
		for (int i = 0; i < _ages.size(); i++) {
			if (_ages[i] < min) {
				min = _ages[i];
				result = i;
			}
			_page_table[_frame_table[i]].referenced = 0;
		}
		_ages[result] = 0;
		return result;
	}

	void updateAges() {
		for (int i = 0; i < _ages.size(); i++) {
			int vir_page_index = _frame_table[i];
			if (!_page_table[vir_page_index].present) {
				cout << "For debug purpose, this should be error in Aging_Phy"
						<< endl;
				cout
						<< "The virtual page referenced by the physical page frame is not presented in address space"
						<< endl;
			}
			unsigned int r = _page_table[vir_page_index].referenced;
			r = r << 31;
			_ages[i] = _ages[i] >> 1;
			_ages[i] = _ages[i] | r;
		}
	}
};

#endif /* AGING_PHY_H_ */
