#include <stdint.h>
#include <math.h>
#include "Particle.h"

particle UpdateParticle(particle p)
{
    p.pos[0] += p.velocity[0];
    p.pos[1] += p.velocity[1];

    return p;
}

float ParticleRenderCalc(particle p, float offset[], uint8_t imgSize[], uint8_t id)
{
    float r[2] = {p.pos[0] - offset[0] - roundf((float)imgSize[0] / 2),
                  p.pos[1] - offset[1] - roundf((float)imgSize[1] / 2)};
    return r[id];
}
