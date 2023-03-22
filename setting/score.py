import sys
import os
import pygame
import csv
from pygame.locals import *
from pygame import mixer
from . import importpngs as pngs
from . import paramater as para
from . import function as f
mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def ranking():
    while True:
        screen = pygame.display.set_mode((1280, 720))
        screen.blit(pngs.ranking_bg,(0,0))
        pygame.font.init()
        font = "misaki_gothic.ttf"
        font3 = pygame.font.Font(font, 60)
        # font3 = pygame.font.SysFont(None, 80)
        with open("setting/score_file.csv","r") as file:
            score_list = list()
            data = csv.reader(file)
            for row in data:
                score_list.extend(row)
            
            for x in range(10):
                
                text6 = font3.render(f"No{x+1}.       {score_list[x]}", True, (200,0,0))
                screen.blit(text6, (420, 85+60*x))

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        return f.start()
        
        pygame.display.update()

def score_save():
    with open("setting/score_file.csv","r") as file:
        score_list = list()
        data = csv.reader(file)
        for row in data:
            score_list.extend(row)

        score_list_2 = list()
        score_list_2.append(para.point)
        for value in score_list:
            score_list_2.append(int(value))

        score_list_2.sort(reverse=True)

        if len(score_list) >= 10:        
            score_list_3 = list()
            for x in range(10):
                score_list_3.append(score_list_2[x])

            file.close()
            with open("setting/score_file.csv","w", newline="") as file:
                writer = csv.writer(file)
                for x in range(10):
                    writer.writerow([score_list_3[x]])
        else:
            with open("setting/score_file.csv","a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([para.point])


#TODO
"""
結果を追加しjson形式でAPIに送信
{
    "name":name,
    "score":score   
}
"""