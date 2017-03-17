#ifndef EMITTER_H
#define EMITTER_H
#include <ngl/Vec3.h>
#include <vector>
#include <memory>
#include <ngl/AbstractVAO.h>
#include <ngl/VAOFactory.h>
#include <ngl/SimpleVAO.h>
#include "Particle.h"

class Emitter
{
public:
    Emitter(ngl::Vec3 _pos, size_t nParticles);
    void draw();
    void update();

    private:
    std::vector<Particle> m_particles;
    ngl::Vec3 m_pos;
    std::unique_ptr<ngl::AbstractVAO> m_vao;
};


#endif
