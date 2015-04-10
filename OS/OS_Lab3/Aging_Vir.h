/*
 * Aging_Vir.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef AGING_VIR_H_
#define AGING_VIR_H_
#include <vector>
#include <limits>
#include "variable.h"
#include "Page_Picker.h"
class Aging_Vir:public PagePicker{
	vector<unsigned int> _ages;
public:
	Aging_Vir(){
		for(int i=0;i<NUM_VIRTUAL_PAGE;i++){
			_ages.push_back(0);
		}
	}
	~Aging_Vir(){

	}
	int getVictim(){
		updateAges();
		int result = -1;
		unsigned int min = numeric_limits<unsigned int>::max();
		for(int i=0;i<NUM_VIRTUAL_PAGE;i++){
			if(_page_table[i].present){
				if(_ages[i]<min){
					min = _ages[i];
					result = i;
				}
				_page_table[i].referenced = 0;
			}
		}
		_ages[result] = 0;
		int _phy_frame = _page_table[result].index_phy_frame;
		return _phy_frame;
	}

	void updateAges(){
		for(int i=0;i<NUM_VIRTUAL_PAGE;i++){
			if(_page_table[i].present){
				unsigned int r = _page_table[i].referenced;
				r = r << 31;
				_ages[i] = _ages[i] >> 1;
				_ages[i] = _ages[i] | r;
			}
		}
	}
};



#endif /* AGING_VIR_H_ */
