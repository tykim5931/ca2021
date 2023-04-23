

#ifndef CACHE_H
#define CACHE_H


int cache_find(int cache_type, int addr);

int get_idx(int block, int idx_bits);

int cache_update(int cahce_type, int block, int replacement, int idx_bits);

void cache_evict(int cache_type, int block);

void set_dirty(int cache_type, int block);

#endif
