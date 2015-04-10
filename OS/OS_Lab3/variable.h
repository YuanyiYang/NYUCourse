/*
 *  This header file is used for global variables in this assgiment.
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */

#ifndef VARIABLE_H_
#define VARIABLE_H_

#include "PTE.h"
#include "Page_Picker.h"
#include "Status.h"
#include "instr.h"
#include <list>

const int NUM_VIRTUAL_PAGE = 64;

PTE _page_table[NUM_VIRTUAL_PAGE];    // page table (hardware)
int _num_phy_frame = 0; // num of physical frame in the frame table
int * _frame_table;	// index is the actual physical frame index and value is its corresponding virtual page
PagePicker * _pk;	// used to choose a victim
Status _status = Status();
int _num_used_phy_frame = 0;  // the num of used physical page frame
int _next_free_phy_frame = 0;
Rand * _r = NULL;

list<instr*> instruction_list;  //all the instruction list; used for -O option

#endif /* VARIABLE_H_ */
