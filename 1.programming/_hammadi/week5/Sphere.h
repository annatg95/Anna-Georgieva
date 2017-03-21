#ifndef _SPHERE_H__
#define _SPHERE_H__
#include "Parent.h"

class Sphere : public Parent
{
	private:
		float m_radius;
	public:
		
		void setRad(float r_in);
		float getRad();
		
		Sphere(int m_xc, int m_yc,int z_xc, float r_in);
		~Sphere();
};

#endif
