#include "Vehicle.h"
#include "Lorry.h"

Lorry::Lorry(int weight_in):Vehicle(fees)
{
	weight=weight_in;
}

Lorry::~Lorry()
{
	//dtor
	
}

void Lorry::setWeight(int weight_in)
{
	weight=weight_in;	
}

int Lorry::getWeight()
{
	std::cout<<"Lorry: Weight of the lorry: " <<weight<<std::endl;
}
