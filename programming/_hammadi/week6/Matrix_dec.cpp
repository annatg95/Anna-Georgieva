#include "Matrix.h"

Matrix::Matrix()
{
	array = new int*[3];
	for (unsigned i=0; i<3; ++i)
	{	
		array[i] = new int[3];
	}
	
	for(unsigned m=0; m<3; ++m)
	{
		for(unsigned n=0; n<3; ++n)
		{
			std::cin>>array[m][n];
		}
	}
	
}

Matrix::~Matrix()
{

}

void Matrix::setArr(int **array_in)
{
	for(unsigned x=0; x<3; x++)
	{
		for(unsigned y=0; y<3; y++)
		{
			array[x][y]=array_in[x][y];
		}
	}
}

int Matrix::getArr()
{
	std::cout<<std::endl;
	for(unsigned m=0; m<3; ++m)
	{
		for(unsigned n=0; n<3; ++n)
		{
			std::cout<<array[m][n]<<" ";
		}
		std::cout<<std::endl;
	}
}

/*

Matrix Matrix::operator+(const Matrix &array_in) 
{
	for(int x=0;x<3;x++)
	{
		for(int y=0;y<3;y++)
		{	
			array[x]=array_in->x+array[x];
			array[y]=array_in->y+array[y];
		}
	}
}
Matrix Matrix::operator-(const Matrix &array_in)
{
	for(int x=0;x<3;x++)
	{
		for(int y=0;y<3;y++)
		{	
			array[x][y]=array[x][y]-array_in[x][y];
		}
	}
}

Matrix Matrix::operator*(const Matrix &array_in) 
{
	for(int x=0;x<3;x++)
	{
		for(int y=0;y<3;y++)
		{	
			array[x][y]=array[x][y]*array_in[x][y];
		}
	}
}

*/
