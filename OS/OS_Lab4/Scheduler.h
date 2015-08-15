/*
 * Scheduler.h
 *
 *  Created on: Apr 15, 2015
 *      Author: yuanyiyang
 */

#ifndef SCHEDULER_H_
#define SCHEDULER_H_

#include "stddef.h"
#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include <sstream>
#include "IOEvent.h"
#include "Variable.h"
using namespace std;

class Scheduler {

protected:
	list<IOEvent> event_list;

public:
	Scheduler() {
	}

	virtual ~Scheduler() {

	}

	virtual bool has_event() {
		return !event_list.empty();
	}
	virtual void put(IOEvent event) =0;
	virtual IOEvent get() =0;

};

#endif /* SCHEDULER_H_ */
