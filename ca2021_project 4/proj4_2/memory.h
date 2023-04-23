#ifndef MEMORY
#define MEMORY

#include <stdio.h>
#include <cstdlib>

class Memory{
    private:
	int instrFirst = 0x400000;
	int dataFirst = 0x10000000;
	int instrEnd;
	int dataEnd;

	int *iMem;
	int *dMem;

	Memory();
	~Memory();

    public:
	static Memory& instance();

	void setMem(int imemsize, int dmemsize);
	void writeMem(int data, int addr, int byte = 4);
	int readMem(int addr, int byte = 4);
	void show(int addr1, int addr2);
};


class Register{
    private:
	int regs[32] = {0,};
	Register();
	~Register();

    public:
        static Register& instance();

	void writeRegs(int data, int num);
	int readRegs(int num);
	void show();
};

#endif
