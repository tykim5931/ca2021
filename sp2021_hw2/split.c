#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string.h>


struct MetaData{
	int flen;
	char name[30];
};

int main(int argc, char** argv){
	
	char* ifname = argv[1];
	int key;
        sscanf(argv[2], "%d", &key);
	key = key&0xFF;	// key is from 0 to 255
	char* dirname = argv[3];
	mkdir(dirname, 0755);
	
	printf("key: 0x%x\n", key);
	printf("directory: %s\n", dirname);

	FILE *fp_merged = fopen(ifname, "rb");
	if(fp_merged == NULL){
		printf("Cannot Open Merged File\n");
		exit(0);
	}

	int ret = 0;	// for checking total byte read

	// read file for units of structures
	while(1){
		struct MetaData met;
		ret += fread(&met, sizeof(struct MetaData), 1, fp_merged);
		
		// end loop when it is end of file
		if(feof(fp_merged)) break;

		int flength = met.flen;
		char* ofname = met.name;
	
		// rename file to be in a directory
		char dir_ofname[100] = {0,};
		strcat(dir_ofname, dirname);
		strcat(dir_ofname, "/");
		strcat(dir_ofname, ofname);

		// open write file
		FILE *fp = fopen(dir_ofname, "wb");
		if(fp == NULL){
			printf("Cannot Open File [%s]\n", dir_ofname);
			exit(0);
		}

		// write to file
		int count = 0;
		int written = 0;
		unsigned char buff[65]={0,};
		while(count < flength-64){
			count += fread(buff, sizeof(char), 64, fp_merged);
			for(int j=0; j<65; ++j)
				buff[j] = buff[j]^key;
			written += fwrite(buff, sizeof(char), 64, fp);
		}
		
		while(count < flength){
			count += fread(buff, sizeof(char), 1, fp_merged);
			buff[0] = buff[0]^key;
			written += fwrite(buff, sizeof(char), 1, fp);
		}

		printf("written: %s, length: %d\n" , dir_ofname, written);

		count += fread(buff, sizeof(char), 1, fp_merged);
		ret += count;
		
		fclose(fp);
	}
	
	printf("Total %d bytes read from merged file\n", ret);
	fclose(fp_merged);

	return 0;
}
