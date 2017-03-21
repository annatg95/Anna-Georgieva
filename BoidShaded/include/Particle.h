#ifndef PARTICLE__
#define PARTICLE__

#include <ngl/Camera.h>
#include <ngl/Vec3.h>
#include <ngl/Colour.h>
#include <ngl/Transformation.h>
#include "ParticleTypeinfo.h"


// predeclare the emitter for inclusion here
class Emitter;


class Particle
{
public:
    Particle(ngl::Vec3 _pos, ngl::Vec3 _dir, ngl::Colour _c, const std::string &_shaderName, Emitter *_parent);
    virtual ~Particle();
    virtual void draw() const =0;
    virtual void update()=0;
    //virtual ParticleType getType() const =0;
    inline void setMaxLife(int _l){m_maxLife=_l;}
protected :
    ngl::Vec3 m_pos;
    ngl::Vec3 m_dir;
    ngl::Colour m_colour;
    GLfloat m_life;
    GLfloat m_maxLife;
    std::string m_shaderName;
    Emitter *m_parent;
};

#endif

