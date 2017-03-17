#include <iostream>
#include <vector>
#include <cstdlib>
#include "Point3.h"


int main()
{
	std::vector <Point3> points;

	for (int i=0; i<10; ++i)
	{
		points.push_back(Point3(i,i,i));
	}
	// we can access elements like a normal array
	points[0][0]=99;
	points[0][1]=99;
	points[0][2]=99;
	
	
	points[5][0]=99;
	points[5][1]=99;
	points[5][2]=99;
	


	for(auto p : points)
	{
		std::cout <<p<<'\n';
	}

	return EXIT_SUCCESS;
}













