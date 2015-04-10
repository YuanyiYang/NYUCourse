/*
 * Clock_Phy.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef CLOCK_PHY_H_
#define CLOCK_PHY_H_
#include "Page_Picker.h"
#include "variable.h"
class Clock_Phy: public PagePicker {
	int count;
public:
	Clock_Phy() {
		count = 0;
	}
	~Clock_Phy() {

	}
	int getVictim() {
		int res = 0;
		while (true) {
			int frame_index = validPageIndex.front();
			int page_index = _frame_table[frame_index];
			if (!_page_table[page_index].referenced) {
				validPageIndex.pop();
				res = frame_index;
				break;
			} else {
				_page_table[page_index].referenced = 0;
				validPageIndex.pop();
				validPageIndex.push(frame_index);
			}
			count++;
			if (count == _num_phy_frame) {
				count = 0;
			}

		}
		return res;
	}
};

#endif /* CLOCK_PHY_H_ */
