import sys
import os
import pygame
from pygame.locals import *
from pygame import mixer
from setting import importpngs as pngs
from setting import function as f
from setting import player as p
from setting import paramater as para
from setting import score
mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))



# while True:
#     player_name = input("player_name:")

#     if player_name != "":
        
#         p.player.name = player_name
#         break

def main():
    
    para.init()

    while True:

        dt = para.fps_clock.tick(60)