import pygame, sys, time, random
from pygame.locals import *
from Scripts.SpriteAnimater import SpriteStripAnim as Sprite

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window.
infoObject = pygame.display.Info()
WINDOWWIDTH = infoObject.current_w
WINDOWHEIGHT = infoObject.current_h
SCREEN = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

RawScaleFactor = infoObject.current_w / 800
scaleFactor = round(RawScaleFactor)

#VARS
player = pygame.Rect(200*scaleFactor,100*scaleFactor,40*scaleFactor,85*scaleFactor)
playerXHitbox = pygame.Rect(200*scaleFactor,100*scaleFactor,40*scaleFactor,85*scaleFactor)
playerYHitbox = pygame.Rect(200*scaleFactor,100*scaleFactor,40*scaleFactor,85*scaleFactor)
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
MOVESPEED = 3*scaleFactor
GRAVITY = 6*scaleFactor
JUMP = False
JumpAllowed = True
CollisionDirectionX = '?'
CollisionDirectionY = '?'
directionX = '?'
directionY = '?'
hitboxes = []
playerAnimation = True
currentAnimation = 'right'
LevelOneConfig = False

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
        
outcrop = Hitbox(400*scaleFactor,300*scaleFactor,50*scaleFactor,50*scaleFactor, True)
floor = Hitbox(0*scaleFactor,350*scaleFactor,800*scaleFactor,50*scaleFactor, True)
LeftEdgeRect = pygame.Rect(100*scaleFactor,0*scaleFactor,50*scaleFactor,800*scaleFactor)
RightEdgeRect = pygame.Rect(650*scaleFactor,0*scaleFactor,50*scaleFactor,800*scaleFactor)
TopEdgeRect = pygame.Rect(0*scaleFactor,50*scaleFactor,800*scaleFactor,50*scaleFactor)
BottomEdgeRect = pygame.Rect(0*scaleFactor,360*scaleFactor,800*scaleFactor,50*scaleFactor)



#Importing Sprites and Animations
#Sprites

#Animations

frames = 120/12
playerAnim = [
    Sprite('Sprites/Entitys/Player/player_Run_L.png', (0,0,50,50), 8, 1, True, frames),
    Sprite('Sprites/Entitys/Player/player_Run_R.png', (0,0,50,50), 8, 1, True, frames),
    Sprite('Sprites/Entitys/Player/player_Idle_R.png', (0,0,50,50), 8, 1, True, frames),
    Sprite('Sprites/Entitys/Player/player_Idle_L.png', (0,0,50,50), 8, 1, True, frames),
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
        MaxJumpHeight = player.top - 150*scaleFactor


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
        playerXHitbox.left = player.left - 6*scaleFactor
        playerYHitbox.left = player.left 
   
    if CollisionDirectionX != 'Right':
        if MOVERIGHT and player.right < WINDOWWIDTH:
            player.left += MOVESPEED
    if MOVERIGHT:
        playerXHitbox.left = player.left + 6*scaleFactor
        playerYHitbox.left = player.left

    if JUMP and player.top > MaxJumpHeight and CollisionDirectionY != 'Up':
        directionY = 'Up'
        player.top -= GRAVITY
        playerXHitbox.top = player.top
        playerYHitbox.top = player.top - 6*scaleFactor
        JumpAllowed = False
    elif player.bottom < WINDOWHEIGHT and CollisionDirectionY != 'Down':
        directionY = 'Down'
        player.top += GRAVITY
        playerXHitbox.top = player.top
        playerYHitbox.top = player.top + 6*scaleFactor
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
    
    playerSize = int(200*scaleFactor)
    scaledPlayerAnimation = pygame.transform.scale(activePlayerAnimation, (playerSize,playerSize))
    SCREEN.blit(scaledPlayerAnimation, (player.left-80*scaleFactor, player.top - 60*scaleFactor))
    print(scaleFactor)
    pygame.display.update()
    mainClock.tick(120)
