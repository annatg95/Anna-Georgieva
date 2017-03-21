#ifndef __Sphere_h_
#define __Sphere_h_
#include "theLargest.h"

class Sphere
{
	private:
		int r;
	
	public:
		void setR(int);
		int getR();
		
		Sphere(int r_in);
		~Sphere();
		
		Sphere operator+(const Sphere &s_in);
	
};

#endif
