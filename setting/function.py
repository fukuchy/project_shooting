import sys
import os
import pygame
import csv
from pygame.locals import *
from pygame import mixer
from . import importpngs as pngs
from . import player as p
from . import paramater as para
from . import score
from . import textbox as t
import main as m
mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def time_count(time, screen):

    elapsed_minute = (time % 3600) // 60
    elapsed_second = (time % 3600 % 60)
    timer = f"{str(elapsed_minute).zfill(2)}:{str(elapsed_second).zfill(2)}"
    font = "misaki_gothic.ttf"
    timer_font = pygame.font.Font(font, 60)
    timer_text = timer_font.render(timer, True, (0, 0, 0))
    screen.blit(timer_text, (20, 15))

def gameover(field):

    pygame.mixer.music.load("音楽/gameover_BGM.mp3")
    pygame.mixer.music.play(-1)

    while True:
        screen = pygame.display.set_mode((1280, 720))
        screen.blit(pngs.keyboard_image, (160, 100))
        screen.blit(pngs.img_gameover, (0, 0))
        pygame.draw.rect(screen, (0, 0, 100), [1040, 45, 200, 20])

        for enemy in field.enemys:

            match enemy.various:
                case 0:
                    screen.blit(pngs.sleepiness_image0, (enemy.x, enemy.y))
                case 1:
                    screen.blit(pngs.sleepiness_image1, (enemy.x, enemy.y))
                case 2:
                    screen.blit(pngs.sleepiness_image2, (enemy.x, enemy.y))
                case 3:
                    screen.blit(pngs.sleepiness_image_boss, (enemy.x, enemy.y))

        screen.blit(pngs.background_up, (0, 0))
        screen.blit(pngs.background_left, (0, 100)) 

        p.player.print_mob(screen, pngs.player_image)
        font = "misaki_gothic.ttf"
        font1 = pygame.font.Font(font, 100)
        font2 = pygame.font.Font(font, 50)
        text1 = font1.render("GAME OVER", True, (200, 0, 0))
        screen.blit(text1, (450, 130))
        text2 = font2.render("つづける key c", True, (200, 0, 0))
        screen.blit(text2, (505, 340))
        text3 = font2.render("おわる key Esc", True, (200, 0, 0))
        screen.blit(text3, (505, 400))
        text4 = font2.render(f"たおしたかず: {para.point}", True, (200,0,0)) 
        screen.blit(text4, (495, 220))

        with open("setting/score_file.csv","r") as file:
            score_list = list()
            data = csv.reader(file)
            for row in data:
                score_list.extend(row)
            for x in range(3):
                text5 = font2.render(f"No{x+1}.       {score_list[x]}", True, (200,0,0))
                screen.blit(text5, (490, 480+60*x))

        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if key[K_c] == 1:
            m.main()
        elif key[K_e] == 1 or key[K_ESCAPE] == 1:
            pygame.quit()
            sys.exit()

        pygame.display.update()

def level_check(cursor):

    if cursor == 1:
        return 2
    elif cursor == 0:
        return 1
    elif cursor == -1:
        return 0

def start():

    cursor = 0
    screen = pygame.display.set_mode((1280, 720))
    pygame.mixer.music.load("音楽/start_BGM.mp3")
    pygame.mixer.music.play(-1)
    input_box,button = t.name_input_init()
    while True:

        screen.blit(pngs.start_menu, (0, 0))
        screen.blit(pngs.arrow, (300, 340-cursor * 120))
        
        for event in pygame.event.get():
            t.name_input(input_box,button,event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and para.input_flag == True:
                if event.key == K_w:
                    if cursor < 1:
                        cursor += 1
                elif event.key == K_s:
                    if cursor > -1:
                        cursor -= 1
                elif event.key == K_r:
                    score.ranking()
        t.draw_textbox(screen,input_box,button)
        key = pygame.key.get_pressed()

        if key[K_SPACE] == 1:

            return cursor
        
        if key[K_ESCAPE] == 1:

            pygame.quit()
            sys.exit()

        pygame.display.update()