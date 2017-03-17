TARGET=QtOpenGL
OBJECTS_DIR=obj


QT+=opengl widgets



INCLUDEPATH += $$PWD//include
CONFIG+=c++11
SOURCES+=$$PWD/src/main.cpp\
         $$PWD/src/OpenGLWindow.cpp

HEADERS+=$$PWD/include/OpenGLWindow.h

linux:LIBS+= -lGLU
