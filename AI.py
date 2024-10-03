import pygame
pygame.init()
from pygame.locals import *

from init import *
from assets import *

from random import randint


class Savely():
    def __init__(self):
        self.rect_box = Rect(200, 200, 64, 64)

        # self.savely_1cam = pygame.image.load()
        # self.savely_2cam = pygame.image.load()
        # self.savely_3cam = pygame.image.load()
        # self.savely_4cam = pygame.image.load()
        # self.savely_5cam = pygame.image.load()
        # self.savely_1cam_look = pygame.image.load()
        # self.savely_2cam_look = pygame.image.load()
        # self.savely_5cam_look = pygame.image.load()

        self.nextroom = pygame.mixer.Sound('sounds/nextroom.wav')

        self.jumpscare_img = pygame.image.load('sprites/325/jumpscare.png').convert_alpha()

        self.callroom = 0

        self.room = 0
        self.timer = 60

        self.newstep = False
        self.scarysound = pygame.mixer.Sound('sounds/scream2cam.wav')

        self.play_scream = True
        self.len_scream = 50
        self.mainscream = pygame.mixer.Sound('sounds/scream.wav')

    def move(self, timer, call):
        if self.newstep:
            if self.room == self.callroom:
                self.callroom = 0
            if not self.callroom:
                self.room = randint(1, 5)
                self.callroom = 0
            else:
                self.room = self.callroom


            if self.room == 2:
                self.scarysound.play(0)
            else:
                self.nextroom.play(0)

            self.newstep = False

        if not int(timer):
            if self.timer != timer:
                self.newstep = True

        self.timer = timer

    def jumpscare(self):
        if self.len_scream > 0:
            self.len_scream -= 1

            if self.play_scream:
                self.mainscream.play(0)
                self.play_scream = False

            window.blit(self.jumpscare_img, (0,0))
            return False

        return True

