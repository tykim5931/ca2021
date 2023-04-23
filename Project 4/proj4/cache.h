

#ifndef CACHE_H
#define CACHE_H


unsigned long int cache_find(int cache_type, unsigned long int addr, int offset);

int get_idx(int block, int idx_bits);

unsigned long int cache_update(int cahce_type, unsigned long int block, int replacement, int offset, int idx_bits, int way);

void cache_evict(int cache_type, unsigned long int block);

void set_dirty(int cache_type, unsigned long int block);

#endif
