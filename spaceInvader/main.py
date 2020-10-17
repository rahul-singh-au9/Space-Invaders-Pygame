import pygame
import random
import math
from pygame import mixer


#initialize the pygame
pygame.init()

# Background
Background = pygame.image.load("background.png")

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#create the screen 
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)


#Player
playerimg=pygame.image.load('space-invaders.png')
playerX=370
playerY=480
playerx_change=0

#Enemy
Enemyimg=[]
EnemyX=[]
EnemyY=[]
Enemyx_change=[]
Enemyy_change=[]

num_of_enemies= 5
for i in range (num_of_enemies):
    Enemyimg.append(pygame.image.load('enemy.png'))
    EnemyX.append(random.randint(0,734))
    EnemyY.append(random.randint(50,150))
    Enemyx_change.append(4)
    Enemyy_change.append(40)

#bullet

# Ready- you can't see the bullet on the screen
# Fire- the bullet is currently moving
bulletimg=pygame.image.load('bullet.png')
bulletX= 0
bulletY=480
bulletx_change=0
bullety_change=10
bullet_state="ready"

# Score
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

def show_score(x,y):
    score= font.render("Score:"+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

# Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text= over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text ,(200,250))


# player fns
def player(x,y):
    screen.blit(playerimg,(x,y))

# Enemy fns
def Enemy(x,y,i):
    screen.blit(Enemyimg[i], (x,y))

# Bullet fns
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16, y+10))

def iscollision(EnemyX,EnemyY,bulletX,bulletY):
    distance= math.sqrt((math.pow(EnemyX-bulletX,2))+(math.pow(EnemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running :
    # RGB red ,green, blue
    screen.fill((0,0,0))

    # background image
    screen.blit(Background, (0,0))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is press check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change=-5
            if event.key == pygame.K_RIGHT:
                playerx_change= 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerx_change=0

    # checking for boundaries so it does'nt go out of the bounds
    playerX += playerx_change

    if playerX <=0:
        playerX =0
    elif playerX>=736:
        playerX=736

    # checking enemy's movement
    for i in range (num_of_enemies):

        # Game over

        if EnemyY[i] > 440:
            for j in range (num_of_enemies):
                EnemyY[j]=2000
            game_over_text()
            break

        EnemyX[i] += Enemyx_change[i]

        if EnemyX[i] <=0:
            Enemyx_change[i] = 4
            EnemyY[i] += Enemyy_change[i]
        elif EnemyX[i]>=736:
            Enemyx_change[i] = -4
            EnemyY[i] += Enemyy_change[i]

        # Collision
        collision = iscollision(EnemyX[i],EnemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+=5

            EnemyX[i]=random.randint(0,734)
            EnemyY[i]=random.randint(50,150)

        Enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bullety_change


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()