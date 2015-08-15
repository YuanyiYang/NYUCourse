/*
 * CSCAN.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef CSCAN_H_
#define CSCAN_H_
#include <list>
#include <cmath>
#include <limits>
#include <iostream>
#include "Variable.h"
using namespace std;
class CSCAN: public Scheduler {
	int start_pos;
	bool circ;
public:

	CSCAN() {
		start_pos = 0;
		circ = false;
	}

	~CSCAN() {

	}
	void put(IOEvent event) {
		process(event, ADD);
		list<IOEvent>::iterator it = event_list.begin();
		// put the event into the list based on the track
		while (it != event_list.end() && event.track >= (*it).track) {
			++it;
		}
		event_list.insert(it, event);
	}
	IOEvent get() {
		list<IOEvent>::iterator it;
		IOEvent event;
		if (!circ){
			start_pos = _head;
		}
		it = event_list.begin();
		// the track position smaller than the start_pos is coming before this loop
		while (it != event_list.end() && (*it).track < start_pos) {
			++it;
		}
		if (it != event_list.end()) {
			event = (*it);
			event_list.erase(it);
			process(event, ISSUE);
			circ = false;
			return event;
		} else {
			start_pos = 0;
			circ = true;
			return get();
		}
	}

};

#endif /* CSCAN_H_ */
