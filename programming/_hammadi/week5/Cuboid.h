#ifndef _CUBOID_H__
#define _CUBOID_H__
#include "Parent.h"

class Cuboid:public Parent
{
	private:
		float m_width;
		float m_height;
		float m_lenght;
	
	public:
		void setW(float w_in);
		void setH(float h_in);
		void setL(float l_in);
		
		float getW();
		float getH();
		float getL();

		Cuboid(float w_in, float h_in, float l_in, int x_in, int y_in, int z_in);
		~Cuboid();
};
#endif
