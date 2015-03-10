/*
 * RR_Scheduler.h
 *
 *  Created on: Mar 2, 2015
 *      Author: yuanyiyang
 */

#ifndef RR_SCHEDULER_H_
#define RR_SCHEDULER_H_

#include <iostream>
#include "Process.h"
#include "Scheduler.h"
using namespace std;

class RR_Scheduler: public Scheduler {

public:
	RR_Scheduler(char * sourceFile, Rand * rand, int qt) :
			Scheduler(4, sourceFile, rand, qt) {
	}

	~RR_Scheduler() {

	}

	bool is_ready_queue_empty() {
		return ready_queue.empty();
	}

	void add_to_ready_queue(Process * p) {
		p->dynamic_prio = p->static_prio - 1;
		ready_queue.push_back(p);
	}

	Process * get_from_ready_queue() {
		Process * proc = ready_queue.front();
		ready_queue.pop_front();
		return proc;
	}

};

#endif /* RR_SCHEDULER_H_ */
