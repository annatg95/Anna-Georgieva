#ifndef ARRAY_H
#define ARRAY_H
#include <iostream>
#include <assert.h> // for assert()
 
template <typename T>
class Array
{
private:
    int size;
    T *arr;
 
public:
    Array()
    {
        size = 0;
        arr = 0;
    }
 
    Array(int size_in)
    {
        arr= new T[size_in];
        size = size_in;
    }
 
    ~Array()
    {
        delete[] arr;
    }
 
    void Erase()
    {
        delete[] arr;
        size= 0;
        arr = 0;
    }
 
 
    T& operator[](int ind)
    {
        assert(ind >= 0 && ind < size);
        return arr[ind];
    }
 
    int getSize(); 
    int compare(T a, T b);
    void swap(int x, int y);
    void insertSort(int n);
    void bubbleSort(int n);
    
};
 
template <typename T>
int Array<T>::getSize() 
{ 
	return size; 
}

template <typename T>
int Array<T>::compare(T a, T b)
{
	if(a<=b)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

template <typename T>
void Array<T>::swap(int x, int y)
{
	T temp;
	temp=(*this)[x];
	(*this)[x]=(*this)[y];
	(*this)[y]=temp;
}


//wikipedia pseudocodes
template <typename T>
void Array<T>::insertSort(int n) 
{
	for(int i=1;i<n;i++)
	{
		int a=(*this)[i];
		int z=i;
		while(z>0 && (*this)[z-1]>=a)
		{
			(*this)[z]=(*this)[z-1];
			--z;
		}
		(*this)[z]=a;
	}
}


//wikipedia pseudocodes
template <typename T>
void Array<T>::bubbleSort(int n) 
{
	for(int i=n;i>0;i--)
	{
		for(int j=1;j<i;j++)
		{
			if((*this)[j-1]>(*this)[j])
			{
				T temp=(*this)[j-1];
				(*this)[j-1]=(*this)[j];
				(*this)[j]=temp;
			}
		}
	}
}


 
#endif
