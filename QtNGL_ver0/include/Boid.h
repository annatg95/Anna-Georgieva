#ifndef BOID_H
#define BOID_H


#include <ngl/Camera.h>
#include <ngl/ShaderLib.h>
#include <ngl/Transformation.h>
#include <ngl/Vec3.h>

/*! \brief a simple sphere class */
class Boid
{
public :

    Boid(ngl::Vec3 _pos,  ngl::Vec3 _dir,	GLfloat _rad	);
    Boid();

  void draw() ;
  void loadMatricesToShader( );

  inline ngl::Vec3 getPos() const {return m_pos;}
  inline ngl::Vec3 getNextPos() const {return m_nextPos;}
    inline GLfloat getRadius() const {return m_radius;}
  inline void setDirection(ngl::Vec3 _d){m_dir=_d;}
  inline ngl::Vec3 getDirection() const { return m_dir;}
    void move();
    void set(ngl::Vec3 _pos, ngl::Vec3 _dir, GLfloat _rad );
private :
  ngl::Vec3 m_pos;
  GLfloat m_radius;
  ngl::Vec3 m_dir;
  ngl::Vec3 m_lastPos;
  ngl::Vec3 m_nextPos;


};
