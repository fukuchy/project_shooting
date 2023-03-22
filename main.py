import sys
import os
import pygame
import csv
from pygame.locals import *
from pygame import mixer
import importpngs as pngs
import Mob as mob
import field as Fi
import function as f
import player as p
import paramater as para
mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():

    cursor=f.start()
    level = f.level_check(cursor)
    para.point = 0
    count = 0
    b_count = 0
    time = 0
    item_flag = False
    time_item1 = 0
    time_item2 = 0
    bossflag = True
    fps_clock = pygame.time.Clock()
    field = Fi.Field()
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    field.width = 200
    pygame.mixer.music.load("音楽/main_BGM.mp3")
    pygame.mixer.music.play(-1)
    ccount = 0

    while True:

        dt = fps_clock.tick(60)
        para.fps = dt
        count += dt
        ccount += dt
        field.remove_bullet()

        if field.bullet_flag == True:
            b_count += dt
            if field.item_flag2 == True:
                if b_count >= 200:
                    field.bullet_flag = False
                    b_count = b_count % 200
            else:
                if b_count >= 750:
                    field.bullet_flag = False
                    b_count = b_count % 750
        if field.item_flag1 != False:
            time_item1 += dt
            if time_item1 >= 10000:
                p.player.attack = p.player.attack/5
                field.item_flag1 = False
                time_item1 = time_item1 % 10000
        if field.item_flag2 != False:
            time_item2 += dt
            if time_item2 >= 10000:
                field.item_flag2 = False
                time_item2 = time_item2 % 15000

        key = pygame.key.get_pressed()
        if key[K_ESCAPE] == 1 or key[QUIT] == 1:
            pygame.quit()
            sys.exit()

        screen.blit(pngs.keyboard_image, (160, 100))
        field.move_player(key, screen, level)
        field.draw_item(screen)
        field.move_sleep(screen, level)
        field.move_bullet(screen)
        screen.blit(pngs.background_up, (0, 0))
        screen.blit(pngs.background_left, (0, 100))
        field.point_print(screen)
        font = "misaki_gothic.ttf"
        font1 = pygame.font.Font(font, 40)
        text1 = font1.render("ねむけゲージ", True, (0, 0, 0))
        screen.blit(text1, (1015, 8))

        if count >= 1000:
            time += 1
            count = count % 1000

        if ccount >= 2000:
            ccount = ccount % 2000
            field.append_sleep()
        if time % 90 == 0 and time != 0 and bossflag:
            field.append_boss()
            bossflag = False
        if time % 91 == 0 and time != 0:
            bossflag = True

        if item_flag == False:
            if time % 30 == 0 and time != 0:
                field.append_item()
                item_flag = True
        else:
            if time % 31 == 0:
                item_flag = False

        f.time_count(time, screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if p.player.hp >= 100:
            f.score_save() 
            return f.gameover(field)

        field.draw_hp(screen)
        if field.item_flag1 == True:
            field.draw_power(screen, time_item1)

        pygame.display.update()

if __name__ == "__main__":
    main()
