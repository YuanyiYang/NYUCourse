/*
 * SCAN.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef SCAN_H_
#define SCAN_H_

#include <list>
#include <limits>
#include "IOEvent.h"
#include "Variable.h"
using namespace std;

class SCAN: public Scheduler {
	bool up;
public:
	SCAN() {
		this->up = true;
	}
	~SCAN() {

	}
	void put(IOEvent event) {
		process(event, ADD);
		event_list.push_back(event);
	}
	IOEvent get() {
		IOEvent event;
		list<IOEvent>::iterator best_it;
		int best = numeric_limits<int>::max();
		int diff;
		bool found = false;

		for (list<IOEvent>::iterator it = event_list.begin();
				it != event_list.end(); it++) {
			if (up) {
				// search through and get the next free loader
				if ((*it).track >= _head) {
					found = true;
					diff = (*it).track - _head;
					if (diff < best) {
						best = diff;
						best_it = it;
					}
				}
			} else {
				if ((*it).track <= _head) {
					found = true;
					diff = _head - (*it).track;
					if (diff < best) {
						best = diff;
						best_it = it;
					}
				}
			}
		}

		if (found) {
			event = (*best_it);
			event_list.erase(best_it);
			process(event, ISSUE);
			return event;
		} else {
			up = !up;
			return get();
		}

	}

};

#endif /* SCAN_H_ */
