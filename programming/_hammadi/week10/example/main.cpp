// Client.cpp
#include "TestTemp.h"
#include "TestTemp.cpp"
int main()
{
	TestTemp<int> TempObj;
	TempObj.SetValue( 2 );
	int nValue = TempObj.GetValue();
	
	TestTemp<char> CharObj;
	CharObj.SetValue('a');
	
	char cValue=CharObj.GetValue();
	std::cout<<"Value: "<<nValue<<std::endl;
	std::cout<<"Value Char: "<<cValue<<std::endl;
	
}
