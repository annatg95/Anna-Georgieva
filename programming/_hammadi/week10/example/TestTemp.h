// TestTemp.h
#ifndef _TESTTEMP_H_
#define _TESTTEMP_H_
#include <iostream>

template<class T>
class TestTemp  
{
public:
    TestTemp();
    void SetValue( T obj_i );
    T GetValue();
private:
    T m_Obj;
};
#endif
