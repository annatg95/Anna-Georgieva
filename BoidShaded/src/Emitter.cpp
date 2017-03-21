#include "Emitter.h"
#include "ParticleFactory.h"
#include <ngl/Random.h>
#include <typeinfo>
#include <Sphere.h>

Emitter::Emitter(ngl::Vec3 _pos, unsigned int _numParticles,const ngl::Camera *_cam )
{

  m_pos=_pos;
  m_numParticles=_numParticles;
  m_cam=_cam;
  m_particles.resize(m_numParticles);

  std::unique_ptr<ParticleFactory> p(  new  ParticleFactory);
  ngl::Random *rng=ngl::Random::instance();
  ngl::Vec3 dir;
  ngl::Colour c;
  int which;



  for(auto &particle : m_particles)
  {
    dir=0;
    //dir=rng->getRandomVec3();
    c=rng->getRandomColour();
    which=0;//(int)rng->randomPositiveNumber(4);
    while(which!=1)
    {
    particle.reset(p->CreateParticle(ParticleType::SPHERE,_pos,dir,c,"Phong",this)); break;

    }
  }
}


Emitter::Emitter( ngl::Vec3 _pos,unsigned int _numParticles, const ngl::Camera *_cam, const ParticleType _type  )
{
  m_cam=_cam;
  m_pos=_pos;
  m_numParticles=_numParticles;
  ParticleFactory *p = new  ParticleFactory;

  ngl::Random *rng=ngl::Random::instance();

  ngl::Vec3 dir;
  ngl::Colour c;

  for(auto &particle : m_particles)
  {
     dir=0;
    c=rng->getRandomColour();
   // std::unique_ptr<Particle> part( );
    particle.reset(p->CreateParticle(_type,_pos,dir,c,"Phong",this));
  }
  delete p;

}


void Emitter::addParticle(ParticleType _type )
{
  // create our render factory
  ParticleFactory *p = new  ParticleFactory;

  ngl::Random *rng=ngl::Random::instance();

  ngl::Vec3 dir;
  ngl::Colour c;
  dir=0;

  c=rng->getRandomColour();
  m_particles.push_back(std::unique_ptr<Particle> (p->CreateParticle(_type,m_pos,dir,c,"Phong",this)));
// we've done with the factory so delete it
  delete p;
  ++m_numParticles;
}

void Emitter::removeParticle()
{
  /// when we remove a particle we need to first check to see if we have any
  if(m_numParticles>0)
  {
    // now remove from the end of the std::vector
    m_particles.pop_back();
    // decrement the number of particles
    --m_numParticles;
  }
}
Emitter::~Emitter()
{
  m_particles.clear();
}


void Emitter::draw() const
{
  // call the draw method for each of the particles
  for(auto &p : m_particles)
  {
    p->draw();
  }
}

void Emitter::update()
{
  // call the update method for each particle
  for(auto &p : m_particles)
  {
    p->update();
  }
}



void Emitter::clearParticles()
{
  // must remember to re-size the std::vector back to 0
  m_particles.clear();
  m_numParticles=0;
}
