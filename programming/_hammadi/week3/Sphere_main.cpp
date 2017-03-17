#include <iostream>
#include "Sphere.h"

using namespace std;

int main()
{
	Sphere sphere1;
	Sphere sphere2;
	
	int x,y,z=0;
	float r=0.0;
	int x1,y1,z1=0;
	int scaleV=0;
	
	cout<<"enter x: "<<endl;
	cin>>x;
	cout<<"enter y: "<<endl;
	cin>>y;
	cout<<"enter z: "<<endl;
	cin>>z;
	cout<<"enter r: "<<endl;
	cin>>r;
	
	sphere1.setX(x);
	sphere1.setY(y);
	sphere1.setZ(z);
	sphere1.setR(r);
	
	
	cout<<" X: "<<sphere1.getX()<<endl;
	cout<<" Y: "<<sphere1.getY()<<endl;
	cout<<" Z: "<<sphere1.getZ()<<endl;
	cout<<" R: "<<sphere1.getR()<<endl;

	cout<<"move x: "<<endl;
	cin>>x1;

	cout<<"move y: "<<endl;
	cin>>y1;

	cout<<"move z: "<<endl;
	cin>>z1;
	
	
	sphere1.moveS(x1,y1,z1);
	
	cout<<"moved X: "<<sphere1.getX()<<endl;
	cout<<"moved Y: "<<sphere1.getY()<<endl;
	cout<<"moved Z: "<<sphere1.getZ()<<endl;
	
	
	cout<<"enter scale value: "<<endl;
	cin>>scaleV;
	
	sphere1.scaleS(scaleV);
	
	r=sphere1.getR();
	cout<<"scaled radius : "<<r<<endl;
	
	sphere1.volumeS(r);
	
}
