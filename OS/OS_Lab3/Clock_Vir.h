/*
 * Clock_Vir.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef CLOCK_VIR_H_
#define CLOCK_VIR_H_
#include "Page_Picker.h"
#include "variable.h"
class Clock_Vir: public PagePicker {
	int count;
public:
	Clock_Vir() {
		count = 0;
	}
	~Clock_Vir() {

	}
	int getVictim() {
		int res = 0;
		while (true) {
			if (count == NUM_VIRTUAL_PAGE) {
				count = 0;
			}
			if (_page_table[count].present) {
				if (_page_table[count].referenced) {
					_page_table[count].referenced = 0;
					count++;
				} else {
					res = _page_table[count].index_phy_frame;
					count++;
					break;
				}
			} else {
				count++;
			}

		}
		return res;
	}
};

#endif /* CLOCK_VIR_H_ */
