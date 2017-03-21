#include "myarray.h"
#include <cstdlib>

int main()
{
	Array<int> a(10);
	Array<double> b(10);
 
	for (int counter = 0; counter < a.getSize(); counter++)
	{
		//a[counter]=counter;
		//b[counter]=counter+0.25;
		
		a[counter] = rand()%25;
		b[counter] = rand()%25+0.25;
	}
 
	
	for (int counter = 0; counter < a.getSize(); counter++)
	{
		std::cout<<"a: "<<a[counter]<<"	b: "<<b[counter]<<std::endl;	
		
	}
	
	int outputA=0;
	int outputB=0;
	
	outputA=a.compare(a[0],a[1]);
	std::cout<<"outputA value :"<<outputA<<std::endl;
	
	outputB=b.compare(b[0],b[1]);
	std::cout<<"outputB value :"<<outputB<<std::endl;
	
	
	//a.insertSort(10);
	//b.insertSort(10);
	
	a.bubbleSort(10);
	b.bubbleSort(10);
	
	for (int counter = 0; counter < a.getSize(); counter++)
	{
		std::cout<<"a: "<<a[counter]<<"	b: "<<b[counter]<<std::endl;		
		
	}
	

	
	return 0;
}


