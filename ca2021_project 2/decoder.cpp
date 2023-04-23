#include "memory.h"
#include "decoder.h"


extern int PC;

int sign_extend(int num, int bitsize){
	int ans_32;
	if((num>>(bitsize-1)&0x01) == 1){
		int masker = 0xffffffff;
		ans_32 = ((masker >> bitsize) << bitsize) | num;
		
	} else ans_32 = num;

	return ans_32;
}

void rExec(int op, int rs, int rt, int rd, int shamt, int funct){
	// increase PC
	PC += 4;

	// read rs and rt from register.
	rs = Register::instance().readRegs(rs);
	rt = Register::instance().readRegs(rt);

	// Do the proper arithmetic according to funct
	if(funct == 0x21)    // ADDU
		Register::instance().writeRegs(rs+rt, rd);
	else if(funct == 0x24)    // AND
		Register::instance().writeRegs(rs&rt, rd);
	else if(funct == 0x27)    // NOR
		Register::instance().writeRegs(~(rs|rt), rd);
	else if(funct == 0x25)    // OR
		Register::instance().writeRegs(rs|rt, rd);
	else if(funct == 0x2b){    // SLTU
		if(rs < rt) Register::instance().writeRegs(1, rd);
		else Register::instance().writeRegs(0, rd);
	}
	else if(funct == 0)	// SLL
		Register::instance().writeRegs(rt<<shamt, rd);
	else if(funct == 2)	// SRL
		Register::instance().writeRegs(rt>>shamt, rd);
	else if(funct == 0x23)	// SUBU
		Register::instance().writeRegs(rs-rt, rd);
	else if(funct == 8)	// JR
		PC = rs;
	return;
}

void jExec(int op, int target){
	// increase PC
	PC += 4;

	int msb_4 = (PC>>28) & 0xf;
	// Do the proper jump operation
	if(op == 2)
		PC = (msb_4 << 28) | (target << 2);
	if(op==3){	// JAL. write PC to $ra and jump
		Register::instance().writeRegs(PC, 31);
		PC = (msb_4 << 28) | (target << 2);
	}
	return;
}

void iExec(int op, int rs, int rt, int offset){
	// increase PC
	PC += 4;

	// Read rs from register
	rs = Register::instance().readRegs(rs);

	// Do proper operations
	if(op==9){	// ADDIU
		int offset_ex = sign_extend(offset, 16);
		Register::instance().writeRegs(rs + offset_ex, rt);
	}else if(op == 0xc){	// ANDI
		Register::instance().writeRegs(rs & offset, rt);
	}else if(op == 0xd){	// ORI
		Register::instance().writeRegs(rs | offset, rt);
	}else if(op == 4){	// BEQ
		rt = Register::instance().readRegs(rt);
		if(rs == rt)
			PC = PC + (offset * 4);
		else return;
	}else if(op==5){	// BNE
		rt = Register::instance().readRegs(rt);
		if(rs != rt)
			PC = PC + (offset*4);
		else return;
	}else if(op == 0xb){	//SLTIU
		if(rs < sign_extend(offset, 16))
			Register::instance().writeRegs(1, rt);
		else
			Register::instance().writeRegs(0, rt);
	}else if(op==0xf){	// LUI
		Register::instance().writeRegs(offset << 16, rt);
	}else if(op==0x23){	// LW
		int addr = rs + offset;
		int val = Memory::instance().readMem(addr);
		Register::instance().writeRegs(val, rt);
	}else if(op == 0x20){	// LB
		int addr = rs + offset;
		int val = Memory::instance().readMem(addr, 1);
		Register::instance().writeRegs(sign_extend(val, 8), rt);
	}else if(op == 0x2b){	// SW
		int addr = rs + offset;
		int val = Register::instance().readRegs(rt);
		Memory::instance().writeMem(val, addr);
	}else if(op == 0x28){	// SB
		int addr = rs+offset;
		int val = Register::instance().readRegs(rt);
		Memory::instance().writeMem(val & 0xFF, addr, 1);
	}
	return;
}


int execute(int PC){
    int instr = Memory::instance().readMem(PC);
    int op = (instr>>26) & 0x3f;
    
    if (op == 0){
	int rs = (instr>>21) & 0x1f;
	int rt = (instr>>16) & 0x1f;
	int rd = (instr>>11) & 0x1f;
	int shamt = (instr>>6) & 0x1f;
	int funct = instr & 0x3f;
	rExec(op, rs, rt, rd, shamt, funct);
    }
    else if(op == 2 || op == 3){
	int target = instr & 0x3ffffff;
	jExec(op, target);
    }
    else{
	int rs = (instr>>21) & 0x1f;
	int rt = (instr>>16) & 0x1f;
	int offset = instr & 0xffff;
	iExec(op, rs, rt, offset);
    }
    return 1;
}



