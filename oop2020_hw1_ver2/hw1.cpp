/////////////////////////////////////////////////////////
// SE271 - Assignment 1: Source file
// 0. Rename this file with your ID: "hw1_YOURSTUDENTID.cpp"
// 1. Implement each function 
/////////////////////////////////////////////////////////

#include "hw1.h"
#include <iostream>

int count_odd(const unsigned int* array, int size) {
    return 0;
}

int normalize(double* array, int size) {
    return 0;
}

int find_nth(const int* array, int size, int n) {
    return 0;
}

int count_pattern(const char *str, const char * pattern) {
    return 0;
}

char* create_shortest_palindrome(const char *src, char* dst) {
    return dst;
}

#ifdef SE271_HW1
int main() {
    using std::cout;
    using std::endl;

    // Problem 1
    unsigned int a[] = {0, 1, 2, 3, 5};
    std::size_t size_a = sizeof(a) / sizeof(int);
    cout << "Problem 1: " << count_odd(a, (int)size_a) << endl;
    
    // Problem 2
    double b[] = {1, 2, 2, 3, 2};
    std::size_t size_b = sizeof(b) / sizeof(double);
    normalize(b, (int)size_b);
    cout << "Problem 2: ";
    for (unsigned int i = 0; i < size_b; ++i) {
        cout << b[i] << " ";
    }
    cout << endl;

    // Problem 3
    int c[] = {1, 5, 3, 2, 4};
    cout << "Problem 3: " << find_nth(c, sizeof(c) / sizeof(int), 3) << endl;

    // Problem 4
    cout << "Problem 4: ex1) " << count_pattern("AABBBBAA", "AA") << endl;
    cout << "Problem 4: ex2) " << count_pattern("AABBBBAA", "BB") << endl;


    // Problem 5
    char d[100] = {0};
    cout << "Problem 5: ex1) " <<create_shortest_palindrome("ABCD", d) << endl;
    cout << "Problem 5: ex2) " << create_shortest_palindrome("AABBCC", d) << endl;

    return 0;
}
#endif
