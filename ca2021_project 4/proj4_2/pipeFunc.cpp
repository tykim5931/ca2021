#include "memory.h"
#include "pipeFunc.h"
#include "pipeRegs.h"
#include "cache.h"
#include <list>

//===============External variables==========
extern int PC;

extern std::list<int> l1_i;
extern std::list<int> l1_d;
extern std::list<int> l2;

extern int capacity;
extern int replacement_plcy;

extern int l1_i_r_miss;
extern int l1_d_r_miss;
extern int l1_i_w_miss;
extern int l1_d_w_miss;

extern int l2_r_miss;
extern int l2_w_miss;

extern int i_r_access;
extern int d_r_access;
extern int w_access;

extern int l1_clean_evict;
extern int l1_dirty_evict;
extern int l2_clean_evict;
extern int l2_dirty_evict;


//=============Math Utility Function===========================
int sign_extend(int num, int bitsize){
	int ans_32;
	if((num>>(bitsize-1)&0x01) == 1){
		int masker = 0xffffffff;
		ans_32 = ((masker >> bitsize) << bitsize) | num;
		
	} else ans_32 = num;

	return ans_32;
}

//============Function for capacity call======================

int cache_check(int wrmode, int l1, int l2, int addr, int capacity){

	// Set variables
	
	int* access;
	int* l1_miss;
	int* l2_miss;

	if(l1 == 0){	// l1_I access
		access = &i_r_access;
		l1_miss = &l1_i_r_miss;
		l2_miss = &l2_r_miss;

	} else{		// l1_D access
		if(wrmode == 0){	// Read
			access = &d_r_access;
			l1_miss = &l1_d_r_miss;
			l2_miss = &l2_r_miss;
		}
		else{			// Write
			access = &w_access;
			l1_miss = &l1_d_w_miss;
			l2_miss = &l2_w_miss;
		}
	}
		
	       	
	if(cache_find(l1, addr)){	// L1 hit
		(*access)++;
		if(wrmode)
			set_dirty(l1,(addr>>4)<<1);
		return 0;
	}

	else{
		if(cache_find(l2, addr)){	// L2 hit
			(*access)++;
			(*l1_miss)++;
		
			if(wrmode)
				set_dirty(l2,(addr>>4)<<1);

			int evicted = cache_update(l1, (addr>>4)<<1, replacement_plcy, capacity>>10);

			if(evicted){
				if(evicted&0x01){
					l1_dirty_evict++;
					set_dirty(l2, evicted);
				}
				else	l1_clean_evict++;
			}
			return 9;
		}
		else{
			(*access)++;
			(*l1_miss)++;
			(*l2_miss)++;

			int evicted = cache_update(l2, (addr>>4)<<1, replacement_plcy, capacity>>6);
			int evicted_l1 = cache_update(l1, (addr>>4)<<1, replacement_plcy, capacity>>10);
			if(cache_find(l1, (evicted>>1)<<4)){
				cache_evict(l1, evicted);
				if(evicted&0x01) l1_dirty_evict++;
				else l1_clean_evict++;
			}
			if(evicted){
				if(evicted&0x01) l2_dirty_evict++;
				else l2_clean_evict++;
			}
			if(evicted_l1){
				if(evicted_l1 & 0x01) l1_dirty_evict++;
				else l1_clean_evict++;
			}
			return 99;
		}
	}

}

// Function for IF stage
int fetch(struct IF_ID* IF_ID){
	IF_ID -> NPC = PC;
	IF_ID -> INSTR = Memory::instance().readMem(PC);
	
	int stall = cache_check(0, 0, 1, PC, capacity);
	return stall;
}


// Function for ID stage
void decode(struct IF_ID* IF_ID, struct ID_EX* ID_EX){
    if(IF_ID->NPC == 0)
	return;
    else{
	// Pass stage regs info
	ID_EX->NPC = IF_ID->NPC;
	
	// Decode instruction
	int instr = IF_ID->INSTR;
	int op = (instr>>26) & 0x3f;
	int funct = instr & 0x3f;

	// set ID_EX components
	ID_EX -> Rs = (instr>>21) & 0x1f;
	ID_EX -> Rt = (instr>>16) & 0x1f;
	ID_EX -> Rd = (instr>>11) & 0x1f;
	ID_EX -> Shamt = (instr>>6) & 0x1f;
	ID_EX -> Immd = instr & 0xffff;

	ID_EX -> ReadData1 = Register::instance().readRegs(ID_EX -> Rs);
	ID_EX -> ReadData2 = Register::instance().readRegs(ID_EX -> Rt);

	// Make Signal
	if((op == 2) || (op == 3) || ((op==0)&&(funct==8)))
	{	// J or JAL or JR
		ID_EX->JMP_SIG = 1;
		ID_EX -> JMP_TARGET = ((ID_EX->NPC >> 28) << 28) | ((instr & 0x3ffffff) << 2);
		if(op == 3){	// IF JAL, WB occurs
			ID_EX -> WB_DEST = 31;
			ID_EX -> WB_SIG = 1;	
		}if((op==0) && (funct == 8))	// JR
			ID_EX -> JMP_TARGET = ID_EX -> ReadData1;
		return;
	}
	else if((op==0x23) || (op==0x20) || (op==0x2b) || (op==0x28))
	{	// Load and Store Instruction
		ID_EX -> ALU_SIG = 0x28;
		ID_EX -> MEM_SIG = 1;
	
		if((op == 0x23) || (op==0x20)){	// Load requires writeback
			ID_EX -> WB_SIG = 1;
			ID_EX -> WB_DEST = ID_EX -> Rt;
		}
	
		if((op==0x20)||(op==0x28)) ID_EX -> MEM_SIG = 2;    // Bytes memOp
		return;
	}
	else if((op==4) || (op==5))
	{	// BEQ or BNE
		ID_EX -> ALU_SIG = op;
		ID_EX->BR_TARGET = ID_EX->NPC+4+(ID_EX->Immd)*4;
		return;
	}
	
	// Instructions that commonly needs writeback and alu signal
	ID_EX -> WB_SIG = 1;
	if(op==0){
		ID_EX -> WB_DEST = ID_EX -> Rd;
		ID_EX -> ALU_SIG = funct;
		if(funct == 0) //SLL
			ID_EX -> ALU_SIG = 1;
		return;
	}
	if((op==9) || (op==0xb))	// ADDIU,SLTIU need sign extension
		ID_EX->Immd = sign_extend(ID_EX->Immd, 16);
	ID_EX -> WB_DEST = ID_EX -> Rt;
	ID_EX -> WB_SIG = 1;
	ID_EX -> ALU_SIG = op;
    }
    return;
}


// Function for EX stage
void execute(struct ID_EX* ID_EX, struct EX_MEM* EX_MEM){
    // Pass stage regs info
    EX_MEM->NPC = ID_EX->NPC;
    EX_MEM->Rt = ID_EX->Rt; 
    EX_MEM->WB_DEST = ID_EX->WB_DEST;
    EX_MEM->JMP_TARGET = ID_EX->JMP_TARGET;
    EX_MEM->BR_TARGET = ID_EX->BR_TARGET;
    EX_MEM->MEM_SIG = ID_EX->MEM_SIG;
    EX_MEM->WB_SIG = ID_EX->WB_SIG;

    // Do ALU execution
    if(ID_EX->ALU_SIG == 0)	// no arithmetic operation(jump)
	    return;
    else{
	int sig = ID_EX->ALU_SIG;
	if(sig == 0x21)    // ADDU
		EX_MEM->ALU_OUT = ((ID_EX -> ReadData1) + (ID_EX -> ReadData2));
	else if(sig == 0x24)    // AND
		EX_MEM->ALU_OUT = ((ID_EX -> ReadData1) & (ID_EX -> ReadData2));
	else if(sig == 0x27)    // NOR
		EX_MEM->ALU_OUT = ~((ID_EX -> ReadData1) | (ID_EX -> ReadData2));
	else if(sig == 0x25)    // OR
		EX_MEM->ALU_OUT = ((ID_EX -> ReadData1) | (ID_EX -> ReadData2));
	else if(sig == 0x2b)    // SLTU
		EX_MEM->ALU_OUT = ((ID_EX -> ReadData1) < (ID_EX -> ReadData2));
	else if(sig == 1)	// SLL
		EX_MEM->ALU_OUT = (ID_EX -> ReadData2) << (ID_EX -> Shamt);
	else if(sig == 2)	// SRL
		EX_MEM->ALU_OUT = (ID_EX -> ReadData2) >> (ID_EX -> Shamt);
	else if(sig == 0x23)	// SUBU
		EX_MEM->ALU_OUT = (ID_EX -> ReadData1) - (ID_EX -> ReadData2);
	else if(sig == 9)	// ADDIU
		EX_MEM->ALU_OUT = (ID_EX -> ReadData1) + (ID_EX -> Immd);
	else if(sig == 0xc)	// ANDI
		EX_MEM->ALU_OUT = (ID_EX -> ReadData1) & (ID_EX -> Immd);
	else if(sig == 0xd)	// ORI
		EX_MEM->ALU_OUT = (ID_EX -> ReadData1) | (ID_EX -> Immd);
	else if(sig == 4)	// BEQ
		EX_MEM->ALU_OUT = ((ID_EX -> ReadData1) == (ID_EX -> ReadData2));
	else if(sig == 5)	// BNE
		EX_MEM->ALU_OUT = ((ID_EX -> ReadData1) != (ID_EX -> ReadData2));
	else if(sig == 0xb)	// SLTIU
		EX_MEM->ALU_OUT = ((ID_EX -> ReadData1) < (ID_EX -> Immd));
	else if(sig == 0xf)	// LUI
		EX_MEM->ALU_OUT = ((ID_EX -> Immd) << 16);
	else if(sig == 0x28){	// LW LB SW SB: calc addr
		EX_MEM->ALU_OUT = (ID_EX -> ReadData1) + (ID_EX -> Immd);
	}
    }
    return;
}


int mem_op(struct EX_MEM* EX_MEM, struct MEM_WB* MEM_WB, int f_val){
    // Pass Stage Regs Info
    MEM_WB->NPC = EX_MEM->NPC;
    MEM_WB->WB_DEST = EX_MEM->WB_DEST;
    MEM_WB->ALU_OUT = EX_MEM->ALU_OUT;
    MEM_WB->JMP_TARGET = EX_MEM->JMP_TARGET;
    MEM_WB->MEM_SIG = EX_MEM->MEM_SIG;
    MEM_WB->WB_SIG = EX_MEM->WB_SIG;

    int stall=0;

    // Load/Store from/to Memory
    if(!(EX_MEM->MEM_SIG))
	return 0;
    else{
	if(EX_MEM->WB_SIG){		// load
	    int addr = EX_MEM->ALU_OUT;
	    if(EX_MEM->MEM_SIG==1)	// LW
		MEM_WB->MEM_OUT = Memory::instance().readMem(addr);
	    else{			// LB
		MEM_WB->MEM_OUT = Memory::instance().readMem(addr, 1);
		MEM_WB->MEM_OUT = sign_extend(MEM_WB->MEM_OUT, 8);//sign extend
	    }

	    stall = cache_check(0, 2, 1, addr, capacity);
	}

	else{			// store
	    int val;
	    int addr = EX_MEM -> ALU_OUT;
	    if(EX_MEM->MEM_SIG==1){	// SW
		    if(EX_MEM->Rt < 0)
			    val = f_val;
		    else
			    val = Memory::instance().readMem(EX_MEM->Rt);
		    Memory::instance().writeMem(val, addr);
	    } else {			// SB
	            if(EX_MEM->Rt < 0)
			    val = f_val;
		    else
			    val = Memory::instance().readMem(EX_MEM->Rt, 1);
		    Memory::instance().writeMem(val&0xFF, addr, 1);
	    }

	    stall = cache_check(1, 2, 1, addr, capacity);
	}
	return stall;
    }
}

void write_back(struct MEM_WB* MEM_WB){
	if(!(MEM_WB->WB_SIG))
		return;
	else{
		if(MEM_WB->JMP_TARGET != 0){
			Register::instance().writeRegs(MEM_WB->NPC+4,
							MEM_WB->WB_DEST);
		}
		else if(MEM_WB->MEM_SIG){
			Register::instance().writeRegs(MEM_WB->MEM_OUT,
							MEM_WB->WB_DEST);
		}
		else{
			Register::instance().writeRegs(MEM_WB->ALU_OUT,
							MEM_WB->WB_DEST);
		}
	}
	return;
}




