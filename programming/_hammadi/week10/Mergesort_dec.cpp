#include "Mergesort.h"

template <class T>
Array<T>::Array(int size_in)
{
	ptr=new T[size_in];
	size=size_in;
}
template <class T>
Array<T>::~Array()
{
	delete[] ptr;
}


template <class T>	
void Array<T>::mergeSort(int l,int m, int r)
{
	int i,j,k;
	int n1=m-l+1;
	int n2=r-m;
	
	Array<T> L[n1], R[n2]; //temp arrays  
	for(int i=0;i<n1;i++)
	{
		L[i]=(this)[l+i];
		std::cout<<"Left: "<<R[j]<<std::endl;
	}
	for(int j=0;j<n2;j++)
	{
		R[j]=(this)[m+1+j];
		std::cout<<"Right: "<<R[j]<<std::endl;
	}
	
	
}

template <class T>
void Array<T>::print()
{
	//aaa
}

template <class T>
void Array<T>::erase(int size_in)
{
	delete[] ptr;
	size= size_in;
	ptr = 0;
}

