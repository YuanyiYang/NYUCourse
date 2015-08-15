/*
 * SSTF.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef SSTF_H_
#define SSTF_H_
#include <iostream>
#include <list>
#include <limits>
#include "Variable.h"
using namespace std;

class SSTF: public Scheduler {
public:
	SSTF() {
	}

	~SSTF() {

	}
	void put(IOEvent event) {
		process(event, ADD);
		event_list.push_back(event);
	}
	IOEvent get() {
		int seek_time = 0;
		int min_seek = numeric_limits<int>::max();
		list<IOEvent>::iterator min_position_iter;
		for (list<IOEvent>::iterator it = event_list.begin();
				it != event_list.end(); ++it) {
			seek_time = abs((*it).track - _head);
			if (seek_time < min_seek) {
				min_seek = seek_time;
				min_position_iter = it;
			}
		}
		IOEvent event = (*min_position_iter);
		event_list.erase(min_position_iter);
		process(event, ISSUE);
		return event;
	}
};

#endif /* SSTF_H_ */
