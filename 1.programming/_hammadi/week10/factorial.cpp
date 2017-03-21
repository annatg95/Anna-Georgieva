#include <iostream>

long factorial(long a)
{
	if(a>1)
	{
		return(a*factorial(a-1));
	}
	else
	{
		return 1;
	}
	
}

int main()
{
	long number=0;
	long result=0;
	std::cout<<"Enter a number to calculate factorial"<<std::endl;
	
	std::cin>>number;
	
	result=factorial(number);
	std::cout<<"Result: "<<result<<std::endl;
	
	return 0;	
}

