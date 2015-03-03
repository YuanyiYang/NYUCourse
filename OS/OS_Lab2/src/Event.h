/*
 * Event.h
 *
 *  Created on: Mar 1, 2015
 *      Author: yuanyiyang
 */

#ifndef EVENT_H_
#define EVENT_H_
#include "Process.h"
using namespace std;
enum Transition {
	DONE, BLOCK, READY, RUNNING, CREATE, PREEMPT
};

/*
 * Represent an event
 */
class Event {
public:
	int a_t;
	int p_id;   // process id of the process involved
	int time_stamp;
	int c_b;   // CPU burst of the next event
	int i_o;  // IO burst of the next event
	int rem;  // since the copy constructor is a shallow copy, we store the rem from the process
	int prio; // also shallow copy
	Process * p;
	Transition trans;

	Event(int a_t, int p_id, int time_stamp, int c_b, int i_o, Transition trans,
			Process * p) {
		this->a_t = a_t;
		this->p_id = p_id;
		this->time_stamp = time_stamp;
		this->c_b = c_b;
		this->i_o = i_o;
		this->trans = trans;
		this->p = p;
		this->rem = p->remainingExeTime;
		this->prio = p->dynamic_prio;
	}

	void output() {
		switch (trans) {
		case DONE: {
			printf("%d %d %d: Done\n", a_t, p_id, a_t-time_stamp);
			break;
		}
		case BLOCK: {
			printf("%d %d %d: RUNNG -> BLOCK  ib=%d rem=%d\n", a_t, p_id,
					a_t - time_stamp, i_o, rem);
			break;
		}
		case READY: {
			printf("%d %d %d: BLOCK -> READY\n", a_t, p_id, a_t-time_stamp);
			break;
		}
		case RUNNING: {
			printf("%d %d %d: READY -> RUNNG cb=%d rem=%d prio=%d\n", a_t, p_id,
					a_t - time_stamp, c_b, rem,
					prio);
			break;
		}
		case CREATE: {
			printf("%d %d %d: CREATED -> READY\n", a_t, p_id, time_stamp - a_t);
			break;
		}
		case PREEMPT: {
			printf("%d %d %d: RUNNG -> READY  cb=%d rem=%d prio=%d\n", a_t, p_id, a_t-time_stamp,
					c_b, rem, prio);
			break;
		}
		default:
			break;
		}
	}
};

#endif /* EVENT_H_ */
