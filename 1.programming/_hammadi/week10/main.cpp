#include "Mergesort.h"
#include "Mergesort_dec.cpp"

int main()
{
	Array<int> a(10);
	Array<double> b(10);

	for(int counter = 0; counter < 10; counter++)
	{
		a[counter] = rand()%25;
		b[counter] = rand()%25+0.25;
	}
 
	
	for(int counter = 0; counter < 10; counter++)
	{
		std::cout<<"a: "<<a[counter]<<"	b: "<<b[counter]<<std::endl;	
		
	}
	int left,middle,right=0;
	left=0;
	middle=5;
	right=9;
	
	a.mergeSort(left,middle,right);
	//b.mergeSort(left,middle,right);
	
	return 0;	
}
