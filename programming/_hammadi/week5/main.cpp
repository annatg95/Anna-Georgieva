#include <iostream>
#include "Parent.h"
#include "Sphere.h"
#include "Cuboid.h"

using namespace std;


int main()
{
	cout<<"test:"<<endl;
	
	
	Parent *p=new Parent(1,2,3);
	cout<<"parent x:"<<p->getX();
	cout<<" y:"<<p->getY();
	cout<<" z:"<<p->getZ()<<endl;
	delete p;
	
	
	Sphere *s=new Sphere(4,5,6,2.0);
	cout<<"sphere x:"<<s->getX()<<" y: "<<s->getY()<<" z: "<<s->getZ()<<" r: "<<s->getRad()<<"\t";
	
	s->setColor(44,34,134);
	cout<<"sphere color r:"<<s->getR()<<" g:"<<s->getG()<<" b:"<<s->getB()<<endl;
	delete s;
	
	
	Cuboid *c=new Cuboid(7.0,8.0,9.0,1,3,5);
	cout<<"cuboid w:"<<c->getW()<<" h:"<<c->getH()<<" l:"<<c->getL()<<endl;
	cout<<"cuboid x:"<<c->getX()<<" y:"<<c->getY()<<" z:"<<c->getZ()<<"\t";
	
	c->setColor(111,255,222);
	cout<<"cuboid color r:"<<c->getR()<<" g:"<<c->getG()<<" b:"<<c->getB()<<endl;
	
	delete c;
	
}

