/*
 * main.cpp
 *
 *  Created on: Feb 28, 2015
 *      Author: yuanyiyang
 */

#include<iostream>
#include<ctype.h>
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string>
#include "Scheduler.h"
#include "rand.h"
#include "FCFS_Scheduler.h"
#include "LCFS_Scheduler.h"
#include "SJF_Scheduler.h"

using namespace std;

int main(int argc, char **argv) {
	Rand * _r = new Rand();
	Scheduler * _sched = NULL;
	// initial value for reading command line arguments
	bool vFlag = false;
	char * svalue = NULL;
	int c;
	while ((c = getopt(argc, argv, "vs:")) != -1)
		switch (c) {
		case 'v':
			vFlag = true;
			break;
		case 's':
			svalue = optarg;
			break;
		case '?':
			break;
		default:
			abort();
		}

	_r->init(argv[optind + 1]);

	switch (svalue[0]) {
	case 'F': {
		_sched = new FCFS_Scheduler(argv[optind], _r);
		break;
	}
	case 'L': {
		_sched = new LCFS_Scheduler(argv[optind], _r);
		break;
	}
	case 'S': {
		_sched = new SJF_Scheduler(argv[optind], _r);
		break;
	}
	case 'R':{

		break;
	}
	default:
		break;
	}
	_sched->beginSchedule();
	if (vFlag) {
		_sched->printEvents();
	}
	_sched->printResult();
	delete _r;
	delete _sched;
}

