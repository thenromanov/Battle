import os
import sys
import pygame
import csv
import random

pygame.init()

FPS = 60
screenSize = (width, height) = 1200, 400

backgroundColor = (116, 120, 128)
floorColor = (35, 41, 49)

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Battle")
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def loadImage(name, size=None, colorkey=None):
    path = os.path.join('data', name)
    image = pygame.image.load(path)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at(0, 0)
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image


objects = {
    'rock-1': loadImage('Rocks/Rock01.png', size=(90, 46)),
    'rock-2': loadImage('Rocks/Rock02.png', size=(112, 130)),
    'tree-1': loadImage('Trees/Tree01.png', size=(90, 164)),
    'tree-2': loadImage('Trees/Tree02.png', size=(94, 194)),
    'tree-3': loadImage('Trees/Tree03.png', size=(82, 64)),
    'treeBack-1': loadImage('Trees/TreeBack01.png', size=(160, 310)),
    'treeBack-2': loadImage('Trees/TreeBack02.png', size=(94, 194)),
    'treeBack-3': loadImage('Trees/TreeBack03.png', size=(90, 164)),
    'sword': loadImage('Trees/GiantSword_01.png', size=(168, 280)),
    'cloud': loadImage('Clouds/Cloud01.png', size=(266, 92))
}


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(groups)
        self.image = loadImage('Clouds/Cloud01.png', size=(133, 46))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.speed = 1
        self.movement = [self.speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.left > width:
            self.kill()


class Background():
    def __init__(self, name, maxHealth=100):
        self.bg = pygame.Surface((width, height))
        self.bg.fill(backgroundColor)
        self.floor = pygame.Surface((width, 60))
        self.floor.fill(floorColor)
        self.healthbar = pygame.Surface((200, 20))
        self.healthbar.fill(pygame.Color('cyan'))
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render('HP', 1, pygame.Color('cyan'))
        self.kills = 0
        self.text1 = self.font.render('KILLS:', 1, pygame.Color('cyan'))
        filename = 'data/' + name
        file = open(filename, encoding='utf8')
        self.level = list(csv.reader(file, delimiter=';', quotechar='"'))
        self.clouds = pygame.sprite.Group()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()

    def setHealth(self, health):
        self.health = health

    def setKills(self, kills):
        self.kills = kills

    def draw(self):
        if len(self.clouds) < 3 and random.randint(0, 400) == 1:
            Cloud(-300, random.randrange(0, 100), self.clouds)
        self.image.blit(self.bg, (0, 0))
        self.image.blit(self.floor, (0, height - self.floor.get_height()))
        self.clouds.update()
        self.clouds.draw(self.image)
        for object in self.level:
            image = objects[object[0]]
            self.image.blit(image, (int(object[1]), height - self.floor.get_height() - image.get_height()))
        self.healthbar = pygame.Surface((int(self.health / self.maxHealth * 200), 20))
        self.healthbar.fill(pygame.Color('cyan'))
        self.image.blit(self.text, (20, 20))
        self.image.blit(self.healthbar, (70, 20))
        self.image.blit(self.text1, (1030, 20))
        kills = self.font.render(str(self.kills), 1, pygame.Color('cyan'))
        self.image.blit(kills, (1130, 20))
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(groups)
        self.idle = [loadImage('Player/Player_Idle_01.png', size=(178, 152)), loadImage('Player/Player_Idle_02.png', size=(178, 152)),
                     loadImage('Player/Player_Idle_03.png', size=(178, 152)), loadImage('Player/Player_Idle_04.png', size=(178, 152)),
                     loadImage('Player/Player_Idle_05.png', size=(178, 152)), loadImage('Player/Player_Idle_06.png', size=(178, 152)),
                     loadImage('Player/Player_Idle_07.png', size=(178, 152)), loadImage('Player/Player_Idle_08.png', size=(178, 152))]
        self.run = [loadImage('Player/Player_Run_01.png', size=(178, 152)), loadImage('Player/Player_Run_02.png', size=(178, 152)),
                    loadImage('Player/Player_Run_03.png', size=(178, 152)), loadImage('Player/Player_Run_04.png', size=(178, 152)),
                    loadImage('Player/Player_Run_05.png', size=(178, 152)), loadImage('Player/Player_Run_06.png', size=(178, 152)),
                    loadImage('Player/Player_Run_07.png', size=(178, 152)), loadImage('Player/Player_Run_08.png', size=(178, 152))]
        self.attack = [loadImage('Player/Player_Attack_01.png', size=(178, 152)), loadImage('Player/Player_Attack_02.png', size=(178, 152)),
                       loadImage('Player/Player_Attack_03.png', size=(178, 152)), loadImage('Player/Player_Attack_04.png', size=(178, 152)),
                       loadImage('Player/Player_Attack_05.png', size=(178, 152)), loadImage('Player/Player_Attack_06.png', size=(178, 152)),
                       loadImage('Player/Player_Attack_07.png', size=(178, 152)), loadImage('Player/Player_Attack_08.png', size=(178, 152)),
                       loadImage('Player/Player_Attack_09.png', size=(178, 152)), loadImage('Player/Player_Attack_10.png', size=(178, 152)),
                       loadImage('Player/Player_Attack_11.png', size=(178, 152)), loadImage('Player/Player_Attack_12.png', size=(178, 152))]
        self.hit = [loadImage('Player/Player_Hit_01.png', size=(178, 152)), loadImage('Player/Player_Hit_02.png', size=(178, 152)),
                    loadImage('Player/Player_Hit_03.png', size=(178, 152)), loadImage('Player/Player_Hit_04.png', size=(178, 152)),
                    loadImage('Player/Player_Hit_05.png', size=(178, 152)), loadImage('Player/Player_Hit_06.png', size=(178, 152)),
                    loadImage('Player/Player_Hit_07.png', size=(178, 152)), loadImage('Player/Player_Hit_08.png', size=(178, 152)),
                    loadImage('Player/Player_Hit_09.png', size=(178, 152))]
        self.death = [loadImage('Player/Player_Death_01.png', size=(178, 152)), loadImage('Player/Player_Death_02.png', size=(178, 152)),
                      loadImage('Player/Player_Death_03.png', size=(178, 152)), loadImage('Player/Player_Death_04.png', size=(178, 152)),
                      loadImage('Player/Player_Death_05.png', size=(178, 152)), loadImage('Player/Player_Death_06.png', size=(178, 152)),
                      loadImage('Player/Player_Death_07.png', size=(178, 152)), loadImage('Player/Player_Death_08.png', size=(178, 152)),
                      loadImage('Player/Player_Death_09.png', size=(178, 152)), loadImage('Player/Player_Death_10.png', size=(178, 152)),
                      loadImage('Player/Player_Death_11.png', size=(178, 152)), loadImage('Player/Player_Death_12.png', size=(178, 152)),
                      loadImage('Player/Player_Death_13.png', size=(178, 152)), loadImage('Player/Player_Death_14.png', size=(178, 152)),
                      loadImage('Player/Player_Death_15.png', size=(178, 152)), loadImage('Player/Player_Death_16.png', size=(178, 152)),
                      loadImage('Player/Player_Death_17.png', size=(178, 152))]
        self.image = self.idle[0]
        self.rect = self.image.get_rect().move((x, y))
        self.counter = 0
        self.index = 0
        self.direction = 0
        self.lastDirection = 1
        self.speed = 3
        self.isAttacking = False
        self.health = 100
        self.isHitted = False
        self.isDead = False
        self.kills = 0

    def move(self, direction):
        self.direction = direction

    def attacking(self):
        self.isAttacking = True
        self.index = 0

    def hitted(self):
        self.isHitted = True
        self.index = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.counter += 1
        self.movement = [0, 0]
        if self.isDead:
            if self.counter % 3 == 0:
                self.index += 1
            if self.index < len(self.death):
                self.image = pygame.transform.flip(self.death[self.index], self.lastDirection < 0, False)
            else:
                self.kill()
        else:
            if self.isHitted:
                if self.counter % 3 == 0:
                    self.index += 1
                if self.index < len(self.hit):
                    self.image = pygame.transform.flip(self.hit[self.index], self.lastDirection < 0, False)
                else:
                    self.isHitted = False
                    self.health -= 10
                    self.index = 0
            else:
                self.movement = [self.direction * self.speed, 0]
                if self.isAttacking:
                    if self.counter % 3 == 0:
                        self.index += 1
                    if self.index < len(self.attack):
                        self.movement = [0, 0]
                        self.image = pygame.transform.flip(self.attack[self.index], self.lastDirection < 0, False)
                        for enemy in enemies:
                            if pygame.sprite.collide_mask(self, enemy) and self.index == 7:
                                enemy.hitted()
                    else:
                        self.isAttacking = False
                        self.index = 0
                elif self.direction == 0:
                    if self.counter % 3 == 0:
                        self.index = (self.index + 1) % len(self.idle)
                    self.image = pygame.transform.flip(self.idle[self.index], self.lastDirection < 0, False)
                else:
                    if self.counter % 3 == 0:
                        self.index = (self.index + 1) % len(self.run)
                    if self.direction < 0 and self.lastDirection > 0:
                        self.rect = self.rect.move(-30, 0)
                    elif self.direction > 0 and self.lastDirection < 0:
                        self.rect = self.rect.move(30, 0)
                    self.image = pygame.transform.flip(self.run[self.index], self.direction < 0, False)
                    self.lastDirection = self.direction
        if self.health <= 0:
            self.isDead = True
        self.rect = self.rect.move(self.movement)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, side, *groups):
        super().__init__(groups)
        self.run = [loadImage('Enemy/Enemy_Run_01.png', size=(156, 98)), loadImage('Enemy/Enemy_Run_02.png', size=(156, 98)),
                    loadImage('Enemy/Enemy_Run_03.png', size=(156, 98)), loadImage('Enemy/Enemy_Run_04.png', size=(156, 98)),
                    loadImage('Enemy/Enemy_Run_05.png', size=(156, 98)), loadImage('Enemy/Enemy_Run_06.png', size=(156, 98)),
                    loadImage('Enemy/Enemy_Run_07.png', size=(156, 98)), loadImage('Enemy/Enemy_Run_08.png', size=(156, 98))]
        self.attack = [loadImage('Enemy/Enemy_Attack_01.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_02.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_03.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_04.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_05.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_06.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_07.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_08.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_09.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_10.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_11.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_12.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_13.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_14.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_15.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_16.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_17.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_18.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_19.png', size=(156, 98)), loadImage('Enemy/Enemy_Attack_20.png', size=(156, 98)),
                       loadImage('Enemy/Enemy_Attack_21.png', size=(156, 98))]
        self.hit = [loadImage('Enemy/Enemy_Hit_01.png', size=(156, 98)), loadImage('Enemy/Enemy_Hit_02.png', size=(156, 98)),
                    loadImage('Enemy/Enemy_Hit_03.png', size=(156, 98)), loadImage('Enemy/Enemy_Hit_04.png', size=(156, 98)),
                    loadImage('Enemy/Enemy_Hit_05.png', size=(156, 98)), loadImage('Enemy/Enemy_Hit_06.png', size=(156, 98)),
                    loadImage('Enemy/Enemy_Hit_07.png', size=(156, 98)), loadImage('Enemy/Enemy_Hit_08.png', size=(156, 98)),
                    loadImage('Enemy/Enemy_Hit_09.png', size=(156, 98))]
        self.image = self.run[0]
        self.rect = self.image.get_rect()
        if side == -1:
            self.rect = self.rect.move(-100, 250)
        elif side == 1:
            self.rect = self.rect.move(1300, 246)
        self.counter = 0
        self.index = 0
        self.direction = -side
        self.lastDirection = -side
        self.speed = random.randint(1, 3)
        self.health = 30
        self.isAttacking = False
        self.isHitted = False
        self.delay = 50

    def draw(self):
        screen.blit(self.image, self.rect)

    def hitted(self):
        self.isHitted = True
        self.index = 0

    def update(self):
        self.counter += 1
        self.movement = [0, 0]
        if self.isHitted:
            if self.counter % 3 == 0:
                self.index += 1
            if self.index < len(self.hit):
                self.image = pygame.transform.flip(self.hit[self.index], self.lastDirection < 0, False)
            else:
                self.isHitted = False
                self.index = 0
                self.health -= 10
        else:
            if pygame.sprite.collide_mask(self, player) and self.isAttacking is False and self.delay <= 0:
                self.index = 0
                self.isAttacking = True
            if self.isAttacking:
                if self.counter % 3 == 0:
                    self.index += 1
                if self.index < len(self.attack):
                    self.image = pygame.transform.flip(self.attack[self.index], self.lastDirection < 0, False)
                    if self.index == 13 and pygame.sprite.collide_mask(self, player):
                        player.hitted()
                else:
                    self.isAttacking = False
                    self.index = 0
                    self.delay = 50
            else:
                self.movement = [self.speed * self.direction, 0]
                if self.counter % 3 == 0:
                    self.index = (self.index + 1) % len(self.run)
                if player.rect[0] + 18 > self.rect[0]:
                    self.direction = 1
                else:
                    self.direction = -1
                self.image = pygame.transform.flip(self.run[self.index], self.direction < 0, False)
                self.lastDirection = self.direction
        if self.health <= 0:
            self.kill()
            player.kills += 1
        self.delay -= 1
        self.rect = self.rect.move(self.movement)


background = Background('level1.csv')
players = pygame.sprite.Group()
player = Player(100, 214, players)
enemies = pygame.sprite.Group()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.attacking()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1)
    elif keys[pygame.K_RIGHT]:
        player.move(1)
    else:
        player.move(0)
    background.setHealth(player.health)
    background.setKills(player.kills)
    background.draw()
    players.update()
    enemies.update()
    if len(enemies) < 4 and random.randrange(0, 200) == 10:
        Enemy(random.choice([-1, 1]), enemies)
    players.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()
