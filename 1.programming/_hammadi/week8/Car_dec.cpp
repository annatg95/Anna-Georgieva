#include "Vehicle.h"
#include "Car.h"

Car::Car(int numOfP_in):Vehicle(fees)
{
	numOfPassengers=numOfP_in;
}

Car::~Car()
{
	//dtor
}

void Car::setNumOfPass(int numOfP_in)
{
	numOfPassengers=numOfP_in;
}

int Car::getNumOfPass()
{
	std::cout<<"Car: Number of passengers: "<<numOfPassengers<<std::endl;
}

