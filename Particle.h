#ifndef CAREENGINE_PARTICLES_H
#define CAREENGINE_PARTICLES_H

typedef struct Particle
{
    float pos[2];
    float velocity[2];
} particle;

particle UpdateParticle(particle p);
float ParticleRenderCalc(particle p, float offset[], uint8_t imgSize[], uint8_t id);

#endif //CAREENGINE_PARTICLES_H
