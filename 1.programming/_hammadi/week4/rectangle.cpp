#include <iostream>
#include "Rectangle.h"
using namespace std;

void Rectangle::setX(int x_in)
{
	x=x_in;
}

void Rectangle::setY(int y_in)
{
	y=y_in;
}

void Rectangle::setZ(int z_in)
{
	z=z_in;
}

int Rectangle::getX()
{
	return x;
}

int Rectangle::getY()
{
	return y;
}

int Rectangle::getZ()
{
	return z;
}

Rectangle::Rectangle()
{
	cout<<"constructor"<<endl;
	x=0;
	y=0;
	z=0;
}

Rectangle::Rectangle(int x_in, int y_in, int z_in)
{
	
	x=x_in;
	y=y_in;
	z=z_in;
}

Rectangle::Rectangle(const Rectangle &Rectangle0)
{
	x=Rectangle0.x;
	y=Rectangle0.y;
	z=Rectangle0.z;
}

Rectangle::~Rectangle()
{
	cout<<"dstr"<<endl;
}

void Rectangle::printR()
{
	cout<<"value of x: "<<x<<endl;
	cout<<"value of y: "<<y<<endl;
	cout<<"value of z: "<<z<<endl;

}

void Rectangle::moveR(int move_x, int move_y, int move_z)
{
	x+=move_x;
	y+=move_y;
	z+=move_z;
		
}

void Rectangle::scaleR(int value)
{
	x/=value;
	y/=value;
	z/=value;
}

void Rectangle::calculateP()
{
	int p=0;	
	p=x+y+z;
	cout<<"Perimeter: "<<endl;
}
