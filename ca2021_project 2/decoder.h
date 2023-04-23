#ifndef DECODER
#define DECODER


int sign_extend(int num, int bits);
void rExec(int op, int rs, int rt, int shamt, int funct);
void jExec(int op, int target);
void iExec(int op, int rs, int rt, int offset);

int execute(int PC);

#endif
