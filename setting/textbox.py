import pygame
from .import paramater as para
from .  import player as p

class Button:
    def __init__(self, x, y, w, h, text=''):
       self.rect = pygame.Rect(x, y, w, h)
       self.color = (200,200,200)
       self.text = text
       self.txt_surface = para.FONT.render(text, True, self.color)
       self.active = False
    def update(self):
       width = max(200, self.txt_surface.get_width()+10)
       self.rect.w = width
    def draw(self, screen):
       pygame.draw.rect(screen, self.color, self.rect, 0)
       self.txt_surface = para.FONT.render(self.text, True, (0,0,0))
       screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
    def onClick(self):
        r = self.active
        self.active = False
        return r


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = para.COLOR_INACTIVE
        self.text = text
        self.txt_surface = para.FONT.render(text, True, self.color)
        self.active = False
    def handle_event(self, event):
        r = ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                para.input_flag = False
            else:
                self.active = False
                r = self.text
                p.player.name = r
                para.input_flag = True
                self.text = ""
                self.txt_surface = para.FONT.render(self.text, True, self.color)
            self.color = para.COLOR_ACTIVE if self.active else para.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    r = self.text
                    self.text = ''
                    p.player.name = r
                    para.input_flag = True
                elif event.key == pygame.K_DELETE:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = para.FONT.render(self.text, True, self.color)
        return r
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def name_input_init():
    input_box = InputBox(950, 500, 140, 32)
    button = Button(950, 500, 140, 32, p.player.name)
    return input_box,button

def name_input(input_box,button,event):
    r = input_box.handle_event(event)
    if r != "":
        button.text = r
    button.handle_event(event)
    button.update()
    input_box.update()
    
def draw_textbox(screen,input_box,button):
    button.draw(screen)
    input_box.draw(screen)
    
    if button.onClick():
        button.text = ""
        
