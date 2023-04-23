#include "modNum.h"


char* dem2bin(const int input, const int bitsize){
	static char bin[27];
	int dem = input;
	int rem = 0;	// remainder	
	int pos = 0;
	char temp[30] = {0,};	// temporory string to hold hexademical

	while (dem != 0){
		rem = dem % 2;
		if(rem == 0) temp[pos++] = '0';
		else temp[pos++] = '1';
		dem /= 2;
	}

	// Reverse String
	int s_length = strlen(temp);
	int zeros = bitsize-s_length;
	int i;
	for (i = 0; i<zeros; i++){
		bin[i] = '0';
	}
	for (i = 0; i < s_length; i++){
		bin[i+zeros] = temp[s_length-i-1];
	}
	bin[i+zeros] ='\0';

	return bin;
}

char* dem2hex(int dem){
	static char hexa[11];
	sprintf(hexa, "0x%x", dem);

	return hexa;
}

char* bin2hex(const char* bin){
	static char hexa[11];
	int num=0;
	for (int i = 0; bin[i] != 0; i++){
		// put lsb to num 1st and sum with keep multiplying by 2.
		num = (num<<1) + bin[i] - '0';
	}
	sprintf(hexa,"0x%x",num);
	return hexa;
}

char* neg2sComp(const char* bin, const int bit){
	
	static char neg[17];
	for(int i = 0; i < bit; i++){
		if(bin[i]=='0') neg[i] = '1';
		else neg[i] = '0';
	}
	int j = 1;
	while(neg[bit-j] != '0'){
		j++;
	}
	neg[bit-j] = '1';
	neg[bit] = '\0';
	return neg;
}
