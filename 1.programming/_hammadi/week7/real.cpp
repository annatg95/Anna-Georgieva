#include "theLargest.h"
#include "Sphere.h"
#include "Cube.h"

int main() 
{
    
    int a[4]={1,11,3,9};
    char b[4]={'s','b','d','e'};

    bubbleS(a,4);
    std::cout<<"\nSorted Order Integers: "<<std::endl;
    for(int i=0;i<4;i++)
    {
        std::cout<<a[i]<<"\t";
    }
    
    bubbleS(b,4);
    std::cout<<"\nSorted Order Characters: "<<std::endl;
    for(int j=0;j<4;j++)
    {
       std::cout<<b[j]<<"\t";   
	}
	std::cout<<std::endl;
	Sphere sp1(2);
	std::cout<<"sp1 radius: "<<sp1.getR()<<std::endl;
	Sphere sp2(3);
	std::cout<<"sp2 radius: "<<sp2.getR()<<std::endl;
	
	Sphere sp3(0);
	sp3=sp1+sp2;
	std::cout<<"sp3 radius: "<<sp3.getR()<<std::endl;
	
	Cube cu1(3,4);
	std::cout<<"cu1 h and w: "<<cu1.getH()<<"  "<<cu1.getW()<<std::endl;
	
	Cube cu2(9,4);
	std::cout<<"cu1 h and w: "<<cu2.getH()<<"  "<<cu2.getW()<<std::endl;
	
	Cube cu3(0,0);
	cu3=cu1+cu2;
	std::cout<<"cu1 h and w: "<<cu3.getH()<<"  "<<cu3.getW()<<std::endl;

	/*if(bubbleS(sp1.getR(),sp2.getR()))
	{
		std::cout<<"a>b"<<std::endl;
	}
	else
	{
		std::cout<<"a<b"<<std::endl;
	}

	*/
  
}
