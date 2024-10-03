import sys
import json

import pygame
pygame.init()
from pygame.locals import *

from init import *
from assets import *
from UI import *


import datetime

class Night():
    def __init__(self):
        '''
            описать текстуры и основные звуки
            описать также кнопки и тд
        '''

        self.font_timer = pygame.font.Font('fonts/rus-pixel.otf', 32)
        self.font_start_time = pygame.font.Font('fonts/rus-pixel.otf', 64)
        self.font_cams = pygame.font.Font('fonts/UND.ttf', 64)
        self.font_watch = pygame.font.Font('fonts/rus-pixel.otf', 64)
        self.timenow = datetime.datetime.now()

        self.var_timer = 0

        self.ventilator = create_sound('sounds/ventilator.wav')
        self.camera_static = pygame.mixer.Sound('sounds/camera static.wav')
        self.camera_static.set_volume(0.1)

        self.string_timer_secs = 0

        self.computer = Computer()

        # self.button_door = Rect()

        self.playending = True
        self.ending = pygame.mixer.Sound('sounds/endnight.wav')
        self.end = False
        self.play_camera = False

        self.killed_sound = pygame.mixer.Sound('sounds/killed.wav')

        self.var_delay_death = 1200
        self.end_from_lose = 300

        self.rect_monitor = Rect(1035, 240, 1468 - 1035, 500 - 240)

        self.mainroom = pygame.transform.scale(pygame.image.load('sprites/rooms/mainroom.png').convert_alpha(),
                                               (1803, 720))



    def button(self, button: Rect, func=None):

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
            # if self.click[0]:
            #     func()

            # window.blit(self.chose_button_text, (button.x - 64, button.y - 16))
            pygame.draw.rect(window, (200, 200, 200), Rect(button.x - 4, button.y - 4,
                                                           button.width + 8, button.height + 8))

        return button, color

    def render_timer(self):
        self.mainstring = ''
        self.string_timer_secs = int((datetime.datetime.now() - self.timenow).seconds)
        if self.string_timer_secs // 60 < 1:
            self.mainstring += '00'
        else:
            self.mainstring += f'0{self.string_timer_secs // 60}'



        if self.string_timer_secs % 60 < 10:
            self.mainstring += f': 0{self.string_timer_secs % 60}'
        else:
            self.mainstring += f': {self.string_timer_secs % 60}'

        window.blit(self.font_timer.render(f'{self.mainstring}', True, (200, 200, 200)),
                    (SIZE[0] - 100, SIZE[1] - 64))

    def showtime(self, night):
        if self.var_timer < 120:

            window.blit(screen, (0,0))
            screen.fill((0,0,0))
            window.blit(self.font_start_time.render(f'ночь {night}', True, (200, 200, 200)), (565, 370))
            window.blit(self.font_start_time.render('00: 00', True, (200, 200, 200)), (565, 320))
            self.var_timer += 1
            if self.var_timer == 119:
                self.ventilator.play(-1)
                # print('hello')


            return False

        return True

    def ending_night(self, night):

        if self.string_timer_secs // 60 == 6:

            self.camera_static.stop()

            if self.playending:
                self.ending.play(0)
                self.playending = False

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            window.blit(self.font_start_time.render('06: 00', True, (200, 200, 200)), (570, 320))

            if self.string_timer_secs % 60 == 12:
                self.end = True

                self.maindata = {
                    "ночь 5" : False,
                    "ночь 4" : False,
                    "ночь 3" : False,
                    "ночь 2" : False,
                    "ночь 1" : False,
                }

                self.maindata[night] = True

                for i in range(1, int(night[-1]) + 1):
                    self.maindata[f'ночь {i}'] = True

                with open('data/data.json', 'w', encoding='utf-8') as file:
                    json.dump(self.maindata, file, indent=4, ensure_ascii=False)


    def lose_screen(self):
        self.camera_static.stop()
        window.blit(screen, (0,0))
        screen.fill((0,0,0))

        window.blit(self.font_start_time.render(f'{self.mainstring}', True, (200, 200, 200)), (570, 320))

        if self.end_from_lose == 300:
            self.killed_sound.play(0)

        self.end_from_lose -= 1
        if not self.end_from_lose:
            self.end = True


    def render_room(self):
        window.blit(self.mainroom, (0 - scroll[0], 0 - scroll[1]))
        window.blit(self.font_cams.render('cams', True, (50, 50, 50)), (1182 - scroll[0], 318 - scroll[1]))
        # print(self.mouse[0] + scroll[0], self.mouse[1] + scroll[1])
        if self.rect_monitor.collidepoint(self.mouse[0] + scroll[0], self.mouse[1] + scroll[1]):
            window.blit(self.font_watch.render('просматривать', True, (50, 50, 50)), (1095 - scroll[0], 380 - scroll[1]))

    def rolemouse(self):
        global scroll
        self.mouse = pygame.mouse.get_pos()

        if scroll[0] >= 0 and scroll[0] <= 1100:
            if self.mouse[0] < 400:
                scroll[0] -= 5
                if self.mouse[0] < 240:
                    scroll[0] -= 10
            if self.mouse[0] > 800:
                scroll[0] += 5
                if self.mouse[0] > 960:
                    scroll[0] += 10

        if scroll[0] < 0:
            scroll[0] = 0
        if scroll[0] > 1100:
            scroll[0] = 1100

        # print(scroll)



class Night1(Night):
    def __init__(self):
        super(Night1, self).__init__()
        # интервал перемещения для 325 будет 1 минута

        self.var_delay_death = 1200

        self.number_dialog = pygame.mixer.Sound('sounds/phone1.wav')  # тут будет записан диалог фонгая на первую ночь

        self.allowed_pc = False

        self.opencams_sound = pygame.mixer.Sound('sounds/opencams.wav')

        self.delay_start_number = 200
        self.turnoff_number = 300





        self.render_night()

    def render_night(self):

        while True:



            self.key = pygame.key.get_pressed()
            self.computer.savely.move(self.computer.timer, self.computer.call)
            self.rolemouse()

            self.mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.allowed_pc -= 1
                        self.allowed_pc = abs(self.allowed_pc)

                        if bool(self.allowed_pc):
                            # print('activated')
                            self.play_camera = True

                        else:
                            self.camera_static.stop()

                        if self.play_camera:
                            # print('activated')
                            self.camera_static.play(-1)
                            self.play_camera = False

                        self.opencams_sound.play(0)

                    if event.key == pygame.K_c:
                        self.turnoff_number = 0
                        self.number_dialog.stop()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.computer.callsound_bool and self.allowed_pc:
                            self.computer.callsound_bool = True

                        if self.rect_monitor.collidepoint(self.mouse[0] + scroll[0], self.mouse[1] + scroll[1]):
                            self.allowed_pc -= 1
                            self.allowed_pc = abs(self.allowed_pc)

                            if bool(self.allowed_pc):
                                self.play_camera = True

                            else:
                                self.camera_static.stop()

                            if self.play_camera:
                                self.camera_static.play(-1)
                                self.play_camera = False

                            self.opencams_sound.play(0)


            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            self.render_room()

            self.delay_start_number -= 1
            if self.delay_start_number == 0:
                self.number_dialog.play(0)
                self.delay_start_number = -1
            elif self.delay_start_number < 0:
                self.delay_start_number = -1
                self.turnoff_number -= 1

            if self.turnoff_number >= 0 and self.delay_start_number < 0:
                window.blit(self.font_timer.render('нажмите <с>, чтотбы сбросить звонок', True, (200, 200, 200)), (820, 32))

            # до окон

            if self.showtime(1):
                if self.allowed_pc:
                    self.computer.render_monitor()
                self.render_timer()

            if self.key[pygame.K_v] and self.key[pygame.K_ESCAPE] and self.key[pygame.K_e]:
                self.string_timer_secs = 60 * 6

            if self.var_delay_death > 0:
                self.ending_night('ночь 1')

            self.lose()

            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            self.computer.timer = 59 - self.string_timer_secs % 60

            if self.end:
                break


    def lose(self):
        if self.computer.savely.room == 2 or self.var_delay_death <= 0:
            if self.computer.savely.callroom != 0 and self.computer.savely.callroom != 2:
                if self.string_timer_secs % 60 == 30:
                    self.computer.savely.room = self.computer.savely.callroom
                return False
            self.var_delay_death -= 1
            if self.var_delay_death < 0:
                self.allowed_pc = 0
                if self.computer.savely.jumpscare():
                    self.total_scare()

    def total_scare(self):
        self.allowed_pc = 0
        if self.computer.savely.jumpscare():
            self.lose_screen()






class Night2(Night):
    def __init__(self):
        super(Night2, self).__init__()

        self.var_delay_death = 1000

        self.number_dialog = pygame.mixer.Sound('sounds/phone2.wav')  # тут будет записан диалог фонгая на первую ночь

        self.allowed_pc = False

        self.opencams_sound = pygame.mixer.Sound('sounds/opencams.wav')

        self.delay_start_number = 200
        self.turnoff_number = 300

        self.smok = Smoke()

        self.render_night()

    def render_night(self):

        while True:

            self.key = pygame.key.get_pressed()
            self.rolemouse()
            self.computer.savely.move(self.computer.timer, self.computer.call)

            self.mouse = pygame.mouse.get_pos()

            self.mouse = self.smok.shake(list(self.mouse))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.allowed_pc -= 1
                        self.allowed_pc = abs(self.allowed_pc)

                        if bool(self.allowed_pc):
                            # print('act')
                            self.play_camera = True

                        else:
                            self.camera_static.stop()

                        if self.play_camera:
                            # print('active')
                            self.camera_static.play(-1)
                            self.play_camera = False

                        self.opencams_sound.play(0)

                    if event.key == pygame.K_c:
                        self.turnoff_number = 0
                        self.number_dialog.stop()



                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.computer.callsound_bool and self.allowed_pc:
                            self.computer.callsound_bool = True

                        if self.rect_monitor.collidepoint(self.mouse[0] + scroll[0], self.mouse[1] + scroll[1]):
                            self.allowed_pc -= 1
                            self.allowed_pc = abs(self.allowed_pc)

                            if self.allowed_pc:
                                # print('act')
                                self.play_camera = True

                            else:
                                self.camera_static.stop()

                            if self.play_camera:
                                # print('active')
                                self.camera_static.play(-1)
                                self.play_camera = False

                                self.opencams_sound.play(0)

            window.blit(screen, (0, 0))
            screen.fill((0, 0, 0))

            self.render_room()

            self.delay_start_number -= 1
            if self.delay_start_number == 0:
                self.number_dialog.play(0)
                self.delay_start_number = -1
            elif self.delay_start_number < 0:
                self.delay_start_number = -1
                self.turnoff_number -= 1

            if self.turnoff_number >= 0 and self.delay_start_number < 0:
                window.blit(self.font_timer.render('нажмите <с>, чтотбы сбросить звонок', True, (200, 200, 200)),
                            (820, 32))

            self.smok.render_smokbar()

            if self.showtime(2):
                if self.allowed_pc:
                    self.computer.render_monitor()
                self.render_timer()

            if self.key[pygame.K_v] and self.key[pygame.K_ESCAPE] and self.key[pygame.K_q]:
                self.string_timer_secs += 20

            if self.var_delay_death > 0:
                self.ending_night('ночь 2')

            self.lose()

            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            self.computer.timer = 44 - self.string_timer_secs % 45

            if self.end:
                break

            if not self.allowed_pc:
                if self.key[pygame.K_e]:
                    self.smok.add()



    def lose(self):

        if self.smok.percents <= 0:
            self.lose_screen()

        if self.computer.savely.room == 2 or self.var_delay_death <= 0:
            if self.computer.savely.callroom != 0 and self.computer.savely.callroom != 2:
                if self.string_timer_secs % 60 == 30:
                    self.computer.savely.room = self.computer.savely.callroom
                return False
            self.var_delay_death -= 1
            if self.var_delay_death < 0:
                self.total_scare()



    def total_scare(self):
        self.allowed_pc = 0
        if self.computer.savely.jumpscare():
            self.lose_screen()


class Night3(Night):
    def __init__(self):
        super(Night3, self).__init__()

        self.var_delay_death = 800

        self.allowed_pc = False

        self.opencams_sound = pygame.mixer.Sound('sounds/opencams.wav')

        self.smok = Smoke()

        self.render_night()

    def render_night(self):

        while True:

            self.key = pygame.key.get_pressed()
            self.rolemouse()
            self.computer.savely.move(self.computer.timer, self.computer.call)

            self.mouse = pygame.mouse.get_pos()

            self.mouse = self.smok.shake(list(self.mouse))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.allowed_pc -= 1
                        self.allowed_pc = abs(self.allowed_pc)

                        if bool(self.allowed_pc):
                            # print('act')
                            self.play_camera = True

                        else:
                            self.camera_static.stop()

                        if self.play_camera:
                            # print('active')
                            self.camera_static.play(-1)
                            self.play_camera = False

                        self.opencams_sound.play(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.computer.callsound_bool and self.allowed_pc:
                            self.computer.callsound_bool = True

                        if self.rect_monitor.collidepoint(self.mouse[0] + scroll[0], self.mouse[1] + scroll[1]):
                            self.allowed_pc -= 1
                            self.allowed_pc = abs(self.allowed_pc)

                            if self.allowed_pc:
                                # print('act')
                                self.play_camera = True

                            else:
                                self.camera_static.stop()

                            if self.play_camera:
                                # print('active')
                                self.camera_static.play(-1)
                                self.play_camera = False

                                self.opencams_sound.play(0)

            window.blit(screen, (0, 0))
            screen.fill((0, 0, 0))

            self.render_room()

            self.smok.render_smokbar(min=0.02)


            if self.showtime(3):
                if self.allowed_pc:
                    self.computer.render_monitor()
                self.render_timer()

            if self.key[pygame.K_v] and self.key[pygame.K_ESCAPE] and self.key[pygame.K_q]:
                self.string_timer_secs += 20

            if self.var_delay_death > 0:
                self.ending_night('ночь 3')

            self.lose()

            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            self.computer.timer = 29 - self.string_timer_secs % 30

            if self.end:
                break

            if not self.allowed_pc:
                if self.key[pygame.K_e]:
                    self.smok.add()

    def lose(self):

        if self.smok.percents <= 0:
            self.lose_screen()

        if self.computer.savely.room == 2  or self.var_delay_death <= 0:
            if self.computer.savely.callroom != 0 and self.computer.savely.callroom != 2:
                if self.string_timer_secs % 60 == 45:
                    self.computer.savely.room = self.computer.savely.callroom
                return False
            self.var_delay_death -= 1
            if self.var_delay_death < 0:
                self.total_scare()

    def total_scare(self):
        self.allowed_pc = 0
        if self.computer.savely.jumpscare():
            self.lose_screen()


class Night4(Night):
    def __init__(self):
        super(Night4, self).__init__()

        self.var_delay_death = 600

        self.number_dialog = pygame.mixer.Sound('sounds/phone4.wav')

        self.allowed_pc = False

        self.opencams_sound = pygame.mixer.Sound('sounds/opencams.wav')

        self.delay_start_number = 200
        self.turnoff_number = 300

        self.smok = Smoke()

        self.render_night()

    def render_night(self):

        while True:

            self.key = pygame.key.get_pressed()
            self.rolemouse()
            self.computer.savely.move(self.computer.timer, self.computer.call)

            self.mouse = pygame.mouse.get_pos()

            self.mouse = self.smok.shake(list(self.mouse))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.allowed_pc -= 1
                        self.allowed_pc = abs(self.allowed_pc)

                        if bool(self.allowed_pc):
                            # print('act')
                            self.play_camera = True

                        else:
                            self.camera_static.stop()

                        if self.play_camera:
                            # print('active')
                            self.camera_static.play(-1)
                            self.play_camera = False

                        self.opencams_sound.play(0)

                    if event.key == pygame.K_c:
                        self.turnoff_number = 0
                        self.number_dialog.stop()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.computer.callsound_bool and self.allowed_pc:
                            self.computer.callsound_bool = True

                        if self.rect_monitor.collidepoint(self.mouse[0] + scroll[0], self.mouse[1] + scroll[1]):
                            self.allowed_pc -= 1
                            self.allowed_pc = abs(self.allowed_pc)

                            if self.allowed_pc:
                                # print('act')
                                self.play_camera = True

                            else:
                                self.camera_static.stop()

                            if self.play_camera:
                                # print('active')
                                self.camera_static.play(-1)
                                self.play_camera = False

                                self.opencams_sound.play(0)

            window.blit(screen, (0, 0))
            screen.fill((0, 0, 0))

            self.render_room()

            self.delay_start_number -= 1
            if self.delay_start_number == 0:
                self.number_dialog.play(0)
                self.delay_start_number = -1
            elif self.delay_start_number < 0:
                self.delay_start_number = -1
                self.turnoff_number -= 1

            if self.turnoff_number >= 0 and self.delay_start_number < 0:
                window.blit(self.font_timer.render('нажмите <с>, чтотбы сбросить звонок', True, (200, 200, 200)),
                            (820, 32))


            self.smok.render_smokbar(night=4, min=0.05)
            self.smok.charge()

            if self.showtime(4):
                if self.allowed_pc:
                    self.computer.render_monitor()
                self.render_timer()

            if self.key[pygame.K_v] and self.key[pygame.K_ESCAPE] and self.key[pygame.K_q]:
                self.string_timer_secs += 20

            if self.var_delay_death > 0:
                self.ending_night('ночь 4')

            self.lose()

            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            self.computer.timer = 14 - self.string_timer_secs % 15

            if self.end:
                break

            if not self.allowed_pc:
                if self.key[pygame.K_e]:
                    self.smok.add()

    def lose(self):

        if self.smok.percents <= 0:
            self.lose_screen()

        if self.computer.savely.room == 2 or self.var_delay_death <= 0:
            if self.computer.savely.callroom != 0 and self.computer.savely.callroom != 2:
                if self.string_timer_secs % 60 == 15:
                    self.computer.savely.room = self.computer.savely.callroom
                return False
            self.var_delay_death -= 1
            if self.var_delay_death < 0:
                self.total_scare()

    def total_scare(self):
        self.allowed_pc = 0
        if self.computer.savely.jumpscare():
            self.lose_screen()


class Night5(Night):
    def __init__(self):
        super(Night5, self).__init__()

        self.var_delay_death = 400

        self.allowed_pc = False

        self.opencams_sound = pygame.mixer.Sound('sounds/opencams.wav')

        self.smok = Smoke()

        self.render_night()

    def render_night(self):

        while True:

            self.key = pygame.key.get_pressed()
            self.rolemouse()
            self.computer.savely.move(self.computer.timer, self.computer.call)

            self.mouse = pygame.mouse.get_pos()

            self.mouse = self.smok.shake(list(self.mouse))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.allowed_pc -= 1
                        self.allowed_pc = abs(self.allowed_pc)

                        if bool(self.allowed_pc):
                            # print('act')
                            self.play_camera = True

                        else:
                            self.camera_static.stop()

                        if self.play_camera:
                            # print('active')
                            self.camera_static.play(-1)
                            self.play_camera = False

                        self.opencams_sound.play(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.computer.callsound_bool and self.allowed_pc:
                            self.computer.callsound_bool = True

                        if self.rect_monitor.collidepoint(self.mouse[0] + scroll[0], self.mouse[1] + scroll[1]):
                            self.allowed_pc -= 1
                            self.allowed_pc = abs(self.allowed_pc)

                            if self.allowed_pc:
                                # /('act')
                                self.play_camera = True

                            else:
                                self.camera_static.stop()

                            if self.play_camera:
                                # print('active')
                                self.camera_static.play(-1)
                                self.play_camera = False

                                self.opencams_sound.play(0)

            window.blit(screen, (0, 0))
            screen.fill((0, 0, 0))

            self.render_room()

            self.smok.render_smokbar(night=5, min=0.08)
            self.smok.charge(add=0.05, eat=1.3)

            if self.showtime(5):
                if self.allowed_pc:
                    self.computer.render_monitor()
                self.render_timer()

            if self.key[pygame.K_v] and self.key[pygame.K_ESCAPE] and self.key[pygame.K_q]:
                self.string_timer_secs += 20

            if self.var_delay_death > 0:
                self.ending_night('ночь 5')

            self.lose()

            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            self.computer.timer = 4 - self.string_timer_secs % 5

            if self.end:
                break

            if not self.allowed_pc:
                if self.key[pygame.K_e]:
                    self.smok.add()

    def lose(self):

        if self.smok.percents <= 0:
            self.lose_screen()

        if self.computer.savely.room == 2 or self.var_delay_death <= 0:
            if self.computer.savely.callroom != 0 and self.computer.savely.callroom != 2:
                if self.string_timer_secs % 60 == 5:
                    self.computer.savely.room = self.computer.savely.callroom
                return False
            self.var_delay_death -= 1
            if self.var_delay_death < 0:
                self.total_scare()

    def total_scare(self):
        self.allowed_pc = 0
        if self.computer.savely.jumpscare():
            self.lose_screen()





class Nights():
    def __init__(self, night):
        self.night = night

        if self.night == 1:
            self.main_night = Night1()
            # print('night 1')
            if self.main_night.end:
                self.night = 6
                # print('night 6')

        elif self.night == 2:
            self.main_night = Night2()

        elif self.night == 3:
            self.main_night = Night3()

        elif self.night == 4:
            self.main_night = Night4()

        elif self.night == 5:
            self.main_night = Night5()

        # self.main_night = self.nights[self.night]
        if self.main_night.end:
            self.night = 6



