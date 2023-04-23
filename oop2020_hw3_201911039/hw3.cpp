////////////////////////////////////////////////////////////////////////////////
// SE271 - Assignment 3: Source file
// 1. Complete the implementation of Ordered
// 2. Add a new class, OrderedSet, using class inheritance
////////////////////////////////////////////////////////////////////////////////
#include "hw3.h"

#include <iostream>
#include <limits>

Ordered::Ordered() {
	m_length = 3;
	m_Varlist = new int[3];	//allocate 3*4 initially
	m_size = 0;
}

Ordered::~Ordered() {
	delete[] m_Varlist;
}

void Ordered::add(int v) {
	// find location to add
	int loc;
	loc = m_size;
	for (int i = 0; i < m_size; ++i) {
		if (v <= m_Varlist[i]) {
			loc = i;
			break;
		}
		else continue;
	}
	// add value
	int new_length;
	if (m_size < 3) new_length = 3;
	else new_length = m_length + 1;

	int* new_Varlist= new int[new_length];
	for (int i{ 0 }; i < loc;++i) {
		new_Varlist[i] = m_Varlist[i];
	}
	new_Varlist[loc] = v;
	for (int i{ loc };i < m_size;++i) {
		new_Varlist[i + 1] = m_Varlist[i];
	}
	delete[] m_Varlist;
	m_Varlist = new_Varlist;
	m_length=new_length;
	m_size++;
}

void Ordered::remove(int index) {
	if (m_length > 3) --m_length;
	else m_length = 3;
	int* new_Varlist = new int[m_length];
	for (int i{ 0 }; i < m_size; ++i) {
		if (i < index) new_Varlist[i] = m_Varlist[i];
		else if (i == index) continue;
		else new_Varlist[i - 1] = m_Varlist[i];
	}
	m_size--;
	delete[] m_Varlist;
	m_Varlist = new_Varlist;
}

void Ordered::add(int* arr, int size) {
	for (int i{ 0 }; i < size;++i) {
		int var;
		var = arr[i];
		this->add(var);
	}
}

int Ordered::operator[](int index) {
	if (index < 0 or index >= m_size) {
		return std::numeric_limits<int>::min();
	}
	return m_Varlist[index];
}

bool Ordered::operator>>(int v) {
	for (int i{ 0 }; i < m_size; ++i) {
		if (m_Varlist[i] == v) return true;
	}
	return false;
}

//OrderedSet
OrderedSet::OrderedSet() {
	m_Varlist = new int[3];
	m_size = 0;
}

OrderedSet::~OrderedSet() {
}

void OrderedSet::add(int v) {
	if ((*this) >> v == false) Ordered::add(v);
}

void OrderedSet::add(int* arr, int size) {
	for (int i{ 0 }; i < size;++i) {
		int var;
		var = arr[i];
		this->OrderedSet::add(var);
	}
}
