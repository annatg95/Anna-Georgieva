#include "Particle.h"
#include <ngl/Random.h>

Particle::Particle(
                      ngl::Vec3 _pos,
                      ngl::Vec3 _dir,
                      Emitter *_parent
                     )
{
    // set the particles position on direction
    pos=_pos;
    dir=_dir;

  ngl::Random *rng=ngl::Random::instance();

  maxLife=rng->randomNumber(0)+1;
    life=0.0;
  parent=_parent;
}

Particle::~Particle()
{
  std::cout<<"particle  dtor\n";
}

