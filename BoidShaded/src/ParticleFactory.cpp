#include "ParticleFactory.h"
#include "Sphere.h"


Particle * ParticleFactory::CreateParticle(
                                            ParticleType _type,
                                            ngl::Vec3 _pos,
                                            ngl::Vec3 _dir,
                                            ngl::Colour _c,
                                            const std::string &_shaderName,
                                            Emitter *_parent
                                          )
{

  if(_type==ParticleType::SPHERE)
  {
    return new Sphere(_pos,_dir,_c,_shaderName,_parent);
  }
  else return nullptr;
}
