/*
 * FCFS_Schedeuler.h
 *
 *  Created on: Feb 28, 2015
 *      Author: yuanyiyang
 */

#ifndef FCFS_SCHEDEULER_H_
#define FCFS_SCHEDEULER_H_

#include <iostream>
#include <deque>
#include <vector>
#include <climits>
#include <algorithm>
#include "Scheduler.h"
#include "Process.h"
using namespace std;

class FCFS_Scheduler: public Scheduler {

public:
	FCFS_Scheduler(char * sourceFile, Rand * rand) :
			Scheduler(1, sourceFile, rand, INT_MAX) {
	}

	~FCFS_Scheduler() {

	}

	void add_to_ready_queue(Process * p) {
		ready_queue.push_back(p);
		/*
		if (ready_queue.size() == 0) {
			ready_queue.push_back(p);
			return;
		} else {
			//cout<<ready_queue.size()<<endl;
			list<Process*>::iterator it = ready_queue.begin();
			while (it != ready_queue.end() && p->ready_time > (*it)->ready_time) {
				++it;
			}
			while (it != ready_queue.end() && (*it)->ready_time == p->ready_time) {
				if (p->index > (*it)->index) {
					it++;
				}else{
					break;
				}
			}
			ready_queue.insert(it, p);
		}
		*/
	}

	Process * get_from_ready_queue() {
		Process * proc = ready_queue.front();
		ready_queue.pop_front();
		return proc;
	}
};

#endif /* FCFS_SCHEDEULER_H_ */
