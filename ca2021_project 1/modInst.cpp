#include "modInst.h"


std::map<std::string,int> Labels;

// map contains operation code and its 6bit opcode
std::map<std::string, const char*> Rmap = {
	{"addu","000000 100001"},	// 0 0x21
	{"and","000000 100100"},	// 0 0x24
	{"jr", "000000 001000"},	// 0 8
	{"nor","000000 100111"},	// 0 0x27
	{"or", "000000 100101"},	// 0 0x25
	{"sltu", "000000 101011"},	// 0 0x2b
	{"sll","000000 000000"},	// 0 0
	{"srl","000000 000010"},	// 0 2
	{"subu","000000 100011"}	// 0 0x23
};
std::map<std::string, const char*> Imap = {
	{"addiu", "001001"},	// 9
	{"andi", "001100"},	// 0xc
	{"beq", "000100"},	// 4
	{"bne", "000101"},	// 5
	{"lui", "001111"},	// 0xf
	{"lw", "100011"},	// 0x23
	{"ori", "001101"},	// 0xd
	{"sltiu", "001011"},	// 0xb
	{"sw", "101011"},	// 0x2b
	{"lb", "100000"},	// 0x20
	{"sb", "101000"}	// 0x28
};
std::map<std::string, const char*> Jmap = {
	{"j", "000010"},	//2
	{"jal","000011"}	//3
};

std::string RmakeBin(const char* inst, const char* oper){
	
	char op[7];
	char funct[7];
	int rs = 0;
	int rt = 0;
	int rd = 0;
	int shamt = 0;		
	std::string bincode;

	// get parts of instruction
	sscanf(Rmap[oper],"%s%s",op,funct);

	if (!strcmp(oper, "jr"))
		sscanf(inst, "%*[^$]$%d",&rs);	
	else if (!strcmp(oper,"sll") || !strcmp(oper, "srl"))
		sscanf(inst, "%*[^$]$%d %*[^$]$%d %*s%d",&rd,&rt,&shamt);
	else
		sscanf(inst, "%*[^$]$%d %*[^$]$%d %*[^$]$%d",&rd,&rs,&rt);
	
	// Create Binary Code
	std::string op_str = op;
	std::string rs_str = dem2bin(rs, 5);
	std::string rt_str = dem2bin(rt, 5);
	std::string rd_str = dem2bin(rd, 5);
	std::string shamt_str = dem2bin(shamt, 5);
	std::string funct_str = funct;

	bincode = op + rs_str + rt_str + rd_str + shamt_str + funct_str; 

	return bin2hex(bincode.c_str());
}


std::string ImakeBin(const char* inst, const char* oper, int current_addr){
	
	char op[7];
	char label[17];	
	int offset = 0;
	int rs = 0;
	int rt = 0;
	std::string bincode;

	// get parts of instruction
	sscanf(Imap[oper], "%s", op);
     
	if (!strcmp(oper, "bne") || !strcmp(oper, "beq")){
		sscanf(inst, "%*[^$]$%d %*[^$]$%d %*s%s", &rs, &rt, label);
		offset = (Labels[label] - current_addr - 4)/4;	// operate offset
	
	}else if (!strcmp(oper, "lui")){			
		sscanf(inst, "%*[^$]$%d %*s%x", &rt, &offset);

	}else if (!strcmp(oper, "lw") || !strcmp(oper, "sw") ||
		  !strcmp(oper, "lb") || !strcmp(oper, "sb")) {	
		sscanf(inst, "%*[^$]$%d %*s%d %*[^$]$%d", &rt, &offset, &rs);
	
	}else {							
		sscanf(inst, "%*[^$]$%d %*[^$]$%d %*s%s",&rt,&rs, label);
		if(strstr(label, "0x") !=NULL)	// if immediate is hexademical
			sscanf(label, "%x", &offset);
		else if(isalpha(label[0]))	// if immediate is given by label of data
			offset = (Labels[label] - current_addr - 4)/4;
		else	offset = atoi(label);	// if immediate is demical
	}
	
	// Create Binary Code
	std::string op_str = op;
	std::string rs_str = dem2bin(rs, 5);
	std::string rt_str = dem2bin(rt, 5);
	
	// if offset is negative, change it to 16bit negative by 2's complement
	if (strstr(label, "-") != NULL)	{	
		std::string offs_str = neg2sComp(dem2bin(offset, 16),16);
		bincode = op_str + rs_str + rt_str + offs_str;
	} else{
		std::string offs_str = dem2bin(offset, 16);
		bincode = op_str + rs_str + rt_str + offs_str;
	}
		
	return bin2hex(bincode.c_str());
}


std::string JmakeBin(const char* inst, const char* oper){
	
	char op[7];
	char target[27];
	int addr=0;
	std::string bincode;

	// get parts of instruction
	sscanf(Jmap[oper], "%s", op);
	if(strstr(inst, ":") != NULL) 
		sscanf(inst, "%*[^:]:%*s%s", target);
	else 
		sscanf(inst, "%*s%s", target);
	addr = Labels[target]/4;	// find target address from Label map & /4
	
	// Create Binary Code
	std::string op_str = op;
	std::string addr_str = dem2bin(addr, 26);
	bincode = op_str + addr_str;	

	return bin2hex(bincode.c_str());
}

std::array<std::string,2> laInst(const char* inst){
	int rt = 0;
	char label[20];
	int addr=0;
	int hex_0x10000 = 65536;
	
	static std::array<std::string,2> instArr;
	char modified[33];

	sscanf(inst, "%*[^$]$%d%*s%s", &rt, label);
	addr = Labels[label];
	
	sprintf(modified, "lui  $%d, 0x%x", rt, addr/hex_0x10000);
	instArr[0] = modified;

	// if 0x1000 0000, divided by 16^4 => no remaining
	if(addr % hex_0x10000 == 0){
		instArr[1] = '\n';
	}	
	else{
		sprintf(modified, "ori  $%d, $%d, 0x%x", rt, rt, addr%hex_0x10000);
		instArr[1] = modified;
	}
	return instArr;
}

std::string getInstruction(const char* inst, const char* oper, int address){
	// return hexademical code of text
	if(Rmap.find(oper) != Rmap.end())
		return RmakeBin(inst,oper);
	else if(Imap.find(oper) != Imap.end())
		return ImakeBin(inst, oper, address);
	else if(Jmap.find(oper) != Jmap.end())
		return JmakeBin(inst, oper);
	else
		return "Something wrong!";
}


void modPseudo(std::list<std::string> codeList, std::string laCode,
		std::list<std::string>::iterator iter){
	
	std::array<std::string,2>instarr = laInst(laCode.c_str());
	codeList.insert(iter, instarr.at(0));
	
	if(instarr.size()==2){
		codeList.insert(iter, instarr.at(1));
	}
	codeList.erase(iter);
}

