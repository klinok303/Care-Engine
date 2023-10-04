from os import listdir
import pygame

BASE_IMAGE_PATH = "Assets/Sprites"


def load_image(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in sorted(listdir(BASE_IMAGE_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images


def palette_swap(surf, old_c, new_c):
    with pygame.PixelArray(surf) as pixelarr:
        pixelarr.replace(old_c, new_c)
        img = pixelarr.make_surface()
        img.set_colorkey(old_c)
        return img


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
