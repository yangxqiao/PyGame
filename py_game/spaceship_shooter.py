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


class Block(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()

        self.image = pygame.image.load(image).convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

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
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect(center=self.rect.center)


class Asteroid(Block):

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

        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0 \
           or self.rect.y > SCREEN_HEIGHT or self.rect.y < 0:
            self.kill()


class Bullet(Block):

    def __init__(self, image, player):
        Block.__init__(self, image)
        self.vel = Vector2(0, -5)

        self.rect.x = player.rect.x + player.width / 2
        self.rect.y = player.rect.y
        self.original_image = self.image
        self.image = pygame.transform.rotate(self.original_image, -player.angle)
        self.image = self.image.convert_alpha()

        self.vel.rotate_ip(player.angle)

    def update_position(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        if self.rect.y < -10:
            self.kill()


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
my_font = pygame.font.SysFont("serif", 32)
pygame.display.set_caption("Spaceship Game")
background = pygame.image.load('img/starry_night.jpg')
clock = pygame.time.Clock()


class SpaceshipShooter:

    def __init__(self, player, all_sprites_list, aliens_list, bullet_list):
        self.player = player
        self.all_sprites_list = all_sprites_list
        self.aliens_list = aliens_list
        self.bullet_list = bullet_list
        self.score = 0

    def draw_screen(self):

        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        self.all_sprites_list.draw(screen)

        score_text = my_font.render("Score: {0}".format(self.score), 3, WHITE)
        screen.blit(score_text, (5, 10))

        pygame.display.flip()

    def generate_aliens_every_interval(self, num, last_record_time, interval):

        curr_record_time = pygame.time.get_ticks()
        if curr_record_time - last_record_time >= interval:

            for i in range(num):
                alien = Asteroid("img/asteroid.png", i)
                self.aliens_list.add(alien)
                self.all_sprites_list.add(alien)

            return curr_record_time
        return last_record_time

    def check_hit_update_score(self):

        for bullet in self.bullet_list:

            alien_hit_list = pygame.sprite.spritecollide(bullet, self.aliens_list, True)

            for alien in alien_hit_list:
                expl = ExplosionEffect((alien.rect.x + alien.width/2, alien.rect.y + alien.height/2))
                self.all_sprites_list.add(expl)
                explosion.add(expl)
                self.all_sprites_list.remove(alien)
                self.all_sprites_list.remove(bullet)

                self.score += 1
                print(self.score)

    def update_all_sprites(self):
        player.update_position()

        for bullet in self.bullet_list:
            bullet.update_position()

        for alien in self.aliens_list:
            alien.update_position()

        for expl in explosion:
            expl.update()

    def spaceship_game_loop(self):

        last_record_time = pygame.time.get_ticks()
        interval = 5000

        done = False
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

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
                    elif event.key == pygame.K_SPACE:
                        bullet = Bullet("img/bullet.png", self.player)
                        self.all_sprites_list.add(bullet)
                        self.bullet_list.add(bullet)

            last_record_time = self.generate_aliens_every_interval(9, last_record_time, interval)

            self.check_hit_update_score()

            if self.score > 20:
                quit_game()

            self.update_all_sprites()

            self.draw_screen()

        quit_game()


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def create_button(message, x, y, width, height, inactive_color, active_color):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))

        if click[0] == 1:
            return True

    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    small_text = pygame.font.SysFont("serif", 40)
    text_surf, text_rect = text_objects(message, small_text, WHITE)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)

    return False


class Explosion(pygame.sprite.Sprite):

    def __init__(self, magnitude, exploding_hit_x, exploding_hit_y):
        super().__init__()
        color_choice = [MAROON, Bright_RED, Bright_Yellow, Bright_Orange, GOLD, Orange_Red]

        self.color = color_choice[random.randrange(0, 5)]
        self.exploding_hit_x = exploding_hit_x + random.randrange(-1 * magnitude, magnitude)
        self.exploding_hit_y = exploding_hit_y + random.randrange(-1 * magnitude, magnitude)
        self.radius = random.randrange(0, 5)

        pygame.draw.circle(screen, self.color,
                           (self.exploding_hit_x, self.exploding_hit_y), self.radius)


def generate_explosion(x, y):

    explosion_list = pygame.sprite.Group()
    for i in range(1, 50):

        exploding_circle = Explosion(i, x, y)
        explosion_list.add(exploding_circle)

    return pygame.time.get_ticks()


class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()

        self.EXPLOSION_IMGS = ["explosions/regularExplosion00.png", "explosions/regularExplosion01.png",
                               "explosions/regularExplosion02.png", "explosions/regularExplosion03.png",
                               "explosions/regularExplosion04.png", "explosions/regularExplosion05.png",
                               "explosions/regularExplosion06.png", "explosions/regularExplosion07.png",
                               "explosions/regularExplosion08.png"]

        self.image = pygame.image.load(self.EXPLOSION_IMGS[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 9

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
        if self.frame == len(self.EXPLOSION_IMGS):
            self.kill()
        else:
            self.image = pygame.image.load(self.EXPLOSION_IMGS[self.frame]).convert_alpha()
            self.rect = self.image.get_rect(center=self.rect.center)


def quit_game():
    pygame.quit()
    quit()


def menu():
        old_time = 0
        mouse = pygame.mouse.get_pos()
        explode = False
        while True:

            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    old_time = generate_explosion(mouse[0], mouse[1])
                    explode = True

            large_text = pygame.font.SysFont("serif", 80)
            text_surf, text_rect = text_objects("Spaceship Shooter", large_text, BLACK)
            text_rect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
            screen.blit(text_surf, text_rect)

            button_play = create_button("Go!", 200, 500, 100, 50, GREEN, Bright_Green)
            button_quit = create_button("Quit :(", 400, 500, 100, 50, MAROON, Bright_RED)

            if explode:
                if pygame.time.get_ticks() - old_time > 50:
                    generate_explosion(mouse[0], mouse[1])

                else:
                    explode = False

            pygame.display.update()
            clock.tick(20)

            if button_play or button_quit:
                if button_play:
                    return True
                else:
                    return False


all_sprites_list = pygame.sprite.Group()
aliens_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
explosion = pygame.sprite.Group()

player = Player("img/spaceship2.png", (350, 620))
all_sprites_list.add(player)
space_shooter = SpaceshipShooter(player, all_sprites_list, aliens_list, bullet_list)


play = menu()

if play:
    space_shooter.spaceship_game_loop()
else:
    quit_game()
