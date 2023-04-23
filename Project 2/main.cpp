#include <iostream>
#include <fstream>
#include <string>
#include <cstring>

#include "memory.h"
#include "decoder.h"


int PC = 0x400000;

int main(int argc, char* argv[]){

    // Create memory and register and PC at the very beginning of program.
    Memory::instance();
    Register::instance();

    // get options
    int addr1 = 0;
    int addr2 = 0;
    int PrintPerInst = 0;
    int exec_num = -1;

    for(int i = 0; i < argc; ++i){
	if(!strcmp(argv[i], "-m")){
	    sscanf(argv[i+1], "%x%*[:]%x", &addr1, &addr2);
	} else if(!strcmp(argv[i], "-d")){
	    PrintPerInst = 1;
	} else if(!strcmp(argv[i], "-n")){
	    sscanf(argv[i+1], "%d", &exec_num);
	}
    }

    //read file using name argv[argc-1]
    char* name;
    name = argv[argc-1];
    std::ifstream fp(name);
    
    // check error
    if(!fp.is_open()) { 
	    std::cerr << "Could not open file" << std::endl;
	return EXIT_FAILURE;
    }

    // memory initialization
    int imemsize, dmemsize;
    std::string buff;
   
    std::getline(fp, buff);
    sscanf(buff.c_str(), "%x", &imemsize);	

    std::getline(fp, buff);
    sscanf(buff.c_str(), "%x", &dmemsize);

    Memory::instance().setMem(imemsize, dmemsize);
   
    // Save instruction and value to memory
    int addr = 0x400000;    // first address of instruction
    int loop_cnt = 0;
    int data;

    while(loop_cnt < (imemsize + dmemsize)/4){

	std::getline(fp, buff);
	sscanf(buff.c_str(), "%x", &data);

	if (loop_cnt == imemsize/4)
	    addr = 0x10000000;    // first address of data
	
	Memory::instance().writeMem(data, addr);

	addr += 4;
	loop_cnt++;
    }

    fp.close();
     
    
    // DECODE and EXECUTE
    int exec_count = 0;
    while(1){
	if(exec_count == exec_num) break;

	if(execute(PC)){    // PC will be changed in each execution
	    if (PrintPerInst){
		printf("Execution[%d]\n", exec_count+1);
    		printf("Current register values:\n");
    		printf("-------------------------------------\n");
		printf("PC: 0x%x\n", PC);
		Register::instance().show();
		if (addr1 || addr2){
			printf("\nMemory content [0x%x..0x%x]:\n", addr1, addr2);
			printf("-------------------------------------\n");
			Memory::instance().show(addr1, addr2);
			printf("\n");
		}
	    }
	    exec_count++;

	} else{ 
	    printf("Cannot Execute Instruction");
	    break;
	}

	if(PC >= 0x400000+imemsize) break;
    }
   

    // print results to console
    printf("Current register values:\n");
    printf("-------------------------------------\n");
    printf("PC: 0x%x\n", PC);
    Register::instance().show();
    
    printf("\nMemory content [0x%x..0x%x]:\n", addr1, addr2);
    printf("-------------------------------------\n");
    Memory::instance().show(addr1, addr2);

    return 0;
}
