#!/usr/bin/env python3

import numpy as np
from pygamehelper import *
from pygame import *
from pygame.locals import *
import random

FRAME_RATE = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Blob(object):
    VELOCITY = int(FRAME_RATE / 4)
    R = 10
    def __init__(self, x=0, y=0, r=None):
        self.r = r
        self.x = x
        self.y = y
        self.velocity = Blob.VELOCITY
        self.trail = []
        self.curr_rect = None
        self.color_select = 1
        self.levelup_sound = pygame.mixer.Sound("levelup.ogg")

    def reset(self):
        if self.r > 50:
            self.color_select = (self.color_select + 1) % 3
            self.levelup_sound.play()

        self.r = Blob.R
        self.velocity = Blob.VELOCITY

    def draw(self, screen):
        self.curr_rect = pygame.draw.circle(screen, (0,0,0),  (self.x, self.y), self.r)

        self.trail.insert(0, [self.x, self.y])
        if len(self.trail) >= 20:
            self.trail.pop()

        for i, past in enumerate(reversed(self.trail)):
            br = 255 - (i * (255 // 20))
            color = [br, br, br]
            color[self.color_select] = 255

            pygame.draw.circle(screen, color, past, self.r)

    def up(self):
        self.y -= self.velocity
    def down(self):
        self.y += self.velocity
    def left(self):
        self.x -= self.velocity
    def right(self):
        self.x += self.velocity


#myfont = pygame.font.SysFont("monospace", 16)
#scoretext = myfont.render("Score {0}".format(score), 1, (0,0,0))
#screen.blit(scoretext, (5, 10))

class Starter(PygameHelper):
    def __init__(self):
        PygameHelper.__init__(self, fill=(255, 255, 255))

        self.blob = Blob(x=10, y=10, r=10)
        self.down_keys = []
        self.coin_rect = None
        #self.coin_rects = []
        self.coin_color = (255, 255, 0)
        self.coin_size = 20
        self.score = 0
        self.coin_rand()
        self.screen_color = (255, 255, 255)

        pygame.mixer.music.load("arcade.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.2)
        
        self.coin_sound = pygame.mixer.Sound("coin.ogg")

    def screen_rand(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.screen_color = (r, g, b)

    def coin_rand(self):
        coin_rx = [0, self.size[0]]
        coin_ry = [0, self.size[1]]
        self.coin_xy = [random.randint(*coin_rx), random.randint(*coin_ry)]
        self.coin_Rect = Rect(self.coin_xy, (self.coin_size,)*2)


    def update(self):
        ups = {"k", "w", "up"}
        downs = {"j", "s", "down"}
        rights = {"l", "d", "right"}
        lefts = {"a", "h", "left"}
        dk_set = set(self.down_keys)

        if ups.intersection(dk_set):
            self.blob.up()
        if downs.intersection(dk_set):
            self.blob.down()
        if lefts.intersection(dk_set):
            self.blob.left()
        if rights.intersection(dk_set):
            self.blob.right()

        #if "space" in self.down_keys:
        #    self.blob.reset()

        if self.coin_rect is not None and self.blob.curr_rect is not None:
            if (self.blob.curr_rect.colliderect(self.coin_rect)):
                self.coin_sound.play()
                self.coin_rand()
                self.blob.velocity = min(300, int(1.5 * self.blob.velocity))
                self.blob.r = min(400, int(1.5 * self.blob.r))
                if self.blob.r == 400:
                    self.blob.reset()
                    self.screen_rand()
                self.score += 3


    def draw(self):
        self.screen.fill(self.screen_color)
        self.blob.draw(self.screen)
        self.coin_rect = pygame.draw.rect(self.screen, self.coin_color, self.coin_Rect)

        myfont = pygame.font.SysFont("monospace", 30)
        # render text
        label = myfont.render("{}".format(self.score), 1, BLACK)
        self.screen.blit(label, (self.size[0] // 2 -  label.get_width() // 2, 0))


    def keyDown(self, key):
        name = pygame.key.name(key)
        self.down_keys.append(name)

    def keyUp(self, key):
        name = pygame.key.name(key)
        self.down_keys.remove(name)

    def mouseUp(self, button, pos):
        pass

    def mouseMotion(self, buttons, pos, rel):
        pass


if __name__ == "__main__":
    s = Starter()
    s.mainLoop(FRAME_RATE)
