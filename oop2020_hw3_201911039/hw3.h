////////////////////////////////////////////////////////////////////////////////
// SE271 - Assignment 3: Header file
// 1. Complete the implementation of Ordered
// 2. Add a new class, OrderedSet, using class inheritance
// 3. You can add your implementation only in "IMPLEMENT HERE"
//    Do not touch other lines
////////////////////////////////////////////////////////////////////////////////
#ifndef __SE271_HW3__
#define __SE271_HW3__

// IMPLEMENT HERE (something if needed)


//////////////////////////////////////
// DO-NOT-TOUCH: Section Start      //
class Ordered {
protected:
	int m_size = 0;

public:
	Ordered();
	virtual ~Ordered();		//포인터의 종류에 관계없이 자식 클래스의 소멸자 먼저 호출
	virtual void add(int v);
	virtual void add(int* arr, int size);
	virtual void remove(int index);

	virtual int size() { return m_size; }
	virtual int operator[](int index);
	virtual bool operator>>(int v);


	Ordered(const Ordered&) = delete;
	Ordered& operator=(const Ordered&) = delete;

	// DO-NOT-TOUCH: Section End       //
	/////////////////////////////////////

	// IMPLEMENT HERE: Complete the Ordered class 

protected:
	int* m_Varlist;
	int m_length;

};

// IMPLEMENT HERE: implement OrderedSet here using class inheritance
class OrderedSet :public Ordered {
public:
	//constructor는 부모 클래스 먼저 불리고 자식 클래스가 불리고, destructor는 자식 클래스가 먼저 불리고 부모 클래스가 불린다
	OrderedSet();
	~OrderedSet();
	virtual void add(int v);
	virtual void add(int* arr, int size);
};


#endif#pragma once
