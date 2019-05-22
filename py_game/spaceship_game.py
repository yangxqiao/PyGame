import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
my_font = pygame.font.SysFont("serif", 32)
pygame.display.set_caption("Spaceship Game")


def draw_screen():
    screen.fill(WHITE)
    all_sprites_list.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), (player.rect.x, player.rect.y - 20, 50, 8))
    pygame.draw.rect(screen, (0, 128, 0), (player.rect.x, player.rect.y - 20, 50 - (5 * (10 - player.health)), 8))
    score_text = my_font.render("Score: {0}".format(score), 3, (0, 0, 0))
    screen.blit(score_text, (5, 10))
    pygame.display.flip()


def generate_enemy(num):

    for i in range(num):

        enemy = Enemy(BLUE, enemy_width, enemy_height)
        if i % 3 == 0:
            enemy.rect.x = 0
            enemy.rect.y = random.randrange(SCREEN_HEIGHT)
        elif i % 3 == 1:
            enemy.rect.x = random.randrange(SCREEN_WIDTH)
            enemy.rect.y = 0
        elif i % 3 == 2:
            enemy.rect.x = SCREEN_WIDTH
            enemy.rect.y = random.randrange(SCREEN_HEIGHT)

        enemy_list.add(enemy)
        all_sprites_list.add(enemy)


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.color = color
        self.width = width
        self.height = height

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update_position(self):
        raise NotImplementedError("This function is meant to be implemented in the subclass")


class Player(Block):

    def __init__(self, color, width, height, vel, pos):
        Block.__init__(self, color, width, height)
        self.vel = vel
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.health = 10
        self.visible = True

    def update_position(self):
            self.collide()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and self.rect.x > self.vel:
                self.rect.x -= self.vel

            if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.width - self.vel:
                self.rect.x += self.vel

            if keys[pygame.K_UP] and self.rect.y > self.vel:
                self.rect.y -= self.vel

            if keys[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - self.height - self.vel:
                self.rect.y += self.vel

    def collide(self):
        blocks_hit_list = pygame.sprite.spritecollide(self, enemy_list, True)

        for _ in blocks_hit_list:
            if self.health > 0:
                self.health -= 1
            else:
                self.visible = False
            print('hit')


class Enemy(Block):

    def __init__(self, color, width, height):
        Block.__init__(self, color, width, height)
        self.vel = pygame.math.Vector2(2, 3).rotate(random.randrange(360))

    def update_position(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]


class Bullet(Block):

    def __init__(self, color, width, height, vel, player):
        Block.__init__(self, color, width, height)
        self.vel = vel
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

    def update_position(self):
        self.rect.y -= self.vel


all_sprites_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

bullet_width = 4
bullet_height = 10
enemy_width = 20
enemy_height = 15
player_width = 20
player_height = 15
player_vel = 5
enemy_vel = 4
bullet_vel = 3

player = Player(RED, player_width, player_height, player_vel, [0, 370])
all_sprites_list.add(player)

clock = pygame.time.Clock()

score = 0

time_loop = 0
done = False
while not done:
    time_loop += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(BLACK, bullet_width, bullet_height, bullet_vel, player)

            all_sprites_list.add(bullet)
            bullet_list.add(bullet)

        elif player.visible is False:
            done = True

    if time_loop == 20:
        generate_enemy(3)
        time_loop = 0

    all_sprites_list.update()

    for bullet in bullet_list:

        block_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    player.update_position()
    for bullet in bullet_list:
        bullet.update_position()
    for enemy in enemy_list:
        if enemy.rect.x > SCREEN_WIDTH or enemy.rect.x < 0 or enemy.rect.y > SCREEN_HEIGHT or enemy.rect.y < 0:
            enemy_list.remove(enemy)
            all_sprites_list.remove(enemy)
        else:
            enemy.update_position()

    draw_screen()
    clock.tick(60)

pygame.quit()
