#ifndef CAREENGINE_SPARK_H
#define CAREENGINE_SPARK_H

#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))

typedef struct Spark
{
    double angle;
    float pos[2];
    float speed;
} spark;

spark VelocityAdjust(spark s, float friction, double force, float terminalVelocity, float move[2], float dt);
spark UpdateSpark(spark s, const float move[2]);

#endif //CAREENGINE_SPARK_H
