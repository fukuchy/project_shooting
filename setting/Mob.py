class Mob:

    def __init__(self, x, y, r, hp, attack, speed, various, name, ):

        self.x = x
        self.y = y
        self.r = r
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.various = various
        self.animation = 0
        self.name = name

    def receive_damege(self, damages):
        self.hp += damages

    def print_mob(self, screen, img):
        screen.blit(img, [self.x, self.y])