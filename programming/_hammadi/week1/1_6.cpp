#include <iostream>
#include <string>
using namespace std;

struct number
{
	int a;
	int b;
	int c;
	int x;
	char x1='x';
	int y;
	char y1='y';
};

void checkF(number *data1, number *data2)
{
	
	if(data1->a >0)
	{	
		if(data1->b>0)
			{
				if(data1->c>0)
				{
					
					cout<<"x=("<<data1->b<<data1->y1<<"-"<<data1->c<<")/"<<data1->a<<endl;
					cout<<"Solution:"<<endl;
					cout<<data2->a<<"(";
					cout<<data1->b<<data1->y1<<"-"<<data1->c<<")/"<<data1->a;
					cout<<"+"<<data2->b<<data2->y1<<"-"<<data2->c<<endl;
				}
				else
				{

					cout<<"x=("<<data1->b<<data1->y1<<"+"<<-data1->c<<")/"<<data1->a<<endl;
					cout<<"Solution:"<<endl;
					cout<<data2->a<<"(";
					cout<<data1->b<<data1->y1<<"-"<<data1->c<<")/"<<data1->a;
					cout<<"+"<<data2->b<<data2->y1<<"-"<<data2->c<<endl;
				}
			}
			else
			{
				//ako b<0
				//vmakni dvete c ta
			}
	}
	else
	{
		cout<<"First equation:";
		cout<<"x=("<<data1->c<<"-"<<data1->b<<data1->y1<<")/"<<-data1->a<<endl;
		cout<<"Solution:"<<endl;
		cout<<data2->a<<"(";
		cout<<data1->c<<"-"<<data1->b<<data1->y1<<")/"<<-data1->a<<"+"<<data2->b<<data2->y1<<-data2->c<<endl;
		
		//vavedi dvete b ta i dvete c ta
	}
	
	
}
	

void getValue(number *data)
{
	cout << "Enter a: ";
	cin >> data->a;
	cout << "Enter b: ";
	cin >> data->b;
	cout << "Enter c: ";
	cin >> data->c;

	cin.sync();
}


int main()
{
	number equation1,equation2;
	getValue(&equation1);
	getValue(&equation2);

	
	checkF(&equation1, &equation2);
	return 0;
}


