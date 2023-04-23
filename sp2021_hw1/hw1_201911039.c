#include <stdio.h>
#include <stdlib.h>

typedef unsigned char* pointer;

// Print bit representation of the given data
// This code was implemented in our lecture
void print_bit(pointer a, int len) {
    for (int i = 0; i < len; ++i) {
        for (int j = 7; j >= 0; --j) {
            printf("%d", (a[i] >> j) & 0x01);
        }
        printf(" ");
    }
    printf("\n");
}

// Problem 1
void reverse_bit(pointer a, int len) {
    int reversed;
    char temp[len];
    for (int i = 0; i < len; ++i){
	reversed = 0;
	for(int j = 7; j>=0; --j)
            reversed += ((a[i] >> j) & 0x01) << 7-j;
	temp[len-1-i] = reversed;
    }
    for(int i=0; i<len; ++i)
	a[i] = temp[i];
}

// Problem 2
void inverse_bit(pointer a, int len) {
    int inversed;
    for (int i = 0; i < len; ++i){
	inversed = 0;
	for(int j = 7; j>=0; --j)
            inversed += !((a[i] >> j) & 0x01) << j;
	a[i] = inversed;
    }
}

// Problem 3
void split_bit(pointer a, pointer out1, pointer out2, int len) {
    int obitval, ebitval;
    int l = 0;
    for (int i = 0; i < len;){	// for elems in a
	ebitval = 0;
	obitval = 0;
	for (int j = 7; j >= 0;){			 // j is for left shifting to fill vals 
	    for(int k = 7; k >= 0; --j, --k){		 // k is for shifting of a[i]
		    obitval += ((a[i] >> k) & 0x01) << j;	// 8-kth bit for odd 
		    --k;
		    ebitval += ((a[i] >> k) & 0x01) << j;	// 8-kth bit for even
	    }
	    ++i;	// we used up a[i], need next one
	}
	out1[l] = obitval;	// put value to lth elem in out1
	out2[l] = ebitval;	// put value to lth elem in out2
	l++;
    }
}
	
// Problem 4
unsigned short partial_mul(unsigned short a, unsigned short b) {
    int ans=0;
    int small = a & 0x3F;   			// get lower 6bits from a
    for(int i = 8; i < 15; ++i){
	    if((b>>i) & 0x01){			// from 8th to 15th bit, check if it is 1 
		   ans += small << (i-8);	// if it is 1, shift small to left
	    }					// as multiplication is total sum of them
	    else continue;
    }
    return ans;
}

// Problem 5
void get_date(unsigned int date, int* pYear, int* pMonth, int* pDay) {
    *pYear = (date>>9); 
    *pMonth = (date>>5) & 0x0F; 
    *pDay = date & 0x1F; 
}

int main() {

    printf("Problem 1\n");
    unsigned int v1 = 0x1234CDEF;
    print_bit((pointer)&v1, sizeof(v1));
    reverse_bit((pointer)&v1, sizeof(v1));
    print_bit((pointer)&v1, sizeof(v1));


    printf("Problem 2\n");
    unsigned int v2 = 0x1234CDEF;
    print_bit((pointer)&v2, sizeof(v2));
    inverse_bit((pointer)&v2, sizeof(v2));
    print_bit((pointer)&v2, sizeof(v2));


    printf("Problem 3\n");
    unsigned int v3 = 0x1234CDEF;
    unsigned short out1 = 0, out2 = 0;
    print_bit((pointer)&v3, sizeof(v3));
    split_bit((pointer)&v3, (pointer)&out1, (pointer)&out2, sizeof(v3));
    print_bit((pointer)&out1, sizeof(out1));
    print_bit((pointer)&out2, sizeof(out2));


    printf("Problem 4\n");
    unsigned short v4 = 0xF0BD;
    print_bit((pointer)&v4, sizeof(v4));
    unsigned short v4_out = partial_mul(v4, v4);
    print_bit((pointer)&v4_out, sizeof(v4_out));


    printf("Problem 5\n");
    unsigned int date = 1034867;
    int year, month, day;
    get_date(date, &year, &month, &day);
    printf("%d -> %d/%d/%d\n", date, year, month, day);

    return 0;
}
