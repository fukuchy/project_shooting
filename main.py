# モジュール欄＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

import sys
import math
import os
import random
import pygame
import csv
from pygame.locals import *
from pygame import mixer
mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 画像ロード欄＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

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
# 初期設定欄(globalで使用する変数)＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

screen_width = 1280
screen_height = 720
frame_width = 6
fps = 30
delay = 60 / (1000 / fps)
point = 0

# クラス定義＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# プライヤーと敵のクラス


class Mob:

    def __init__(self, x, y, r, hp, attack, speed, various):

        self.x = x
        self.y = y
        self.r = r
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.various = various
        self.animation = 0

# ダメージ計算をするメソッド
    def receive_damege(self, damages):
        self.hp += damages

# 描画メソッド
    def print_mob(self, screen, img):
        screen.blit(img, [self.x, self.y])

# アイテムのクラス
class Item:

    def __init__(self, x, y, r, t, various):

        self.x = x
        self.y = y
        self.r = r
        self.various = various

# 弾のクラス
class Bullet:

    def __init__(self, x, y, dx, dy):

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.r = 80

# globalで使用するプレイヤー情報
player = Mob(x=640, y=360, r=80, hp=0,
             attack=10, speed=4, various=10)

# 画面のクラス(画面上で怒ることをつかさどる(プレイヤーや敵の挙動など))
class Field:

    global player, screen_width, screen_height, delay, point

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
            player.x -= player.speed * buff
            if player.x < 160:
                player.x = 160
        if key[K_d] == 1:
            player.x += player.speed * buff
            if player.x > screen_width - player.r:
                player.x = screen_width - player.r
        if key[K_w] == 1:
            player.y -= player.speed * buff
            if player.y < 100:
                player.y = 100
        if key[K_s] == 1:
            player.y += player.speed * buff
            if player.y > screen_height - player.r:
                player.y = screen_height - player.r

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
                screen.blit(bullet_direction_light, (self.x-45, self.y-35))

        player.print_mob(screen, player_image)

    def vect_bullet(self, dx, dy, level):

        X = dx - player.x
        Y = dy - player.y

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

        self.bullets.append(Bullet(player.x, player.y, vx, vy))

    def move_bullet(self, screen):

        for bullet in self.bullets:
            bullet.x += bullet.dx
            bullet.y += bullet.dy

            screen.blit(bullet_player_image, (bullet.x, bullet.y))

    def remove_bullet(self):

        for u, bullet in enumerate(self.bullets):
            if bullet.x >= screen_width or bullet.x <= 0 or bullet.y <= 0 or bullet.y >= screen_height:
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
                Mob(x, y, r=80, hp=-50, attack=30, speed=1, various=0))
        elif enemy_choice == 1:
            self.enemys.append(
                Mob(x, y, r=60, hp=-20, attack=10, speed=2.5, various=1))
        elif enemy_choice == 2:
            self.enemys.append(
                Mob(x, y, r=45, hp=-10, attack=5, speed=4, various=2))

    # レベルを考慮するか
    def move_sleep(self, screen, level):
        global point
        for c, enemy in enumerate(self.enemys):

            

            if enemy.hp < 0:

                if self.touch(player, enemy):
                    player.receive_damege(enemy.attack)
                    self.enemys.pop(c)
                
                if level ==2:
                    dx = enemy.speed
                elif level == 1:
                    dx = enemy.speed * 0.75
                else:
                    dx = enemy.speed * 0.8

                x, y = self.length(player, enemy)

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
                        enemy.receive_damege(player.attack)
                        self.bullets.pop(c_b)

                if enemy.various == 0:
                    enemy.print_mob(screen, sleepiness_image0)
                elif enemy.various == 1:
                    enemy.print_mob(screen, sleepiness_image1)
                elif enemy.various == 2:
                    enemy.print_mob(screen, sleepiness_image2)
                elif enemy.various == 3:
                    enemy.print_mob(screen, sleepiness_image_boss)
            
            elif enemy.hp >= 0:

                if enemy.animation == 0:
                    point += 1

                if enemy.animation < 35:
                    img = animation_list[enemy.animation // 6]
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
            Mob(x, y, r=160, hp=-150, attack=50, speed=0.5, various=3))

    def append_item(self):

        choice = random.choice([0, 1, 2])
        # choice = random.choice([2])
        x = random.randint(205, 1200)
        y = random.randint(148, 640)

        if choice == 0:
            self.items.append(Item(x, y, 60, 15, 0))
        elif choice == 1:
            self.items.append(Item(x, y, 60, 15, 1))
        elif choice == 2:
            self.items.append(Item(x, y, 60, 15, 2))

    def draw_item(self, screen):

        if self.items != None:
            for i in self.items:
                if i.various == 0:
                    screen.blit(item_image0, (i.x, i.y))
                elif i.various == 1:
                    screen.blit(item_image1, (i.x, i.y))
                elif i.various == 2:
                    screen.blit(item_image2, (i.x, i.y))

        for c_i, item in enumerate(self.items):
            if self.touch(player, item):
                if item.various == 0:
                    if player.hp > 0:
                        player.hp -= 30
                    else:
                        player.hp = 0
                elif item.various == 1 and self.item_flag1 == False:
                    self.item_flag1 = True
                    if self.item_flag1 == True:
                        player.attack = player.attack*5
                elif item.various == 2 and self.item_flag2 == False:
                    self.item_flag2 = True
                    if self.item_flag2 == True:
                        for enemy in self.enemys:
                            enemy.speed = enemy.speed/2

                self.items.pop(c_i)

    def draw_hp(self, screen):

        pygame.draw.rect(screen, (0, 0, 0), [1040, 45, 200, 20])
        if 70 < player.hp <= 100:
            pygame.draw.rect(screen, (0, 0, 139), [
                             1040, 45, player.hp*2, 20])
        elif 50 < player.hp <= 70:
            pygame.draw.rect(screen, (0, 0, 205), [
                             1040, 45, player.hp*2, 20])
        elif player.hp <= 50:
            pygame.draw.rect(screen, (135, 206, 235), [
                             1040, 45, player.hp*2, 20])

    def draw_power(self, screen, time_item1):

        range = 70-(time_item1*70)//10000
        screen.blit(power_up_image, (940, 8))
        pygame.draw.rect(screen, (0, 0, 0), (965, 75, 70, 10))
        pygame.draw.rect(screen, (255, 0, 0), (965, 75, range, 10))
    
    def point_print(self, screen):
        font = "misaki_gothic.ttf"
        point_font = pygame.font.Font(font, 50)
        score = f"たおしたかず:{point}"
        point_text = point_font.render(score, True, (0,0,0))
        screen.blit(point_text, (240,15))  

def time_count(time, screen):

    elapsed_minute = (time % 3600) // 60
    elapsed_second = (time % 3600 % 60)
    timer = f"{str(elapsed_minute).zfill(2)}:{str(elapsed_second).zfill(2)}"
    font = "misaki_gothic.ttf"
    timer_font = pygame.font.Font(font, 60)
    timer_text = timer_font.render(timer, True, (0, 0, 0))
    screen.blit(timer_text, (20, 15))

def gameover(field):
    global point

    pygame.mixer.music.load("音楽/gameover_BGM.mp3")
    pygame.mixer.music.play(-1)

    while True:
        screen = pygame.display.set_mode((1280, 720))
        screen.blit(keyboard_image, (160, 100))
        screen.blit(img_gameover, (0, 0))
        pygame.draw.rect(screen, (0, 0, 100), [1040, 45, 200, 20])

        for enemy in field.enemys:

            match enemy.various:
                case 0:
                    screen.blit(sleepiness_image0, (enemy.x, enemy.y))
                case 1:
                    screen.blit(sleepiness_image1, (enemy.x, enemy.y))
                case 2:
                    screen.blit(sleepiness_image2, (enemy.x, enemy.y))
                case 3:
                    screen.blit(sleepiness_image_boss, (enemy.x, enemy.y))
        screen.blit(background_up, (0, 0))
        screen.blit(background_left, (0, 100)) 

        player.print_mob(screen, player_image)
        font = "misaki_gothic.ttf"
        font1 = pygame.font.Font(font, 100)
        font2 = pygame.font.Font(font, 50)
        text1 = font1.render("GAME OVER", True, (200, 0, 0))
        screen.blit(text1, (450, 130))
        text2 = font2.render("つづける key c", True, (200, 0, 0))
        screen.blit(text2, (505, 340))
        text3 = font2.render("おわる key Esc", True, (200, 0, 0))
        screen.blit(text3, (505, 400))
        text4 = font2.render(f"たおしたかず: {point}", True, (200,0,0)) 
        screen.blit(text4, (495, 220))

        with open("score_file.csv","r") as file:
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
            return start()
        elif key[K_e] == 1 or key[K_ESCAPE] == 1:
            pygame.quit()
            sys.exit()

        pygame.display.update()

def ranking():
    while True:
        screen = pygame.display.set_mode((1280, 720))
        screen.blit(ranking_bg,(0,0))
        pygame.font.init()
        font = "misaki_gothic.ttf"
        font3 = pygame.font.Font(font, 60)
        # font3 = pygame.font.SysFont(None, 80)
        with open("score_file.csv","r") as file:
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
                        return start()
        
        pygame.display.update()

def score_save():
    global point
    with open("score_file.csv","r") as file:
        score_list = list()
        data = csv.reader(file)
        for row in data:
            score_list.extend(row)

        score_list_2 = list()
        score_list_2.append(point)
        for value in score_list:
            score_list_2.append(int(value))

        score_list_2.sort(reverse=True)

        if len(score_list) >= 10:        
            score_list_3 = list()
            for x in range(10):
                score_list_3.append(score_list_2[x])

            file.close()
            with open("score_file.csv","w", newline="") as file:
                writer = csv.writer(file)
                for x in range(10):
                    writer.writerow([score_list_3[x]])
        else:
            with open("score_file.csv","a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([point])

def level_check(cursor):

    if cursor == 1:
        return 2
    elif cursor == 0:
        return 1
    elif cursor == -1:
        return 0

def start():

    global player

    cursor = 0
    screen = pygame.display.set_mode((1280, 720))
    pygame.mixer.music.load("音楽/start_BGM.mp3")
    pygame.mixer.music.play(-1)

    while True:

        screen.blit(start_menu, (0, 0))
        screen.blit(arrow, (300, 340-cursor * 120))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w:
                    if cursor < 1:
                        cursor += 1
                elif event.key == K_s:
                    if cursor > -1:
                        cursor -= 1
                elif event.key == K_r:
                    ranking()

        key = pygame.key.get_pressed()

        if key[K_SPACE] == 1:
            mixer.Sound("音楽/selective_sound.mp3").play()
            player.hp = 0
            player.x = 640
            player.y = 360
            main(cursor)
        if key[K_ESCAPE] == 1:
            pygame.quit()
            sys.exit()

        pygame.display.update()

def main(cursor):

    global fps, delay, point
    level = level_check(cursor)
    point = 0
    count = 0
    b_count = 0
    time = 0
    item_flag = False
    time_item1 = 0
    time_item2 = 0
    bossflag = True
    fps_clock = pygame.time.Clock()
    field = Field()
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    field.width = 200
    pygame.mixer.music.load("音楽/main_BGM.mp3")
    pygame.mixer.music.play(-1)
    ccount = 0

    while True:

        dt = fps_clock.tick(60)
        fps = dt
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
                player.attack = player.attack/5
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

        screen.blit(keyboard_image, (160, 100))
        field.move_player(key, screen, level)
        field.draw_item(screen)
        field.move_sleep(screen, level)
        field.move_bullet(screen)
        screen.blit(background_up, (0, 0))
        screen.blit(background_left, (0, 100))
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

        time_count(time, screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if player.hp >= 100:
            score_save() 
            return gameover(field)

        field.draw_hp(screen)
        if field.item_flag1 == True:
            field.draw_power(screen, time_item1)

        pygame.display.update()


if __name__ == "__main__":
    start()
