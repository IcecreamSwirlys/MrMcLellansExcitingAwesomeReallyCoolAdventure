import pygame, sys, time, random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

infoObject = pygame.display.Info()
SCREEN = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
scaleFactor = infoObject.current_w / 800

def importSprites():
    LevelOne = pygame.Rect(0, 0, 0, 0)
    LevelOneImage = pygame.image.load('Sprites/Levels/LevelOne/LevelOne.png').convert_alpha()
    LevelOneStretchedImage = pygame.transform.scale(LevelOneImage, (int(800*scaleFactor), int(800*scaleFactor)))

##def hitboxConfig():
##    class Hitbox:
##        Hitbox1 = Hitbox(0,0,0,0 )
    

def levelOneConfig():
    importSprites()
##    hitboxConfig()
    


pygame.display.update()
mainClock.tick(120)
