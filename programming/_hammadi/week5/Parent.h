#ifndef _Parent_H__
#define _Parent_H__

class Parent
{
	protected:
		int m_xc;
		int m_yc;
		int m_zc;
		
		int color[3];
		
	public:
		void setX(int x_in);
		void setY(int y_in);
		void setZ(int z_in);
		
		int getX();
		int getY();
		int getZ();
		
		Parent(int,int,int);
		~Parent();
		
		void setColor(int r_in,int g_in, int b_in);
		int getR();
		int getG();
		int getB();
		
};

#endif
