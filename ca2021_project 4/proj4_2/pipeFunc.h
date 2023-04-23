#ifndef PIPEFUNC
#define PIPEFUNC



int sign_extend(int num, int bits);

int fetch(struct IF_ID* IF_ID);

void decode(struct IF_ID* IF_ID, struct ID_EX* ID_EX);

void execute(struct ID_EX* ID_EX, struct EX_MEM* EX_MEM);

int mem_op(struct EX_MEM* EX_MEM, struct MEM_WB* MEM_WB, int f_val = 0);

void write_back(struct MEM_WB* MEM_WB);



#endif
