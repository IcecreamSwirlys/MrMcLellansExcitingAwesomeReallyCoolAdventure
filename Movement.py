import pygame, sys, time, random
from pygame.locals import *

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window.
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

#VARS
player = pygame.Rect(0,200,100,200)
WHITE = (255,255,255)
LeftKey = K_a
RightKey = K_d
JumpKey = K_SPACE
MOVELEFT = False
MOVERIGHT = False
MOVESPEED = 10
GRAVITY = 15
MaxJumpHeight = player.top - 200
JUMP = False
JumpAllowed = True


#Main Loop
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == LeftKey:
                MOVERIGHT = False
                MOVELEFT = True
            if event.key == RightKey:
                MOVELEFT = False
                MOVERIGHT = True
            if event.key == JumpKey and JumpAllowed:
                JUMP = True
        if event.type == KEYUP:
            if event.key == LeftKey:
                MOVELEFT = False
            if event.key == RightKey:
                MOVERIGHT = False
            if event.key == JumpKey:
                JUMP = False
            

    if MOVELEFT and player.left > 0:
        player.left -= MOVESPEED
    if MOVERIGHT and player.right < WINDOWWIDTH:
        player.left += MOVESPEED
    if JUMP and player.top > MaxJumpHeight:
        player.top -= GRAVITY 
        JumpAllowed = False
    elif player.bottom < WINDOWHEIGHT:   
        player.top += GRAVITY
        JUMP = False
    if player.bottom > WINDOWHEIGHT - 1:
        JumpAllowed = True

    
    
    
      

    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, (255,0,0), (player))

    pygame.display.update()
    mainClock.tick(40)
    
