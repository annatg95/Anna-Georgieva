#include "Emitter.h"
#include <iostream>
#include <ngl/Random.h>
#include <ngl/NGLInit.h>

Emitter::Emitter(ngl::Vec3 _pos, size_t nParticles)
{
    m_pos=_pos;
    m_particles.resize(nParticles);

    ngl::Random *rng=ngl::Random::instance();

    for(auto &p: m_particles)
    {
        p.dir=rng->getRandomVec3();
        p.colour.m_r=rng->randomPositiveNumber(1.0);
          p.colour.m_g=rng->randomPositiveNumber(1.0);
          p.colour.m_b=rng->randomPositiveNumber(1.0);
        p.maxLife=rng->randomPositiveNumber(1000);

    }
    m_vao.reset(ngl::VAOFactory::createVAO(ngl::simpleVAO, GL_POINTS));
}

void Emitter::draw()
{
    std::cout<<"drawing\n";
    m_vao->bind();

    struct part
    {
        ngl::Vec3 p;
        ngl::Vec3 c;
    };

    std::vector<part> part;
    part.resize(m_particles.size());

    for(size_t i=0; i<m_particles.size(); ++i)
    {
        part[i].p=m_particles[i].pos;

        part[i].c=m_particles[i].colour;
    }

    m_vao->setData(ngl::SimpleVAO::VertexData(part.size()*sizeof(part),
                                              part[0].p.m_x));
    m_vao->setVertexAttributePointer(0,3,GL_FLOAT,0,0);
    m_vao->setVertexAttributePointer(1,3,GL_FLOAT,0,0);

    m_vao->setNumIndices(part.size());
    m_vao->draw();
    m_vao->unbind();
}


void Emitter::update()
{
    std::cout<<"update\n";

    for(auto &p : m_particles)
    {
        p.pos+=p.dir;
    }
}

