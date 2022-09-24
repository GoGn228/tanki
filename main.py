import pygame
import os
import sys
import random

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()

from load import *


class GameLvl:
    def __init__(self):
        self.lvl = 1

    def update(self):
        sc.fill("black")
        pl_gr.update()
        pl_gr.draw(sc)
        block_group.update()
        block_group.draw(sc)
        enemy_group.update()
        enemy_group.draw(sc)
        pygame.display.update()

    def drawmaps(self, file_name):
        maps = []
        source = "maps lvl/" + str(file_name)
        with open(source, "r") as file:
            for i in range(0, 20):
                maps.append(file.readline().replace("\n", "").split(",")[0:-1])
        pos = [0, 0]
        for i in range(0, len(maps)):
            pos[1] = i * 40
            for j in range(0, len(maps[0])):
                pos[0] = 40 * j
                if maps[i][j] == "1":
                    block = Block(block_image, pos)
                    block_group.add(block)
                if maps[i][j] == "2":
                    enemy = Enemy(enemy_image, pos)
                    enemy_group.add(enemy)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 5
        self.dir = "top"

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.image = pygame.transform.rotate(player_image, 90)
            self.rect.x -= self.speed
            self.dir = "left"
        elif key[pygame.K_d]:
            self.image = pygame.transform.rotate(player_image, -90)
            self.rect.x += self.speed
            self.dir = "right"
        elif key[pygame.K_w]:
            self.image = pygame.transform.rotate(player_image, 0)
            self.rect.y -= self.speed
            self.dir = "top"
        elif key[pygame.K_s]:
            self.image = pygame.transform.rotate(player_image, 180)
            self.rect.y += self.speed
            self.dir = "bottom"


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 1
        self.dir = "top"
        self.timer_move = 0

    def update(self):
        self.timer_move += 1
        if self.timer_move / FPS > 2:
            if random.randint(1, 4) == 1:
                self.dir = "top"
            elif random.randint(1, 4) == 2:
                self.dir = "right"
            elif random.randint(1, 4) == 3:
                self.dir = "bottom"
            elif random.randint(1, 4) == 4:
                self.dir = "left"
                self.image = pygame.transform.rotate(enemy_image, 90)
            self.timer_move = 0
        if self.dir == "top":
            self.image = pygame.transform.rotate(enemy_image, 0)
            self.rect.y -= self.speed
        elif self.dir == "right":
            self.image = pygame.transform.rotate(enemy_image, -90)
            self.rect.x += self.speed
        elif self.dir == "bottom":
            self.image = pygame.transform.rotate(enemy_image, 180)
            self.rect.y += self.speed
        elif self.dir == "left":
            self.image = pygame.transform.rotate(enemy_image, 90)
            self.rect.x -= self.speed
        if pygame.sprite.spritecollide(self, block_group, False):
            self.timer_move = 0
            if self.dir == "top":
                self.dir = "bottom"
            elif self.dir == "right":
                self.dir = "left"
            elif self.dir == "bottom":
                self.dir = "top"
            elif self.dir == "left":
                self.dir = "right"


class Block(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 10

    def update(self):
        if pygame.sprite.spritecollide(self, pl_gr, False):
            if pl.dir == "left":
                pl.rect.left = self.rect.right
            elif pl.dir == "right":
                pl.rect.right = self.rect.left
            elif pl.dir == "top":
                pl.rect.top = self.rect.bottom
            elif pl.dir == "bottom":
                pl.rect.bottom = self.rect.top


pl = Player(player_image, (100, 100))
pl_gr = pygame.sprite.Group()
pl_gr.add(pl)
game_lvl = GameLvl()
block_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
game_lvl.drawmaps("1.txt")
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    game_lvl.update()
    clock.tick(FPS)
