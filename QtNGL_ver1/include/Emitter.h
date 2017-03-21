#ifndef EMITTER_H
#define EMITTER_H
#include <ngl/Vec3.h>
#include <vector>
#include <memory>

#include <ngl/AbstractVAO.h>
#include <ngl/VAOFactory.h>
#include <ngl/SimpleVAO.h>
#include <ngl/Camera.h>

#include "Particle.h"

class Emitter
{
public:
    Emitter(ngl::Vec3 _pos, size_t nParticles, const ngl::Camera *_cam);
    //~Emitter();
    void draw();
    void update();

    void addParticle();
    void rmParticle();

    inline unsigned int getNumParticles()const {return m_numParticles;}
    inline const ngl::Camera *getCamera() const {return m_cam;}
    void clearParticles();
    inline ngl::Vec3 getPos()const {return m_pos;}
     inline void setPos(const ngl::Vec3 &_v){m_pos=_v;}
    inline void setGlobalTransform(const ngl::Mat4 &_t){m_globalMouseTX=_t;}
    inline const ngl::Mat4 & getGlobalTransform() const { return m_globalMouseTX;}


    private:

    ngl::Vec3 m_pos;
    ngl::Mat4 m_globalMouseTX;

    std::unique_ptr<ngl::AbstractVAO> m_vao;
    //std::vector<Particle> m_particles;

    const ngl::Camera *m_cam;
    unsigned int m_numParticles;

};


#endif
