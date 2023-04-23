#ifndef PIPEREGS
#define PIPEREGS


struct IF_ID{
	int INSTR;
	int NPC;
};

struct ID_EX{
	int NPC;

	int Rs;
	int Rt;
	int Rd;
	int Immd;
	int Shamt;
	int JMP_TARGET;
	int WB_DEST;

	int ReadData1;
	int ReadData2;

	int ALU_SIG;	// -1 for ALU not used, other for ALU used
	int WB_SIG;	// 0 or 1
	int MEM_SIG;	// 0 or 1(word) or 2(byte)
	int JMP_SIG;	// 0 or 1
	int BR_TARGET;	// target to branch
};

struct EX_MEM{
	int NPC;

	int Rt;		// for store operation
	int WB_DEST;	// register number to write back. rd or rt
	int ALU_OUT;	// output value of ALU
	int JMP_TARGET;

	int MEM_SIG;	// control signal for mem stage
	int WB_SIG;	// control signal for wb satge
	int BR_TARGET;	// target to branch
};

struct MEM_WB{
	int NPC;

	int WB_DEST;
	int ALU_OUT;
	int JMP_TARGET;
	int MEM_OUT;

	int WB_SIG;
	int MEM_SIG;
};


#endif
