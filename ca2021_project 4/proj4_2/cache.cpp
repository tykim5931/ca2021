#include <iostream>
#include <list>
#include <cstring>
#include <cstdlib>

#include "cache.h"

extern std::list<int> l1_i;
extern std::list<int> l1_d;
extern std::list<int> l2;


int cache_find(int cache_type, int addr){
	
	std::list<int>* cache;
	if (cache_type == 0)
		cache = &l1_i;
	else if(cache_type == 1)
		cache = &l2;
	else
		cache = &l1_d;

	int temp = addr>>4;

	int return_block = 0;

	std::list<int>::iterator iter;

	int val;	
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++){
		val = (*iter) >> 1;
		if(val == temp){
			return_block = (*iter);
			break;
		}
	}
	return return_block;
}

int get_idx(int block, int idx_bits){
	int tag = block >> (idx_bits+1);
	int idx_dirt = block - (tag<<(idx_bits+1));
	return (idx_dirt>>1);
}

int cache_update(int cache_type, int block, int replacement, int idx_bits){
	
	std::list<int>* cache;
	int way = 1;
	int newb;

	if (cache_type == 0)	cache = &l1_i;
	else if(cache_type == 1){
		cache = &l2;
		way = 4;
	}
	else cache = &l1_d;

	int idx = get_idx(block, idx_bits);

	// Check if set in the cache is full.
	int count=0;
	int set=0;
	
	std::list<int>::iterator iter;
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++)
	{
		set = get_idx((*iter), idx_bits);
		if(set == idx){
			count++;
		}
	}
	int return_block = 0;

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


void cache_evict(int cache_type, int block){
		
	std::list<int>* cache;
	if (cache_type == 0)
		cache = &l1_i;
	else if(cache_type == 1)
		cache = &l2;
	else
		cache = &l1_d;


	std::list<int>::iterator iter;
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++){
		if((*iter) == block){
			(*cache).erase(iter);
			break;
		}
	}
}

void set_dirty(int cache_type, int block){
			
	std::list<int>* cache;
	if (cache_type == 0)
		cache = &l1_i;
	else if(cache_type == 1)
		cache = &l2;
	else
		cache = &l1_d;
	
	std::list<int>::iterator iter;
	for(iter = (*cache).begin(); iter!= (*cache).end(); iter++){
		if((*iter) == block){
			*iter += 1;
			break;
		}
	}
}
