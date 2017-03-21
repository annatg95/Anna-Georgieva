#include <iostream>
#include "Cuboid.h"


void Cuboid::setW(float w_in)
{
	m_width=w_in;
}
void Cuboid::setH(float h_in)
{
	m_height=h_in;
}
void Cuboid::setL(float l_in)
{
	m_lenght=l_in;
}

float Cuboid::getW()
{
	return m_width;
}

float Cuboid::getH()
{
	return m_height;
}

float Cuboid::getL()
{
	return m_lenght;
}

Cuboid::Cuboid(float w_in, float h_in, float l_in, int x_in, int y_in, int z_in):Parent(m_xc, m_yc, m_zc)
{
	m_width=w_in;
	m_height=h_in;
	m_lenght=l_in;
	m_xc=x_in;
	m_yc=y_in;
	m_zc=z_in;

}

Cuboid::~Cuboid()
{
	//dtor
}
