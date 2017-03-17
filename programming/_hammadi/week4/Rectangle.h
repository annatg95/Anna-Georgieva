#ifndef __Rectangle_H__
#define __Rectangle_H__
#include <vector>

class Rectangle
{
	private:
		int x;
		int y;
		int z;
		
		
	public:
		void setX(int);
		void setY(int);
		void setZ(int);
		
		int getX();
		int getY();
		int getZ();
		
		
		Rectangle();
		Rectangle(int,int,int);
		Rectangle(const Rectangle &Rectangle0);
		
		~Rectangle();
		
		void printR();
		void moveR(int,int,int);
		void scaleR(int);
		void calculateP();
	
		//int getObjCount();
};

#endif
