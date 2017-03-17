#include <stdio.h>
#include <iostream>
using namespace std;

int main()
{
	int n=0;
	
	cout<<"enter a number"<<endl;
	cin>>n;
	
	if(n!=1 && n!=0)
	{
		if(n%2!=0)
		{
			int i=2;
			do
			{
				
				if(n%i!=0)
				{
					cout<<"n :"<<n<<"	is not divisible by "<<i<<"	"<<endl;
				}
				else
				{
					cout<<"not a prime number"<<endl; 
				}
				i++;
			}while(i<n);
		}
		else
		{
			cout<<"not a prime number"<<endl; 
		}
	}
	else
	{
		cout<<"not a prime number / you have entered 0 or 1"<<endl;
	}
	
return 0;
}
