import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def draw_screen():
    screen.fill(WHITE)
    all_sprites_list.draw(screen)
    pygame.display.flip()


def generate_rand_move_block(num, block_width, block_height, vel=3):

    for i in range(num):
        block = FallingCoin(BLACK, block_width, block_height, vel)

        coin_list.add(block)
        all_sprites_list.add(block)


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.color = color
        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def update_position(self):
        raise NotImplementedError("This function is meant to be implemented in the subclass")


class Player(Block):

    def __init__(self, color, width, height, pos, vel):
        Block.__init__(self, color, width, height)

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

        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.width - self.vel:
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


class FallingCoin(Block):

    def __init__(self, color, width, height, vel):
        Block.__init__(self, color, width, height)

        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = 0
        self.vel = vel

    def update_position(self):
        self.rect.y += self.vel


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
all_sprites_list = pygame.sprite.Group()
coin_list = pygame.sprite.Group()

player = Player(RED, 40, 40, [100, 750], 7)
all_sprites_list.add(player)
score = 0

done = False
while not done:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    generate_rand_move_block(1, 15, 15, 5)

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

pygame.quit()
