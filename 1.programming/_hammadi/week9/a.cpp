#include <iostream>
using namespace std;

int main()
{
	int array[5]={46,60,56,81,16};

	for(int i=1; i<5; i++)
	{
		int index = array[i];
		int dec = i;
			while(dec>0 && array[dec-1]>=index)
			{
					array[dec]=array[dec-1];
					--dec;
			}
			array[dec]=index;
	}

	for(int i=0; i<5;i++)
	cout << array[i] << "\t";
	return 0;
}
