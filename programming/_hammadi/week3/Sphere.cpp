#include <iostream>
#include <math.h>
#include "Sphere.h"

using namespace std;

void Sphere::setX(int x)
{
	m_xc=x;
}

void Sphere::setY(int y)
{
	m_yc=y;
}

void Sphere::setZ(int z)
{
	m_zc=z;
}

void Sphere::setR(float radius)
{
	m_r=radius;
}

int Sphere::getX()
{
	return m_xc;
}

int Sphere::getY()
{
	return m_yc;
}

int Sphere::getZ()
{
	return m_zc;
}

float Sphere::getR()
{
	return m_r;
}

Sphere::Sphere()
{
	m_xc=0;
	m_yc=0;
	m_zc=0;
	m_r=0;
	
}

Sphere::Sphere(int x,int y, int z,float r)
{
	m_xc=x;
	m_yc=y;
	m_zc=z;
	m_r=r;
	
}

Sphere::Sphere(const Sphere &sphere0)
{
	m_xc=sphere0.m_xc;
	m_yc=sphere0.m_yc;
	m_zc=sphere0.m_zc;
	m_r=sphere0.m_r;	
}

void Sphere::moveS(int mX,int mY,int mZ)
{
	m_xc+=mX;
	m_yc+=mY;
	m_zc+=mZ;

}

void Sphere::scaleS(int value)
{
	m_r/=value;
}

void Sphere::volumeS(float radius) const
{
	float pi=3.14159;
	float volume=0;
	
	volume= (4.0/3.0)*pi*(pow(radius,3.0));
	cout<<"volume: "<<volume<<endl;
}
