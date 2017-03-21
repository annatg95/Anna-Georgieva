#include "ParticleFactory.h"
#include "Boid.h"


Particle * ParticleFactory::CreateParticle( ngl::Vec3 _pos,ngl::Vec3 _dir,Emitter *_parent )
{


   return new Boid(_pos,_dir,_parent);

}
