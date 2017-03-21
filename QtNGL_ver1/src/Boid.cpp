#include "Boid.h"
#include "ngl/VAOFactory.h"
#include "ngl/SimpleVAO.h"

Boid::Boid(ngl::Vec3 _pos, ngl::Vec3 _dir)
{
    m_pos=_pos;
    m_dir=_dir;
    m_hit=false;
}

Boid::Boid(int a_in)
{
    /*static*/ int a=0;
    a=a_in;
    m_hit=false;
   // std::cout<<"Boid is created: "<<a<<std::endl;
}


void Boid::loadMatricesToShader( ngl::Transformation &_tx, const ngl::Mat4 &_globalMat, ngl::Camera *_cam  ) const
{
  ngl::ShaderLib *shader=ngl::ShaderLib::instance();

  ngl::Mat4 MV;
  ngl::Mat4 MVP;
  ngl::Mat3 normalMatrix;
  MV=_tx.getMatrix()*_globalMat*_cam->getViewMatrix() ;
  MVP=MV*_cam->getProjectionMatrix();
  normalMatrix=MV;
  normalMatrix.inverse();
  shader->setShaderParamFromMat4("MVP",MVP);
  shader->setShaderParamFromMat3("normalMatrix",normalMatrix);
}


void Boid::draw( )
{
  ngl::VAOFactory::listCreators();
  // draw wireframe if hit
  if(m_hit)
  {
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE);
  }
  else
  {
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
  }

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


  m_vao->draw();

  m_vao->unbind();

  //std::cout<<"Working?1"<<std::endl;

}



void Boid :: set(ngl::Vec3 _pos, ngl::Vec3 _dir)
{
  m_pos=_pos;
  m_dir=_dir;
}

void Boid::move()
{
  m_lastPos=m_pos;
  m_pos+=m_dir;
  m_nextPos=m_pos+m_dir;
  m_hit=false;
}



