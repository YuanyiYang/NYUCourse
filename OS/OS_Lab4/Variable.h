/*
 * Variable.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef VARIABLE_H_
#define VARIABLE_H_

#include <vector>
#include "IOEvent.h"
using namespace std;

enum Operation {
	ADD, ISSUE, FINISH
};

int _time = 1;
int _head = 0;
int _idle = 0;
int _events_num = 0;
int _i = 0;
const bool _verbose = false;

int tot_movement = 0;
double sum_TurnAroundTime = 0.0;
double sum_WaitTime = 0.0;
int max_waittime = 0;

vector<IOEvent> io_events;

void process(IOEvent event, Operation op) {
	switch (op) {
	case ADD:
		if (_verbose) {
			printf("%d:%6d add %d\n", event.arr_time, event.io_op, event.track);
		}
		break;
	case ISSUE:
		io_events[event.io_op].start_time = _time;
		if (_verbose) {
			printf("%d:%6d issue %d %d\n", _time, event.io_op, event.track,
					_head);
		}
		break;
	case FINISH:
		io_events[event.io_op].end_time = _time;
		if (_verbose) {
			printf("%d:%6d finish %d\n", _time, event.io_op, _time - event.arr_time);
		}
		break;
	}
}

#endif /* VARIABLE_H_ */
