////////////////////////////////////////////////////////////////////////////////
// SE271 - Assignment 2: Header file
// 1. Complete the implementation of VariableList
// 2. You can add your implementation only in "IMPLEMENT HERE"
//    Do not touch other lines
////////////////////////////////////////////////////////////////////////////////
#ifndef SE271_HW2
#define SE271_HW2

#include <string>

// Use DataType for VariableList::getType
enum class DataType { Integer, Float, Str, NotAvailable };

class VariableList {
public:
	///////////////////////////////////////////////////////////////////////////
	// 1. Implement the following member functions in hw2.cpp (NOT HERE!!)
	// 2. Do not touch anything below declared in public
	///////////////////////////////////////////////////////////////////////////

	// Constructors
	VariableList();
	VariableList(const int* initialArray, const int size);
	VariableList(const float* initialArray, const int size);
	VariableList(const std::string* initialArray, const int size);

	// Destructor
	~VariableList();

	// Member functions
	// add: Add the value at the end of the list
	void add(const int val);
	void add(const float val);
	void add(const std::string& val);

	// append: Copy all values of varList and append them at the end of the list
	void append(const VariableList& varList);

	// replace: replace the value at the given index in the list
	bool replace(const int idx, const int val);
	bool replace(const int idx, const float val);
	bool replace(const int idx, const std::string& val);

	// remove: remove the item at the given index in the list
	bool remove(const int idx);

	// getSize: return the number of elements of the List
	unsigned int getSize() const;

	// getType: return the data type for the element at the given index
	DataType getType(const int idx) const;

	// getValue: copy the value to the variable
	bool getValue(const int idx, int& val) const;
	bool getValue(const int idx, float& val) const;
	bool getValue(const int idx, std::string& val) const;

	///////////////////////////////////////////////////////////////////////////
	// End of the functions that you have to implement in hw2.cpp :)
	///////////////////////////////////////////////////////////////////////////


	///////////////////////////////////////////////////////////////////////////
	// Do not implement the copy operators below in this assignment
	// You can assume that we will not use them
	///////////////////////////////////////////////////////////////////////////
	VariableList(const VariableList&) = delete;
	VariableList& operator=(const VariableList&) = delete;

private:
	///////////////////////////////////////////////////////////////////////////
	// 1. Include variables and extra member functions HERE (!!) as needed
	// 2. All of your implementations have to be private
	///////////////////////////////////////////////////////////////////////////
	class Node {
	public:
		int i_data;
		float f_data;
		std::string s_data;
		DataType dtype;
		Node* next = nullptr;
	};
	Node* n_head = new Node;
	Node* n_end;
	int list_size{ 0 };
};


#endif
