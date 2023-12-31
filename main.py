from array import array

import pygame
import argparse
import math
import random

from scripts.Entities import PhysicsEntity
from scripts.Tilemap import Tilemap
from scripts.shaders import *
from scripts.untils import palette_swap, load_images, load_image, Animation
from scripts.Particle import Particle
from scripts.Spark import Spark

RENDER_SCALE = 0.98


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game")

        self.screen = pygame.display.set_mode((500, 500), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.display = pygame.Surface((512, 512))
        self.clock = pygame.time.Clock()

        self.fullscreen = False

        self.movement = [False, False]
        self.shaderIndex = 0

        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))

        self.default_shader = self.ctx.program(vertex_shader=vert_default, fragment_shader=frag_default)
        self.retro = self.ctx.program(vertex_shader=vert_default, fragment_shader=frag_retro)
        self.glitch = self.ctx.program(vertex_shader=vert_default, fragment_shader=glitch_frag)

        self.render_obj = self.ctx.vertex_array(self.default_shader, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.assets = {}

        self.tilemap = Tilemap(self)

        self.sparks = []

    def load_level(self, chapter, map):
        self.tilemap.load('Assets/maps/' + str(chapter) + '/' + str(map) + '.json')

        self.useBg = self.tilemap.has_bg
        self.shaderIndex = self.tilemap.shader_id

    def run(self):
        t = 0
        while True:
            self.display.fill((0, 0, 0))
            t += 1

            self.tilemap.render(self.display, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            frame_tex = surf_to_texture(self.display, self.ctx)
            frame_tex.use(0)

            match self.shaderIndex:
                case 1:
                    self.render_obj = self.ctx.vertex_array(self.retro,
                                                            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
                    self.retro['tex'] = 0
                    self.retro['time'] = t
                case 2:
                    self.render_obj = self.ctx.vertex_array(self.glitch,
                                                            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
                    self.glitch['tex'] = 0
                case _:
                    self.render_obj = self.ctx.vertex_array(self.default_shader,
                                                            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
                    self.default_shader['tex'] = 0

            self.render_obj.render(mode=moderngl.TRIANGLE_STRIP)

            pygame.display.flip()

            frame_tex.release()

            self.clock.tick(24)


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Adventure Of Care: Editor")

        self.screen = pygame.display.set_mode((500, 500), pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface((512, 512))
        self.clock = pygame.time.Clock()

        self.movement = [False, False, False, False]
        self.shaderIndex = 0

        self.colors = [(0, 0, 0), (255, 255, 255)]

        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))

        self.default_shader = self.ctx.program(vertex_shader=vert_default, fragment_shader=frag_default)
        self.retro = self.ctx.program(vertex_shader=vert_default, fragment_shader=frag_retro)
        self.glitch = self.ctx.program(vertex_shader=vert_default, fragment_shader=glitch_frag)

        self.render_obj = self.ctx.vertex_array(self.default_shader, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.assets = {
            'metal': load_images('/tiles/metal/'),
            'pipes': load_images('/tiles/pipes/'),
            'spawners': load_images('/spawners/')
        }

        self.tilemap = Tilemap(self)
        self.curTheme = False

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        # self.player = Player(self, (50, 50), (16, 16))
        self.cameraSpeed = 10

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.onGrid = True
        self.tileWorld = 'both'
        self.useBg = False
        self.sparks = []

    def run(self):
        t = 0
        while True:
            self.display.fill(self.colors[self.curTheme])

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2 * self.cameraSpeed
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2 * self.cameraSpeed
            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, renderScroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(128)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.onGrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                     tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.onGrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = \
                    {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                         tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            if self.useBg:
                for i, spark in sorted(enumerate(self.sparks), reverse=True):
                    spark.update(1, 0.05)
                    spark.render(self.display)
                    spark.color = self.colors[not self.curTheme]
                    if not spark.alive:
                        self.sparks.pop(i)

                self.sparks.append(
                    Spark([self.display.get_width() / 2, self.display.get_height() / 2],
                          math.radians(random.randint(0, 360)), random.randint(3, 6), (0, 0, 0),
                          2))

            t += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.onGrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group],
                                                               'variant': self.tile_variant,
                                                               'pos': (
                                                                   mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_RSHIFT:
                        self.shift = True
                    if event.key == pygame.K_q or event.key == pygame.K_F1:
                        self.onGrid = not self.onGrid
                    if event.key == pygame.K_o or event.key == pygame.K_F2:
                        self.tilemap.save('map.json', self.useBg, self.shaderIndex)
                    if event.key == pygame.K_e or event.key == pygame.K_F3:
                        if self.tileWorld == 'both':
                            self.tileWorld = True
                        elif not self.tileWorld:
                            self.tileWorld = 'both'
                        else:
                            self.tileWorld = not self.tileWorld
                    if event.key == pygame.K_q or event.key == pygame.K_F4:
                        self.useBg = not self.useBg
                    if event.key == pygame.K_r or event.key == pygame.K_F5:
                        if self.shaderIndex < 2:
                            self.shaderIndex += 1
                        else:
                            self.shaderIndex = 0

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_RSHIFT:
                        self.shift = False

            frame_tex = surf_to_texture(self.display, self.ctx)
            frame_tex.use(0)

            match self.shaderIndex:
                case 1:
                    self.render_obj = self.ctx.vertex_array(self.retro,
                                                            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
                    self.retro['tex'] = 0
                    self.retro['time'] = t
                case 2:
                    self.render_obj = self.ctx.vertex_array(self.glitch,
                                                            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
                    self.glitch['tex'] = 0
                case _:
                    self.render_obj = self.ctx.vertex_array(self.default_shader,
                                                            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
                    self.default_shader['tex'] = 0

            self.render_obj.render(mode=moderngl.TRIANGLE_STRIP)

            pygame.display.flip()

            frame_tex.release()

            self.clock.tick(24)


parser = argparse.ArgumentParser(description='Choose playing game or make levels for him')
parser.add_argument('-Editor', type=bool, default=False, help='Run editor')
app_args = parser.parse_args()

if app_args.Editor:
    g = Editor()
else:
    g = Game()

g.run()
