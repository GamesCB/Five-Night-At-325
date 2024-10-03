import json
import sys

import pygame
pygame.init()

from pygame.locals import *
from random import randint


SIZE = [1280, 720]
window = pygame.display.set_mode(SIZE, pygame.FULLSCREEN|DOUBLEBUF)
screen = pygame.Surface(SIZE)
scroll = [0,0]
true_scroll = scroll

clock = pygame.time.Clock()
FPS = 60



class Animation():
    def __init__(self, list_sprites, delay):
        self.list_sprites = list_sprites
        self.anim_count = 0
        self.delay = delay

    def show_anim(self, x, y):
        if self.anim_count < (len(self.list_sprites) * self.delay - 1):
            window.blit(self.list_sprites[self.anim_count//self.delay], (x - scroll[0], y - scroll[1]))
            self.anim_count += 1
        else:
            self.anim_count = 0
            return True

        return False

    def show_anim_static(self, x, y):
        if self.anim_count < (len(self.list_sprites) * self.delay - 1):
            window.blit(self.list_sprites[self.anim_count//self.delay], (x, y))
            self.anim_count += 1
        else:
            self.anim_count = 0
            return True

        return False

def create_sound(path, vol=1):

    sound = pygame.mixer.music
    sound.load(path)
    sound.set_volume(vol)

    return sound


pygame.mouse.set_visible(False)

