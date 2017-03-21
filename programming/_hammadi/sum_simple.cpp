#include <iostream>

int sum(int a, int b) 
{
	return a+b;
}


int main()
{
	int x=1;
	int y=2;
	 int result=0;
	 
	result=sum(x, y);
	std::cout<<result<<std::endl;
	
	return 0;
}
