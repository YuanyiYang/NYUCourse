/*
 * Process.h
 *
 *  Created on: Feb 28, 2015
 *      Author: yuanyiyang
 */

#ifndef PROCESS_H_
#define PROCESS_H_

class Process {
public:
	int AT; // arrival time
	int TC; // total CPU time
	int CB; // CPU burst
	int IO; // IO burst
	int ready_time; //the time for which the process could run but may not be picked

	int static_prio;  // static priority
	int dynamic_prio; // dynamic priority
	int CPUBurst; // the actual CPU burst
	int IOBurst; // the actual IO burst

	int remainingExeTime;
	int finishTime;
	int turnaroundTime;
	int IOTime;
	int CPUWaitingTime;

	int index; // the number of the process in the file

	Process(int index, int AT, int TC, int CB, int IO) {
		this->index = index;
		this->AT = AT;
		this->CB = CB;
		this->IO = IO;
		this->TC = TC;
		this->remainingExeTime = TC;
		static_prio = 0;
		dynamic_prio = 0;
		ready_time = 0;
		CPUBurst = 0;
		IOBurst = 0;
		finishTime = 0;
		turnaroundTime = 0;
		IOTime = 0;
		CPUWaitingTime = 0;
	}
};

#endif /* PROCESS_H_ */
