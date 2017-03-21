#include "NGLScene.h"
#include <iostream>
#include <ngl/Vec3.h>
#include <ngl/Light.h>
#include <ngl/NGLInit.h>

#include <ngl/Material.h>
#include <ngl/ShaderLib.h>
#include <QColorDialog>

NGLScene::NGLScene( QWidget *_parent ) : QOpenGLWidget( _parent )
{
  setFocus();
  this->resize(_parent->size());
}

void NGLScene::initializeGL()
{

  ngl::NGLInit::instance();
  glClearColor(0.4f, 0.4f, 0.4f, 1.0f);			   // Grey Background
  glEnable(GL_DEPTH_TEST);
  glEnable(GL_MULTISAMPLE);

  ngl::Vec3 eye(5,2,0);
  ngl::Vec3 look(0,0,0);
  ngl::Vec3 up(0,1,0);
  m_cam.set(eye,look,up);
  m_cam.setShape(45,float(1024/720),0.1,300);

  m_bbox.reset( new ngl::BBox(ngl::Vec3(),60.0f,60.0f,60.0f));
  m_bbox->setDrawMode(GL_LINE);

  buildVAO();
  ngl::VAOFactory::listCreators();
  update();
}

void NGLScene::resizeGL( int _w, int _h )
{
  m_cam.setShape( 45.0f, static_cast<float>( _w ) / _h, 0.05f, 350.0f );
  m_win.width  = static_cast<int>( _w * devicePixelRatio() );
  m_win.height = static_cast<int>( _h * devicePixelRatio() );
}

void NGLScene::buildVAO()
{
  std::vector<ngl::Vec3> verts=
  {
    ngl::Vec3(0,1,1),
    ngl::Vec3(0,0,-1),
    ngl::Vec3(-0.5,0,1),
    ngl::Vec3(0,1,1),
    ngl::Vec3(0,0,-1),
    ngl::Vec3(0.5,0,1),
    ngl::Vec3(0,1,1),
    ngl::Vec3(0,0,1.5),
    ngl::Vec3(-0.5,0,1),
    ngl::Vec3(0,1,1),
    ngl::Vec3(0,0,1.5),
    ngl::Vec3(0.5,0,1)

  };
  std::cout<<"Initial "<<verts.size()<<'\n';
  ngl::Vec3 n=ngl::calcNormal(verts[2],verts[1],verts[0]);
  verts.push_back(n);
  verts.push_back(n);
  verts.push_back(n);
  n=ngl::calcNormal(verts[3],verts[4],verts[5]);
  verts.push_back(n);
  verts.push_back(n);
  verts.push_back(n);

  n=ngl::calcNormal(verts[6],verts[7],verts[8]);
  verts.push_back(n);
  verts.push_back(n);
  verts.push_back(n);

  n=ngl::calcNormal(verts[11],verts[10],verts[9]);
  verts.push_back(n);
  verts.push_back(n);
  verts.push_back(n);


  std::cout<<"sizeof(verts) "<<sizeof(verts)<<" sizeof(ngl::Vec3) "<<sizeof(ngl::Vec3)<<"\n";
  m_vao.reset(ngl::VAOFactory::createVAO("simpleVAO",GL_TRIANGLES) );
  m_vao->bind();
  m_vao->setData(ngl::SimpleVAO::VertexData(verts.size()*sizeof(ngl::Vec3),verts[0].m_x));
  m_vao->setVertexAttributePointer(0,3,GL_FLOAT,0,0);
  m_vao->setVertexAttributePointer(2,3,GL_FLOAT,0,12*3);
  m_vao->setNumIndices(verts.size());
  m_vao->unbind();


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

   m_vao->bind();
   m_vao->draw();
   m_vao->unbind();


}


NGLScene::~NGLScene()
{
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
