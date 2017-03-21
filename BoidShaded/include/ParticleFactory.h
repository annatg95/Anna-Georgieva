#ifndef PARTICLE_FACTORY_H__
#define PARTICLE_FACTORY_H__

#include "Particle.h"

class Emitter;

class ParticleFactory
{
  public :
    Particle *CreateParticle( ParticleType _type, ngl::Vec3 _pos, ngl::Vec3 _dir, ngl::Colour _c,const std::string &_shaderName, Emitter *_parent);

  private :

};


#endif
