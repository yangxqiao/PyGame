import pygame
from pygame.math import Vector2
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
Bright_RED = (255, 0, 0)
Bright_Green = (0, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
MAROON = (128, 0, 0)
Bright_Yellow = (255, 255, 0)
Bright_Orange = (255, 165, 0)
Orange_Red = (255, 69, 0)
GOLD = (255, 215, 0)

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
my_font = pygame.font.SysFont("serif", 32)
pygame.display.set_caption("Spaceship Game")
background = pygame.image.load('img/starry_night.jpg')
clock = pygame.time.Clock()


def draw_screen(score):

    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    all_sprites_list.draw(screen)
    score_text = my_font.render("Score: {0}".format(score), 3, WHITE)
    screen.blit(score_text, (5, 10))
    pygame.display.flip()


def generate_enemy_every_interval(num, last_record_time, interval):

    curr_record_time = pygame.time.get_ticks()
    if curr_record_time - last_record_time >= interval:

        for i in range(num):
            enemy = Enemy("img/ET.png", i)
            enemy_list.add(enemy)
            all_sprites_list.add(enemy)

        return curr_record_time
    return last_record_time


def check_hit_update_score(score):

    for bullet in bullet_list:

        block_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

        for _ in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    return score


def update_all_sprites(player):

    all_sprites_list.update()
    player.update_position()

    for bullet in bullet_list:
        bullet.update_position()

    for enemy in enemy_list:
        if enemy.rect.x > SCREEN_WIDTH or enemy.rect.x < 0 or enemy.rect.y > SCREEN_HEIGHT or enemy.rect.y < 0:
            enemy_list.remove(enemy)
            all_sprites_list.remove(enemy)
        else:
            enemy.update_position()


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def create_button(message, x, y, width, height, inactive_color, active_color, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))

        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    small_text = pygame.font.SysFont("serif", 40)
    text_surf, text_rect = text_objects(message, small_text, WHITE)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)


def explosion(x, y):

    explode = True
    while explode:

        color_choice = [MAROON, Bright_RED, Bright_Yellow, Bright_Orange, GOLD, Orange_Red]

        magnitude = 1
        while magnitude < 50:

            exploding_hit_x = x + random.randrange(-1 * magnitude, magnitude)
            exploding_hit_y = y + random.randrange(-1 * magnitude, magnitude)

            pygame.draw.circle(screen, color_choice[random.randrange(0, 5)],
                               (exploding_hit_x, exploding_hit_y), random.randrange(0, 5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)

        explode = False


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

    def __init__(self, color, width, height, player):
        super().__init__()
        self.vel = Vector2(0, -3)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = player.rect.x + 30
        self.rect.y = player.rect.y
        self.vel.rotate_ip(player.angle)

    def update_position(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]


def quit_game():
    pygame.quit()
    quit()


def game_start():
        intro = True
        while intro:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    explosion(mouse[0], mouse[1])

            large_text = pygame.font.SysFont("serif", 80)
            text_surf, text_rect = text_objects("Spaceship Shooter", large_text, BLACK)
            text_rect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
            screen.blit(text_surf, text_rect)

            create_button("Go!", 200, 500, 100, 50, GREEN, Bright_Green, game_loop)
            create_button("Quit :(", 400, 500, 100, 50, MAROON, Bright_RED, quit_game)

            pygame.display.update()
            clock.tick(20)


def game_loop():

    player = Player("img/spaceship.png", (350, 620))
    all_sprites_list.add(player)

    last_record_time = pygame.time.get_ticks()
    interval = 5000
    score = 0

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(WHITE, 4, 10, player)
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

                # mouse = pygame.mouse.get_pos()
                # explosion(mouse[0], mouse[1])

        last_record_time = generate_enemy_every_interval(9, last_record_time, interval)

        score = check_hit_update_score(score)

        update_all_sprites(player)

        draw_screen(score)

    pygame.quit()


all_sprites_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

game_start()
