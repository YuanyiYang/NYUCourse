/*
 * instr.h
 *
 *  Created on: Apr 8, 2015
 *      Author: yuanyiyang
 */

#ifndef INSTR_H_
#define INSTR_H_

struct instr {

	int i_type;
	int instr_index;
	int op_code;
	int virtual_page_index;
	int frame_index;

	instr(int i_type) {
		this->i_type = i_type;
		this->instr_index = 0;
		this->op_code = 0;
		this->virtual_page_index = 0;
		this->frame_index = 0;
	}

	void printInstr() {
		switch (i_type) {
		case 0:
			printf("==> inst: %d %d\n", op_code, virtual_page_index);
			break;
		case 1:
			printf("%d: MAP     %d   %d\n", instr_index, virtual_page_index,
					frame_index);
			break;
		case 2:
			printf("%d: UNMAP   %d   %d\n", instr_index, virtual_page_index,
					frame_index);
			break;
		case 3:
			printf("%d: IN      %d   %d\n", instr_index, virtual_page_index,
					frame_index);
			break;
		case 4:
			printf("%d: OUT    %d   %d\n", instr_index, virtual_page_index,
					frame_index);
			break;
		case 5:
			printf("%d: ZERO        %d\n", instr_index, frame_index);
			break;
		}
	}
};

#endif /* INSTR_H_ */
