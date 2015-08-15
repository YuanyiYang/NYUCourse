/*
 * FCFS.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef FCFS_H_
#define FCFS_H_

#include <list>
#include "IOEvent.h"
#include "Scheduler.h"
#include "Variable.h"
using namespace std;

class FCFS: public Scheduler {

public:
	FCFS() {
	}

	~FCFS() {

	}
	void put(IOEvent event) {
		process(event, ADD);
		event_list.push_back(event);
	}
	IOEvent get() {
		IOEvent event = event_list.front();
		event_list.pop_front();
		process(event, ISSUE);
		return event;
	}
};

#endif /* FCFS_H_ */
