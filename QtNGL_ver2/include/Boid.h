#ifndef BOID_H
#define BOID_H

#include "Particle.h"


class Boid:public Particle
{
public :

    Boid(ngl::Vec3 _pos,  ngl::Vec3 _dir, Emitter *_parent);

    //the boid VAO pointer
    std::unique_ptr<ngl::AbstractVAO> m_vao;


    //bind draw unbind the m_vao
    void draw() ;
    void loadMatricesToShader(ngl::Transformation &_tx, const ngl::Mat4 &_globalMat,ngl::Camera *_cam )const;

    //collision check
    /*
    inline void reverse(){m_dir=m_dir*-1.0;}
    inline void setHit(){m_hit=true;}
    inline void setNotHit(){m_hit=false;}
    inline bool isHit()const {return m_hit;} */

      inline ngl::Vec3 getPos() const {return m_pos;}
      inline ngl::Vec3 getNextPos() const {return m_nextPos;}

  inline void setDirection(ngl::Vec3 _d){m_dir=_d;}
  inline ngl::Vec3 getDirection() const { return m_dir;}
  void move();
  void set(ngl::Vec3 _pos, ngl::Vec3 _dir);

private :
  ngl::Vec3 m_pos;
  ngl::Vec3 m_dir;
  ngl::Vec3 m_lastPos;
  ngl::Vec3 m_nextPos;
  bool m_hit;


};
#endif
