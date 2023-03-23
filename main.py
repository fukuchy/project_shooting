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

    print(p.player.name)
    
    while True:

        dt = para.fps_clock.tick(60)
        para.fps = dt
        para.count += dt
        para.ccount += dt
        para.field.remove_bullet()

        if para.field.bullet_flag == True:
            para.b_count += dt
            if para.field.item_flag2 == True:
                if para.b_count >= 200:
                    para.field.bullet_flag = False
                    para.b_count = para.b_count % 200
            else:
                if para.b_count >= 750:
                    para.field.bullet_flag = False
                    para.b_count = para.b_count % 750
        if para.field.item_flag1 != False:
            para.time_item1 += dt
            if para.time_item1 >= 10000:
                p.player.attack = p.player.attack/5
                para.field.item_flag1 = False
                para.time_item1 = para.time_item1 % 10000
        if para.field.item_flag2 != False:
            para.time_item2 += dt
            if para.time_item2 >= 10000:
                para.field.item_flag2 = False
                para.time_item2 = para.time_item2 % 15000

        key = pygame.key.get_pressed()
        if key[K_ESCAPE] == 1 or key[QUIT] == 1:
            pygame.quit()
            sys.exit()

        para.screen.blit(pngs.keyboard_image, (160, 100))
        para.field.move_player(key, para.screen, para.level)
        para.field.draw_item(para.screen)
        para.field.move_sleep(para.screen, para.level)
        para.field.move_bullet(para.screen)
        para.screen.blit(pngs.background_up, (0, 0))
        para.screen.blit(pngs.background_left, (0, 100))
        para.field.point_print(para.screen)
        font = "misaki_gothic.ttf"
        font1 = pygame.font.Font(font, 40)
        text1 = font1.render("ねむけゲージ", True, (0, 0, 0))
        para.screen.blit(text1, (1015, 8))

        if para.count >= 1000:
            para.time += 1
            para.count = para.count % 1000

        if para.ccount >= 2000:
            para.ccount = para.ccount % 2000
            para.field.append_sleep()
        if para.time % 90 == 0 and para.time != 0 and bossflag:
            para.field.append_boss()
            bossflag = False
        if para.time % 91 == 0 and para.time != 0:
            bossflag = True

        if para.item_flag == False:
            if para.time % 30 == 0 and para.time != 0:
                para.field.append_item()
                para.item_flag = True
        else:
            if para.time % 31 == 0:
                para.item_flag = False

        f.time_count(para.time, para.screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if p.player.hp >= 100:
            score.score_save() 
            return f.gameover(para.field)

        para.field.draw_hp(para.screen)
        if para.field.item_flag1 == True:
            para.field.draw_power(para.screen, para.time_item1)

        pygame.display.update()

if __name__ == "__main__":
    main()
