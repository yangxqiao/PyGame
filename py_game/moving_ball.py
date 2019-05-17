import sys
import pygame
pygame.init()

size = width, height = 900, 700
speed = [4, 4]
white = (245, 255, 250)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Moving ball")

ball = pygame.image.load("img/intro_ball.jpg")
ball_rect = ball.get_rect()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            if ball_rect.collidepoint(pos):
                if speed != [0, 0]:
                    speed = [0, 0]
                else:
                    speed = [4, 4]

    ball_rect = ball_rect.move(speed)
    if ball_rect.left < 0 or ball_rect.right > width:
        speed[0] = -speed[0]

    if ball_rect.top < 0 or ball_rect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(white)
    screen.blit(ball, ball_rect)
    pygame.display.update()
