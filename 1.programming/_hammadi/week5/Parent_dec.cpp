#include <iostream>
#include "Parent.h"

void Parent::setX(int x_in)
{
	m_xc=x_in;
}
void Parent::setY(int y_in)
{
	m_yc=y_in;
}
void Parent::setZ(int z_in)
{
	m_zc=z_in;
}
int Parent::getX()
{
	return m_xc;
}
int Parent::getY()
{
	return m_yc;
}
int Parent::getZ()
{
	return m_zc;
}

Parent::Parent(int x_in, int y_in, int z_in)
{
	m_xc=x_in;
	m_yc=y_in;
	m_zc=z_in;
	
	//color[0]=255;
	//color[1]=255;
	//color[2]=255;
}

Parent::~Parent()
{
	//dtor
}

void Parent::setColor(int r_in, int g_in, int b_in)
{
	color[0]=r_in;
	color[1]=g_in;
	color[2]=b_in;
}

int Parent::getR()
{
	return color[0];
}
int Parent::getG()
{
	return color[1];
}
int Parent::getB()
{
	return color[2];
}

