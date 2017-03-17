#include <iostream>
#include <string>
using namespace std;

int main()
{
	int sec=0;
	
	int s,m, m1,h=0;
	
	cout<<"Seconds:"<<endl;
	cin>>sec;
	
	if(sec>3600)
	{
		s=sec%60;
		m=sec/60;
		m1=m%60;
		h=m/60;
		cout<<"hours: "<<h<<" minutes:"<<m1<<" seconds:	"<<s<<endl;
	}
	else
	{
		s=sec%60;
		m=sec/60;
		h=m/60;
		cout<<"hours: "<<h<<" minutes:"<<m<<" seconds:	"<<s<<endl;
	}
	
	
	return 0;
}
