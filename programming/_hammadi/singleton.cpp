#include<iostream>
#include<string>
using namespace std;

class Product{
public:
	virtual string getName() = 0;
};

class ConcreteProductA : public Product
{
public:
	string getName()
	{
		return "A";
	}
};

class ConcreteProductB : public Product
{
public:
	string getName()
	{
		return "B";
	}
};

class Creator
{
public:
	virtual Product* FactoryMethod() = 0;
};

class ConcreteCreatorA : public Creator
{
public:
	Product* FactoryMethod() 
	{
		return new ConcreteProductA();
	}
};

class ConcreteCreatorB : public Creator
{
public:
	Product* FactoryMethod() 
	{
		return new ConcreteProductB();
	}
};

int main()
{
	const int size = 2;
	Creator* creators[size];
      creators[0] = new ConcreteCreatorA();
      creators[1] = new ConcreteCreatorB();

	for(int i=0;i<size;i++)
	{
		Product* product = creators[i]->FactoryMethod();
		cout<<product->getName()<<endl;
		delete product;
	}

	int a;
	cin>>a;

	for(int i=0;i<size;i++){
		delete creators[i];
	}
	return 0;
}
