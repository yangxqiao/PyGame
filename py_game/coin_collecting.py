import pygame
import random
import sys

pygame.init()
my_font = pygame.font.SysFont("serif", 32)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def draw_screen():
    screen.fill(WHITE)
    all_sprites_list.draw(screen)

    score_text = my_font.render("Score: {0}".format(score), 3, (0,0,0))
    screen.blit(score_text, (5, 10))

    pygame.display.flip()


def generate_rand_move_block(num):

    for i in range(num):
        block = FallingCoin()

        coin_list.add(block)
        all_sprites_list.add(block)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, vel):
        super().__init__()

        self.image = pygame.image.load("img/basket.jpg").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.rect = self.image.get_rect()

        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vel = vel

        self.jump_count = 10
        self.not_jump = True

    def update_position(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > self.vel:
            self.rect.x -= self.vel

        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width - self.vel:
            self.rect.x += self.vel

        if self.not_jump:

            if keys[pygame.K_SPACE]:
                self.not_jump = False

        else:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) / 2 * neg
                self.rect.x += 3
                self.jump_count -= 1
            else:
                self.not_jump = True
                self.jump_count = 10


class FallingCoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("img/coin.jpg").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = 0
        self.vel = random.randrange(4, 5)

    def update_position(self):
        self.rect.y += self.vel


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
all_sprites_list = pygame.sprite.Group()
coin_list = pygame.sprite.Group()

player = Player([100, 600], 7)
all_sprites_list.add(player)
score = 0

while True:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    generate_rand_move_block(1)

    player.update_position()
    for coin in coin_list:
        coin.update_position()
        if coin.rect.y > SCREEN_HEIGHT - 10:
            coin_list.remove(coin)
            all_sprites_list.remove(coin)

    blocks_hit_list = pygame.sprite.spritecollide(player, coin_list, True)

    for block in blocks_hit_list:
        score += 1
        print("Your scores: %s." % score)

    draw_screen()
