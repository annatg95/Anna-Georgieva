#include <iostream>
#include "Vehicle.h"

int Vehicle::numOfVeh=0;
int Vehicle::money=0;

Vehicle::Vehicle(int fees_in)
{
	numOfVeh++;
	fees=fees_in;
}

Vehicle::~Vehicle()
{
	numOfVeh--;
}

void Vehicle::setFees(int fees_in)
{
	fees=fees_in;
	money+=fees_in;
}

int Vehicle::getFees()
{
	std::cout<<"Fees: "<<fees<<std::endl;
}

int Vehicle::getNumber()
{
	std::cout<<"Vehicles in the Queue: "<<numOfVeh<<std::endl;
}

int Vehicle::getMoney()
{
	std::cout<<"TOTAL SUM: "<<money<<std::endl;
}
