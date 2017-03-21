#ifndef _MERGESORT_H_
#define _MERGESORT_H_
#include <iostream>
#include <assert.h> 
#include <stdlib.h>


template <typename T> 
class Array
{
	private:
		int size;
		T *ptr;
	public:
		Array(int size_in);
		~Array();
		T& operator[](const int ind)
		{
			assert(ind >= 0 && ind < size);
			return ptr[ind];
			
		}
		T& operator<<(const )
			
		void erase(int size_in);
		void mergeSort(int l, int m, int r);
		void print();
};



#endif
