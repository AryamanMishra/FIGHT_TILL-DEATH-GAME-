'''
GAME - FIGHT_TILL_DEATH
DEVELOPER - ARYAMAN MISHRA
TESTERS - MITUL GARG, SANIDHYA MAHAJAN, PRIYANKA JAIN
LANGUAGE - PYTHON
OPEN SOURCE

'''
# Necessary Header files and their sub-headers
import pygame
import math
import random
from pygame import mixer
from pygame.constants import KEYDOWN, KEYUP, K_DOWN, K_UP

# Initialising Pygame
pygame.init()

# Creating Pygame Display Screen
screen = pygame.display.set_mode((800,600))

# Setting title
pygame.display.set_caption("FIGHT_TILL_DEATH")

# Setting title image icon
icon = pygame.image.load("game-console.png")
pygame.display.set_icon(icon)

# Setting bg-image
bgimage = pygame.image.load("bgimage.png")

# Player image and fields
playerimage = pygame.image.load("athlete.png")
playerX = 400
playerY = 550
playerX_change = 0
playerY_change = 0

# Player method
def player(a,b):
    screen.blit(playerimage,(a,b))

# Enemy image and fields
no_of_enemies = 6
enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for it in range(no_of_enemies):
    enemyimage.append(pygame.image.load("shredder.png"))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(0.3)
    enemyY_change.append(50)

# Bullet image and fields
bulletimage_ver = pygame.image.load("bullet_ver.png")
bulletX = playerX
bulletY = 550
bullet_state_ver = "ready"
# ready - stationary bomb
# fired - moving bomb

# Bomb image and fields
bombimage_ver = pygame.image.load("bomb.png")
bombX = playerX
bombY = 550
bomb_state_ver = "ready" 
# ready - stationary bullet
# fired - moving bullet

# Enemy method
def enemy(a,b,i):
    screen.blit(enemyimage[i],(a,b))

# Vertical Bullet method
def fire_bullet_ver(a,b):
    global bullet_state_ver
    bullet_state_ver = "fired"
    screen.blit(bulletimage_ver,(a,b))
    
# Vertical Bomb method
def fire_bomb_ver(a,b):
    global bomb_state_ver
    bomb_state_ver = "fired"
    screen.blit(bombimage_ver,(a,b))

# Method to give distance between 2 points
def distance(a,b,c,d):
    return math.sqrt(math.pow((c-a),2) + math.pow((d-b),2))

# Checking if enemy is colliding with bullet
def checkCollisionBl(a,b,c,d):
    dist = distance(a,b,c,d)
    if dist <= 25:
        return True
    return False

# Checking if enemy is colliding with bomb
def checkCollisionBb(a,b,c,d):
    dist = distance(a,b,c,d)
    if dist <= 30:
        return True
    return False

# Resets the bullet after shooting to shoot multiple bullets
def resetbullet():
    bulletY = 550
    bullet_state_ver = "ready"

# Resets the bomb after shooting to shoot multiple bombs
def resetbomb():
    bombY = 550
    bomb_state_ver = "ready"

# Score fields
score_value = 0
font = pygame.font.Font('heavycopper.otf',30)
fontX = 10
fontY = 10

# Score Method
def display_score(a,b):
    score = font.render("YOUR SCORE: "+  str(score_value),True,(0,0,0))
    screen.blit(score,(a,b))

# Game over fields
game_over_font = pygame.font.Font("heavycopper.otf",60)

# Game_over method 
def game_over_message():
    game_over_f = game_over_font.render("GAME OVER",True,(0,0,0))
    screen.blit(game_over_f,(180,250))

# Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# The most imp variable in the whole code
check = True

# Game Loop
while check:

    # Using (R,G,B) to fill bg color
    screen.fill((0,0,0)) # Presently set to black

    # Adding bg-image
    screen.blit(bgimage,(0,0))

    # Checking events taking place
    for event in pygame.event.get():

        # Checks if event is of quitting
        if event.type == pygame.QUIT:
            check = False
    
        # Checks if event is pressing any key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerX_change = -0.3

            if event.key == pygame.K_SPACE:
                # Checking if bullet is not already in the screen
                if bullet_state_ver == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet_ver(bulletX,bulletY)

            if event.key == pygame.K_LSHIFT:
                # Checking if bomb is not already in the screen
                if bomb_state_ver == "ready":
                    bomb_sound = mixer.Sound("Bomb+3.wav")
                    bomb_sound.play()
                    bombX = playerX
                    fire_bomb_ver(bombX,playerY)
                
        # Checks if event is releasing any key
        if event.type == pygame.KEYUP:
            playerX_change = 0
            playerY_change = 0

    # Updating position after the events 
    playerX += playerX_change
    playerY += playerY_change

    # Boundary restricting
    # The image size is 32px
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768
    if playerY <= 0:
        playerY = 0
    elif playerY >= 568:
        playerY = 568

    # Enemy movements control
    for it in range(no_of_enemies):

        # Game Over algo
        if enemyY[it] > 350:
            for jt in range(no_of_enemies):
                enemyY[jt] = 1000
            game_over_message()
            game_over_sound = mixer.Sound("Recording.wav")
            game_over_sound.play()
            break

        # Enemy Movements
        enemyX[it] += enemyX_change[it]
        if enemyX[it] <= 0:
            enemyX_change[it] = 0.26
            enemyY[it] += enemyY_change[it] # The enemy moves down each time after hitting the boundaries
        elif enemyX[it] >= 768:
            enemyX_change[it] = -0.26
            enemyY[it] += enemyY_change[it] # The enemy moves down each time after hitting the boundaries   

        # Checking Bullet Collision occurence
        checkingBlcol = checkCollisionBl(enemyX[it],enemyY[it],bulletX,bulletY)
        if checkingBlcol:
            bullet_collission = mixer.Sound("explosion.wav")
            bullet_collission.play()
            resetbullet()
            score_value += 1
            enemyX[it] = random.randint(0,800)
            enemyY[it] = random.randint(50,100) 

        # Checking Bomb Collision occurence
        checkingBbcol = checkCollisionBb(enemyX[it],enemyY[it],bombX,bombY)
        if checkingBbcol:
            bullet_collission = mixer.Sound("explosion.wav")
            bullet_collission.play()
            resetbomb()
            score_value += 1
            enemyX[it] = random.randint(0,800)
            enemyY[it] = random.randint(50,100) 
        
        # Calling enemy method
        enemy(enemyX[it],enemyY[it],it)

    # For firing multiple bullets and bombs
    if bulletY <= 32:
        bulletY = playerY
        bullet_state_ver = "ready"
    if bombY <= 32:
        bombY = playerY
        bomb_state_ver = "ready"
    
    # Firing bullets and bombs
    if bullet_state_ver == "fired":
        fire_bullet_ver(bulletX + 5,bulletY - 25)
        bulletY -= 0.3
    if bomb_state_ver == "fired":
        fire_bomb_ver(bombX + 2,bombY - 25)
        bombY -= 0.3

    # Calling player method
    player(playerX,playerY)

    # Displaying Score
    display_score(fontX,fontY)

    # Updating game after each iteration
    pygame.display.update()

'''
END OF THE PROGRAM
THANKS FOR VISITING
GITHUB-ID - modest_aryaman09

'''
