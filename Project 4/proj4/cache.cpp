#include <iostream>
#include <list>
#include <cstring>
#include <cstdlib>

#include "cache.h"

extern std::list<unsigned long int> l1;
extern std::list<unsigned long int> l2;


unsigned long int cache_find(int cache_type, unsigned long int addr, int offset){
	
	std::list<unsigned long int>* cache;
	if (cache_type == 0)
		cache = &l1;
	else if(cache_type == 1)
		cache = &l2;

	unsigned long int temp = addr>>offset;

	unsigned long int return_block = 0;

	std::list<unsigned long int>::iterator iter;

	unsigned long int val;	
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++){
		val = (*iter) >> 1;
		if(val == temp){
			return_block = (*iter);
			break;
		}
	}
	return return_block;
}

int get_idx(unsigned long int block, int idx_bits){
	int tag = block >> (idx_bits+1);
	int idx_dirt = block - (tag<<(idx_bits+1));
	return (idx_dirt>>1);
}

unsigned long int cache_update(int cache_type, unsigned long int block, int replacement, int offset, int idx_bits, int way){
	
	std::list<unsigned long int>* cache;
	unsigned long int newb;

	if (cache_type == 0)	cache = &l1;
	else	cache = &l2;

	int idx = get_idx(block, idx_bits);

	// Check if set in the cache is full.
	int count=0;
	int set=0;
	
	std::list<unsigned long int>::iterator iter;
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++)
	{
		set = get_idx((*iter), idx_bits);
		if(set == idx){
			count++;
		}
	}
	unsigned long int return_block = 0;

	// If set in the cache is full, evict one block.
	if(count >= way){
		int evict = 0;		// LRU, evict first element
		if(replacement == 1)	// if random, evict random element
			evict = std::rand() % way;

		int i = 0;
		for(iter = (*cache).begin(); iter != (*cache).end(); iter++){
			set = get_idx((*iter), idx_bits);
			if(set == idx){
				if(i == evict){
					return_block = *iter;
					iter = (*cache).erase(iter);
					break;
				}
				i++;
			}
		}
	}

	(*cache).push_back(block);
	
	return return_block;
}


void cache_evict(int cache_type, unsigned long int block){
			
	std::list<unsigned long int>* cache;
	if (cache_type == 0)
		cache = &l1;
	else
		cache = &l2;

	std::list<unsigned long int>::iterator iter;
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++){
		if((*iter) == block){
			(*cache).erase(iter);
			break;
		}
	}
}

void set_dirty(int cache_type, unsigned long int block){
	
	std::list<unsigned long int>* cache;
	if(cache_type == 0)
		cache = &l1;
	else
		cache = &l2;
	std::list<unsigned long int>::iterator iter;
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++){
		if((*iter) == block){
			*iter += 1;
			break;
		}
	}
}
