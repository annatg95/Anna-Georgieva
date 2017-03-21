#include <QMouseEvent>
#include <QGuiApplication>

#include "NGLScene.h"
#include <ngl/Camera.h>
#include <ngl/Light.h>
#include <ngl/Transformation.h>
#include <ngl/Material.h>
#include <ngl/NGLInit.h>
#include <ngl/VAOPrimitives.h>
#include <ngl/ShaderLib.h>
#include <array>



NGLScene::NGLScene()
{
  setTitle("Qt5 Simple NGL Demo");
}


NGLScene::~NGLScene()
{
  std::cout<<"Shutting down NGL, removing VAO's and Shaders\n";
  m_vao->removeVOA();
}

void NGLScene::resizeGL( int _w, int _h )
{
  m_cam.setShape( 45.0f, static_cast<float>( _w ) / _h, 0.05f, 350.0f );
  m_win.width  = static_cast<int>( _w * devicePixelRatio() );
  m_win.height = static_cast<int>( _h * devicePixelRatio() );
}


void NGLScene::initializeGL()
{
  // we need to initialise the NGL lib which will load all of the OpenGL functions, this must
  // be done once we have a valid GL context but before we call any GL commands. If we dont do
  // this everything will crash
  ngl::NGLInit::instance();

  glClearColor(0.4f, 0.4f, 0.4f, 1.0f);			   // Grey Background
  // enable depth testing for drawing

  glEnable(GL_DEPTH_TEST);
  glEnable(GL_MULTISAMPLE);
  // Now we will create a basic Camera from the graphics library
  // This is a static camera so it only needs to be set once
  // First create Values for the camera position
  ngl::Vec3 from(5,150,0);
  ngl::Vec3 to(0,0,0);
  ngl::Vec3 up(0,1,0);

  m_cam.set(from,to,up);
  // set the shape using FOV 45 Aspect Ratio based on Width and Height
  // The final two are near and far clipping planes of 0.5 and 10
  m_cam.setShape(45,720.0/576.0,0.01f,150.0f);

  // now to load the shader and set the values
  // grab an instance of shader manager
  ngl::ShaderLib* shader = ngl::ShaderLib::instance();
  // we are creating a shader called Phong to save typos
  // in the code create some constexpr
  constexpr auto shaderProgram = "Phong";
  constexpr auto vertexShader  = "PhongVertex";
  constexpr auto fragShader    = "PhongFragment";
  // create the shader program
  shader->createShaderProgram( shaderProgram );
  // now we are going to create empty shaders for Frag and Vert
  shader->attachShader( vertexShader, ngl::ShaderType::VERTEX );
  shader->attachShader( fragShader, ngl::ShaderType::FRAGMENT );
  // attach the source
  shader->loadShaderSource( vertexShader, "shaders/PhongVertex.glsl" );
  shader->loadShaderSource( fragShader, "shaders/PhongFragment.glsl" );
  // compile the shaders
  shader->compileShader( vertexShader );
  shader->compileShader( fragShader );
  // add them to the program
  shader->attachShaderToProgram( shaderProgram, vertexShader );
  shader->attachShaderToProgram( shaderProgram, fragShader );


  // now we have associated that data we can link the shader
  shader->linkProgramObject( shaderProgram );
  // and make it active ready to load values
  ( *shader )[ shaderProgram ]->use();
  // the shader will use the currently active material and light0 so set them
  ngl::Material m( ngl::STDMAT::GOLD );
  // load our material values to the shader into the structure material (see Vertex shader)
  m.loadToShader( "material" );
  shader->setShaderParam3f("viewerPos",m_cam.getEye().m_x,m_cam.getEye().m_y,m_cam.getEye().m_z);
  // now create our light this is done after the camera so we can pass the
  // transpose of the projection matrix to the light to do correct eye space
  // transformations
  ngl::Mat4 iv=m_cam.getViewMatrix();
  iv.transpose();
  iv=iv.inverse();
  ngl::Light l(ngl::Vec3(0,1,0),ngl::Colour(1,1,1,1),ngl::Colour(1,1,1,1),ngl::LightModes::POINTLIGHT);
  l.setTransform(iv);
  // load these values to the shader as well
  l.loadToShader("light");

  buildVAO();
  glViewport(0,0,width(),height());

  m_bbox.reset( new ngl::BBox(ngl::Vec3::zero(),60.0f,60.0f,60.0f));

  m_bbox->setDrawMode(GL_LINE);

  ngl::VAOPrimitives *prim=ngl::VAOPrimitives::instance();
  prim->createSphere("sphere",1.0,20);

  m_emitter.reset( new Emitter(ngl::Vec3::zero()/*m_emitterPos*/,15,&m_cam) );
  m_text.reset( new ngl::Text(QFont("Arial",14)));
  m_text->setScreenSize(width(),height());
 m_sphereUpdateTimer=startTimer(100);

}


void NGLScene::buildVAO()
{
  std::array<ngl::Vec3,12> verts=
  {{
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

  }};

  std::vector <ngl::Vec3> normals;
  ngl::Vec3 n=ngl::calcNormal(verts[2],verts[1],verts[0]);
  normals.push_back(n);
  normals.push_back(n);
  normals.push_back(n);
  n=ngl::calcNormal(verts[3],verts[4],verts[5]);
  normals.push_back(n);
  normals.push_back(n);
  normals.push_back(n);

  n=ngl::calcNormal(verts[6],verts[7],verts[8]);
  normals.push_back(n);
  normals.push_back(n);
  normals.push_back(n);

  n=ngl::calcNormal(verts[11],verts[10],verts[9]);
  normals.push_back(n);
  normals.push_back(n);
  normals.push_back(n);

  std::cout<<"sizeof(verts) "<<sizeof(verts)<<" sizeof(ngl::Vec3) "<<sizeof(ngl::Vec3)<<"\n";
  // create a vao as a series of GL_TRIANGLES
  m_vao.reset( ngl::VertexArrayObject::createVOA(GL_TRIANGLES));
  m_vao->bind();

  // in this case we are going to set our data as the vertices above

	m_vao->setData(sizeof(verts),verts[0].m_x);
	// now we set the attribute pointer to be 0 (as this matches vertIn in our shader)

	m_vao->setVertexAttributePointer(0,3,GL_FLOAT,0,0);

	m_vao->setData(sizeof(verts),normals[0].m_x);
	// now we set the attribute pointer to be 2 (as this matches normal in our shader)

	m_vao->setVertexAttributePointer(2,3,GL_FLOAT,0,0);

	m_vao->setNumIndices(sizeof(verts)/sizeof(ngl::Vec3));

 // now unbind
  m_vao->unbind();


}



void NGLScene::paintGL()
{
  // clear the screen and depth buffer
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glViewport(0,0,m_win.width,m_win.height);

  // Rotation based on the mouse position for our global
  // transform
  ngl::Mat4 rotX;
  ngl::Mat4 rotY;
  // create the rotation matrices
  rotX.rotateX(m_win.spinXFace);
  rotY.rotateY(m_win.spinYFace);
  // multiply the rotations
  m_mouseGlobalTX=rotY*rotX;
  // add the translations
  m_mouseGlobalTX.m_m[3][0] = m_modelPos.m_x;
  m_mouseGlobalTX.m_m[3][1] = m_modelPos.m_y;
  m_mouseGlobalTX.m_m[3][2] = m_modelPos.m_z;

  m_emitter->setGlobalTransform(m_mouseGlobalTX);
  m_emitter->draw();

  QString text;
  text.sprintf("number of particles %d",m_emitter->getNumParticles());
  m_text->setColour(1,1,1);
  m_text->renderText(10,10,text);
  m_text->renderText(10,30,QString("1 add Sphere"));
  m_text->renderText(10,50,QString("r remove last particle"));
  m_text->renderText(10,90,QString("Space clears all particles"));

  ngl::ShaderLib *shader=ngl::ShaderLib::instance();
  (*shader)["Phong"]->use();

 m_bbox->draw();

  ngl::Mat4 MV;
  ngl::Mat4 MVP;
  ngl::Mat3 normalMatrix;
  ngl::Mat4 M;
  ngl::Transformation tx;

  m_vao->bind();

for(int x=1; x<5; ++x)
{
//  for(int y=1; y<10; ++y)

    tx.addPosition(x,0,0);

      M=tx.getMatrix()*m_mouseGlobalTX;
      MV=  M*m_cam.getViewMatrix();
      MVP= M*m_cam.getVPMatrix();
      normalMatrix=MV;
      normalMatrix.inverse();
      shader->setShaderParamFromMat4("MV",MV);
      shader->setShaderParamFromMat4("MVP",MVP);
      shader->setShaderParamFromMat3("normalMatrix",normalMatrix);
      shader->setShaderParamFromMat4("M",M);


  m_vao->draw();
}
  m_vao->unbind();
}

void NGLScene::addParticles( int _type)
{
if(_type==0)
{
  m_emitter->addParticle(ParticleType::SPHERE);
}


}

//----------------------------------------------------------------------------------------------------------------------
void NGLScene::mouseMoveEvent( QMouseEvent* _event )
{
  // note the method buttons() is the button state when event was called
  // that is different from button() which is used to check which button was
  // pressed when the mousePress/Release event is generated
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


//----------------------------------------------------------------------------------------------------------------------
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

//----------------------------------------------------------------------------------------------------------------------
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

//----------------------------------------------------------------------------------------------------------------------
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
//----------------------------------------------------------------------------------------------------------------------

void NGLScene::keyPressEvent(QKeyEvent *_event)
{
  // this method is called every time the main window recives a key event.
  // we then switch on the key value and set the camera in the GLWindow
  switch (_event->key())
  {
  // escape key to quite
  case Qt::Key_Escape : QGuiApplication::exit(EXIT_SUCCESS); break;
  // turn on wirframe rendering
  case Qt::Key_W : glPolygonMode(GL_FRONT_AND_BACK,GL_LINE); break;
  // turn off wire frame
  case Qt::Key_S : glPolygonMode(GL_FRONT_AND_BACK,GL_FILL); break;
  // show full screen
  case Qt::Key_F : showFullScreen(); break;
  // show windowed
  case Qt::Key_N : showNormal(); break;
  case Qt::Key_1 : addParticles(0); break;
  case Qt::Key_Space : m_emitter->clearParticles(); break;
  case Qt::Key_R : m_emitter->removeParticle(); break;

  default : break;

  }
  // finally update the GLWindow and re-draw
  //if (isExposed())
    update();
}


void NGLScene::timerEvent( QTimerEvent *_event)
{
    m_emitter->update();
    update();
}
