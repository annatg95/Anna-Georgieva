#include <stdio.h>
#include <iostream>
using namespace std;

void mergeA(int arr1[], int arr2[], int arr3[], int size1, int size2, int totalS)
{
	int i=0;
	int j=0;
	int k=0;
    while(i<=totalS && j<=size1 && k<=size2)
	{	
		arr3[i++]=arr1[j++];
		arr3[totalS--]=arr2[k++];
		
	}
	
	cout<<"size1:	"<<size1<<endl;
	cout<<"size2:	"<<size2<<endl;

    for(int a=0;a<=size1+size2;a++)
    {
		
		cout<<" arr3["<<a<<"] :"<<arr3[a]<<endl;

	}
}

int main()
{
	int size1=0;
	int size2=0;
	
	cout<<"Enter the size of the first array"<<endl;
	cin>> size1;
	cout<<"Enter the size of the second array"<<endl;
	cin>> size2;
	
	int totalS=size1+size2;
    int arrX[size1];
    int arrY[size2];
    int arrZ[totalS];
    fill(arrX,arrX+size1,0);
    fill(arrY,arrY+size2,0);
    fill(arrZ,arrZ+totalS,0);
     
    for(int i=0,y=0; i<=size1,y<=size2; i++,y++)
    {
		cin>>arrX[i];
		cin>>arrY[y];
	}
	
    for(int i=0,y=0; i<=size1,y<=size2; i++,y++)
    {
		cout<<"first array element ["<<i<<"]"<<arrX[i]<<endl;
		cout<<"second array element ["<<y<<"]"<<arrY[y]<<endl;
	}
    
	mergeA(arrX,arrY,arrZ,size1,size2,totalS);
}



