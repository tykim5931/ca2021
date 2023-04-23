#include <iostream>
#include <fstream>
#include <list>
#include <cstring>
#include <cstdlib>
#include <string.h>

#include "cache.h"


std::list<unsigned long int> l1;
std::list<unsigned long int> l2;


int main(int argc, char *argv[]){

	//Random setting for rand
	std::srand(5323);

	// Get options
	unsigned int l2_cap = 3;
	unsigned int l2_asso= 0;
	unsigned int block_size = 3;
	unsigned int replacement_plcy = 2; // 0 means LRU, 1 means random

	for(int i = 0; i < argc; ++i){
		if(!strcmp(argv[i], "-c")){
		       sscanf(argv[i+1], "%d", &l2_cap);
		       l2_cap = l2_cap<<10; // match unit because it's KB
		} else if(!strcmp(argv[i], "-a")){
			sscanf(argv[i+1], "%d", &l2_asso);
		} else if(!strcmp(argv[i], "-b")){
			sscanf(argv[i+1], "%d", &block_size);
		} else if(!strcmp(argv[i], "-random")){
			replacement_plcy = 1;
		} else if(!strcmp(argv[i], "-lru")){
			replacement_plcy = 0;
		}
	}

	if(l2_cap == 3 || l2_asso == 0 || block_size == 3 || replacement_plcy == 2){
		printf("Please Give Whole options!\n");
		exit(0);
	}

	// Get offset bit
	int offset;
	int i=7;
	while(!((block_size>>i)&0x01)){
		i--;
	}
	offset = i;

	// Set l1 cache variables
	int l1_cap = l2_cap>>2;
	int l1_asso = l2_asso>>2;
	if(l2_asso<=2) l1_asso = l2_asso;

	// Get index bits;
	unsigned int l2_setsize = (l2_cap/l2_asso)/block_size;
	unsigned int l1_idx_bits;
	unsigned int l2_idx_bits;
	int j = 0;
	while(!(l2_setsize&0x01)){
		j++;
		l2_setsize = l2_setsize>>1;
	}
	l2_idx_bits = j;
	if(l2_asso >2) l1_idx_bits = l2_idx_bits;
	else l1_idx_bits = l2_idx_bits-2;


	// Open readfile
	char* input_file;
	input_file = argv[argc-1];
	std::ifstream fin;
	fin.open(input_file);

	if(fin.fail()){
		std::cerr << "Cannot Open Input File"<< std::endl;
		exit(100);
	}
	
	char op; // This contains W or R
	unsigned long int addr; // This contains address number

	int r_l1_miss = 0;
	int r_l2_miss = 0;
	int w_l1_miss = 0;
	int w_l2_miss = 0;
	int r_access = 0;
	int w_access = 0;
	int l1_clean_evict = 0;
	int l1_dirty_evict = 0;
	int l2_clean_evict = 0;
	int l2_dirty_evict = 0;
       
	while(!fin.eof()){

		std::string line;
		unsigned long int block;
		unsigned long int victim;
		
		getline(fin, line);

		sscanf(line.c_str(), "%c%lx", &op, &addr);

		// get tag and index to find from cache
		block = cache_find(0, addr, offset);

		// L1 hit
		if(block){
			if(op == 'R')
				r_access++;
			else{
				w_access++;
				if(!(block & 0x01)){
					set_dirty(0, block); // set dirty bit to 1
					set_dirty(1, block);
				}
			}
			continue;
		}


		// L1 miss
		block = cache_find(1, addr, offset);

		// L2 hit
		if(block){
			if(op == 'R'){
				r_l1_miss++;
				r_access++;
			}
			else{
				w_l1_miss++;
				w_access++;
				if(!(block&0x01))
					set_dirty(1, block);
			}

			victim = cache_update(0, block, replacement_plcy, offset, l1_idx_bits, l1_asso);
			
			if(victim){
				if(victim & 0x01)	
					l1_dirty_evict++;
				else	
					l1_clean_evict++;
			}
			continue;
		}


		// L2 miss. block is nullptr, so create new block.
		if(op == 'R'){
			r_l1_miss++;
			r_l2_miss++;
			r_access++;
		}
		else{
			w_l1_miss++;
			w_l2_miss++;
			w_access++;
		}
		
		unsigned long int newb = (addr>>offset)<<1;
		victim = cache_update(1, newb, replacement_plcy, offset, l2_idx_bits, l2_asso);

		if (victim){
			if(victim & 0x01)	// if dirty
				l2_dirty_evict++;
			else
				l2_clean_evict++;
			
			// If l1 cache has evicted bloc, then evict it too.
			unsigned long int v_addr = (victim >> 1) << offset;
			unsigned long int e_block = cache_find(0, v_addr, offset);

			if (e_block){
				cache_evict(0, victim);

				if(victim & 0x01)
					l1_dirty_evict++;
				else
					l1_clean_evict++;
			}
		}

		victim = cache_update(0, newb, replacement_plcy, offset, l1_idx_bits, l1_asso);

		if(victim){
			if(victim & 0x01)	l1_dirty_evict++;
			else		l1_clean_evict++;
		}
		continue;
	}
	
	fin.close();


	// Open writefile

	char* fname;
	fname = strtok(argv[argc-1], ".");
	char ofname[100];
	snprintf(ofname, sizeof(ofname), "%s_%d_%d_%d.out",
			fname,
			l2_cap>>10,
			l2_asso,
			block_size);
		
	std::ofstream fout;
	fout.open(ofname);

	if(fout.fail()){
		std::cerr << "Cannot Open Output File"<< std::endl;
		exit(100);
	}
	unsigned int l1_count=0;
	unsigned int l2_count=0;

	std::list<unsigned long int>::iterator iter;
	for(iter= l1.begin(); iter != l1.end(); iter++)
		l1_count++;
	for(iter = l2.begin(); iter != l2.end(); iter++)
		l2_count++;


	fout<<"-- General Stats --\n";
	fout<<"L1 Capacity: " << (l1_cap >> 10) << "\n";
	fout<<"L1 way: " << l1_asso << "\n";
	fout<<"L2 Capacity: " << (l2_cap>>10) << "\n";
	fout<<"L2 way: " << l2_asso << "\n";
	fout<<"Block Size: " <<  block_size << "\n";

	fout << "Total accesses: " << (r_access + w_access) << "\n";
	fout << "Read accesses: " << r_access << "\n";
	fout << "Write accesses: " << w_access << "\n";
	
	fout << "L1 Read misses: " << r_l1_miss << "\n";
	fout << "L2 Read misses: " << r_l2_miss << "\n";
	
	fout << "L1 Write misses: " << w_l1_miss << "\n";
	fout << "L2 Write misses: " << w_l2_miss << "\n";
	
	fout << "L1 Read miss rate: " << (((float)r_l1_miss/r_access)*100)<<"%\n";
	fout << "L2 Read miss rate: " << (((float)r_l2_miss/r_l1_miss)*100)<<"%\n";
	fout << "L1 Write miss rate: " << (((float)w_l1_miss/w_access)*100)<<"%\n";
	fout << "L2 Write miss rate: " << (((float)w_l2_miss/w_l1_miss)*100)<<"%\n";
	
	fout << "L1 Clean eviction: " <<  l1_clean_evict << "\n";
	fout <<"L2 Clean eviction: " << l1_clean_evict << "\n";

	fout <<"L1 Dirty eviction: " <<  l1_dirty_evict << "\n";
	fout <<"L2 Dirty eviction: " <<  l2_dirty_evict << "\n";

	fout.close();
	return 0;
}
