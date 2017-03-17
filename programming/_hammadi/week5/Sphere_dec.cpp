#include <iostream>
#include "Sphere.h"


void Sphere::setRad(float r_in)
{
	m_radius=r_in;
}

float Sphere::getRad()
{
	return m_radius;
}

Sphere::Sphere(int x_in, int y_in, int z_in,float r_in):Parent(m_xc, m_yc, m_zc)
{
	m_xc=x_in;
	m_yc=y_in;
	m_zc=z_in;
	m_radius=r_in;
}

Sphere::~Sphere()
{
	//dtor
}
