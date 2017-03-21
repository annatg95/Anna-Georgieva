#include "Vehicle.h"
#include "Car.h"
#include "Lorry.h"

int main()
{
	int feeCar=5,feeLorry=10;
	
	int *FerryArray= new int[10];
	for(int i=0; i<10;i++)
	{
		std::cout<<"ferryArray["<<i<<"]"<<FerryArray[i]<<std::endl;
	}
	
	
	Car *vehicle1=new Car(3);
	
	vehicle1->getNumOfPass();
	vehicle1->setFees(feeCar);

	Car *vehicle2=new Car(1);
	
	vehicle2->getNumOfPass();
	vehicle2->setFees(feeCar);
	
	Lorry *vehicle3=new Lorry(200);
	
	vehicle3->getWeight();
	vehicle3->setFees(feeLorry);
	
	Lorry *vehicle4=new Lorry(3500);

	vehicle4->getWeight();
	vehicle4->setFees(feeLorry);
	
	Lorry *vehicle5=new Lorry(1500);
	
	vehicle5->getWeight();
	vehicle5->setFees(feeLorry);

	vehicle5->getNumber();
	vehicle5->getMoney();
	
	for(int i=0; i<10;i++)
	{
		*(FerryArray+i)=i;
		
	}
	
	//menu switch.....
	
	
	delete vehicle1;
	
	delete vehicle2;
	
	delete vehicle3;
	
	delete vehicle4;
	
	delete vehicle5;
	
	delete FerryArray;
}
