#include "Sphere.h"
#include "theLargest.h"

void Sphere::setR(int r_in)
{
	r=r_in;
}

int Sphere::getR()
{
	return r;
}

Sphere::Sphere(int r_in)
{
	r=r_in;
}

Sphere::~Sphere()
{
	
}

Sphere Sphere::operator +(const Sphere &s_in)
{
	return Sphere(r+s_in.r);
}
