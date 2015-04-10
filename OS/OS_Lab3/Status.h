/*
 * Status.h
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef STATUS_H_
#define STATUS_H_

struct Status {
	int instr_count;
	int unmaps;
	int maps;
	int ins;
	int outs;
	int zeros;

	Status() :
			instr_count(0), unmaps(0), maps(0), ins(0), outs(0), zeros(0) {
	}

	unsigned long long total_cost() {
		return (unsigned long long) ((maps + unmaps) * 400 + (ins + outs) * 3000
				+ zeros * 150 + instr_count);
	}
	void printStatus() {
		printf("SUM %d U=%d M=%d I=%d O=%d Z=%d ===> %llu\n", instr_count,
				unmaps, maps, ins, outs, zeros, total_cost());
	}
};

#endif /* STATUS_H_ */
