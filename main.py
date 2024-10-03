import pygame
pygame.init()
from pygame.locals import *

from init import *
from UI import *
from nights import *

render_start_window()

class Game():
    def __init__(self):
        self.menu = Menu()

        self.night = Nights(self.menu.night)

        self.__init__()

if __name__ == '__main__':
    game = Game()