import sys
import math
import os
import random
import pygame
import csv
from pygame.locals import *
from pygame import mixer
from . import importpngs as pngs
from . import Mob as mob
from . import item as item
from . import bullet
from . import player as p
from . import paramater as para

class Field:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.enemys = []
        self.items = []
        self.bullets = []
        self.bullet_flag = False
        self.item_flag1 = False
        self.item_flag2 = False

    def length(self, o1, o2):

        o1x = o1.x + o1.r / 2
        o1y = o1.y + o1.r / 2
        o2x = o2.x + o2.r / 2
        o2y = o2.y + o2.r / 2

        x = o1x - o2x
        y = o1y - o2y

        return x, y

    def touch(self, o1, o2):

        x, y = self.length(o1, o2)

        leng = math.sqrt(x ** 2 + y ** 2)
        if leng < (o1.r + o2.r) / 2:
            return True

    def move_player(self, key, screen, level):

        if level == 2:
            buff = 0.9
        else:
            buff = 1

        if key[K_a] == 1:
            p.player.x -= p.player.speed * buff
            if p.player.x < 160:
                p.player.x = 160
        if key[K_d] == 1:
            p.player.x += p.player.speed * buff
            if p.player.x > para.screen_width - p.player.r:
                p.player.x = para.screen_width - p.player.r
        if key[K_w] == 1:
            p.player.y -= p.player.speed * buff
            if p.player.y < 100:
                p.player.y = 100
        if key[K_s] == 1:
            p.player.y += p.player.speed * buff
            if p.player.y > para.screen_height - p.player.r:
                p.player.y = para.screen_height - p.player.r
        if key[K_BACKSPACE] == 1:
            p.player.hp = 100
        if self.bullet_flag == False:

            self.x = 0
            self.y = 0

            if key[K_r] == 1:
                self.x = 222
                self.y = 182
                self.bullet_flag = True
            elif key[K_t] == 1:
                self.x = 402
                self.y = 182
                self.bullet_flag = True
            elif key[K_y] == 1:
                self.x = 584
                self.y = 182
                self.bullet_flag = True
            elif key[K_u] == 1:
                self.x = 764
                self.y = 182
                self.bullet_flag = True
            elif key[K_i] == 1:
                self.x = 945
                self.y = 182
                self.bullet_flag = True
            elif key[K_o] == 1:
                self.x = 1125
                self.y = 182
                self.bullet_flag = True
            elif key[K_f] == 1:
                self.x = 252
                self.y = 363
                self.bullet_flag = True
            elif key[K_g] == 1:
                self.x = 433
                self.y = 363
                self.bullet_flag = True
            elif key[K_h] == 1:
                self.x = 615
                self.y = 363
                self.bullet_flag = True
            elif key[K_j] == 1:
                self.x = 796
                self.y = 363
                self.bullet_flag = True
            elif key[K_k] == 1:
                self.x = 977
                self.y = 363
                self.bullet_flag = True
            elif key[K_v] == 1:
                self.x = 301
                self.y = 546
                self.bullet_flag = True
            elif key[K_b] == 1:
                self.x = 483
                self.y = 546
                self.bullet_flag = True
            elif key[K_n] == 1:
                self.x = 663
                self.y = 546
                self.bullet_flag = True
            elif key[K_m] == 1:
                self.x = 844
                self.y = 546
                self.bullet_flag = True

            if self.x != 0 and self.y != 0:
                self.vect_bullet(self.x, self.y, level)
                mixer.Sound("音楽/new_bullet_sound.mp3").play()

        else:
            if self.x != 0 and self.y != 0:
                screen.blit(pngs.bullet_direction_light, (self.x-45, self.y-35))

        p.player.print_mob(screen, pngs.player_image)

    def vect_bullet(self, dx, dy, level):

        X = dx - p.player.x
        Y = dy - p.player.y

        if X == 0:
            X = 0.0001
        if Y == 0:
            Y = 0.0001

        theta = math.atan(Y / X)
        v = 4

        if level == 0:
            v = 4 * 0.8

        if X > 0:
            vx = math.cos(theta) * v 
            vy = math.sin(theta) * v 
        else:
            vx = -(math.cos(theta) * v) 
            vy = -(math.sin(theta) * v) 

        self.bullets.append(bullet.Bullet(p.player.x, p.player.y, vx, vy))

    def move_bullet(self, screen):

        for bullet in self.bullets:
            bullet.x += bullet.dx
            bullet.y += bullet.dy

            screen.blit(pngs.bullet_player_image, (bullet.x, bullet.y))

    def remove_bullet(self):

        for u, bullet in enumerate(self.bullets):
            if bullet.x >= para.screen_width or bullet.x <= 0 or bullet.y <= 0 or bullet.y >= para.screen_height:
                self.bullets.pop(u)

    def append_sleep(self):

        flag = random.randint(0, 3)

        if flag == 0:  # 上 0
            x = random.randint(205, 1274)
            y = 68  # 148
        elif flag == 1:  # 下
            x = random.randint(205, 1274)
            y = 717
        elif flag == 2:  # 右
            x = 1274
            y = random.randint(148, 717)
        else:  # 左
            x = 125  # 205
            y = random.randint(148, 717)

        enemy_choice = random.choice([0, 1, 1, 1, 2, 2])

        if enemy_choice == 0:
            self.enemys.append(
                mob.Mob(x, y, r=80, hp=-50, attack=30, speed=1, various=0, name= ""))
        elif enemy_choice == 1:
            self.enemys.append(
                mob.Mob(x, y, r=60, hp=-20, attack=10, speed=2.5, various=1, name= ""))
        elif enemy_choice == 2:
            self.enemys.append(
                mob.Mob(x, y, r=45, hp=-10, attack=5, speed=4, various=2, name= ""))

    # レベルを考慮するか
    def move_sleep(self, screen, level):
        for c, enemy in enumerate(self.enemys):

            

            if enemy.hp < 0:

                if self.touch(p.player, enemy):
                    p.player.receive_damege(enemy.attack)
                    self.enemys.pop(c)
                
                if level ==2:
                    dx = enemy.speed
                elif level == 1:
                    dx = enemy.speed * 0.75
                else:
                    dx = enemy.speed * 0.8

                x, y = self.length(p.player, enemy)

                if x == 0:
                    x = 0.0001
                if y == 0:
                    y = 0.0001

                theta = math.atan(y / x)

                if x > 0:
                    enemy.x += math.cos(theta) * dx 
                    enemy.y += math.sin(theta) * dx 
                else:
                    enemy.x -= math.cos(theta) * dx 
                    enemy.y -= math.sin(theta) * dx 

                for c_b, bullet in enumerate(self.bullets):
                    if self.touch(bullet, enemy):
                        enemy.receive_damege(p.player.attack)
                        self.bullets.pop(c_b)

                if enemy.various == 0:
                    enemy.print_mob(screen, pngs.sleepiness_image0)
                elif enemy.various == 1:
                    enemy.print_mob(screen, pngs.sleepiness_image1)
                elif enemy.various == 2:
                    enemy.print_mob(screen, pngs.sleepiness_image2)
                elif enemy.various == 3:
                    enemy.print_mob(screen, pngs.sleepiness_image_boss)
            
            elif enemy.hp >= 0:

                if enemy.animation == 0:
                    para.point += 1

                if enemy.animation < 35:
                    img = pngs.animation_list[enemy.animation // 6]
                    enemy.animation += 1
                    screen.blit(img, (enemy.x, enemy.y))
                else:
                    self.enemys.pop(c)
                     
    def append_boss(self):

        flag = random.randint(0, 3)
        if flag == 0:  # 上
            x = random.randint(205, 1274)
            y = 68
        elif flag == 1:  # 下
            x = random.randint(205, 1274)
            y = 717
        elif flag == 2:  # 右
            x = 1274
            y = random.randint(148, 717)
        else:  # 左
            x = 125
            y = random.randint(148, 717)

        self.enemys.append(
            mob.Mob(x, y, r=160, hp=-150, attack=50, speed=0.5, various=3, name = ""))

    def append_item(self):

        choice = random.choice([0, 1, 2])
        # choice = random.choice([2])
        x = random.randint(205, 1200)
        y = random.randint(148, 640)

        if choice == 0:
            self.items.append(item.Item(x, y, 60, 15, 0))
        elif choice == 1:
            self.items.append(item.Item(x, y, 60, 15, 1))
        elif choice == 2:
            self.items.append(item.Item(x, y, 60, 15, 2))

    def draw_item(self, screen):

        if self.items != None:
            for i in self.items:
                if i.various == 0:
                    screen.blit(pngs.item_image0, (i.x, i.y))
                elif i.various == 1:
                    screen.blit(pngs.item_image1, (i.x, i.y))
                elif i.various == 2:
                    screen.blit(pngs.item_image2, (i.x, i.y))

        for c_i, item in enumerate(self.items):
            if self.touch(p.player, item):
                if item.various == 0:
                    if p.player.hp > 0:
                        p.player.hp -= 30
                    else:
                        p.player.hp = 0
                elif item.various == 1 and self.item_flag1 == False:
                    self.item_flag1 = True
                    if self.item_flag1 == True:
                        p.player.attack = p.player.attack*5
                elif item.various == 2 and self.item_flag2 == False:
                    self.item_flag2 = True
                    if self.item_flag2 == True:
                        for enemy in self.enemys:
                            enemy.speed = enemy.speed/2

                self.items.pop(c_i)

    def draw_hp(self, screen):

        pygame.draw.rect(screen, (0, 0, 0), [1040, 45, 200, 20])
        if 70 < p.player.hp <= 100:
            pygame.draw.rect(screen, (0, 0, 139), [
                             1040, 45, p.player.hp*2, 20])
        elif 50 < p.player.hp <= 70:
            pygame.draw.rect(screen, (0, 0, 205), [
                             1040, 45, p.player.hp*2, 20])
        elif p.player.hp <= 50:
            pygame.draw.rect(screen, (135, 206, 235), [
                             1040, 45, p.player.hp*2, 20])

    def draw_power(self, screen, time_item1):

        range = 70-(time_item1*70)//10000
        screen.blit(pngs.power_up_image, (940, 8))
        pygame.draw.rect(screen, (0, 0, 0), (965, 75, 70, 10))
        pygame.draw.rect(screen, (255, 0, 0), (965, 75, range, 10))
    
    def point_print(self, screen):
        font = "misaki_gothic.ttf"
        point_font = pygame.font.Font(font, 50)
        score = f"たおしたかず:{para.point}"
        point_text = point_font.render(score, True, (0,0,0))
        screen.blit(point_text, (240,15))  