// TestTemp.cpp
#include "TestTemp.h"

template <class T>
TestTemp<T>::TestTemp()
{
	m_Obj=0;
}
 
template <class T>
void TestTemp<T>::SetValue( T obj_i )
{
	m_Obj=obj_i;
}
 
template <class T>
T TestTemp<T>::GetValue()
{
   return m_Obj;
}
