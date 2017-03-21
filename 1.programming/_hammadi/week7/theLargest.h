#ifndef __theLargest_h__
#define __theLargest_h__
#include <iostream>

template<class T>void bubbleS(T a[], int n)
{
    int i, j;
    for(i=0;i<n-1;i++)
    {
        for(j=i+1;j<n;j++)
        {
            if(a[i]>a[j])
            {
                T element;
                element = a[i];
                a[i] = a[j];
                a[j] = element;
            }
        }
    }
}

#endif
