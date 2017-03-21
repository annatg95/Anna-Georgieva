#ifndef PARTICLE_H_
#define PARTICLE_H_
#include <ngl/Camera.h>
#include <ngl/ShaderLib.h>
#include <ngl/Transformation.h>
#include <ngl/Vec3.h>

class Emitter;

class Particle
{
protected:
    Emitter *parent;

    ngl::Vec3 pos;
    ngl::Vec3 dir;
    ngl::Vec3 colour;

    int life=0;
    int maxLife;

public:

   Particle(ngl::Vec3 _pos, ngl::Vec3 _dir, Emitter *_parent);
   virtual ~Particle();
   void draw();
   void update();
   inline void setMaxLife(int _l){maxLife=_l;}


};

#endif



