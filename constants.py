from typing import *
from math import *
import pygame

mass: Final = 1
gravity: Final = 0.03
speedGoal: Final = 1.5
horizontalAccPercent: Final = 0.05
blorbRadius: Final = 45
colideForce: Final = 0.003
secsUntilFalling: Final = 0.2
atatchGap: Final = 20   #If the gap between blorbs is less than or equal to this they will attatch when gripping
releaseGap: Final = 25
angleForce: Final = 0.03
frontGapTillGrip: Final = blorbRadius
dampingConstant: Final = 0.1
springConstant: Final = 0.1
springExponent: Final = 0.7
nAttatchmentPoints: Final = 5

sideBlockWidth: Final = 150
blockHeightPercent: Final = 0.4 #Percent from the bottom
blockColor: Final = [100, 100, 115]
middleBlockWidth: Final = 200

pygame.init()
screenSize = pygame.display.get_desktop_sizes()[0]
screenSize = (screenSize[0], screenSize[1] - 80)
screenFlags = pygame.RESIZABLE
screen = pygame.display.set_mode(screenSize, screenFlags)
timer = pygame.time.Clock()
frameRate: Final = 90
width:Final = screen.get_width()
height:Final = screen.get_height()

xSpawn: Final = 60
yPercentSpawn: Final = 0.9 #Percent from the bottom
secsPerSpawn = 1.5

grabbingImage = pygame.image.load("Gripping.png")
walkingImage = pygame.image.load("Walking.png")
fallingImage = pygame.image.load("Falling.png")