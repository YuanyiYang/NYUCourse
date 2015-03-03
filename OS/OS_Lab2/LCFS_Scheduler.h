/*
 * LCFS_Schedeuler.h
 *
 *  Created on: Mar 2, 2015
 *      Author: yuanyiyang
 */

#ifndef LCFS_SCHEDEULER_H_
#define LCFS_SCHEDEULER_H_

#include <iostream>
#include <vector>
#include <climits>
#include "Scheduler.h"
#include "Process.h"
using namespace std;

class LCFS_Scheduler: public Scheduler {

public:
	LCFS_Scheduler(char * sourceFile, Rand * rand) :
			Scheduler(2, sourceFile, rand, INT_MAX) {
	}

	~LCFS_Scheduler() {

	}

	void add_to_ready_queue(Process * p) {
		ready_queue.push_back(p);
		/*
		if (ready_queue.size() == 0) {
			ready_queue.push_back(p);
			return;
		} else {
			list<Process*>::iterator it = ready_queue.begin();
			while (it != ready_queue.end() && p->ready_time > (*it)->ready_time) {
				++it;
			}
			while (it != ready_queue.end() && (*it)->ready_time == p->ready_time) {
				if (p->index > (*it)->index) {
					++it;
				}else{
					break;
				}
			}
			ready_queue.insert(it, p);
		}
		*/
	}

	Process * get_from_ready_queue() {
		Process * proc = ready_queue.back();
		ready_queue.pop_back();
		return proc;
	}

};

#endif /* LCFS_SCHEDEULER_H_ */
