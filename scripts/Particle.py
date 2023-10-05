import ctypes


class CParticle(ctypes.Structure):
    _fields_ = [("pos", ctypes.c_float * 2), ("velocity", ctypes.c_float * 2)]


class Particle:
    def __init__(self, game, p_type, pos, velocity=None, frame=0):
        if velocity == None: velocity = [0.0, 0.0]

        self.lib = ctypes.CDLL("./libParticle.dll")
        self.lib.ParticleUpdate.restype = CParticle

        self.struct = CParticle((ctypes.c_float * 2)(*list(pos)), (ctypes.c_float * 2)(*list(velocity)))

        self.game = game

        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame

    def update(self):
        kill = False
        if self.animation.done: kill = True

        self.struct = self.lib.ParticleUpdate(self.struct)

        self.animation.update()

        return kill

    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        surf.blit(img, (self.lib.ParticleRenderCalc(self.struct, (ctypes.c_float * 2)(*list(offset)),
                                                    (ctypes.c_uint8 * 2)(*[img.get_height(), img.get_width()]), 0),
                        self.lib.ParticleRenderCalc(self.struct, (ctypes.c_float * 2)(*list(offset)),
                                                    (ctypes.c_uint8 * 2)(*[img.get_height(), img.get_width()]), 1)))
