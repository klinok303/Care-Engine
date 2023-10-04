import ctypes


class ParticleData(ctypes.Structure):
    _fields_ = [("type", ctypes.c_char_p), ("pos", ctypes.c_float * 2), ("velocity", ctypes.c_float * 2)]


class Particle:
    def __init__(self, game, p_type, pos, velocity=None, frame=0):
        if velocity == None: velocity = [0.0, 0.0]

        self.lib = ctypes.CDLL("./Particle.dll")
        self.lib.ParticleUpdate.restype = ParticleData

        self.particle = ParticleData(bytes(p_type.encode('utf-8')), (ctypes.c_float * 2)(*list(pos)),
                                     (ctypes.c_float * 2)(*list(velocity)))

        self.game = game

        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame

    def update(self):
        kill = False
        if self.animation.done: kill = True

        self.particle = self.lib.ParticleUpdate(self.particle)

        self.animation.update()

        return kill

    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        surf.blit(img, (self.particle.pos[0] - offset[0] - img.get_width() // 2,
                        self.particle.pos[1] - offset[1] - img.get_height() // 2))
