/*
 * SecondChance.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef SECONDCHANCE_H_
#define SECONDCHANCE_H_

#include "Page_Picker.h"
#include "variable.h"
class SecondChance: public PagePicker {
public:
	SecondChance() {

	}
	~SecondChance() {

	}

	int getVictim() {

		bool is_stop = false;
		int res = 0;
		while (!is_stop) {
			int temp = validPageIndex.front();
			int vir = _frame_table[temp];
			if (_page_table[vir].referenced) {
				_page_table[vir].referenced = 0;
				validPageIndex.pop();
				validPageIndex.push(temp);
			} else {
				validPageIndex.pop();
				res = temp;
				is_stop = true;
			}
		}
		return res;
	}
};

#endif /* SECONDCHANCE_H_ */
