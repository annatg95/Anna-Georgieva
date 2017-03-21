#include "NGLScene.h"
#include <iostream>
#include <ngl/Vec3.h>
#include <ngl/Light.h>
#include <ngl/NGLInit.h>
#include <ngl/Random.h>
#include <ngl/Material.h>

#include <ngl/Transformation.h>

#include <QColorDialog>
const static int s_extents=20;

NGLScene::NGLScene( QWidget *_parent, int _numOfBoids ) : QOpenGLWidget( _parent )
{
    m_numOfBoids=_numOfBoids; //std::cout<<_numOfBoids<<std::endl;
    m_animate=true;

    setFocus();
  //?  this->resize(_parent->size());
}

void NGLScene::resetBoids()
{
    m_boidArray.clear();
    ngl::Vec3 dir;
    ngl::Random *rng=ngl::Random::instance();

    for(int i=0; i<m_numOfBoids; ++i)
    {
        dir=rng->getRandomVec3();

        m_boidArray.push_back(Boid(rng->getRandomPoint(s_extents,s_extents,s_extents),dir));

        std::cout<<"m_boidArray working:"<<std::endl;
    }

}

NGLScene::~NGLScene()
{
    std::cout<<"Shutting down NGL, removing VAO's and Shaders\n";
}

void NGLScene::resizeGL( int _w, int _h )
{
  m_cam.setShape( 45.0f, static_cast<float>( _w ) / _h, 0.05f, 350.0f );
  m_win.width  = static_cast<int>( _w * devicePixelRatio() );
  m_win.height = static_cast<int>( _h * devicePixelRatio() );
}


void NGLScene::initializeGL()
{
  ngl::NGLInit::instance();
  glClearColor(0.4f, 0.4f, 0.4f, 1.0f);			   // Grey Background
  glEnable(GL_DEPTH_TEST);
  glEnable(GL_MULTISAMPLE);

  ngl::Vec3 eye(65,80,150);
  ngl::Vec3 look(0,0,0);
  ngl::Vec3 up(0,1,0);
  m_cam.set(eye,look,up);
  m_cam.setShape(45,float(1024/720),0.1,300);

  ngl::ShaderLib *shader=ngl::ShaderLib::instance();
  (*shader)["nglDiffuseShader"]->use();
  shader->setShaderParam4f("Colour",1.0f,1.0f,0.0f,1.0f);
  shader->setShaderParam3f("lightPos",1.0f,1.0f,1.0f);
  shader->setShaderParam4f("lightDiffuse",1.0f,1.0f,1.0f,1.0f);
  (*shader)["nglColourShader"]->use();
  shader->setShaderParam4f("Colour",1.0f,1.0f,1.0f,1.0f);

 glEnable(GL_DEPTH_TEST); // for removal of hidden surfaces




glPointSize(5);
 startTimer(200);

  m_bbox.reset( new ngl::BBox(ngl::Vec3(),60.0f,60.0f,60.0f));
  m_bbox->setDrawMode(GL_LINE);

  update();
}


void NGLScene::loadMatricesToShader()
{
    ngl::ShaderLib *shader=ngl::ShaderLib::instance();
      (*shader)["nglDiffuseShader"]->use();

      ngl::Mat4 MV;
      ngl::Mat4 MVP;
      ngl::Mat3 normalMatrix;
      MV= m_mouseGlobalTX*m_cam.getViewMatrix() ;
      MVP=MV*m_cam.getProjectionMatrix() ;
      normalMatrix=MV;
      normalMatrix.inverse();
      shader->setShaderParamFromMat4("MVP",MVP);
      shader->setShaderParamFromMat3("normalMatrix",normalMatrix);
}

void NGLScene::loadMatricesToColourShader()
{
  ngl::ShaderLib *shader=ngl::ShaderLib::instance();
  (*shader)["nglColourShader"]->use();
  ngl::Mat4 MV;
  ngl::Mat4 MVP;

  MV= m_mouseGlobalTX*m_cam.getViewMatrix() ;
  MVP=MV*m_cam.getProjectionMatrix();
  shader->setShaderParamFromMat4("MVP",MVP);

}

void NGLScene::paintGL()
{
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glViewport(0,0,m_win.width,m_win.height);

  ngl::Mat4 rotX;
  ngl::Mat4 rotY;
  rotX.rotateX(m_win.spinXFace);
  rotY.rotateY(m_win.spinYFace);
  m_mouseGlobalTX=rotY*rotX;
  m_mouseGlobalTX.m_m[3][0] = m_modelPos.m_x;
  m_mouseGlobalTX.m_m[3][1] = m_modelPos.m_y;
  m_mouseGlobalTX.m_m[3][2] = m_modelPos.m_z;

  ngl::ShaderLib *shader=ngl::ShaderLib::instance();
  (*shader)["nglColourShader"]->use();
  loadMatricesToColourShader();
  m_bbox->draw();
  shader->use("nglDiffuseShader");

//if you remove this your boid is gone! why ?
  ngl::ShaderLib *shader1=ngl::ShaderLib::instance();
  (*shader1)["nglColourShader"]->use();
  loadMatricesToColourShader();

 // std::cout<<"Working2"<<std::endl; pass test

//for loop store all the boids in the std::vector<Boid> m_boidArray;
 // ...........
ngl::Transformation t;
// ngl::Random *rng=ngl::Random::instance();

 //ngl::Vec3 m_pos=rng->getRandomVec3();


  Boid b1(1);
  b1.draw();
  t.setPosition(-10.0f,0.0f,0.0f);
  ngl::Mat4 MVP= m_mouseGlobalTX*t.getMatrix()*m_cam.getVPMatrix();
  shader->setUniform("MVP",MVP);

  Boid b2(1);
  b2.draw();
  t.setPosition(-20.0f,0.0f,0.0f);
  MVP= m_mouseGlobalTX*t.getMatrix()*m_cam.getVPMatrix();
  shader->setUniform("MVP",MVP);


  Boid b3(1);
  b3.draw();
  t.setPosition(5.0f,0.0f,0.0f); //m_pos
  MVP= m_mouseGlobalTX*t.getMatrix()*m_cam.getVPMatrix();
  shader->setUniform("MVP",MVP);

  ngl::ShaderLib:: instance()->setUniform("MVP", ngl::Mat4());
 // ngl::VAOPrimitives::instance()->draw("teapot");


//m_emitter->draw();

}


void NGLScene::addBoid()
{
    std::cout<<"add boid"<<std::endl;
}

void NGLScene::removeBoid()
{
    std::cout<<"rm boid"<<std::endl;
}


void NGLScene::setColour()
{
    QColor colour = QColorDialog::getColor();
    if( colour.isValid())
    {
        ngl::ShaderLib *shader=ngl::ShaderLib::instance();
        (*shader)["nglColourShader"]->use();
        shader->setShaderParam4f("Colour",colour.redF(),colour.greenF(),colour.blueF(),1.0);
        update();
    }
}


void NGLScene::mouseMoveEvent( QMouseEvent* _event )
{
  if ( m_win.rotate && _event->buttons() == Qt::LeftButton )
  {
    int diffx = _event->x() - m_win.origX;
    int diffy = _event->y() - m_win.origY;
    m_win.spinXFace += static_cast<int>( 0.5f * diffy );
    m_win.spinYFace += static_cast<int>( 0.5f * diffx );
    m_win.origX = _event->x();
    m_win.origY = _event->y();
    update();
  }
  // right mouse translate code
  else if ( m_win.translate && _event->buttons() == Qt::RightButton )
  {
    int diffX      = static_cast<int>( _event->x() - m_win.origXPos );
    int diffY      = static_cast<int>( _event->y() - m_win.origYPos );
    m_win.origXPos = _event->x();
    m_win.origYPos = _event->y();
    m_modelPos.m_x += INCREMENT * diffX;
    m_modelPos.m_y -= INCREMENT * diffY;
    update();
  }
}

void NGLScene::mousePressEvent( QMouseEvent* _event )
{
  // that method is called when the mouse button is pressed in this case we
  // store the value where the maouse was clicked (x,y) and set the Rotate flag to true
  if ( _event->button() == Qt::LeftButton )
  {
    m_win.origX  = _event->x();
    m_win.origY  = _event->y();
    m_win.rotate = true;
  }
  // right mouse translate mode
  else if ( _event->button() == Qt::RightButton )
  {
    m_win.origXPos  = _event->x();
    m_win.origYPos  = _event->y();
    m_win.translate = true;
  }
}

void NGLScene::mouseReleaseEvent( QMouseEvent* _event )
{
  // that event is called when the mouse button is released
  // we then set Rotate to false
  if ( _event->button() == Qt::LeftButton )
  {
    m_win.rotate = false;
  }
  // right mouse translate mode
  if ( _event->button() == Qt::RightButton )
  {
    m_win.translate = false;
  }
}

void NGLScene::wheelEvent( QWheelEvent* _event )
{

  // check the diff of the wheel position (0 means no change)
  if ( _event->delta() > 0 )
  {
    m_modelPos.m_z += ZOOM;
  }
  else if ( _event->delta() < 0 )
  {
    m_modelPos.m_z -= ZOOM;
  }
  update();
}

void NGLScene::timerEvent(QTimerEvent *)
{
    //   update();
}


