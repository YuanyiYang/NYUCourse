/*
 * PRIO_Scheduler.h
 *
 *  Created on: Mar 3, 2015
 *      Author: yuanyiyang
 */

#ifndef PRIO_SCHEDULER_H_
#define PRIO_SCHEDULER_H_

#include <iostream>
#include <list>
#include <map>
#include "Process.h"
#include "Scheduler.h"
using namespace std;

class PRIO_Scheduler: public Scheduler {

public:
	int active_queue_size;
	int expire_queue_size;
	map< int, list<Process*> * > * active_queue;
	map< int, list<Process*> * > * expired_queue;

	PRIO_Scheduler(char * sourceFile, Rand * rand, int qt) :
			Scheduler(5, sourceFile, rand, qt) {
		active_queue = new map< int, list<Process*> * >;
		expired_queue = new map< int, list<Process*> * >;
		for (int i = 0; i < 4; i++) {
			list<Process*> * queue = new list<Process*>;
			(*active_queue)[i] = queue;
			list<Process*> * another_queue = new list<Process*>;
			(*expired_queue)[i] = another_queue;
			this->active_queue_size = 0;
			this->expire_queue_size = 0;
		}
	}

	~PRIO_Scheduler() {

	}

	void add_to_ready_queue(Process * p) {
//		cout<<"Add to ready_queue"<<endl;
//		cout<<"Index "<<p->index<<endl;
		int cur_prio = p->dynamic_prio;
		int next_prio = cur_prio - 1;
		if (next_prio <= -1) {
			// this time it should add to the expired queue with its static prio
			next_prio = p->static_prio - 1;
			p -> dynamic_prio = next_prio;
			add_to_expire_queue_with_prio(p, next_prio);
		} else {
			p -> dynamic_prio = next_prio;
			add_to_ready_queue_with_prio(p, next_prio);
		}
	}

	void add_to_ready_queue_with_prio(Process * p, int prio) {
		//cout<<"Add to active queue with prio "<< prio << endl;
		list<Process*> * queue = (*active_queue)[prio];
		queue->push_back(p);
		this->active_queue_size++;
		//cout<<"active_queue_size "<< this->active_queue_size<<endl;
	}

	void add_to_expire_queue_with_prio(Process * p, int prio) {
		list<Process*> * queue = (*expired_queue)[prio];
		queue->push_back(p);
		this->expire_queue_size++;
	}

	void swap_queue() {
		map<int, list<Process*> * > * temp = active_queue;
		active_queue = expired_queue;
		expired_queue = temp;
		int temp_size = this->active_queue_size;
		this->active_queue_size = this->expire_queue_size;
		this->expire_queue_size = temp_size;
	}

	bool is_ready_queue_empty() {
		return this->active_queue_size==0;
	}

	Process * get_from_ready_queue() {
		Process * p = NULL;
		//cout<<"Get From Ready_queue: size " << this->active_queue_size<<endl;
		for (int i = 3; i >= 0; i--) {
			//cout<<"i " << i << endl;
			list<Process*> * queue = (*active_queue)[i];
			//cout<<"Active_queue " << i << " size " << queue->size() << endl;
			if (!(queue->empty())) {
				p = queue->front();
				queue->pop_front();
				break;
			}
		}
		active_queue_size--;
		if (active_queue_size == 0) {
			swap_queue();
		}
		return p;
	}

};

#endif /* PRIO_SCHEDULER_H_ */
