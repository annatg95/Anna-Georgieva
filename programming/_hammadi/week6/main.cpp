
#include "Matrix.h"

// int [3][3] != int **

int main()
{
	Matrix *mptr=new Matrix(); 
	mptr->getArr();
	
	int **arr=new int*[3];
	for(unsigned a=0; a<3; ++a)
	{
		arr[a]=new int[3];
		for(unsigned b=0;b<3; ++b)
		{
			std::cin>>arr[a][b];
		}
	}
		
	mptr->setArr(arr);
	
	mptr->getArr();

	

	delete mptr;
	
	delete arr;
}
