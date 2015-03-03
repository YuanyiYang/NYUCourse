/*
 * SJF_Scheduler.h
 *
 *  Created on: Mar 2, 2015
 *      Author: yuanyiyang
 */

#ifndef SJF_SCHEDULER_H_
#define SJF_SCHEDULER_H_

#include <iostream>
#include <vector>
#include <climits>
#include "Scheduler.h"
#include "Process.h"
using namespace std;

class SJF_Scheduler: public Scheduler {

public:
	SJF_Scheduler(char * sourceFile, Rand * rand) :
			Scheduler(3, sourceFile, rand, INT_MAX) {
	}

	~SJF_Scheduler() {

	}

	bool is_ready_queue_empty() {
		return ready_queue.empty();
	}

	void add_to_ready_queue(Process * p) {
		if (ready_queue.empty()) {
			ready_queue.push_back(p);
		} else {
			list<Process*>::iterator iter = ready_queue.begin();
			while (iter != ready_queue.end()
					&& (*iter)->remainingExeTime <= p->remainingExeTime) {
				++iter;
			}
			ready_queue.insert(iter, p);
		}
	}

	Process * get_from_ready_queue() {
		Process * proc = ready_queue.front();
		ready_queue.pop_front();
		return proc;
	}

};

#endif /* SJF_SCHEDULER_H_ */
