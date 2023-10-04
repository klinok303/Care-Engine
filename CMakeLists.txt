cmake_minimum_required(VERSION 3.27)
project(CareEngine C)

set(CMAKE_C_STANDARD 23)

add_library(Particle SHARED Particle.c Particle.h)
add_library(Spark SHARED Spark.c Spark.h)
