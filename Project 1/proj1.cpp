#include "modInst.h"
#include "modNum.h"
#include "modFile.h"

int main(int argc, char *argv[]){

	// Get File length and create file list 
	std::list<std::string> fileLines(getFileList(argv[1]));	
	std::list<std::string>::iterator iter;

	// variable declaration
	int dataCount = 0;
	int textCount = 0;
	char label[10] = {0,};
	char firstword[20] = {0,};
	
	// Address for Labels and PC
	int dataAddr = 268435456;	//data address starts from 0x10000000
	int textAddr = 4194304;		// text address starts from 0x400000

	// Queue to save variable and instruction hexademical
	std::queue<std::string> dataQueue;
	std::queue<std::string> textQueue;

	// Find the point where data and text starts
	std::list<std::string> :: iterator dataPoint;
	std::list<std::string> :: iterator textPoint;

	for(iter = fileLines.begin(); iter != fileLines.end(); iter++){
		if((*iter).find(".data") != -1)
			dataPoint = ++iter;
		else if((*iter).find(".text") != -1)
			textPoint = ++iter;
		else continue;
	}


	// Save data label, and save data to dataQueue
	for(iter = dataPoint; iter != textPoint; iter++){
		firstword[0] = '\0';
	
		if ((*iter).find(":") != -1){
			sscanf((*iter).c_str(), "%[^:]:%*s%s", label, firstword);
			Labels.insert(std::make_pair(label, dataAddr));
			
		}else sscanf((*iter).c_str(), "%*s%s", firstword);

		if (firstword[0]=='\0')	continue;
		else{
			if(strchr(firstword,'x')==NULL)	// change to hexademical
				strcpy(firstword, dem2hex(atoi(firstword)));
			else{				// change to lowercase
				for (int i = 0; i < strlen(firstword); i++)
					firstword[i] = tolower(firstword[i]);
			}
			dataAddr += 4;
			dataQueue.push(firstword);
			dataCount++;
		}
	}
	
	// Find pseudo instruction and modify the instruction list
	for(iter = textPoint; iter != fileLines.end(); iter){
		if ((*iter).find(":")!=-1)
			sscanf((*iter).c_str(), "%*[^:]:%s", firstword);
		else sscanf((*iter).c_str(), "%s", firstword);

		if (!strcmp(firstword, "la")){
			std::list<std::string>::iterator temp_iter = iter;
			++iter;
			modPseudo(fileLines, (*temp_iter), temp_iter);
		} else ++iter;		
	}

	// Save text labels and address to Lables
	for(iter = textPoint; iter != fileLines.end(); iter++){
		firstword[0] = '\0';

		if ((*iter).find(":") != -1){
			sscanf((*iter).c_str(), "%[^:]:%s", label, firstword);
			Labels.insert(std::make_pair(label, textAddr));
		}else 
			sscanf((*iter).c_str(), "%s", firstword);

		if (firstword[0] == '\0') continue;
		else	textAddr += 4;
	}
	
	// Save text to textQueue
	textAddr = 4194304;	// initialize text address for PC
	for(iter = textPoint; iter != fileLines.end(); iter++){
		firstword[0] = '\0';

		if ((*iter).find(":")!=-1)
			sscanf((*iter).c_str(), "%*[^:]:%s", firstword);
		else sscanf((*iter).c_str(), "%s", firstword);

		if (firstword[0] == '\0') continue;
		else{
			textQueue.push(getInstruction((*iter).c_str(),firstword,textAddr));
			textCount++;
			textAddr+=4;
		}
	}
	
	// Count is multiplied by 4 because of wordsize
	textCount *= 4;
	dataCount *= 4;

	// Write result to file
	// Create WriteFile
	char fname[20];
	sscanf(argv[1], "%[^.].", fname);
	strcat(fname, ".o");
	std::ofstream writeFile;
        writeFile.open(fname);

	// Print text and data counts
	writeFile.write(dem2hex(textCount), strlen(dem2hex(textCount)));
	writeFile.write("\n", 1);
	
	writeFile.write(dem2hex(dataCount), strlen(dem2hex(dataCount)));
	writeFile.write("\n", 1);
	
	// print texts
	while (!textQueue.empty()){
		writeFile.write(textQueue.front().c_str(), textQueue.front().size());
		writeFile.write("\n", 1);
		textQueue.pop();
	}
	// print datas
	while (!dataQueue.empty()){
		writeFile.write(dataQueue.front().c_str(), dataQueue.front().size());
		writeFile.write("\n", 1);
		dataQueue.pop();
	}

	// Close File
	writeFile.close();
	
	return 0;
}
