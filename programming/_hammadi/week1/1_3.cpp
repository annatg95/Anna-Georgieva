#include <stdio.h>
#include <iostream>
using namespace std;

int maximumValue(int array[], int size)
{
     int max = array[0];       

     for(int i = 1; i<size; i++)
     {
          if(array[i] > max)
          {
              max = array[i];
          }
     }
     return max;
}

int minimumValue(int array[], int size)
{
     int min = array[0];       

     for(int i = 1; i<size; i++)
     {
          if(array[i] < min)
          {
              min = array[i];
          }
     }
     return min;
}

int main()
{
	int size=0;
	cout<<"Enter the size of the array:"<<endl;
    cin>>size;
    
    int arr[size];
    cout<<"size of the array: "<<size<<endl;
    
    for(int i=0; i<size; i++)
    {
		 cin >> arr[i];
		 //cout<<"numbers in the array"<<arr[i] <<endl;
	}
		
    
   cout<<"maximum value is: "<<maximumValue(arr,size)<<endl;
   cout<<"minimum value is: "<<minimumValue(arr,size)<<endl;


return 0;
}

    
