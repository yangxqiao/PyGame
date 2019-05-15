import pygame

SCREENWIDTH = 852
SCREENHEIGHT = 480
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)

win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Jumping rectangle")

bg = pygame.image.load('img/bg.jpg')

x = 0
y = 400
width = 64
height = 64
vel = 5

isJump = False
jumpCount = 10


def redraw_game_window():

    win.fill(WHITE)
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, GRAY, (x, y, width, height))
    pygame.display.update()


run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel

    if keys[pygame.K_RIGHT] and x < SCREENWIDTH - width - vel:
        x += vel

    if not isJump:

        if keys[pygame.K_UP] and y > vel:
            y -= vel

        if keys[pygame.K_DOWN] and y < SCREENHEIGHT - height - vel:
            y += vel

        if keys[pygame.K_SPACE]:
            isJump = True

    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) / 2 * neg
            x += 3
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    redraw_game_window()


pygame.quit()
