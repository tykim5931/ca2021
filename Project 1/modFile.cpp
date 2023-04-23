#include "modFile.h"


std::list<std::string> getFileList(char* name){
	FILE *fp;
	int line = 0;
	char buff[100];
	static std::list<std::string> fileLines;

	// Handle error
	if(fp == NULL){
		printf("Wrong File Name!\n");
		exit(1);
	}

	fp = fopen(name, "r");
	while(fgets(buff, sizeof(buff), fp) != NULL)
		fileLines.push_back(buff);

	fclose(fp);
	return fileLines;
}


