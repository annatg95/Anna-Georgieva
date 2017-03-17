#include <iostream>
#include <QtGui/QGuiApplication>
#include "OpenGLWindow.h"

int main(int argc, char **argv)
{
  //  std::cout<<"aaaaaaaaaaaazn";

    QGuiApplication app (argc, argv);
    OpenGLWindow window;

    window.resize(1024, 720);
    window.show();

    return app.exec();
}
