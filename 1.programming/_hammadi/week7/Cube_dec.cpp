#include "Cube.h"
#include "theLargest.h"

void Cube::setHW(int h_in, int w_in)
{
	h=h_in;
	w=w_in;
}

int Cube::getH()
{
	return h;
}

int Cube::getW()
{
	return w;
}

Cube::Cube(int h_in, int w_in)
{
	h=h_in;
	w=w_in;
}

Cube::~Cube()
{
	
}

Cube Cube::operator +(const Cube &c_in)
{
	return Cube(h+c_in.h,w+c_in.w);
}
