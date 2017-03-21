#ifndef SPHERE_H__
#define SPHERE_H__


#include "Particle.h"


class Sphere : public Particle
{
    public :

    Sphere(ngl::Vec3 _pos, ngl::Vec3 _dir, ngl::Colour _c, const std::string &_shaderName, Emitter *_parent);
    virtual ~Sphere();
    virtual void draw() const;
    virtual void update();
    virtual inline ParticleType getType()const {return m_type;}

  private :
    GLfloat m_emitAngle;
    GLfloat m_radius;
    const static ParticleType m_type=ParticleType::SPHERE;



 };


#endif
