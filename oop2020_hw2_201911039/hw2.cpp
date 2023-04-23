////////////////////////////////////////////////////////////////////////////////
// SE271 - Assignment 2: Source file
// 1. Complete the implementation of VariableList
// 2. You can add your implementation only in "IMPLEMENT HERE" & "CHANGE HERE"
//    Do not touch other lines; but you can change main() for testing
////////////////////////////////////////////////////////////////////////////////
#include "hw2.h"

#include <iostream>

////////////////////////////////////////////////////////////////////////////////
// You may also want to have additional functions, 
// e.g., static functions or forward declaration of functions, Then
//
// IMPLEMENT HERE
//
// NOTE: DO NOT USE global, static variables
////////////////////////////////////////////////////////////////////////////////


// Constructors
VariableList::VariableList() {
    n_head->next = nullptr;
    n_head->dtype = DataType::NotAvailable;
    n_end = n_head;
    list_size = 0;
}
VariableList::VariableList(const int* initialArray, const int size) {
    n_head->next = nullptr;
    n_head->dtype = DataType::NotAvailable;
    n_end = n_head;
    list_size = 0;
    
    for (int i = 0;i < size;++i) {
        Node* new_node = new Node;
        new_node->i_data = initialArray[i];
        new_node->dtype = DataType::Integer;
        new_node->next = nullptr;
        this->n_end->next = new_node;
        this->n_end = new_node;
        this->list_size+=1;
    }
}
VariableList::VariableList(const float* initialArray, const int size) {
    n_head->next = nullptr;
    n_head->dtype = DataType::NotAvailable;
    n_end = n_head;
    list_size = 0;
    
    for (int i = 0;i < size;++i) {
        Node* new_node = new Node;
        new_node->f_data = initialArray[i];
        new_node->dtype = DataType::Float;
        new_node->next = nullptr;
        this->n_end->next = new_node;
        this->n_end = new_node;
        this->list_size += 1;
    }
}
VariableList::VariableList(const std::string* initialArray, const int size) {
    n_head->next = nullptr;
    n_head->dtype = DataType::NotAvailable;
    n_end = n_head;
    list_size = 0;
    
    for (int i = 0;i < size;++i) {
        Node* new_node = new Node;
        new_node->s_data = initialArray[i];
        new_node->dtype = DataType::Str;
        new_node->next = nullptr;
        this->n_end->next = new_node;
        this->n_end = new_node;
        this->list_size += 1;
    }
}

// Destructor
// Note: Please delete(free) the memory you allocated 
VariableList::~VariableList() {
    Node* where = n_head;
    Node* temp;
    while (where != n_end) {
        temp = where;
        where = where->next;
        delete temp;
    }
    n_head->next=n_end;
    delete n_head->next;
}

// Member functions
// add: Add the value at the end of the list
void VariableList::add(const int val) {
    Node* new_node = new Node;
    new_node->i_data = val;
    new_node->dtype = DataType::Integer;
    new_node->next = nullptr;

    this->n_end->next = new_node;
    this->n_end = new_node;
    this->list_size += 1;
}
void VariableList::add(const float val) {
    Node* new_node = new Node;
    new_node->f_data = val;
    new_node->dtype = DataType::Float;
    new_node->next = nullptr;

    this->n_end->next = new_node;
    this->n_end = new_node;
    this->list_size += 1;
}
void VariableList::add(const std::string& val) {
    Node* new_node = new Node;
    new_node->dtype = DataType::Str;
    new_node->s_data = val;
    new_node->next = nullptr;

    this->n_end->next = new_node;
    this->n_end = new_node;
    this->list_size += 1;
}

// append: Copy all values of varList and append them at the end of the list
void VariableList::append(const VariableList& varList) {
    int end = varList.list_size;
    for (int i = 0;i < end;++i) {
        if (varList.getType(i) == DataType::Integer) {
            int val;
            varList.getValue(i, val);
            this->add(val);
        }
        else if (varList.getType(i) == DataType::Float) {
            float val;
            varList.getValue(i, val);
            this->add(val);
        }
        else {
            std::string val;
            varList.getValue(i, val);
            this->add(val);
        }
    }
}


// replace: replace the value at the given index in the list
bool VariableList::replace(const int idx, const int val) {
    if (idx >= list_size || idx < 0) return false;
    else {
        Node* where = n_head;
        for (int i = 0;i <= idx;++i) {
            where = where->next;
        }
        where->i_data = val;
        where->f_data = 0;
        where->s_data = "";
        where->dtype = DataType::Integer;
        if (idx == list_size - 1) n_end = where;
        return true;
    }
}
bool VariableList::replace(const int idx, const float val) {
    if (idx >= list_size || idx < 0) return false;
    else {
        Node* where = n_head;
        for (int i = 0;i <= idx;++i) {
            where = where->next;
        }
        where->i_data = 0;
        where->f_data = val;
        where->s_data = "";
        where->dtype = DataType::Float;
        if (idx == list_size - 1) n_end = where;
        return true;
    }
}
bool VariableList::replace(const int idx, const std::string& val) {
    if (idx >= list_size || idx < 0) return false;
    else {
        Node* where = n_head;
        for (int i = 0;i <= idx;++i) {
            where = where->next;
        }
        where->i_data = 0;
        where->f_data = 0;
        where->s_data = val;
        where->dtype = DataType::Str;
        if (idx == list_size - 1) n_end = where;
        return true;
    }
}

// remove: remove the item at the given index in the list
bool VariableList::remove(const int idx) {

    if (idx >= list_size || idx < 0) return false;
    else {
        Node* prev = n_head;
        for (int i = -1;i < idx - 1;++i) {
            prev = prev->next;
        }
        Node* where = prev->next;
        prev->next = where->next;
        delete where;
        --list_size;
        if (idx == list_size - 1) n_end = prev;
        return true;
    }
}


// getSize: return the number of elements of the List
unsigned int VariableList::getSize() const {
    return list_size;
}


// getType: return the data type for the value at the given index
DataType VariableList::getType(const int idx) const {
    if (idx >= list_size || idx < 0) return DataType::NotAvailable;
    else {
        Node* where = n_head;
        for (int i = 0;i <= idx;++i) {
            where = where->next;
        }
        return where->dtype;
    }
}


// getValue: copy the value to the variable
bool VariableList::getValue(const int idx, int& val) const {
    if (idx >= list_size || idx < 0 || this->getType(idx) != DataType::Integer) return false;
    else {
        Node* where = n_head;
        for (int i = 0;i <= idx;++i) {
            where = where->next;
        }
        val = where->i_data;
        return true;
    }
}
bool VariableList::getValue(const int idx, float& val) const {
    if (idx >= list_size || idx < 0 || this->getType(idx) != DataType::Float) return false;
    else {
        Node* where = n_head;
        for (int i = 0;i <= idx;++i) {
            where = where->next;
        }
        val = where->f_data;
        return true;
    }
}
bool VariableList::getValue(const int idx, std::string& val) const {
    if (idx >= list_size || idx < 0 || this->getType(idx) != DataType::Str) return false;
    else {
        Node* where = n_head;
        for (int i = 0;i <= idx;++i) {
            where = where->next;
        }
        val = where->s_data;
        return true;
    }
}

////////////////////////////////////////////////////////////////////////////////
// You may also want to implement additional, private member functions here
// NOTE: DO NOT USE global, static variables
//
// IMPLEMENT HERE
//
////////////////////////////////////////////////////////////////////////////////



void printList(const VariableList& varList) {
    for (unsigned int idx = 0; idx < varList.getSize(); ++idx) {
        DataType curType = varList.getType(idx);
        if (idx > 0)
            std::cout << ", ";

        switch (curType) {
        case DataType::Integer:
        {
            int val;
            if (varList.getValue(idx, val) == false)
                std::cout << "SOMETHING_WRONG";
            else
                std::cout << val;
        }
        break;
        case DataType::Float:
        {
            float val;
            if (varList.getValue(idx, val) == false)
                std::cout << "SOMETHING_WRONG";
            else
                std::cout << val;
        }
        break;
        case DataType::Str:
        {
            std::string val;
            if (varList.getValue(idx, val) == false)
                std::cout << "SOMETHING_WRONG";
            else
                std::cout << "\"" << val << "\"";
        }
        break;
        default:
            std::cout << "SOMETHING_WRONG";
            break;
        }
    }
    std::cout << std::endl;
}

void simpleTest1() {
    VariableList varList;
    varList.add(1);
    varList.add(3);
    varList.add(5);
    varList.add(7);
    printList(varList);

    varList.remove(1);
    printList(varList);
}

void simpleTest2() {
    VariableList varList;
    varList.add(1.0f);
    varList.add("Carrot");
    varList.add(3);
    varList.add(4);
    varList.remove(0);
    varList.remove(0);
    varList.remove(0);
    printList(varList);
}

void simpleTest3() {
    VariableList varList;
    VariableList varList2;
    varList.add(1);
    varList.add(2);
    varList.add(3);
    varList2.add(5.1f);
    varList2.add(5.1f);
    varList.append(varList2);
    printList(varList);
}

void simpleTest4() {
    VariableList varList;
    varList.add(1);
    varList.add(2.1f);
    varList.add(3);
    varList.replace(2, "Apple");
    printList(varList);
}

void complexTest() {
    int initialArray[] = { 1, 2, 3, 4 };
    VariableList varList(initialArray, sizeof(initialArray) / sizeof(int));
    printList(varList);

    std::cout << "Add 1" << std::endl;
    varList.add(1);
    printList(varList);

    std::cout << "Add 2.1f" << std::endl;
    varList.add(2.1f);
    printList(varList);

    std::cout << "Appended another list with strings" << std::endl;
    std::string anotherArray[] = { "Apple", "Banana" };
    VariableList anotherVarList(anotherArray, 2);
    printList(anotherVarList);
    varList.append(anotherVarList);
    printList(varList);

    std::string anotherStr = "Cucumber";
    std::cout << "Replace Index=1 element with \"Cucumber\"" << std::endl;
    varList.replace(1, anotherStr);
    printList(varList);

    std::cout << "Replace Index=7 element with 4.5" << std::endl;
    varList.replace(7, 4.5f);
    printList(varList);

    std::cout << "Remove an element of Index=6" << std::endl;
    varList.remove(6);
    printList(varList);

    std::cout << "Remove elements of Index=6 and Index=0 again" << std::endl;
    varList.remove(6);
    varList.remove(0);
    printList(varList);

    std::cout << "Try to replace an element of out-of-index" << std::endl;
    bool ret = varList.replace(5, 1);
    std::cout << "Return value: " << std::boolalpha << ret << std::endl;

    std::cout << "Get the list size" << std::endl;
    std::cout << varList.getSize() << std::endl;

    std::cout << "Change a string already added and add the changed one" << std::endl;
    anotherStr = "Carrot";
    varList.add(anotherStr);
    printList(varList);
}

int main() {
    std::cout << "<<Simple Test 1>>" << std::endl;
    simpleTest1();

    std::cout << "<<Simple Test 2>>" << std::endl;
    simpleTest2();

    std::cout << "<<Simple Test 3>>" << std::endl;
    simpleTest3();

    std::cout << "<<Simple Test 4>>" << std::endl;
    simpleTest4();

    std::cout << std::endl << "<<Complex Test>>" << std::endl;
    complexTest();

    return 0;
}
