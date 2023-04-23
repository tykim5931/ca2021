#include <stdio.h>
#include <stdlib.h>


struct MetaData{
	int flen;
	char name[30];
};

int main(int argc, char** argv){
	char* ofname = argv[1];
	int key;
        sscanf(argv[2], "%d", &key);
	key = key&0xFF;	// key is from 0 to 255

	printf("key: 0x%x\n", key);
	
	// create file for output
	FILE *fp_merged = fopen(ofname, "wb");
	if(fp_merged == NULL){
		printf("Cannot Open Write File\n");
		exit(0);
	}

	int written=0;
	char* ifname;
	for(int i = 3; i < argc; ++i){
		ifname = argv[i];
		// open file
		FILE* fp = fopen(ifname, "rb");
		if(fp == NULL){
			printf("Cannot Open File");
			exit(0);
		}

		// get file length to write data structure for metadata
		fseek(fp, 0, SEEK_END);
		int flength = ftell(fp);	
		struct MetaData met;
		
		met.flen = flength;
		
		int i;
		for(i=0; ifname[i] != '\0'; i++)
			met.name[i] = ifname[i];
		met.name[i] = '\0';

		written += fwrite(&met, sizeof(struct MetaData), 1, fp_merged);	
		
		// return read file pointer to start
		fseek(fp, 0, SEEK_SET);

		int count = 0;
		unsigned char buff[65]={0,};
		while(count < flength-64){
			count += fread(buff, sizeof(char), 64, fp);
			for(int j=0; j<65; ++j)
				buff[j] = buff[j]^key;
			written += fwrite(buff, sizeof(char), 64, fp_merged);
		}
		
		// read by bytes and xor with key, then write to merge file
		while(!feof(fp)){
			count += fread(buff, sizeof(char), 1, fp);
			for(int j=0; j<1; ++j)
				buff[j] = buff[j]^key;
			written += fwrite(buff, sizeof(char), 1, fp_merged);
		}


		fclose(fp);
		printf("writing: %s, length: %d\n", ifname, flength);

	}

	printf("Total %d bytes written to merged file\n", written);
	fclose(fp_merged);
	return 0;
}
