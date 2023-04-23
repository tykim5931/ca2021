
#ifndef _NUM_H
#define _NUM_H


#include <stdio.h>
#include <string.h>

char* dem2bin(const int input, const int bitsize);
char* dem2hex(int dem);
char* bin2hex(const char* bin);
char* neg2sComp(const char* bin, const int bit);
	
#endif
