#ifndef _Sphere_H_
#define _Sphere_H_

class Sphere
{
	private:
	int m_xc;
	int m_yc;
	int m_zc;
	float m_r;
	
	public:
	
	void setX(int x);
	void setY(int y);
	void setZ(int z);
	void setR(float r);
	
	int	getX();
	int	getY();
	int	getZ();
	float getR();
	
	Sphere();
	Sphere(int, int, int, float);
	Sphere(const Sphere &sphere0);
	void moveS(int, int, int);
	void scaleS(int);
	void volumeS(float);
};

#endif
