#include <stdio.h>
#include <iostream>
#include <math.h>
using namespace std;

typedef struct vector
{
	int x;
	int y;
	int z;
};

void getValue(vector *data)
{
	cout << "Enter x: ";
	cin >> data->x;
	cout << "Enter y: ";
	cin >> data->y;
	cout << "Enter z: ";
	cin >> data->z;

	cin.sync();
}


int main()
{
	double a,b=0;
	double a1,b1=0;
	double angle=0;
	double cosangle=0;
	vector U,V;
	
	getValue(&U);
	getValue(&V);
	
	
	cout<<U.x<<endl;
	cout<<U.y<<endl;
	cout<<U.z<<endl;
	
	cout<<V.x<<endl;
	cout<<V.y<<endl;
	cout<<V.z<<endl;
	
	
	a=sqrt(pow(U.x,2)+pow(U.y,2)+pow(U.z,2));
	b=sqrt(pow(V.x,2)+pow(V.y,2)+pow(V.z,2));
	
	cosangle=((U.x*V.x)+(U.y*V.y))/(a*b);
	
	angle = acos(cosangle);
	
	//dobavi za vektori z !!!
	
	cout<<"|A|: "<<a<<endl;
	cout<<"|B|: "<<b<<endl;
	cout<<"cosangle: "<<cosangle<<endl<<"angle: "<<angle<<endl;
	
	return 0;
}
