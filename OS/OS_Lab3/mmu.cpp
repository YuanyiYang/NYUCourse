/*
 *	The main class.
 *
 *  Created on: Apr 7, 2015
 *      Author: yuanyiyang
 */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

#include "rand.h"
#include "PTE.h"
#include "variable.h"
#include "NRU.h"
#include "LRU.h"
#include "Random.h"
#include "FiFO.h"
#include "SecondChance.h"
#include "Clock_Phy.h"
#include "Clock_Vir.h"
#include "Aging_Phy.h"
#include "Aging_Vir.h"
#include "instr.h"

void run(char *);
void execute_instr(int, int, int);
void print_O_Result();
void print_FrameTable();
void print_PageTable();
void print_Sum();

int main(int argc, char **argv) {

	// get command line argument
	char *avalue = NULL;
	char *fvalue = NULL;
	char *ovalue = NULL;
	char *input_file = NULL;
	char *random_file = NULL;
	bool _OFlag = false;
	bool _PFlag = false;
	bool _FFlag = false;
	bool _SFlag = false;
	bool fFlag = false;
	bool aFlag = false;
	int c;
	while ((c = getopt(argc, argv, "a:o:f:")) != -1) {
		switch (c) {
		case 'a':
			aFlag = true;
			avalue = optarg;
			break;
		case 'f':
			fFlag = true;
			fvalue = optarg;
			break;
		case 'o':
			ovalue = optarg;
			break;
		default:
			abort();
		}
	}
	if (!aFlag) {
		avalue = "l";
	}
	if (!fFlag) {
		fvalue = "32";
	}
	//cout << avalue << endl;
	//cout << ovalue << endl;
	//cout << fvalue << endl;
	_num_phy_frame = atoi(fvalue);
	_frame_table = new int[_num_phy_frame];

	input_file = argv[optind];
	random_file = argv[optind + 1];
	switch (avalue[0]) {
	case 'N':
		_r = new Rand(random_file);
		_pk = new NRU();
		break;
	case 'l':
		_pk = new LRU();
		break;
	case 'r': {
		_r = new Rand(random_file);
		_pk = new Random(_r, _num_phy_frame);
		break;
	}
	case 'f':
		_pk = new FIFO();
		break;
	case 's':
		_pk = new SecondChance();
		break;
	case 'c':
		_pk = new Clock_Phy();
		break;
	case 'X':
		_pk = new Clock_Vir();
		break;
	case 'a':
		_pk = new Aging_Phy();
		break;
	case 'Y':
		_pk = new Aging_Vir();
		break;
	default:
		break;
	}

	size_t i;
	for (i = 0; ovalue[i]; i++) {
		switch (ovalue[i]) {
		case 'O':
			_OFlag = true;
			break;
		case 'P':
			_PFlag = true;
			break;
		case 'F':
			_FFlag = true;
			break;
		case 'S':
			_SFlag = true;
			break;
		default:
			continue;
		}
	}
	run(input_file);

	if (_OFlag) {
		print_O_Result();
	}
	if (_PFlag) {
		print_PageTable();
	}
	if (_FFlag) {
		print_FrameTable();
	}
	if (_SFlag) {
		print_Sum();
	}
	return 0;
}

void run(char * file) {
	ifstream infile;
	infile.open(file);
	string str;
	int op_code;
	int virtual_page_index;
	stringstream str_stream;
	int instr_index = 0;
	if (infile.is_open()) {
		while (getline(infile, str)) {
			if (str.at(0) == '#') {
				continue;
			}
			str_stream.clear();
			str_stream.str(str);
			str_stream >> op_code >> virtual_page_index;
			execute_instr(instr_index, op_code, virtual_page_index);
			instr_index++;
			_status.instr_count++;
		}
	}
	infile.close();
}

void execute_instr(int instr_index, int op_code, int virtual_page_index) {
	//cout<<"exe "<<op_code<<" "<<virtual_page_index<<endl;
	instr * _instr = new instr(0);
	_instr->op_code = op_code;
	_instr->virtual_page_index = virtual_page_index;
	instruction_list.push_back(_instr);

	// first check whether this virtual page is present in the page table
	// if hit, perform the instruction
	if (_page_table[virtual_page_index].present) {
		if (op_code) {
			_page_table[virtual_page_index].modified = 1;
		}
		_page_table[virtual_page_index].referenced = 1;
		_pk->updateLRU_List(_page_table[virtual_page_index].index_phy_frame);
	} else {
		// not hit, determine whether we need to find a victim
		if (_next_free_phy_frame < _num_phy_frame) {
			// no need to choose a victim page
			// check is it a page-in operatin or zero operation
			if (_page_table[virtual_page_index].pageout) {
				//page in operation
				instr * _instr = new instr(3);
				_instr->instr_index = instr_index;
				_instr->virtual_page_index = virtual_page_index;
				_instr->frame_index = _next_free_phy_frame;
				instruction_list.push_back(_instr);
				_status.ins++;
			} else {
				// zero operation
				instr *_instr = new instr(5);
				_instr->instr_index = instr_index;
				_instr->frame_index = _next_free_phy_frame;
				_status.zeros++;
				instruction_list.push_back(_instr);
			}
			// map operation

			instr * _instr = new instr(1);
			_instr->instr_index = instr_index;
			_instr->virtual_page_index = virtual_page_index;
			_instr->frame_index = _next_free_phy_frame;
			instruction_list.push_back(_instr);
			_status.maps++;

			// update PTE and (vise verse)frame table
			_page_table[virtual_page_index].index_phy_frame =
					_next_free_phy_frame;
			_frame_table[_next_free_phy_frame] = virtual_page_index;
			if (op_code) {
				_page_table[virtual_page_index].modified = 1;
			}
			_page_table[virtual_page_index].referenced = 1;
			_page_table[virtual_page_index].present = 1;
			_pk->addPhyPageToList(_next_free_phy_frame);
			_pk->updateLRU_List(_next_free_phy_frame);
			_next_free_phy_frame++;
			return;

		} else {
			// Need to choose a victim; perform memory operation
			int victim_frame_index = _pk->getVictim();
			int page_to_evict = _frame_table[victim_frame_index];
			// first unmap
			instr * _instr = new instr(2);
			_instr->instr_index = instr_index;
			_instr->virtual_page_index = page_to_evict;
			_instr->frame_index = victim_frame_index;
			instruction_list.push_back(_instr);
			_status.unmaps++;
			// check whether need to perform an out/ swap operation
			if (_page_table[page_to_evict].modified) {
				instr * _instr = new instr(4);
				_instr->instr_index = instr_index;
				_instr->virtual_page_index = page_to_evict;
				_instr->frame_index = victim_frame_index;
				instruction_list.push_back(_instr);
				_status.outs++;
				_page_table[page_to_evict].pageout = 1;
				_page_table[page_to_evict].modified = 0;
			}
			_page_table[page_to_evict].present = 0;
			// check whether we need to page in the new frame or perform a zero operation
			if (_page_table[virtual_page_index].pageout) {
				instr * _instr = new instr(3);
				_instr->instr_index = instr_index;
				_instr->virtual_page_index = virtual_page_index;
				_instr->frame_index = victim_frame_index;
				instruction_list.push_back(_instr);
				_status.ins++;
			} else {
				instr * _instr = new instr(5);
				_instr->instr_index = instr_index;
				_instr->frame_index = victim_frame_index;
				instruction_list.push_back(_instr);
				_status.zeros++;
			}
			_instr = new instr(1);
			_instr->instr_index = instr_index;
			_instr->virtual_page_index = virtual_page_index;
			_instr->frame_index = victim_frame_index;
			instruction_list.push_back(_instr);
			_status.maps++;
			_page_table[virtual_page_index].index_phy_frame =
					victim_frame_index;
			_frame_table[victim_frame_index] = virtual_page_index;
			// perform the instruction
			if (op_code) {
				_page_table[virtual_page_index].modified = 1;
			}
			_page_table[virtual_page_index].referenced = 1;
			_page_table[virtual_page_index].present = 1;
			_pk->addPhyPageToList(victim_frame_index);
			_pk->updateLRU_List(victim_frame_index);
		}
	}
}

void print_O_Result() {
	//list<instr*> instruction_list;
	list<instr*>::iterator iterator;
	for (iterator = instruction_list.begin();
			iterator != instruction_list.end(); ++iterator) {
		(*iterator)->printInstr();
	}
}
void print_FrameTable() {
	for (int i = 0; i < _num_phy_frame; i++) {
		if (i < _next_free_phy_frame) {
			cout << _frame_table[i] << " ";
		} else {
			cout << "* ";
		}
	}
	cout << endl;
}
void print_PageTable() {
	for (int i = 0; i < 64; i++) {
		if (_page_table[i].present == 0) {       // if PRESENT not set
			if (_page_table[i].pageout) {
				cout << "# ";
			} else {
				cout << "* ";
			}
		} else {                                // if PRESENT set
			cout << i << ":";
			if (_page_table[i].referenced) {
				cout << "R";
			} else {
				cout << "-";
			}
			if (_page_table[i].modified) {
				cout << "M";
			} else {
				cout << "-";
			}
			if (_page_table[i].pageout) {
				cout << "S";
			} else {
				cout << "-";
			}
			cout << " ";
		}
	}
	cout << endl;

}
void print_Sum() {
	_status.printStatus();
}

