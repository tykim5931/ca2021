#include "memory.h"
#include "decoder.h"

Memory::Memory(){}

Memory::~Memory(){
	free(iMem);
	free(dMem);
}

Memory& Memory::instance(){
	static Memory* instance = new Memory();
	return *instance;
}

void Memory::setMem(int imemsize, int dmemsize){

	instrEnd = instrFirst + imemsize;
	dataEnd = dataFirst + dmemsize;
	
	iMem = (int*)malloc(sizeof(int) * imemsize);
	dMem = (int*)malloc(sizeof(int) * dmemsize);
	for(int i = 0; i <= instrEnd-instrFirst+1; i++)
		iMem[i]=0;
	for(int i = 0; i <= dataEnd - dataFirst+1; i++)
		dMem[i]=0;
}

void Memory::writeMem(int data, int addr, int byte){

	if(addr >= 0x10000000){
		// if addr is out of bound, reset dMem
		if(addr > dataEnd-4){
			int newsize = addr - instrFirst + 4;
			dMem = (int*)realloc(dMem, sizeof(int)*newsize);
			for(int i = dataEnd; i < addr; i+=4){
				dMem[i-dataFirst] = 0;
			}
			dataEnd = addr+4;
		}

		addr = addr - dataFirst;
		if(data < 0){	// if data is smaller than 0, sign extend it
			int bitsize;
			for(int i=31; i>=0; --i){
				if(((data>>i) & 0x01) == 1){
				bitsize = i+1;
				break;
				}
			}
			sign_extend(data, bitsize);
		}
		if(byte == 1){	// if byte==1, store 1 byte
			dMem[addr] = data;
			return;
		}else{
			for(int i = 0; i < byte; ++i)
				dMem[addr+i] = (data >> (24 - 8*i)) & 0xFF;
		}

	} else{
		addr = addr - instrFirst;
		for(int i = 0; i < byte; ++i){
			iMem[addr+i] = (data >> (24 - 8*i)) & 0xFF;
		}
	}
	return;
}

int Memory::readMem(int addr, int byte){
	// if address is not valid, return 0
	if(addr<instrFirst || (addr>instrEnd-4 && addr<dataFirst) || addr>dataEnd-4){
		return 0;
	}
	int value = 0;
	if(addr >= 0x10000000){
		addr = addr - dataFirst;
		if(byte == 1){
			value += dMem[addr];
			return value;
		}
		for(int i = 0; i < byte; ++i)
			value += (dMem[addr+i] << (24 - 8*i));
	} else{
		addr = addr - instrFirst;
		for(int i = 0; i < byte; ++i)
			value += (iMem[addr+i] << (24 - 8*i));
	}
	return value;
}

void Memory::show(int addr1, int addr2){
	int addr = addr1;
	while(addr <= addr2){
		printf("0x%x: 0x%x\n", addr, this->readMem(addr));
		addr += 4;
	
	}
}



// Here implements Constructor and methods of registers
Register::Register(){}

Register& Register::instance(){
	static Register* instance = new Register();
	return *instance;
}

void Register::writeRegs(int data, int num){
	if(data < 0){	// if data is smaller than 0, sign extend it
		int bitsize;
		for(int i=31; i>=0; --i){
			if(((data>>i) & 0x01) == 1){
				bitsize = i+1;
				break;
			}
		}
		sign_extend(data, bitsize);
	}
	regs[num] = data;
}

int Register::readRegs(int num){
	return regs[num];
}

void Register::show(){
	printf("Registers:\n");
	for(int i = 0; i < 32; ++i)
		printf("R%d: 0x%x\n", i, regs[i]);
}
