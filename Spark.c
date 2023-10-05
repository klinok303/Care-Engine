#include <math.h>
#include "Spark.h"


spark VelocityAdjust(spark s, float friction, double force, float terminalVelocity, float move[2], float dt)
{
    move[1] = MIN(terminalVelocity, move[1] + force * dt);
    move[0] *= friction;
    s.angle = atan2f(move[1], move[0]);
    return s;
}

spark UpdateSpark(spark s, const float move[2])
{
    s.pos[0] += move[0];
    s.pos[1] += move[1];

    return s;
}
