# 画像ロード欄＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
import pygame
player_image = pygame.image.load("画像/player.png")
rect_player = player_image.get_rect()
keyboard_image = pygame.image.load("画像/keyboard3.png")
arrow = pygame.image.load("画像/point.png")
start_menu = pygame.image.load("画像/title.png")
sleepiness_image0 = pygame.image.load("画像/enemy0.png")
sleepiness_image1 = pygame.image.load("画像/enemy1.png")
sleepiness_image2 = pygame.image.load("画像/enemy2.png")
sleepiness_image_boss = pygame.image.load("画像/bos1.png")
power_up_image = pygame.image.load("画像/power_up.png")
item_image0 = pygame.image.load("画像/item0.png")
item_image1 = pygame.image.load("画像/item1.png")
item_image2 = pygame.image.load("画像/item2.png")
img_gameover = pygame.image.load("画像/gameover.png")
bullet_player_image = pygame.image.load("画像/bullet.png")
bullet_direction_light = pygame.image.load("画像/cell2.png")
background_up = pygame.image.load("画像/haikei_up.png")
background_left = pygame.image.load("画像/background_left.png")
ranking_bg = pygame.image.load("画像/rank.png")
animation_list = []
for i in range(6):
    x = pygame.image.load(f"画像/爆発アニメーション/{i + 1}.png")
    animation_list.append(x)
pygame.display.set_caption("限界大学生  -genkaidaigakusei-")
icon=pygame.image.load("画像/icon.png")
pygame.display.set_icon(icon)