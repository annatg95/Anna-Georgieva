#ifndef __Lorry_H__
#define __Lorry_H__
#include "Vehicle.h"

class Lorry:public Vehicle
{
	private:
		int weight;
		
	public:
		Lorry(int weight_in);
		~Lorry();
		
		void setWeight(int weight_in);
		int getWeight();
	
	
};

#endif
