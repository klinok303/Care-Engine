#ifndef CAREENGINE_SPARK_H
#define CAREENGINE_SPARK_H

#define CALC_MOVEMENT(s, dt) {cos(s.angle) * s.speed * dt, sin(s.angle) * s.speed * dt}
#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))

typedef struct Spark
{
    double angle;
    float pos[2];
    float speed;
} spark;

spark PointTowads(spark s, double angle, float rate);
spark VelocityAdjust(spark s, float friction, double force, float terminalVelocity, float dt);
spark UpdateSpark(spark s, float dt);

#endif //CAREENGINE_SPARK_H
