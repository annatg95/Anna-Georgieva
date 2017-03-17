#ifndef __Car_H__
#define __Car_H__
#include "Vehicle.h"

class Car:public Vehicle
{
	private:
		int numOfPassengers;
		
	public:
	
		Car(int numOfP_in);
		~Car();
		
		void setNumOfPass(int numOfP_in);
		int getNumOfPass();
		
	
};



#endif
