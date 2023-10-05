from math import cos, sin, pi
from ctypes import Structure, CDLL, c_double, c_float
import pygame

class CSpark(Structure):
    _fields_ = [('angle', c_double), ('pos', c_float * 2), ('speed', c_float)]

class Spark:
    def __init__(self, pos, angle, speed, color, scale=1):
        self.lib = CDLL("./libSpark.dll")
        self.lib.VelocityAdjust.restype = CSpark
        self.lib.UpdateSpark.restype = CSpark

        self.struct = CSpark(angle, (c_float * 2)(*list(pos)), speed)
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.struct.angle + pi * 3) % (pi * 2)) - pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sing = 1
        if abs(rotate_direction) < rate:
            self.struct.angle = angle
        else:
            self.struct.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [cos(self.struct.angle) * self.struct.speed * dt, sin(self.struct.angle) * self.struct.speed * dt]

    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt, movement):
        self.struct = self.lib.VelocityAdjust(self.struct, c_float(friction), c_double(force), c_float(terminal_velocity),
                                              (c_float * 2)(*list(movement)), c_float(dt))

    def update(self, dt, angle):
        movement = self.calculate_movement(dt)
        self.struct = self.lib.UpdateSpark(self.struct, (c_float * 2)(*list(movement)))

        self.velocity_adjust(0.975, 0.2, 8, dt, movement)

        self.struct.angle += angle

        self.struct.speed -= 0.05

        if self.struct.speed <= 0: self.alive = False

    def render(self, surf):
        if self.alive:
            points = [
                [self.struct.pos[0] + cos(self.struct.angle) * self.struct.speed * self.scale,
                 self.struct.pos[1] + sin(self.struct.angle) * self.struct.speed * self.scale],
                [self.struct.pos[0] + cos(self.struct.angle + pi / 2) * self.struct.speed * self.scale * 0.3,
                 self.struct.pos[1] + sin(self.struct.angle + pi / 2) * self.struct.speed * self.scale * 0.3],
                [self.struct.pos[0] - cos(self.struct.angle) * self.struct.speed * self.scale * 3.5,
                 self.struct.pos[1] - sin(self.struct.angle) * self.struct.speed * self.scale * 3.5],
                [self.struct.pos[0] + cos(self.struct.angle - pi / 2) * self.struct.speed * self.scale * 0.3,
                 self.struct.pos[1] - sin(self.struct.angle + pi / 2) * self.struct.speed * self.scale * 0.3],
            ]
            s = pygame.draw.polygon(surf, self.color, points)
