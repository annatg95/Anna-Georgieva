#include <stdio.h>
#include <iostream>
using namespace std;

void sumA(int arr1[], int arr2[], int arr3[], int size1, int size2, int totalS)
{
	int i=0;
	int j=0;
	int k=0;
    while(i<=totalS && j<=size1 && k<=size2)
	{	
		arr3[i++]=arr1[j++]+arr2[k++];
	}
	

    for(int a=0;a<=size1+size2;a++)
    {
		
		cout<<" arr3["<<a<<"] :"<<arr3[a]<<endl;

	}
}

void mulA(int arr1[], int arr2[], int arr3[], int size1, int size2, int totalS)
{
	int i=1;
	int j=1;
	int k=1;
    while(i<=totalS && j<=size1 && k<=size2)
	{	
		arr3[i++]=arr1[j++]*arr2[k++];
	}
	

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
     
    for(int i=1,y=1; i<=size1,y<=size2; i++,y++)
    {
		cin>>arrX[i];
		cin>>arrY[y];
	}
	
    for(int i=1,y=1; i<=size1,y<=size2; i++,y++)
    {
		cout<<"first array element ["<<i<<"]"<<arrX[i]<<endl;
		
	}
    
    for(int i=1,y=1; i<=size1,y<=size2; i++,y++)
    {
		cout<<"second array element ["<<y<<"]"<<arrY[y]<<endl;
	}
	
	sumA(arrX,arrY,arrZ,size1,size2,totalS);
	mulA(arrX,arrY,arrZ,size1,size2,totalS);
}



