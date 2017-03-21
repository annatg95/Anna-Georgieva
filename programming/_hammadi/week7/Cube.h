#ifndef __Cube_h_
#define __Cube_h_
#include "theLargest.h"

class Cube
{
	private:
		int h;
		int w;
	
	public:
		void setHW(int,int);
		int getH();
		int getW();
		
		Cube(int h_in, int w_in);
		~Cube();
		
		Cube operator+(const Cube &c_in);
	
};

#endif
