import random
import math
import pygame
from pygame import mixer


# initialzing pygame
pygame.init()

# Screen loading
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# background
bg = pygame.image.load("SpaceA.png")

#bg sound
mixer.music.load('background.wav')
mixer.music.play(-1)

icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("mainShip.png")
plyX = 370
plyY = 480
PosXChange = 0.0

# Alien
alienImg = []
alienX = []
alienY = []
alienXChange = []
alienYChange = []
no_of_aliens = 6

for i in range(no_of_aliens):
    alienImg.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 200))
    alienXChange.append(2.7)
    alienYChange.append(30)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 6
bullet_state = "ready"

# Score

score_val = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("score: " + str(score_val), True, (255,255,255))
    screen.blit(score,(x,y))

#game over text

over_text = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over = over_text.render("GAME OVER" + str(score_val), True, (255,255,255))
    screen.blit(over,(200,250))

def player(x, y):
    screen.blit(playerImg, (int(x), int(y)))


def enemy(x, y, i):
    screen.blit(alienImg[i], (x,y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (int(x + 16), int(y + 10)))


def isCollided(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    # RBG
    screen.fill((0, 0, 25))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed and released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PosXChange = -3
            if event.key == pygame.K_RIGHT:
                PosXChange = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = plyX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                PosXChange = 0.0
            if event.key == pygame.K_RIGHT:
                PosXChange = 0.0

    # player movement restriction
    plyX += PosXChange
    if plyX <= 0:
        plyX = 0
    elif plyX >= 736:
        plyX = 736

    # Enemy movement

    for i in range(no_of_aliens):

        if alienY[i] > 200.000000:
             for j in range(no_of_aliens):
                 alienY = 2000
             game_over_text()
             break


        alienX[i] += alienXChange[i]
        if alienX[i] <= 0:
            alienXChange[i] = 1.5
            alienY[i] += alienYChange[i]
        elif alienX[i] >= 736:
            alienXChange[i] = -1.5
            alienY[i] += alienYChange[i]

        # Collision
        collision = isCollided(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 200)

        enemy(alienX[i], alienY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    player(plyX, plyY)
    show_score(textX,textY)
    pygame.display.update()
