#include <iostream>
#include <fstream>
#include <string>
#include <cstring>

#include "memory.h"
#include "pipeFunc.h"
#include "pipeRegs.h"


int PC = 0x400000;

int main(int argc, char* argv[]){

    // Create memory and register and PC at the very beginning of program.
    Memory::instance();
    Register::instance();

    // get options
    int br_pred = -1;	// 0 : always taken, 1 : always not taken
    int addr1 = 0;
    int addr2 = 0;
    int showregs = 0;
    int exec_num = -1;
    int showpipe = 0;

    for(int i = 0; i < argc; ++i){
	if(!strcmp(argv[i], "-atp") || !strcmp(argv[i], "-antp")){
		if(!strcmp(argv[i], "-atp"))
			br_pred = 0;
		else
			br_pred = 1;
	}else if(!strcmp(argv[i], "-m")){
	    sscanf(argv[i+1], "%x%*[:]%x", &addr1, &addr2);
	} else if(!strcmp(argv[i], "-d")){
	    showregs = 1;
	} else if(!strcmp(argv[i], "-n")){
	    sscanf(argv[i+1], "%d", &exec_num);
	} else if(!strcmp(argv[i], "-p")){
	    showpipe = 1;		
	}
    }

    // handle error
    if(br_pred == -1){
	    printf("Please give branch prediction option: -atp or -antp\n");
	    return 0;
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
    const int LASTPC = 0x400000 + imemsize;

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
     
    
    // Run Pipeline
    // create stall_cnt and Pipeline registers
    int stall = 0;
    IF_ID IF_ID={};
    ID_EX ID_EX={};
    EX_MEM EX_MEM={};
    MEM_WB MEM_WB={};

    char if_inst[10];
    char id_inst[10];
    char ex_inst[10];
    char mem_inst[10];
    char wb_inst[10];

    int cycle_count = 0;
    int instr_count = 0;
    int last_instr = 0;
    int wb_pc;

    while(1){
	    
	    // Forwarding
	    // EX/MEM to EX Forwarding(arith)
	    if( EX_MEM.MEM_SIG == 0 && 
		EX_MEM.WB_SIG != 0 && EX_MEM.WB_DEST != 0){
		    if(EX_MEM.WB_DEST == ID_EX.Rs)
			    ID_EX.ReadData1 = EX_MEM.ALU_OUT;	//ForwardA
		    if(EX_MEM.WB_DEST == ID_EX.Rt)
			    ID_EX.ReadData2 = EX_MEM.ALU_OUT;	//ForwardB
	    }
	    // MEM/WB to EX Forwarding(arith, load)
	    if(MEM_WB.WB_SIG != 0 && MEM_WB.WB_DEST != 0 
			    && MEM_WB.WB_DEST != EX_MEM.WB_DEST){
		    int forward;
		    if(MEM_WB.MEM_OUT == 0) 
			    forward = MEM_WB.ALU_OUT;	//arith
		    else 
			    forward = MEM_WB.MEM_OUT;	// load
		    if(MEM_WB.WB_DEST == ID_EX.Rs)
			   ID_EX.ReadData1 = forward;
		    if(MEM_WB.WB_DEST == ID_EX.Rt)
			   ID_EX.ReadData2 = forward; 
	    }
	    // MEM/WB to MEM Forwarding(load)
	    int Mf_val = 0;
	    if(MEM_WB.MEM_SIG != 0 && MEM_WB.WB_SIG != 0 && 
			EX_MEM.MEM_SIG != 0 && EX_MEM.WB_SIG == 0 &&
			MEM_WB.WB_DEST == EX_MEM.Rt){ // if store follows and use same regs
		    EX_MEM.Rt = -1;
		    Mf_val = MEM_WB.MEM_OUT;
	    }
	    

	    // 1 CYCLE execution
	    // WB
	    if(MEM_WB.NPC && MEM_WB.NPC != LASTPC){
		    sprintf(wb_inst, "0x%x", MEM_WB.NPC);
		    instr_count++;
	    } else 
		    wb_inst[0] = '\0';
	    wb_pc = MEM_WB.NPC;
	    write_back(&MEM_WB);
	    MEM_WB = {};


	    // MEM
	    if(EX_MEM.NPC && EX_MEM.NPC != LASTPC) 
		    sprintf(mem_inst, "0x%x", EX_MEM.NPC);
	    else 
		    mem_inst[0] = '\0';
	    mem_op(&EX_MEM, &MEM_WB, Mf_val);

	    // at MEM stage, check BEQ flush
	    if(EX_MEM.BR_TARGET != 0){
		    if(br_pred == 1 && EX_MEM.ALU_OUT == 1){	// always not taken & branch
			    stall = 3;
			    PC = EX_MEM.BR_TARGET;
		    } else if(br_pred == 0 && EX_MEM.ALU_OUT == 0){ // always taken & not branch
			    stall = 2;
			    PC = EX_MEM.NPC + 4;
		    }
	    }
	    EX_MEM = {};


	    // EX
	    if(ID_EX.NPC && ID_EX.NPC != LASTPC) 
		    sprintf(ex_inst, "0x%x", ID_EX.NPC);
	    else 
		    ex_inst[0] = '\0';
	    execute(&ID_EX, &EX_MEM);
	    ID_EX = {};


	    // ID
	    if(IF_ID.NPC && IF_ID.NPC != LASTPC) 
		    sprintf(id_inst, "0x%x", IF_ID.NPC);
	    else 
		    id_inst[0] = '\0';
	    decode(&IF_ID, &ID_EX);
	    
	    // Check STALL
	    // if branch & always taken, change PC and stall 1 cycle
	    if(ID_EX.BR_TARGET != 0 && br_pred == 0){
		    PC = ID_EX.BR_TARGET;
		    stall = 1;
	    } 
	    // IF Jump in ID stage, stall one cycle
	    if(ID_EX.JMP_SIG == 1){
		    PC = ID_EX.JMP_TARGET;
		    stall = 1;
	    }
	    IF_ID={};


	    // IF
	    if(last_instr){	// After fetching last instruction, stop fetching and hold PC
		    PC = LASTPC-4;
	    } else {
		    sprintf(if_inst, "0x%x", PC);
		    fetch(&IF_ID);
	    }
	    	    

	    // Data Hazard
	    // Load-Use Data Hazards
	    if(ID_EX.MEM_SIG != 0 && ID_EX.WB_SIG != 0){  // if ID/EX.MemRead(load)
		    if((ID_EX.Rt == ((IF_ID.INSTR)>>21)&0x1f) ||
			(ID_EX.Rt == ((IF_ID.INSTR)>>16)&0x1f))
			    stall = 1;
	    }
	    // Do stall if stall != 0;   
	    if(stall > 0){
		    if_inst[0] = '\0';
		    IF_ID={};
		    --stall;
		    if(stall>0){
			    id_inst[0] = '\0';
			    ID_EX = {};
			    --stall;
			    if(stall > 0){
				    ex_inst[0] = '\0';
				    EX_MEM = {};
				    --stall;
			    }
		    }
	    }else if(!stall) PC += 4;
	    

	    // After Finishing Last Instruction, Loop needs to be ended.
	    if(IF_ID.NPC == LASTPC){
		    last_instr = 1;
		    IF_ID.INSTR = 0;
		    if_inst[0] ='\0';
	    }
	    
	    if(wb_pc == LASTPC)
		    break;
	    else if(wb_pc == 0 && MEM_WB.NPC == LASTPC)
		    break;
	    if(exec_num != -1 && instr_count == exec_num+1)
		    break;

	    cycle_count++;

	    // After Fetching last PC, Pipeline should not fetch more instruction.
	    if(PC > LASTPC){
		    PC = LASTPC;
	    }


	    // Print Current Cycle's State
	    if(showpipe || showregs)
		printf("===== Cycle %d =====\n", cycle_count);
	    if(showpipe){
	    	printf("Current pipeline PC state:\n");
	    	printf("{%s|%s|%s|%s|%s}\n\n", if_inst,id_inst,ex_inst, mem_inst, wb_inst);
	    }
	    if(showregs){ 
	    	printf("Current register values:\n");
	    	printf("PC: 0x%x\n", PC);
	    	Register::instance().show();
		printf("\n");
    		if (addr1 || addr2){
			printf("Memory content [0x%x..0x%x]:\n", addr1, addr2);
			Memory::instance().show(addr1, addr2);
			printf("\n");
		}

	    }
    }
    
    // Print Final State
    cycle_count++;
    printf("===== Completion cycle: %d =====\n\n", cycle_count);
    
    printf("Current pipeline PC state:\n");
    printf("{%s|%s|%s|%s|%s}\n\n", if_inst,id_inst,ex_inst, mem_inst, wb_inst);
    
    printf("Current register values:\n");
    printf("PC: 0x%x\n", PC);
    Register::instance().show();
    printf("\n");
    
    if (addr1 || addr2){
	    printf("Memory content [0x%x..0x%x]:\n", addr1, addr2);
	    Memory::instance().show(addr1, addr2);
	    printf("\n");
    }
    return 0;
}
   
