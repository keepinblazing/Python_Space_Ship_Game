
import pygame
from pygame.rect import *
import random

def restart() :
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(star)) :
        recstar[i].y = -1
    for i in range(len(missle)) :
        recmissle[i].y = -1
def eventProcess() :
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    pygame.quit()
                    
                if event.key == pygame.K_LEFT :
                    move.x = -1
                if event.key == pygame.K_RIGHT :
                    move.x = 1
                if event.key == pygame.K_UP :
                    move.y = -1
                if event.key == pygame.K_DOWN :
                    move.y = 1
                if event.key == pygame.K_r :
                    restart()
                if event.key == pygame.K_SPACE :
                    makemissle()


def moveplayer() :
    if not isGameOver :
        recplayer.x += move.x
        recplayer.y += move.y

    if recplayer.x < 0 :
        recplayer.x = 0
    if recplayer.x > SCREEN_WIDTH-recplayer.width :
        recplayer.x = SCREEN_WIDTH-recplayer.width

    if recplayer.y < 0 :
        recplayer.y = 0
    if recplayer.y > SCREEN_HEIGHT-recplayer.height :
        recplayer.y = SCREEN_HEIGHT-recplayer.height
    

    SCREEN.blit(player, recplayer)


def timeDelay500ms():
    global time_delay_500ms
    if time_delay_500ms > 5 :
        time_delay_500ms = 0
        return True

    time_delay_500ms += 1
    return False

def makestar() :
    if timeDelay500ms() :
        idex = random.randint(0,len(star)-1)
        if recstar[idex].y == -1:
            recstar[idex].x = random.randint(0, SCREEN_WIDTH)
            recstar[idex].y = 0

def movestar() :
    makestar()

    for i in range(len(star)) :
        if recstar[i].y == -1 :
            continue

        if not isGameOver:
            recstar[i].y += 1
        if recstar[i].y > SCREEN_HEIGHT :
            recstar[i].y = 0

        SCREEN.blit(star[i], recstar[i])

#####################################################
def CheckCollsionmissle() :
    global score, isGameOver
    if isGameOver :
        return
    for rec in recstar :
        if rec.y == -1:
            continue
        for recM in recmissle :
            if recM.y == -1 :
                continue
            if rec.top < recM.bottom \
                and recM.top < rec.bottom \
                and rec.left < recM.right \
                and recM.left < rec.right :
                rec.y = -1
                recM.y = -1
                score += 10
                break

def makemissle() :
    if isGameOver :
        return
    for i in range(len(missle)) : 
        if recmissle[i].y == -1:
            recmissle[i].x = recplayer.x
            recmissle[i].y = recplayer.y
            break

def movemissle() :
    #makemissle()

    for i in range(len(missle)) :
        if recmissle[i].y == -1 :
            continue

        if not isGameOver:
            recmissle[i].y -= 1
        if recmissle[i].y < 0 :
            recmissle[i].y = -1

        SCREEN.blit(missle[i], recmissle[i])

#####################################################

def CheckCollsion() :
    global score, isGameOver

    if isGameOver :
        return

    for rec in recstar :
        if rec.y == -1:
            continue
        if rec.top < recplayer.bottom \
            and recplayer.top < rec.bottom \
            and rec.left < recplayer.right \
            and recplayer.left < rec.right :
            print('충돌')
            isGameOver = True   
            break 
    score += 1

def blinking() :

    global time_delay_4sec, toggle
    time_delay_4sec += 1
    if time_delay_4sec > 40 :
        time_delay_4sec = 0
        toggle = ~toggle
        

    return toggle


def setText() :
    mFont = pygame.font.SysFont("arial",20, True, False)
    SCREEN.blit(mFont.render(
        f'score : {score}', True, 'green'), (10,10,0,0))

    if isGameOver and blinking() :
        SCREEN.blit(mFont.render(
            'GAME OVER!', True, 'red'), (135,300,0,0))

        SCREEN.blit(mFont.render(
            'PRESS R - RESTART', True, 'red'), (102,320,0,0))

isActive = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0,0,0,0)
time_delay_500ms = 0
time_delay_4sec = 0
toggle = False
score = 0
isGameOver = False



pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Myfirstgame')


player = pygame.image.load('전투기.png')
player = pygame.transform.scale(player, (20,30))
recplayer = player.get_rect()
recplayer.centerx = (SCREEN_WIDTH/2)
recplayer.centery = (SCREEN_HEIGHT/2)

star = [pygame.image.load('운석.png') for i in range(40)]
recstar = [None for i in range(len(star))]
for i in range(len(star)) :
    star[i] = pygame.transform.scale(star[i], (20,20))
    recstar[i] = star[i].get_rect()
    recstar[i].y = -1

missle = [pygame.image.load('미사일.png') for i in range(40)]
recmissle = [None for i in range(len(missle))]
for i in range(len(missle)) :
    missle[i] = pygame.transform.scale(missle[i], (20,20))
    recmissle[i] = missle[i].get_rect()
    recmissle[i].y = -1


clock = pygame.time.Clock()


while isActive:

    SCREEN.fill((0,0,0))

    eventProcess()

    moveplayer()

    movestar()

    movemissle()

    CheckCollsionmissle()

    CheckCollsion()

    setText()

    pygame.display.flip()

    clock.tick(100)