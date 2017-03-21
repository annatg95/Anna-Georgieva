#ifndef __Vehicle_H__
#define __Vehicle_H__
#include <iostream>

class Vehicle
{
	protected:
		static int numOfVeh;
		int fees;
		static int money;
		
	public:
		
		Vehicle(int fees_in);
		~Vehicle();
		
		void setFees(int fees_in);
		
		virtual int getNumber();
		virtual int getFees();
		virtual int getMoney();
	
};

#endif
