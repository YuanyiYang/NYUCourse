/*
 * iosched.cpp
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <list>
#include <iostream>
#include <algorithm>
#include "FCFS.h"
#include "SSTF.h"
#include "SCAN.h"
#include "FSCAN.h"
#include "CSCAN.h"
#include "IOEvent.h"
#include "Variable.h"
using namespace std;

void printSUM();
void print_each_event();
void load_input(char*);

int main(int argc, char **argv) {
	char* sValue = NULL;
	char* input_file = NULL;
	Scheduler * _sched = NULL;
	int c;
	while ((c = getopt(argc, argv, "s:")) != -1) {
		switch (c) {
		case 's':
			sValue = optarg;
			break;
		default:
			abort();
		}
	}
	input_file = argv[optind];
	switch (sValue[0]) {
	case 'i':
		_sched = new FCFS();
		break;
	case 'j':
		_sched = new SSTF();
		break;
	case 's':
		_sched = new SCAN();
		break;
	case 'c':
		_sched = new CSCAN();
		break;
	case 'f':
		_sched = new FSCAN();
		break;
	default:
		break;
	}
	load_input(input_file);
	if (_verbose) {
		cout << "TRACE" << endl;
	}
	while (_i < io_events.size()) {
		_idle += (io_events[_i].arr_time - _time);
		_time = io_events[_i].arr_time;
		_sched->put(io_events[_i++]);
		while (_sched->has_event()) {
			IOEvent event = _sched->get();
			_time += abs(event.track - _head);
			while (_i < io_events.size() && io_events[_i].arr_time <= _time) {
				_sched->put(io_events[_i++]);
			}
			_head = event.track;
			process(event, FINISH);
		}
	}
	print_each_event();
	printSUM();

}

void printSUM() {
	tot_movement = _time - 1 - _idle;
	printf("SUM: %d %d %.2lf %.2lf %d\n", _time, tot_movement,
			(double) sum_TurnAroundTime / _events_num,
			(double) sum_WaitTime / _events_num, max_waittime);
}

void print_each_event() {
	if (_verbose) {
		cout << "IOREQS INFO" << endl;
	}
	for (unsigned int i = 0; i < io_events.size(); i++) {
		int wait_time = io_events[i].start_time - io_events[i].arr_time;
		sum_TurnAroundTime += io_events[i].end_time - io_events[i].arr_time;
		sum_WaitTime += io_events[i].start_time - io_events[i].arr_time;
		if (wait_time > max_waittime) {
			max_waittime = wait_time;
		}
		if (_verbose) {
			io_events[i].printEvent();
		}
	}
}

void load_input(char* input_file) {
	ifstream infile;
	infile.open(input_file);
	int io_op = 0;
	string str;
	stringstream str_stream;
	if (infile.is_open()) {
		while (getline(infile, str)) {
			if (str.at(0) == '#') {
				continue;
			}
			int arr_time;
			int track;
			str_stream.clear();
			str_stream.str(str);
			str_stream >> arr_time >> track;
			IOEvent event = IOEvent(io_op, arr_time, track);
			io_events.push_back(event);
			io_op++;
		}
	}
	_events_num = io_op;
	infile.close();
}
