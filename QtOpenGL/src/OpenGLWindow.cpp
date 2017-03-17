#include "OpenGLWindow.h"
#include <QKeyEvent>
#include <QApplication>
#include <GL/glu.h>


OpenGLWindow::OpenGLWindow()
{
    setTitle("QT5 and opengl");
}


OpenGLWindow::~OpenGLWindow()
{
    //dtor;
}

void OpenGLWindow::initializeGL()
{
    glClearColor(0.8,0.8,0.8,1);
    glMatrixMode(GL_PROJECTION);
    gluPerspective(45.0f, (float)m_width/m_height, 0.01f, 10.0f);
    glMatrixMode(GL_MODELVIEW);
    gluLookAt(2,10,2,0,0,0,0,1,0);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_NORMALIZE);

    startTimer(5);
}

void OpenGLWindow::drawTriangle(int _pX, int _pY, int _pZ)
{
  //  glPushMatrix();
      glRotatef(m_rotY,0,1,0);
      glBegin(GL_TRIANGLES);

       glColor3f(0.3,0.4,0.5);
       glVertex3f(-_pX,-_pY,0);

       glColor3f(0.5,0.4,0.3);
       glVertex3f(_pX,-_pY,0);

       glColor3f(0.0,0,0.9);
       glVertex3f(0,_pY,0);
      glEnd();
   //glPopMatrix();
}

void OpenGLWindow::paintGL()
{
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
   glViewport(0,0,m_width,m_height);
glPushMatrix();
    drawTriangle(1,1,1);
//glPopMatrix();
    for(int j=-5; j<5; ++j)
    for(int k=-5; k<5; ++k)
    for(int i=-5; i<5; ++i)
    {
    glPushMatrix();
      glRotated(m_rotY,0,1,0);
      glTranslated(i,j,k);
      glScalef(0.1,0.1,0.1);
       drawTriangle(1,1,1);
    glPopMatrix();
    }

}





void OpenGLWindow::resizeGL(int _w, int _h)
{
    m_width=_w;
    m_height=_h;
     glMatrixMode(GL_PROJECTION);
     glLoadIdentity();
     gluPerspective(45.0f, (float)m_width/m_height, 0.01f, 10.0f);
     glMatrixMode(GL_MODELVIEW);

}

void OpenGLWindow::keyPressEvent(QKeyEvent *_event)
{
    switch(_event->key())
    {
    case Qt::Key_Escape : QApplication::exit(EXIT_SUCCESS); break;
    case Qt::Key_W: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE); break;
    case Qt::Key_S: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL); break;
    }
    update();
}

void OpenGLWindow::timerEvent(QTimerEvent *_event)
{
    m_rotY+=0.5;
    update();
}
