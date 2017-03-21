#include <stdio.h>
#include <iostream>
#include <math.h>
using namespace std;


void bubbleSort(int *a,int n)
{
	int i,j,tmp=0;
	
	for (i=n;i>0;i--)
	{
		for(j=1;j<i;j++)
		{
			if(a[j-1]>a[j])
			{
				tmp=a[j-1];
				a[j-1]=a[j];
				a[j]=tmp;
			}
		}
	}
	
	for(int b=0; b<n;b++)
	{
		cout<<b[a]<<endl;
	}
	
}

void quickSort(int *a, int s, int e)
{
	int tmp, pivot,l,r=0;
	
	if(s<e)
	{
		pivot=a[s+(e-s)/2];
		l=s;
		r=e;
		while(l<r)
		{
			while((a[l]<pivot)&&(l<=e)) l++;
			while((a[r]<pivot)&&(r>=s)) r--;
			if(l<=r)
			{
				tmp=a[l];
				a[l]=a[r];
				a[r]=tmp;
				l++;
				r--;
			}
		}
	quickSort(a,s,r);
	quickSort(a,l,e);
	}
}
			
void insertionSort(int *a, int size)
{
	for(int i=0; i<size; i++)
	{
		int first=a[i];
		int dec=i;
		while(dec>0 && a[dec-1]>=first)
		{
			a[dec]=a[dec-1];
			--dec;
		}     
		a[dec]=first;
	}
	for(int i=0;i<5;i++)
	{
		cout<<a[i]<<endl;
	}
}
	

int main()
{
	int choice=0;
	int size1=0;
	
	
	cout<<"Enter a choice"<<endl<<"1:bubbleSort"<<endl<<"2:QuickSort"<<endl<<"3:InsertionSort"<<endl;
	cin>>choice;
	
	cout<<"Enter a size of the array"<<endl;
	cin>>size1;
	
	int arr[size1];
	fill(arr,arr+size1,0);
	
	for(int i=0; i<size1; i++)
	{
		cin>>arr[i];
	}
	for(int i=0; i<size1; i++)
	{
		cout<<arr[i];
	}
	
	int start=arr[0];
	cout<<"Start: "<<start;
	int end=arr[size1];
	cout<<"End: "<<end;
	
	switch(choice)
	{
		case 1: cout<<"bubbleSort"<<endl;
				bubbleSort(arr,size1);
				break;
		case 2: cout<<"QuickSort"<<endl;
				quickSort(arr,start,end);
				break;
		case 3: cout<<"InsertionSort"<<endl;
				insertionSort(arr,size1);
				break;
	}
	
	return 0;
}
