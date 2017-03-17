#include <iostream>
#include "Rectangle.h"
using namespace std;

//Rectangle rectangle1;

int main()
{
	int x,y,z=0;
	int x2,y2,z2=0;
	int mx,my,mz=0;
	int scale_value=0;
/*	
	cout<<"Global Rectangle"<<endl;
	cout<<"Enter x:"<<endl;
	cin>>x;
	cout<<"Enter y:"<<endl;
	cin>>y;
	cout<<"Enter z:"<<endl;
	cin>>z;
	
	rectangle1.setX(x);
	rectangle1.setY(y);
	rectangle1.setZ(z);
	
	cout<<"Global values"<<endl;
	rectangle1.printR();
	*/
	{
		cout<<"Start of Static Rectangle"<<endl;
		static Rectangle rectangle2;
		
		cout<<"Enter x2:"<<endl;
		cin>>x2;
		cout<<"Enter y2:"<<endl;
		cin>>y2;
		cout<<"Enter z2:"<<endl;
		cin>>z2;
		
		rectangle2.setX(x2);
		rectangle2.setY(y2);
		rectangle2.setZ(z2);
		
		cout<<"Static Values"<<endl;
		rectangle2.printR();
		
		cout<<"Enter move x:"<<endl;
		cin>>mx;
		cout<<"Enter move y:"<<endl;
		cin>>my;
		cout<<"Enter move z:"<<endl;
		cin>>mz;
		
		rectangle2.moveR(mx,my,mz);
		rectangle2.printR();
		
		
		cout<<"Enter a scale value"<<endl;
		cin>>scale_value;
		rectangle2.scaleR(scale_value);
		
		rectangle2.printR();	
		cout<<"End of Static Rectangle"<<endl;
	}
	
	cout<<"Start of Dynamic Object"<<endl;
	
	Rectangle *rectPtr;
	rectPtr =new Rectangle[3];

	
	delete [] rectPtr;
	
	return 0;
}
