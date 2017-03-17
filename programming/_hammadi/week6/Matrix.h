#ifndef _Matrix_H__
#define _Matrix_H__

#include <iostream>

class Matrix
{
	private:
		int **array;
			
	public:
		
		Matrix();
		~Matrix();
		
		void setArr(int **array_in);
		int getArr();
		
		/*
		Matrix operator+(const Matrix &array_in);
		Matrix operator-(const Matrix &array_in);
		Matrix operator*(const Matrix &array_in);
		*/
};


#endif
