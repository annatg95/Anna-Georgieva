//#include <QCoreApplication>
#include <iostream>

using namespace std;

class sortalg {
    int *p, num;
  public:
    sortalg (int *a,int b) : num(b) {p=a;};
    void sorted();
    int compare(int a,int b) 
    { 
		if (a>=b) 
			return 1; 
		else 	
			return 0; 
	};
	
    void swap(int j,int i) 
    {
		int tmp; 
		tmp=p[j];
		p[j]=p[i]; 
		p[i]=tmp;
	};
    void prt() 
    {
        for (int i=0;i<num;i++)
        {
			cout<<"sorted(inside): "<<p[i]<<endl;
		}
    }
};

void sortalg::sorted () {
  int i,j,k;
  for(i=1; i<num; i++) {
      j=i-1;
      k=i;
      while (compare(p[j],p[k]) && j>=0) 
      {
          swap(j,k);
          j--; k--;
      }
  }
}

int main () 
{
    int datap[8]={42,20,17,13,28,14,23,15};
    sortalg iuser (&datap[0],8);

    iuser.sorted();
    iuser.prt();

    for(int i=0 ; i<8;i++){
        cout << "sorted(outside): " << datap[i]<<endl;
    }
    return 0;
}
