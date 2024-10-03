import sys
import json

import pygame
pygame.init()
from pygame.locals import *

from init import *
from assets import *
from AI import *




class Menu():
    def __init__(self):
        self.mainfont_32 = pygame.font.Font('fonts/mainfont.ttf', 32)

        self.name = pygame.font.Font('fonts/UND.ttf', 64)

        self.savely_menu = pygame.transform.scale(pygame.image.load('sprites/menu/savely_menu.png').convert_alpha(), (
                                                  pygame.image.load('sprites/menu/savely_menu.png').get_width() * 1.5,
                                                  pygame.image.load('sprites/menu/savely_menu.png').get_height() * 1.5))

        self.chose_button_text = pygame.transform.scale(pygame.image.load('sprites/menu/chose.png').convert_alpha(),
                                                        (64, 64))

        with open('data/data.json', encoding='utf-8') as file:
            self.load_data = json.load(file)

        self.main_data = self.load_data

        self.btn_new_game = pygame.Rect(100, 300, 176, 48)
        self.color_new_game = (200, 200, 200)

        self.btn_continue = pygame.Rect(100, 400, 192, 48)
        self.color_continue = (200, 200, 200)

        self.btn_authors = pygame.Rect(100, 500, 113, 48)
        self.color_authors = (200, 200, 200)

        self.exit_game_btn = pygame.Rect(100, 600, 100, 48)
        self.exit_game_color = (200, 200, 200)

        self.show_except = False
        self.surf_except = pygame.Surface(SIZE).convert_alpha()
        self.alpha_except = 0

        self.font_pix16 = pygame.font.Font('fonts/rus-pixel.otf', 24)

        self.sound_menu = create_sound('sounds/menu.wav', 1)

        self.game_start = False
        self.continue_game = False




        self.render_menu()

    def render_menu(self):
        self.sound_menu.play(-1)
        while True:
            self.mouse = pygame.mouse.get_pos()
            # print(self.mouse)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            window.blit(self.savely_menu, (800, 100))

            self.render_buttons()

            if self.show_except:
                self.exception()
            else:
                if self.alpha_except > 0:
                    self.alpha_except -= 4
                    self.surf_except.set_alpha(self.alpha_except)
                    window.blit(self.surf_except, (0,0))

            window.blit(mouse_cursor, self.mouse)

            pygame.display.update()
            clock.tick(FPS)

            if self.game_start:
                break

            # print((datetime.datetime.now() - self.timenow).seconds)

        self.game_start = False



    def exit_game(self):
        self.quicksave()
        self.sound_menu.stop()
        pygame.quit()
        sys.exit()

    def quicksave(self):
        self.load_data = self.main_data
        with open('data/data.json', 'w', encoding='utf-8') as file:
            json.dump(self.load_data, file, ensure_ascii=False, indent=4)

    def render_buttons(self):

        window.blit(self.name.render('Five Nights', True, (200, 200, 200)), (100, 100))
        window.blit(self.name.render('At 325\'s', True, (200, 200, 200)), (100, 200))


        self.btn_new_game, self.color_new_game = self.chose_btn(self.btn_new_game, self.new_game)
        window.blit(self.mainfont_32.render('новая игра', True, self.color_new_game),
                    (self.btn_new_game.x, self.btn_new_game.y))

        self.btn_continue, self.color_continue = self.chose_btn(self.btn_continue, self.except_continue)
        window.blit(self.mainfont_32.render('продолжить', True, self.color_continue),
                    (self.btn_continue.x, self.btn_continue.y))

        if self.main_data['ночь 1']:
            for key, val in self.main_data.items():
                if val == True:
                    self.night = int(key[-1]) + 1
                    if self.night == 6:
                        self.night = 5
                    # print(self.night)
                    break
            window.blit(self.font_pix16.render(f'ночь {self.night}', True, (200, 200, 200)), (100, 380))

        self.btn_authors, self.color_authors = self.chose_btn(self.btn_authors, self.authors)
        window.blit(self.mainfont_32.render('авторы', True, self.color_authors),
                    (self.btn_authors.x, self.btn_authors.y))

        self.exit_game_btn, self.exit_game_color = self.chose_btn(self.exit_game_btn, self.exit_game)
        window.blit(self.mainfont_32.render('выход', True, self.exit_game_color),
                    (self.exit_game_btn.x, self.exit_game_btn.y))

    def authors(self):
        self.back = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back = True

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            self.mouse = pygame.mouse.get_pos()
            # print(self.mouse)


            window.blit(self.mainfont_32.render('Программист - Cartoon Box', True, (200, 200, 200)), (420, 180))
            window.blit(self.mainfont_32.render('Арт-Дизайн - Rogalchik', True, (200, 200, 200)), (460, 260))
            window.blit(self.mainfont_32.render('Идея - Rogalchik, Cartoon Box', True, (200, 200, 200)), (420, 340))

            window.blit(mouse_cursor, self.mouse)

            pygame.display.update()
            clock.tick(FPS)

            if self.back:
                break

    def new_game(self):
        self.main_data = {
            "ночь 5": False,
            "ночь 4": False,
            "ночь 3": False,
            "ночь 2": False,
            "ночь 1": False
        }
        self.quicksave()
        self.sound_menu.stop()
        self.night = 1
        self.game_start = True

    def chose_btn(self, button: Rect, func=None):

        ''' controlling buttons like a func use or hover '''

        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        color = (200, 200, 200)
        if button.collidepoint(self.mouse[0], self.mouse[1]):
            # print('func')
            color = (172, 109, 25)
            # print(func)
            # print(self.click[0])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and func != None:
                        # print('used func')
                        func()
            if self.click[0]:
                func()

            window.blit(self.chose_button_text, (button.x - 64, button.y - 16))

        return button, color

    def exception(self):
        if self.alpha_except < 180:
            self.alpha_except += 4
            self.surf_except.set_alpha(self.alpha_except)
            window.blit(self.surf_except, (0,0))
        else:
            window.blit(self.surf_except, (0, 0))
            self.click = pygame.mouse.get_pressed()
            window.blit(exception, (340, 210))
            window.blit(self.mainfont_32.render('сохранений не обнаружено', True, (20, 20, 20)), (415, 250))
            window.blit(self.mainfont_32.render('начните новую игру', True, (20, 20, 20)), (480, 412))
            if self.click[0]:
                self.show_except = False

    def except_continue(self):

        if not self.main_data['ночь 1']:
            self.show_except = True

        else:
            # выход из класса в меню, там уже создаем объект night класса Nights, передаем ночь, в зависимости от ночи будет выстраиваться сложность игры
            self.sound_menu.stop()
            self.continue_game = True
            self.game_start = True






def render_start_window():
    texture = pygame.image.load('sprites/icons/icon_CB.png').convert_alpha()

    alpha_channel = 150
    # texture.set_alpha(alpha_channel)
    font_x32_us = pygame.font.Font('fonts/UND.ttf', 32)
    font_x24_ru = pygame.font.Font('fonts/rus-pixel.otf', 24)
    screen.set_alpha(alpha_channel)
    reverse = False
    exited = False
    wait = 100
    while alpha_channel < 255 and (not exited):
        # mouse = pygame.mouse.get_pos()
        # print(mouse)
        # pygame.draw.rect(window, (255,255,255), Rect(mouse[0], mouse[1], 5,5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(texture, (475, 150))
        window.blit(font_x32_us.render('Cartoon Box', True, (255,255,255)), (520, 473))
        window.blit(font_x24_ru.render('представляет', True, (255,255,255)), (570, 520))

        window.blit(screen, (0, 0))
        screen.fill((0, 0, 0))
        screen.set_alpha(alpha_channel)
        if alpha_channel <= 255:
            alpha_channel -= 2
            if alpha_channel == 0:
                reverse = True
            if reverse:
                alpha_channel += 3
        else:
            wait -= 2
            if wait == 0:
                exited = True

        pygame.display.update()
        clock.tick(FPS)

class Computer():
    def __init__(self):
        self.map_monitor = pygame.image.load('sprites/monitor/map_monitor.png').convert_alpha()
        self.callbtn_img = pygame.image.load('sprites/monitor/call btn.png').convert_alpha()

        self.callbtn = Rect(1072, 367, self.callbtn_img.get_width(), self.callbtn_img.get_height())

        self.map_font = pygame.font.Font('fonts/rus-pixel.otf', 16)
        self.font_en = pygame.font.Font('fonts/UND.ttf', 16)
        self.font_en32 = pygame.font.Font('fonts/UND.ttf', 32)
        self.font_ru32 = pygame.font.Font('fonts/rus-pixel.otf', 32)
        self.cam = None

        self.savely = Savely()

        self.callfox_sound = pygame.mixer.Sound('sounds/callfox.wav')
        self.callfox_sound.set_volume(0.6)


        self.change_cam = pygame.mixer.Sound('sounds/changecam.wav')
        self.change_cam.set_volume(0.5)
        self.change_cam_bool = False

        self.call = False

        self.callsound_bool = False


        self.cam1_rect = pygame.Rect(911, 176, 50, 35)
        self.cam2_rect = pygame.Rect(968, 295, 50, 35)
        self.cam3_rect = pygame.Rect(1009, 85, 50, 35)
        self.cam4_rect = pygame.Rect(1099, 210, 50, 35)
        self.cam5_rect = pygame.Rect(1098, 306, 50, 35)

        self.cam1_325 = pygame.image.load('sprites/325/3.png').convert_alpha()
        self.cam2_325 = pygame.transform.scale(pygame.image.load('sprites/325/1.png').convert_alpha(),
                                               (1280, 720)).convert_alpha()
        self.cam3_325 = pygame.image.load('sprites/325/4.png').convert_alpha()
        self.cam4_325 = pygame.image.load('sprites/325/2.png').convert_alpha()
        self.cam5_325 = pygame.image.load('sprites/325/5.png').convert_alpha()


        self.cam1_img = pygame.transform.scale(pygame.image.load('sprites/rooms/mid.JPG'), (1280, 720)).convert_alpha()
        self.cam2_img = pygame.transform.scale(pygame.image.load('sprites/rooms/toilet.JPG'), (1280, 720)).convert_alpha()
        self.cam3_img = pygame.transform.scale(pygame.image.load('sprites/rooms/kitchen.JPG'), (1280, 720)).convert_alpha()
        self.cam4_img = pygame.transform.scale(pygame.image.load('sprites/rooms/guests.JPG'), (1280, 720)).convert_alpha()
        self.cam5_img = pygame.transform.scale(pygame.image.load('sprites/rooms/par.JPG'), (1280, 720)).convert_alpha()

        self.timer = 60

    def callto(self):
        self.savely.callroom = self.maincam
        if self.callsound_bool:
            self.callfox_sound.play(0)
            self.callsound_bool = False


    def render_monitor(self):

        if self.cam == self.cam5_rect:
            self.cam5()

        elif self.cam == self.cam2_rect:
            self.cam2()

        elif self.cam == self.cam3_rect:
            self.cam3()

        elif self.cam == self.cam4_rect:
            self.cam4()

        else:
            self.cam1()

        window.blit(self.callbtn_img, (self.callbtn.x, self.callbtn.y))

        self.callbtn = self.chose_btn(self.callbtn, self.callto)

        window.blit(self.font_ru32.render('позвать', True, (200, 200, 200)), (1115, 370))
        self.render_map()

    def render_map(self):



        self.cam1_rect = self.chose_btn(self.cam1_rect, self.cam1)
        self.cam2_rect = self.chose_btn(self.cam2_rect, self.cam2)
        self.cam3_rect = self.chose_btn(self.cam3_rect, self.cam3)
        self.cam4_rect = self.chose_btn(self.cam4_rect, self.cam4)
        self.cam5_rect = self.chose_btn(self.cam5_rect, self.cam5)

        window.blit(self.map_monitor, (800, 40))
        self.mouse = pygame.mouse.get_pos()
        # print(self.mouse, 'mouse')


        window.blit(self.map_font.render('01', True, (255, 255, 255)), (935, 190))
        window.blit(self.map_font.render('02', True, (255, 255, 255)), (990, 308))
        window.blit(self.map_font.render('03', True, (255, 255, 255)), (1032, 98))
        window.blit(self.map_font.render('04', True, (255, 255, 255)), (1120, 222))
        window.blit(self.map_font.render('05', True, (255, 255, 255)), (1120, 318))
        window.blit(self.font_en.render('you', True, (255, 255, 255)), (980, 380))

    def chose_btn(self, button: Rect, func=None):

        ''' controlling buttons like a func use or hover '''

        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        color = (200, 200, 200)
        if button.collidepoint(self.mouse[0], self.mouse[1]):
            color = (172, 109, 25)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and func != None:
                        self.cam = button
                        func()
            if self.click[0] and self.cam != button:
                self.cam = button
                self.change_cam_bool = True
                func()



        return button

    def cam1(self):

        window.blit(self.cam1_img, (0,0))

        if self.savely.room == 1:
            window.blit(self.cam1_325, (1280 - self.cam1_325.get_width(), 0))


        if self.change_cam_bool:
            self.change_cam.play(0)
            self.change_cam_bool = False
        pygame.draw.rect(window, (121, 81, 137),
                         Rect(self.cam1_rect.x - 4, self.cam1_rect.y - 4,
                              self.cam1_rect.width + 8, self.cam1_rect.height + 8))

        window.blit(self.font_en32.render('CAM 1', True, (220, 220, 220)), (24,24))
        self.maincam = 1

    def cam2(self):

        window.blit(self.cam2_img, (0,0))

        if self.savely.room == 2:
            window.blit(self.cam2_325, (0,0))
        # self.savely.move(self.timer)
        if self.change_cam_bool:
            self.change_cam.play(0)
            self.change_cam_bool = False
        pygame.draw.rect(window, (121, 81, 137),
                         Rect(self.cam2_rect.x - 4, self.cam2_rect.y - 4,
                              self.cam2_rect.width + 8, self.cam2_rect.height + 8))
        window.blit(self.font_en32.render('CAM 2', True, (220, 220, 220)), (24, 24))

        self.maincam = 2

    def cam3(self):

        window.blit(self.cam3_img, (0,0))

        if self.savely.room == 3:
            window.blit(self.cam3_325, (-100, 200))
        # self.savely.move(self.timer)
        if self.change_cam_bool:
            self.change_cam.play(0)
            self.change_cam_bool = False
        pygame.draw.rect(window, (121, 81, 137),
                         Rect(self.cam3_rect.x - 4, self.cam3_rect.y - 4,
                              self.cam3_rect.width + 8, self.cam3_rect.height + 8))
        window.blit(self.font_en32.render('CAM 3', True, (220, 220, 220)), (24, 24))

        self.maincam = 3

    def cam4(self):

        window.blit(self.cam4_img, (0,0))

        if self.savely.room == 4:
            window.blit(self.cam4_325, (0, 0))
        # self.savely.move(self.timer)
        if self.change_cam_bool:
            self.change_cam.play(0)
            self.change_cam_bool = False
        pygame.draw.rect(window, (121, 81, 137),
                         Rect(self.cam4_rect.x - 4, self.cam4_rect.y - 4,
                              self.cam4_rect.width + 8, self.cam4_rect.height + 8))
        window.blit(self.font_en32.render('CAM 4', True, (220, 220, 220)), (24, 24))

        self.maincam = 4

    def cam5(self):

        window.blit(self.cam5_img, (0,0))

        if self.savely.room == 5:
            window.blit(self.cam5_325, (997, 340))
        # self.savely.move(self.timer)
        if self.change_cam_bool:
            self.change_cam.play(0)
            self.change_cam_bool = False
            pygame.draw.rect(window, (121, 81, 137),
                         Rect(self.cam5_rect.x - 4, self.cam5_rect.y - 4,
                              self.cam5_rect.width + 8, self.cam5_rect.height + 8))
        window.blit(self.font_en32.render('CAM 5', True, (220, 220, 220)), (24, 24))

        self.maincam = 5

class Smoke():
    def __init__(self):
        self.smokbar = pygame.image.load('sprites/icons/smokbar.png').convert_alpha()
        self.chargebar = pygame.image.load('sprites/icons/chargebar.png').convert_alpha()
        self.smokborder = pygame.image.load('sprites/icons/smokborder.png').convert_alpha()

        self.heart = pygame.transform.scale(pygame.image.load('sprites/icons/heart.png'),
                                            (64, 64)).convert_alpha()

        self.font = pygame.font.Font('fonts/rus-pixel.otf', 16)
        self.und_font = pygame.font.Font('fonts/UND.ttf', 16)

        self.percents = 100
        self.percents_charge = 100

        self.length = self.smokbar.get_width()
        self.length_charge = self.chargebar.get_width()

        self.total_length = self.length
        self.total_length_charge = self.length_charge

    def render_smokbar(self, night=3, min=0.02):
        window.blit(self.smokborder, (50, 760 - 100))
        window.blit(self.smokbar, (54, 760 - 92))
        window.blit(self.font.render(f'{int(self.percents)}', True, (200, 200, 200)), (32, 760 - 96))

        window.blit(self.heart, (32, 32))
        window.blit(self.font.render(f'{int(90 + ((100 - self.percents)))}', True, (0, 0, 0)), (56, 48))

        if int(self.percents) <= 50:
            window.blit(self.und_font.render('E', True, (200, 200, 200)), (290, 760 - 96))

        if night != 3:
            self.charge()


        self.eat(min)

    def eat(self, min):
        self.length -= min
        self.percents = (self.length / self.total_length) * 100
        # print(self.percents)
        if self.percents > 0:
            self.smokbar = pygame.transform.scale(self.smokbar, (self.length, self.smokbar.get_height()))

    def add(self):
        if int(self.percents_charge) > 0:
            if self.length < self.total_length:
                self.length += 1
            else:
                self.length = self.total_length


    def charge(self, add=0.05, eat=1):
        window.blit(self.font.render(f'{int(self.percents_charge)}', True, (200, 200, 200)), (32, 720 - 96))
        window.blit(self.smokborder, (50, 720 - 100))
        window.blit(self.chargebar, (54, 720 - 92))

        if int(self.percents_charge) <= 50:
            window.blit(self.und_font.render('Q', True, (200, 200, 200)), (290, 720 - 96))

        self.key = pygame.key.get_pressed()
        if self.key[pygame.K_q]:
            self.chargeadd(add)
        if self.key[pygame.K_e]:
            self.chargeeat(eat)

    def chargeadd(self, add=0.05):

        self.length_charge += add

        self.percents_charge = (self.length_charge / self.total_length_charge) * 100

        if self.length_charge < self.total_length_charge:
            self.length_charge += add

        else:
            self.length_charge = self.total_length_charge

        if self.percents_charge < 100:
            self.chargebar = pygame.transform.scale(self.chargebar,
                                                    (self.length_charge, self.chargebar.get_height()))

    def chargeeat(self, eat=1):
        self.length_charge -= eat

        self.percents_charge = (self.length_charge / self.total_length_charge) * 100

        if int(self.percents_charge) > 0:
            self.chargebar = pygame.transform.scale(self.chargebar,
                                                    (self.length_charge, self.chargebar.get_height()))
        else:
            self.length_charge = 1
            self.percents_charge = 0


    def shake(self, cords):

        # if self.percents < 50:
        self.shake_coef = 10 - (self.percents / 10)

        randchose1 = randint(1, 2)
        if randchose1 == 1:
            cords[0] += self.shake_coef
            if self.percents < 50:
                cords[0] += self.shake_coef * 2
        else:
            if self.percents < 50:
                cords[0] -= self.shake_coef * 2
            cords[0] -= self.shake_coef

        randchose2 = randint(1, 2)
        if randchose2 == 1:
            cords[1] += self.shake_coef
            if self.percents < 50:
                cords[1] += self.shake_coef * 2
        else:
            cords[1] -= self.shake_coef
            if self.percents < 50:
                cords[1] -= self.shake_coef * 2

        return cords



