import pygame
from pygame.locals import *
from sys import exit


pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Pygame Rotation Demo")

player = pygame.image.load('Game/standing.png').convert_alpha()

clock = pygame.time.Clock()
player_pos = pygame.math.Vector2(300, 250)

player_rotation = 0.
player_rotation_speed = 360.  # 360 degrees per second

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    rotation_direction = 0.

    if pressed_keys[K_LEFT]:
        rotation_direction = -1.0
    if pressed_keys[K_RIGHT]:
        rotation_direction = +1.0

    screen.fill((255, 255, 255))

    rotated_player = pygame.transform.rotate(player, player_rotation)  # Return the rotated_player surface object
    w, h = rotated_player.get_size()
    player_draw_pos = pygame.math.Vector2(player_pos.x - w / 2, player_pos.y - h / 2)
    screen.blit(rotated_player, player_draw_pos)

    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0

    player_rotation += rotation_direction * player_rotation_speed * time_passed_seconds

    pygame.display.update()