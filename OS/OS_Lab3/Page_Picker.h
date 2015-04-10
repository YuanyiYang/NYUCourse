/*
 * Page_Picker.h
 * This class is used as the subtype of all page selecting algo when encountering a page fault
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef PAGE_PICKER_H_
#define PAGE_PICKER_H_

#include <queue>

class PagePicker {

protected:
	queue<int> validPageIndex; // For FIFO, Second chance and Clock algo, we need a queue
							   // to record the physical used page
	deque<int> LRU_List;

public:
	PagePicker() {

	}

	virtual ~PagePicker() {

	}

	// Always return the physical frame index
	virtual int getVictim() = 0;

	void addPhyPageToList(int phy_page_index) {
		validPageIndex.push(phy_page_index);
	}

	void updateLRU_List(int frame_index) {
		int index = -1;
		for (int i = 0; i < LRU_List.size(); i++) {
			if (LRU_List[i] == frame_index) {
				index = i;
				break;
			}
		}
		if (index == -1) {
			LRU_List.push_front(frame_index);
		} else {
			LRU_List.erase(LRU_List.begin() + index);
			LRU_List.push_front(frame_index);
		}
	}

};

#endif /* PAGE_PICKER_H_ */
