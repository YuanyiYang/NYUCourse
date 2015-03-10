/*
 * Scheduler.h
 *
 *  Created on: Feb 28, 2015
 *      Author: yuanyiyang
 */

#ifndef SCHEDULER_H_
#define SCHEDULER_H_

#include <fstream>
#include <iostream>
#include <vector>
#include <sstream>
#include <list>
#include "Process.h"
#include "rand.h"
#include "Event.h"
using namespace std;

enum Tyepe {
	NONE, FCFS, LCFS, SJF, RR, PRIO
};

class Scheduler {

protected:
	char * sourceFile;
	Rand * rand;
	int schedulerType;
	float sys_non_IO_time;
	float pro_IO_time;
	vector<Process*> allProcesses;
	list<Process*> ready_queue;
	list<Event*> event_queue;
	vector<Event> results_events;

	Process * cur_process;

	int qt; // the quantum of the schedeuler

public:
	Scheduler(int schedulerType, char * sourceFile, Rand * rand, int qt) {
		this->schedulerType = schedulerType;
		this->sourceFile = sourceFile;
		this->rand = rand;
		cur_process = NULL;
		this->qt = qt;
		this->sys_non_IO_time = 0;
		this->pro_IO_time = 0;
		readProcessFile(this->sourceFile);
	}

	virtual ~Scheduler() {

	}

	virtual void add_to_ready_queue(Process *) = 0; // virtual function for different scheduler to implement
	virtual Process * get_from_ready_queue() = 0; // virtual function for differnt scheduler to provide the next ready process
	virtual bool is_ready_queue_empty() = 0;

	vector<string> stringSplit(string str) {
		vector<string> tokens;
		string token;
		stringstream ss(str);
		while (ss >> token) {
			tokens.push_back(token);
		}
		return tokens;
	}

	// add the event to the event_queue based on their arrival time
	void add_to_events_queue(Event * e) {
		list<Event*>::iterator it = event_queue.begin();
		while (it != event_queue.end() && e->a_t >= (*it)->a_t) {
			++it;
		}
		event_queue.insert(it, e);
	}

	void readProcessFile(char * file) {
		ifstream infile;
		infile.open(file);
		string str;
		if (infile.is_open()) {
			int index = 0;
			while (getline(infile, str)) {
				vector<string> tokens = stringSplit(str);
				Process * process = new Process(index, atoi(tokens[0].c_str()),
						atoi(tokens[1].c_str()), atoi(tokens[2].c_str()),
						atoi(tokens[3].c_str()));
				process->static_prio = rand->next(4); // assign the static priority
				process->dynamic_prio = process->static_prio - 1;
				allProcesses.push_back(process);
				index++;
			}
		}
		infile.close();
	}

	void prepareInitialEvents() {
		for (unsigned int i = 0; i < allProcesses.size(); i++) {
			Process * p = allProcesses[i];
			Event *e = new Event(p->AT, p->index, p->AT, 0, 0, CREATE, p);
			add_to_events_queue(e);
		}
	}

	list<Event*> getEventsWithSameTimeAT() {
		list<Event*> results;
		Event * front_event = event_queue.front();
		int i = 0;
		int size = event_queue.size();
		int time_stamp = front_event->a_t;
		while (i <= size - 1 && front_event->a_t == time_stamp) {
			results.push_back(front_event);
			event_queue.pop_front();
			front_event = event_queue.front();
			i++;
		}
		//cout<<results.size()<<endl;
		return results;
	}

	// You must process all events at a given timestamp before invoking the dispatcher
	void execute_event(list<Event*> & execute_events) {
		int current_system_time = execute_events.front()->a_t;
		int size = execute_events.size();
		for (int i = 0; i < size; i++) {
			Event * next_event = NULL;
			Event * cur_event = execute_events.front();
			execute_events.pop_front();
			Process * temp_process = cur_event->p;
			switch (cur_event->trans) {
			case CREATE: {
				temp_process->ready_time = cur_event->a_t;
				add_to_ready_queue(temp_process);
				break;
			}
			case READY: {
				temp_process->ready_time = cur_event->a_t; // when the process is picked by the dispatcher, we substract these two values and get the CPU wait time
				add_to_ready_queue(temp_process);
				break;
			}
			case DONE: {
				temp_process->finishTime = cur_event->a_t;
				cur_process = NULL;
				break;
			}
			case BLOCK: {
				// first get the executing time for the current process
				cur_process->remainingExeTime -= cur_event->a_t
						- cur_event->time_stamp;
				cur_event->rem = cur_process->remainingExeTime;
				// for now, it should be equal to the c_b in the current event
				/*
				 if ((cur_event->a_t - cur_event->time_stamp)
				 != cur_event->c_b) {
				 cout << "For debug issue" << endl;
				 }
				 if (cur_process->index != cur_event->p_id) {
				 cout << "ERROR" << endl;
				 }
				 */
				// update the system IO time
				if (this->pro_IO_time < cur_event->a_t) {
					this->sys_non_IO_time += cur_event->a_t - this->pro_IO_time;
				}
				// update the pro_IO_time
				if (this->pro_IO_time < cur_event->a_t + cur_event->i_o) {
					this->pro_IO_time = cur_event->a_t + cur_event->i_o;
				}
				cur_process->IOTime += cur_event->i_o; // add the total IO time
				cur_process->remainCPUBurst = 0;
				int next_event_at = cur_event->a_t + cur_event->i_o;
				cur_process->ready_time = next_event_at; // since next state for block is ready, so we could compute the ready time for process
				cur_process->dynamic_prio = cur_process->static_prio - 1;
				next_event = new Event(next_event_at, cur_event->p_id,
						cur_event->a_t, 0, 0, READY, cur_process); // the next event for this should be the READY event
				cur_process = NULL;
				add_to_events_queue(next_event);
				break;
			}
			case RUNNING: {
				// add the time the process has been waited to be picked
				temp_process->CPUWaitingTime += cur_event->a_t
						- temp_process->ready_time;
				// whwn receive event, we know which process get picked by dispatcher
				cur_process = temp_process;
				if (cur_event->c_b > qt) {
					// In such case, it should fire an PREEMPT Event
					int next_event_at = cur_event->a_t + qt;
					next_event = new Event(next_event_at, cur_event->p_id,
							cur_event->a_t, 0, 0, PREEMPT, cur_process);
					// should consider fire an DONE
					if (cur_process->remainingExeTime <= qt) {
						next_event->trans = DONE;
					} else {
						next_event->c_b = cur_event->c_b - qt;
					}
				} else {
					int next_event_at = cur_event->a_t + cur_event->c_b;
					next_event = new Event(next_event_at, cur_event->p_id,
							cur_event->a_t, 0, 0, BLOCK, cur_process); //The default is considered tranformed into blocked state since no preemption
					if (cur_process->remainingExeTime <= cur_event->c_b) {
						// then the process will be terminated
						next_event->trans = DONE;
					} else {
						// we need to compute the io_burst for this process
						next_event->i_o = rand->next(cur_process->IO);
					}
					next_event->c_b = cur_event->c_b;
				}

				temp_process->dynamic_prio--;
				//cout<<"prio" << temp_process->dynamic_prio<<endl;
				add_to_events_queue(next_event);
				break;
			}
			case PREEMPT: {
				// At Running State, it should fire the PREEMPT event properly
				// in the PREEMPT event, we should fire a ready event next
				temp_process->remainingExeTime = temp_process->remainingExeTime
						- qt;
				temp_process->ready_time = cur_event->a_t;
				temp_process->remainCPUBurst = cur_event->c_b;
				//cout<<"In PREEMPT, prio" << temp_process->dynamic_prio<<endl;
				add_to_ready_queue(temp_process);
				cur_process = NULL;
				cur_event->rem = temp_process->remainingExeTime;
				break;
			}
			}
			results_events.push_back(*cur_event);
			//cur_event->output();
		}
		Event * next_event;
		//cout << "In base class, is Ready_Queue empty? " << is_ready_queue_empty() << endl;
		if (cur_process == NULL && !is_ready_queue_empty()) {
			cur_process = get_from_ready_queue();
			//cout<<"Get Running Procee " << cur_process -> index << endl;
			next_event = new Event(current_system_time, cur_process->index,
					cur_process->ready_time, 0, 0, RUNNING, cur_process);
			// due to preemption; the CPU burst has not been exhausted; no need to initialize a new one
			int burst = 0;
			if (cur_process->remainCPUBurst > 0) {
				burst = cur_process->remainCPUBurst;
			} else {
				// otherwise assign a new one every time
				burst = rand->next(cur_process->CB);
			}
			if (burst > cur_process->remainingExeTime) {
				burst = cur_process->remainingExeTime;
			}
			next_event->c_b = burst;
			add_to_events_queue(next_event);
			cur_process = NULL;
		}
	}

	void beginSchedule() {
		prepareInitialEvents();
		while (event_queue.size() != 0) {
			list<Event*> events = getEventsWithSameTimeAT();
			execute_event(events);
		}
	}

	void printEvents() {

		for (vector<Event>::iterator it = results_events.begin();
				it != results_events.end(); it++) {
			Event e = *it;
			e.output();
		}
	}

	void printResult() {
		int FTime = 0;
		for (vector<Process*>::iterator iter = allProcesses.begin();
				iter != allProcesses.end(); iter++) {
			Process * p = *iter;
			int temp = p->finishTime;
			if (temp > FTime) {
				FTime = temp;
			}
		}
		if (schedulerType == FCFS) {
			cout << "FCFS" << endl;
		} else if (schedulerType == LCFS) {
			cout << "LCFS" << endl;
		} else if (schedulerType == SJF) {
			cout << "SJF" << endl;
		} else if (schedulerType == RR) {
			cout << "RR " << qt << endl;
		} else {
			cout << "PRIO " << qt << endl;
		}

		this->sys_non_IO_time += FTime - this->pro_IO_time;
		float sumOfCPUTime = 0;
		float sumOfIOTime = FTime - sys_non_IO_time;
		float sumOfTurnaroundTime = 0;
		float sumOfCPUWaiting = 0;

		for (int i = 0; i < allProcesses.size(); i++) {
			Process * p = allProcesses[i];
			p->turnaroundTime = p->finishTime - p->AT;
			printf("%04d: %4d %4d %4d %4d %1d | %5d %5d %5d %5d\n", p->index,
					p->AT, p->TC, p->CB, p->IO, p->static_prio, p->finishTime,
					p->turnaroundTime, p->IOTime, p->CPUWaitingTime);
			sumOfCPUTime += p->TC;
			sumOfTurnaroundTime += p->turnaroundTime;
			sumOfCPUWaiting += p->CPUWaitingTime;
		}
		float num = allProcesses.size();
		printf("SUM: %d %.2lf %.2lf %.2lf %.2lf %.3lf\n", FTime,
				sumOfCPUTime / FTime * 100, sumOfIOTime / FTime * 100,
				sumOfTurnaroundTime / num, sumOfCPUWaiting / num,
				num / FTime * 100);
	}
};

#endif /* SCHEDULER_H_ */
