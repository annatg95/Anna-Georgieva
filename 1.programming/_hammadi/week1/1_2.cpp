#include <stdio.h>
#include <iostream>
using namespace std;

int main()
{
    int n=0;
    cin>>n;
    
    if(n<0)
    {
        cout<<"n is less than 1"<<endl;
    }
    else
    {
        int result=1;
        for(int i=n;i>0;i-- )
        {
            result*=i;
            
        }
        cout<<result<<endl;
    }
}
