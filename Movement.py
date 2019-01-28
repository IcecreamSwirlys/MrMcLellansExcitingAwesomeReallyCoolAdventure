import pygame, sys, time, random
from pygame.locals import *

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window.
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

#VARS
player = pygame.Rect(200,100,100,200)
playerXHitbox = pygame.Rect(200,100,100,200)
playerYHitbox = pygame.Rect(200,100,100,200)
WHITE = (255,255,255)
LeftKey = K_a
RightKey = K_d
JumpKey = K_SPACE
MOVELEFT = False
MOVERIGHT = False
MOVEUP = False
CanMoveLeft = True
CanMoveRight = True
CanMoveUp = True
MOVESPEED = 5
GRAVITY = 6
MaxJumpHeight = player.top - 100
JUMP = False
JumpAllowed = True
CollisionDirectionX = '?'
CollisionDirectionY = '?'
directionX = '?'
directionY = '?'
hitboxes = []

class Hitbox:
    selfcollidedX = '?'
    selfcollidedY = '?'
    
    def __init__(self, x, y, w, h, hitboxVisible):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hitboxVisible = hitboxVisible
        hitboxes.append(self)

    def draw(self):
        if self.hitboxVisible:
            pygame.draw.rect(SCREEN, (0,0,255), (self.x, self.y, self.w, self.h))
        
outcrop = Hitbox(400,300,50,50, True)
floor = Hitbox(0,350,800,50, True)
outcrop1 = Hitbox(100,0,50,50, True)

#Main Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == LeftKey:
                MOVERIGHT = False
                MOVELEFT = True
            if event.key == RightKey:
                MOVELEFT = False
                MOVERIGHT = True
            #if event.key == JumpKey and JumpAllowed:
                #JUMP = True
                #MOVEUP = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()  
            if event.key == LeftKey:
                MOVELEFT = False
            if event.key == RightKey:
                MOVERIGHT = False
            if event.key == JumpKey:
                JUMP = False
                MOVEUP = False

    keys = pygame.key.get_pressed()

    if keys[JumpKey] and JumpAllowed:
        JUMP = True
        MOVEUP = True    

    if MOVELEFT: 
        directionX = 'Left'
    elif MOVERIGHT: 
        directionX = 'Right'

    for i in hitboxes:
        if playerXHitbox.colliderect(i.x,i.y,i.w,i.h):
            if directionX == 'Left':
                i.selfcollidedX = 'Left'
            elif directionX == 'Right':
                i.selfcollidedX = 'Right'

            
        if playerYHitbox.colliderect(i.x,i.y,i.w,i.h):
            if directionY == 'Down':
                i.selfcollidedY = 'Down'
                JumpAllowed = True
            if directionY == 'Up':
                i.selfcollidedY = 'Up'

    CollisionDirectionX = '?'
    CollisionDirectionY = '?'
    
    for i in hitboxes:
        if i.selfcollidedX == 'Right':
            CollisionDirectionX = 'Right'
        if i.selfcollidedX == 'Left':
            CollisionDirectionX = 'Left'
        if i.selfcollidedY == 'Down':
            CollisionDirectionY = 'Down'
        if i.selfcollidedY == 'Up':
            CollisionDirectionY = 'Up'
        
        i.selfcollidedX = '?'
        i.selfcollidedY = '?'
        
        
    if CollisionDirectionX != 'Left':
        if MOVELEFT and player.left > 0:
            player.left -= MOVESPEED
    if MOVELEFT:
        playerXHitbox.left = player.left - 5
        playerYHitbox.left = player.left 
   
    if CollisionDirectionX != 'Right':
        if MOVERIGHT and player.right < WINDOWWIDTH:
            player.left += MOVESPEED
    if MOVERIGHT:
        playerXHitbox.left = player.left + 5
        playerYHitbox.left = player.left

    if JUMP and player.top > MaxJumpHeight and CollisionDirectionY != 'Up':
        directionY = 'Up'
        player.top -= GRAVITY
        playerXHitbox.top = player.top
        playerYHitbox.top = player.top - 5
        JumpAllowed = False
    elif player.bottom < WINDOWHEIGHT and CollisionDirectionY != 'Down':
        directionY = 'Down'
        player.top += GRAVITY
        playerXHitbox.top = player.top
        playerYHitbox.top = player.top + 5
        JUMP = False
    if player.bottom > WINDOWHEIGHT - 1:
        JumpAllowed = True

      
    SCREEN.fill(WHITE)
    for i in hitboxes:
        i.draw()
    #pygame.draw.rect(SCREEN, (0,255,255), (playerYHitbox))
    #pygame.draw.rect(SCREEN, (0,255,0), (playerXHitbox))
    pygame.draw.rect(SCREEN, (255,0,0), (player))
    
    

    pygame.display.update()
    mainClock.tick(120)
    
