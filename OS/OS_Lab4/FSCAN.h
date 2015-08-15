/*
 * FSCAN.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef FSCAN_H_
#define FSCAN_H_

#include <limits>
#include "Variable.h"
#include "IOEvent.h"
using namespace std;
class FSCAN: public Scheduler {
	bool up;
	list<IOEvent> ready_queue;
	list<IOEvent> wait_queue;
public:
	FSCAN() {
		this->up = true;
	}
	~FSCAN() {

	}

	bool has_event() {
		return !(ready_queue.empty() && wait_queue.empty());
	}

	void put(IOEvent event) {
		process(event, ADD);
		wait_queue.push_back(event);
	}
	IOEvent get() {
		if (ready_queue.size() == 0) {
			ready_queue = wait_queue;
			wait_queue = list<IOEvent>();
			up = true;
		}
		IOEvent event;
		list<IOEvent>::iterator best_it;
		int best = numeric_limits<int>::max();
		int diff;
		bool found = false;

		for (list<IOEvent>::iterator it = ready_queue.begin();
				it != ready_queue.end(); it++) {
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
			ready_queue.erase(best_it);
			process(event, ISSUE);
			return event;
		} else {
			up = !up;
			return get();
		}
	}

};

#endif /* FSCAN_H_ */
