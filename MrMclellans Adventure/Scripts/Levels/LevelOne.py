import pygame, sys, time, random
from pygame.locals import *
from Main import *


def importSprites():
    LevelOne = pygame.Rect(0, 0, 0, 0)
    LevelOneImage = pygame.image.load('Sprites/Levels/LevelOne/LevelOne.png').convert_alpha()
    LevelOneStretchedImage = pygame.transform.scale(LevelOneImage, (int(800*scaleFactor), int(800*scaleFactor)))

##def hitboxConfig():
##      Hitbox1 = Hitbox(0,0,0,0 )
    
    

importSprites()

SCREEN.blit(LevelOneStretchedImage, LevelOne)
