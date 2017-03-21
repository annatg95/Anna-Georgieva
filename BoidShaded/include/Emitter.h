#ifndef EMITTER_H__
#define EMITTER_H__

#include "ParticleFactory.h"
#include "ParticleTypeinfo.h"
#include <ngl/Camera.h>
#include <vector>
#include <memory>
class Emitter
{
  public :

    Emitter(ngl::Vec3 _pos, unsigned int _numParticles, const ngl::Camera *_cam  );
     Emitter(ngl::Vec3 _pos, unsigned int _numParticles,const ngl::Camera *_cam, ParticleType _type  );

    ~Emitter();
    void update();
    void draw() const;
    void addParticle( ParticleType _type );
    void removeParticle();

    inline unsigned int getNumParticles()const {return m_numParticles;}
    inline const ngl::Camera *getCamera() const {return m_cam;}
    void clearParticles();
    inline ngl::Vec3 getPos()const {return m_pos;}
     inline void setPos(const ngl::Vec3 &_v){m_pos=_v;}
    inline void setGlobalTransform(const ngl::Mat4 &_t){m_globalMouseTX=_t;}
    inline const ngl::Mat4 & getGlobalTransform() const { return m_globalMouseTX;}


  private :
    ngl::Vec3 m_pos;
    ngl::Mat4 m_globalMouseTX;

    std::vector < std::unique_ptr<Particle>> m_particles;

    const ngl::Camera *m_cam;
    unsigned int m_numParticles;

};


#endif
