/*
 * FiFO.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef FIFO_H_
#define FIFO_H_
#include "Page_Picker.h"

class FIFO : public PagePicker{
public:
	FIFO(){

	}
	~FIFO(){

	}
	int getVictim(){
		int res = validPageIndex.front();
		validPageIndex.pop();
		return res;
	}
};



#endif /* FIFO_H_ */
