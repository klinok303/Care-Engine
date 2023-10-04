import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0), curTheme=None):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(9, self.velocity[1] + 0.5)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        if movement[0] > 0: self.flip = False
        if movement[0] < 0: self.flip = True

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0],
                                                                                  self.pos[1] - offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)

        self.air_time = 0
        self.jumps = 1

    def update(self, tilemap, movement=(0, 0), curTheme=None):
        super().update(tilemap, movement, curTheme)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        if self.air_time > 4: self.set_action('jump')
        elif movement[0] != 0: self.set_action('walk')
        else: self.set_action('idle')

    def jump(self):
        if self.jumps:
            self.velocity[1] = -8.5
            self.jumps -= 1
            self.air_time = 5


class SpikeSlime(PhysicsEntity):
    def __init__(self, game, pos, size, themeSpawns='both'):
        super().__init__(game, 'spikeSlime', pos, size)

        self.themeSpawns = themeSpawns
        self.set_action('walk')

    def update(self, tilemap, movement=(0, 0), curTheme=None):
        if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23), curTheme):
            if self.collisions['right'] or self.collisions['left']: self.flip = not self.flip
            else: movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
        else: self.flip = not self.flip

        super().update(tilemap, movement, curTheme)

    def render(self, surf, offset=(0, 0), curTheme=None):
        if self.themeSpawns == 'both' or curTheme == self.themeSpawns: super().render(surf, offset)
