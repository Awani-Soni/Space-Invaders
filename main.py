import pygame
import random
import math
from pygame import mixer

# initialise pygame
pygame.init()

# creating screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load("background.png")

# background sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("player.png")
playerx = 370
playery = 480
playerx_change = 0

# enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png")) 
    enemyx.append(random.randint(0,735))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(2)
    enemyy_change.append(40)

# bullet

# ready: you can't see the bullet on the screen
# fire: the bullet is currently moving

bulletImg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 7
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textx = 10
texty = 10

# game over text
over_font = pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))


def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def iscollision(bulletx,bullety,enemyx,enemyy):
    distance = math.sqrt(math.pow(enemyx-bulletx,2)+math.pow(enemyy-bullety,2))
    if distance < 27:
        return True
    else:
        return False

running = True

# game loop
while running:

    #RGB = red green blue
    screen.fill((0,0,0))
    # background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
            running = False

        # if keystroke is pressed then check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.mp3")
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletx = playerx
                    fire_bullet(bulletx,bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # checking for boundaries of spaceship so it doesn't go out of bounds.            

    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy movement
    for i in range(no_of_enemies):

        #game over

        if enemyy[i] > 440:
            for j in range(no_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = 2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -2
            enemyy[i] += enemyy_change[i]

        # collision
        collision = iscollision(bulletx,bullety,enemyx[i],enemyy[i])
        if collision:
            explosion_sound = mixer.Sound("explosion.mp3")
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0,735)
            enemyy[i] = random.randint(50,150)
        enemy(enemyx[i],enemyy[i],i)


    # bullet movement
        
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    
    if bullet_state == "fire":
        fire_bullet(bulletx,bullety)
        bullety -= bullety_change


    player(playerx,playery)
    show_score(textx,texty)
    
    pygame.display.update()