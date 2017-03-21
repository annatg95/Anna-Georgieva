#include <stdio.h>
#include <iostream>
using namespace std;

int main()
{
    int l,m,n=0;
    int counter=0;
    
    
    cout<<"make sure m<n "<<endl;
    cin>>m;
    cin>>n;
    cin>>l;
        
    int size=n-m;
    cout<<"size of array ="<<size<<endl;
    int array[size];
    fill( array, array+size, 0);
    
	if(m>n)
	{
		cout<<"enter m<n"<<endl;
	}
	else
	{
		
		for(int i=0,counter=m;counter<n;counter++)
		{
			i++;
			array[i]=counter;
		}
		
	}
	
	for(int a=0;a<size+1; a++)
	{
		//cout<<array[a]<<endl;
		if(array[a]%l==0)
		{
			cout<<"divisible by "<< l<<" are: "<<array[a]<<endl;
		}
		
	}


return 0;
}
