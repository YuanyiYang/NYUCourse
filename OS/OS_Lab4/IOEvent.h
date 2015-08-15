/*
 * IOEvent.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef IOEVENT_H_
#define IOEVENT_H_

struct IOEvent {
	int io_op;
	int arr_time;
	int start_time;
	int end_time;
	int track;  // the request track

	IOEvent() :
			io_op(0), arr_time(0), start_time(0), end_time(0), track(0) {
	}

	IOEvent(int io_op, int arr_time, int track) {
		this->io_op = io_op;
		this->arr_time = arr_time;
		this->start_time = 0;
		this->end_time = 0;
		this->track = track;
	}

	void printEvent() {
		printf("%5d: %5d %5d %5d\n", io_op, arr_time, start_time, end_time);
	}

};

#endif /* IOEVENT_H_ */
