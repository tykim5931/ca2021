
#ifndef _INST_H
#define _INST_H


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <queue>
#include <array>
#include <list>
#include <map>
#include <ctype.h>
#include "modNum.h"


// map that contains labels from assembly file
extern std::map<std::string,int> Labels;

std::string RmakeBin(const char* inst, const char* oper);
std::string ImakeBin(const char* inst, const char* oper, int current_addr);
std::string JmakeBin(const char* inst, const char* oper);
std::array<std::string,2> laInst(const char* inst);
std::string getInstruction(const char* inst, const char* oper, int address);
void modPseudo(std::list<std::string> codeList, std::string laCode,
		std::list<std::string>::iterator iter);
	
	
#endif
