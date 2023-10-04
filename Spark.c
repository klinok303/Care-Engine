#include <math.h>
#include "Spark.h"

spark PointTowads(spark s, double angle, float rate)
{
    float rotateSign;
    double rotateDir = fmod(angle - s.angle + M_PI * 3, M_PI * 2) - M_PI;

    if (fabs(rotateDir) / rotateDir != 0) rotateSign = (float)(fabs(rotateDir) / rotateDir);
    else rotateSign = 1;

    if (fabs(rotateDir) < rate) s.angle = angle;
    else s.angle += rate * rotateSign;

    return s;
}

spark VelocityAdjust(spark s, float friction, double force, float terminalVelocity, float dt)
{
    double movement[2] = CALC_MOVEMENT(s, dt);
    movement[1] = MIN(terminalVelocity, movement[1] + force * dt);
    movement[0] *= friction;
    s.angle = atan2(movement[1], movement[0]);
    return s;
}

spark UpdateSpark(spark s, float dt)
{
    float movement[2] = CALC_MOVEMENT(s, dt);
    s.pos[0] += movement[0];
    s.pos[1] += movement[1];

    return s;
}
