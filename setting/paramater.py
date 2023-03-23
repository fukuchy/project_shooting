import sys
import os
import pygame
from pygame.locals import *
from pygame import mixer
from . import importpngs as pngs
from . import field as Fi
from . import function as f
from . import player as p
from . import paramater as para
from . import score

screen_width = 1280
screen_height = 720
frame_width = 6
fps = 30
delay = 60 / (1000 / fps)
point = 0
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

def init():
    
    p.player.hp = 0
    p.player.x = 640
    p.player.y = 360
    cursor=f.start()
    para.level = f.level_check(cursor)
    para.point = 0
    para.count = 0
    para.b_count = 0
    para.time = 0
    para.item_flag = False
    para.time_item1 = 0
    para.time_item2 = 0
    para.bossflag = True
    para.fps_clock = pygame.time.Clock()
    field = Fi.Field()
    pygame.init()
    para.screen = pygame.display.set_mode((1280, 720))
    field.width = 200
    pygame.mixer.music.load("音楽/main_BGM.mp3")
    pygame.mixer.music.play(-1)
    para.ccount = 0