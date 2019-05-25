import pygame
from pygame.math import Vector2
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
my_font = pygame.font.SysFont("serif", 32)
pygame.display.set_caption("Spaceship Game")
background = pygame.image.load('img/starry_night.jpg')
clock = pygame.time.Clock()


def draw_screen():
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    all_sprites_list.draw(screen)

    pygame.display.flip()


def generate_enemy_every_interval(num, last_record_time):

    curr_record_time = pygame.time.get_ticks()

    if curr_record_time - last_record_time >= interval:

        for i in range(num):
            enemy = Enemy("img/ET.png", i)
            enemy_list.add(enemy)
            all_sprites_list.add(enemy)

        return curr_record_time

    return last_record_time


class Block(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()

        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update_position(self):
        raise NotImplementedError("This function is meant to be implemented in the subclass")


class Player(Block):

    def __init__(self, image, position):
        Block.__init__(self, image)

        self.rect = self.image.get_rect(center=position)
        self.original_image = self.image
        self.pos = Vector2(position)
        self.direction = Vector2(90, 0)
        self.angle = 0
        self.angle_speed = 0

    def update_position(self):

        if self.angle_speed:

            self.angle += self.angle_speed
            self.direction.rotate_ip(self.angle_speed)
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)


class Enemy(Block):

    def __init__(self, image, side):
        Block.__init__(self, image)
        self.vel = Vector2(3, 3)

        if side % 3 == 0:
            self.rect.x = 0
            self.rect.y = random.randrange(SCREEN_HEIGHT)
            self.vel.rotate_ip(random.randrange(-45, 45))
        elif side % 3 == 1:
            self.rect.x = random.randrange(SCREEN_WIDTH)
            self.rect.y = 0
            self.vel.rotate_ip(random.randrange(0, 90))
        elif side % 3 == 2:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randrange(SCREEN_HEIGHT)
            self.vel.rotate_ip(random.randrange(45, 135))

    def update_position(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]


class Bullet(pygame.sprite.Sprite):

    def __init__(self, color, width, height, vel, player):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.vel = vel

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

    def update_position(self):
        self.rect.y -= self.vel


all_sprites_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()

player = Player("img/spaceship.png", (350, 620))
all_sprites_list.add(player)

last_record_time = pygame.time.get_ticks()
interval = 5000

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.angle_speed = -10
            elif event.key == pygame.K_RIGHT:
                player.angle_speed = 10

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.angle_speed = 0
            elif event.key == pygame.K_RIGHT:
                player.angle_speed = 0

    last_record_time = generate_enemy_every_interval(9, last_record_time)

    all_sprites_list.update()
    player.update_position()

    for enemy in enemy_list:
        if enemy.rect.x > SCREEN_WIDTH or enemy.rect.x < 0 or enemy.rect.y > SCREEN_HEIGHT or enemy.rect.y < 0:
            enemy_list.remove(enemy)
            all_sprites_list.remove(enemy)
        else:
            enemy.update_position()

    draw_screen()

pygame.quit()
