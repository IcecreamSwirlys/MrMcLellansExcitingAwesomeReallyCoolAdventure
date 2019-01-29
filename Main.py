import pygame, sys, time, random
from pygame.locals import *
from SpriteAnimater import SpriteStripAnim as Sprite

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window.
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

#VARS
player = pygame.Rect(200,100,40,90)
playerXHitbox = pygame.Rect(200,100,40,90)
playerYHitbox = pygame.Rect(200,100,40,90)
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
MOVESPEED = 3
GRAVITY = 6
JUMP = False
JumpAllowed = True
CollisionDirectionX = '?'
CollisionDirectionY = '?'
directionX = '?'
directionY = '?'
hitboxes = []
playerAnimation = True
currentAnimation = 'right'

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
        self.hitbox = pygame.Rect(x, y, w, h)

    def perFrame(self):
        self.x = self.hitbox.x
        self.y = self.hitbox.y
        self.w = self.hitbox.w
        self.h = self.hitbox.h

    def draw(self):
        if self.hitboxVisible:
            pygame.draw.rect(SCREEN, (0,0,255), (self.x, self.y, self.w, self.h))

global attackAnimationTimer
attackAnimationTimer = 0

def animationHandler():
    global attackDirection
    global currentAnimation
    global activePlayerAnimation
    global playerAttack
    global attackAnimationTimer
    global attackFrames
    attackAnimationTimer += 1
    if playerAnimation:
##        if playerAttack and attackDirection == 'up':
##            activePlayerAnimation = playerAnim[6].next()
##            attackFrames = 4
##        elif playerAttack and attackDirection == 'right':
##            activePlayerAnimation = playerAnim[2].next()
##            attackFrames = 6
##        elif playerAttack and attackDirection == 'down':
##            activePlayerAnimation = playerAnim[7].next()
##            attackFrames = 3
##        elif playerAttack and attackDirection == 'left':
##            activePlayerAnimation = playerAnim[5].next()
##            attackFrames = 6
        if MOVERIGHT:
            activePlayerAnimation = playerAnim[1].next()
            currentAnimation = 'right'
            attackFrames = 0
            attackAnimationTimer = 0
        elif MOVELEFT:
            activePlayerAnimation = playerAnim[0].next()
            currentAnimation = 'left'
            attackFrames = 0
            attackAnimationTimer = 0
        else:
            # Idle animation
            if currentAnimation == 'right':
                activePlayerAnimation = playerAnim[2].next()
            elif currentAnimation == 'left':
                activePlayerAnimation = playerAnim[3].next()
            attackFrames = 0
            attackAnimationTimer = 0
            
##        if attackAnimationTimer >= 120/12*attackFrames:
##            playerAttack = False
##            attackAnimationTimer = 0
        
outcrop = Hitbox(400,300,50,50, True)
floor = Hitbox(0,350,800,50, True)
LeftEdgeRect = pygame.Rect(100,0,50,800)
RightEdgeRect = pygame.Rect(650,0,50,800)
TopEdgeRect = pygame.Rect(0,50,800,50)
BottomEdgeRect = pygame.Rect(0,350,800,50)



#Importing Sprites and Animations
#Sprites

#Animations

frames = 120/12
playerAnim = [
    Sprite('player_Run_L.png', (0,0,50,50), 8, 1, True, frames),
    Sprite('player_Run_R.png', (0,0,50,50), 8, 1, True, frames),
    Sprite('player_Idle_R.png', (0,0,50,50), 8, 1, True, frames),
    Sprite('player_Idle_L.png', (0,0,50,50), 8, 1, True, frames),
    ]  
activePlayerAnimation = playerAnim[0]

#Main Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
        MaxJumpHeight = player.top - 150

    #perframe call for hitboxes
    for i in hitboxes:
        i.perFrame()

    if MOVELEFT: 
        directionX = 'Left'
    elif MOVERIGHT: 
        directionX = 'Right'

    #Hitbox detection

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

    if playerXHitbox.colliderect(LeftEdgeRect) and CollisionDirectionX != 'Right' and CollisionDirectionX != 'Left':
        if MOVELEFT:
            CollisionDirectionX = 'Left'   
            for i in hitboxes:
                i.hitbox.left += MOVESPEED
        
    if playerXHitbox.colliderect(RightEdgeRect) and CollisionDirectionX != 'Right' and CollisionDirectionX != 'Left':
        if MOVERIGHT:
            CollisionDirectionX = 'Right'   
            for i in hitboxes:
                i.hitbox.left -= MOVESPEED

    if playerYHitbox.colliderect(TopEdgeRect) and CollisionDirectionY != 'Up' and CollisionDirectionY != 'Down':   
        for i in hitboxes:
            i.hitbox.top += GRAVITY
        
    if playerYHitbox.colliderect(BottomEdgeRect) and CollisionDirectionY != 'Up' and CollisionDirectionY != 'Down':   
        for i in hitboxes:
            i.hitbox.top -= GRAVITY
        player.top -= GRAVITY
        playerXHitbox.top = player.top
        playerYHitbox.top = player.top
    
        
    #Movement
        
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

    #Animation
    animationHandler()

    #Drawing
      
    SCREEN.fill(WHITE)
    for i in hitboxes:
        i.draw()
##    pygame.draw.rect(SCREEN, (0,255,255), (playerYHitbox))
##    pygame.draw.rect(SCREEN, (0,255,0), (playerXHitbox))
##    pygame.draw.rect(SCREEN, (255,0,0), (player))
    

    scaledPlayerAnimation = pygame.transform.scale(activePlayerAnimation, (200,200))
    SCREEN.blit(scaledPlayerAnimation, (player.left-80, player.top - 60))

    pygame.display.update()
    mainClock.tick(120)
