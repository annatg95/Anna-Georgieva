//#include <QCoreApplication>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

using namespace std;

class sortalg {
    int *p, *temp, num;
  public:
    sortalg (int *a,int b) : num(b) { p=a; temp = new int[b]; }
    void InsertSort();
    int compare(int a,int b) { if (a>=b) return 1; else return 0; };
    void swap(int j,int i) {int tmp; tmp=p[j]; p[j]=p[i]; p[i]=tmp;};
    void prt() {
        for (int i=0;i<num;i++){
        cout<<"sorted(inside): "<<p[i]<<endl;}
    }
    void MergeSort(int left, int right) {
        if (right>left) {

            MergeSort(left,floor((right+left)/2));

            MergeSort(floor((right+left)/2)+1,right);

            Merge(left,(int) floor((right+left)/2),right);

        }
    }
    void Merge(int left, int middle, int right);
};


void sortalg::InsertSort () {
  int i,j,k;
  for(i=1; i<num; i++) {
      j=i-1;
      k=i;
      while (compare(p[j],p[k]) && j>=0) {
          swap(j,k);
          j--; k--;
      }
  }
}


void sortalg::Merge (int left, int middle, int right) {
    int i, j, k;

    i=left; j=middle+1;

    for(k=left;k<=right;k++) {
         if(i>middle)
             temp[k]=p[j++];
         else if (j>right)
             temp[k]=p[i++];
         else if (p[i]>p[j])
             temp[k]=p[j++];
         else temp[k]=p[i++];
    }

    for(k=left;k<right+1;k++) {
         cout<<p[k]<<"<--->"<<temp[k]<<endl;
         p[k]=temp[k];
    }
    cout<<"---merge---"<<endl;
}


int main () {
    int datap[10]={42,20,17,13,28,14,23,15,-9,-1};
    sortalg iuser (&datap[0],10);
//    iuser.MergeSort(0,9);
    iuser.InsertSort();
    iuser.prt();

    for(int i=0 ; i<10;i++){
        cout << "sorted(outside): " << datap[i]<<endl;
    }
    return 0;
}
