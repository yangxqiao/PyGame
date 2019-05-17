import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def draw_screen():

    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    screen.fill(WHITE)


def generate_rand_move_block(num):

    for i in range(num):
        block = BlockMoveRandom(BLACK, block_width, block_height)

        block_list.add(block)
        all_sprites_list.add(block)


def check_collide(player, blocks):

    pos = pygame.mouse.get_pos()

    if 0 <= pos[0] <= screen_width - block_width:
        player.rect.x = pos[0]
    if 0 <= pos[1] <= screen_height - block_height:
        player.rect.y = pos[1]

    return pygame.sprite.spritecollide(player, blocks, True)


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class BlockMoveRandom(Block):

    def __init__(self, color, width, height):
        Block.__init__(self, color, width, height)

        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(screen_height)
        self.speed = pygame.math.Vector2(5, 0).rotate(random.randrange(360))

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.x < 0 or self.rect.right > screen_width:
            self.speed[0] *= -1
        if self.rect.y < 0 or self.rect.bottom > screen_height:
            self.speed[1] *= -1


pygame.init()

screen_width = 700
screen_height = 400
block_width = 20
block_height = 15


screen = pygame.display.set_mode((screen_width, screen_height))

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

generate_rand_move_block(20)
player = Block(RED, block_width, block_height)
all_sprites_list.add(player)

done = False
clock = pygame.time.Clock()
score = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    check_collide(player, block_list)

    blocks_hit_list = check_collide(player, block_list)

    for block in blocks_hit_list:
        score += 1
        print("Your scores: %s." % score)

    block_list.update()
    draw_screen()

pygame.quit()
