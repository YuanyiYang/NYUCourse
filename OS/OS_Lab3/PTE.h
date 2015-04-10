/*
 *  The instance of this class represent a page table entry in the hardware.
 *  In this assignment, we assume that the address space for one process contains 64
 *  virtual pages, which means there are 64 entries in the page table.
 *  The page table is maintained by hardware and we are simulating hardware here.
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef PTE_H_
#define PTE_H_

struct PTE {
	unsigned int present :1;
	unsigned int modified :1;
	unsigned int referenced :1;
	unsigned int pageout :1;
	unsigned int index_phy_frame :28;

	PTE() :
			present(0), modified(0), referenced(0), pageout(0), index_phy_frame(
					0) {
	}
};

#endif /* PTE_H_ */
