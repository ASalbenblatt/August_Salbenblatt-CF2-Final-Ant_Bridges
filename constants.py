from typing import *
from math import *
import pygame

mass: Final = 1
gravity: Final = 0.1
speedGoal: Final = 1.5
horizontalAccPercent: Final = 0.05
blorbRadius: Final = 20
colideForce: Final = 0.1
framesUntilFalling: Final = 3
atatchGap: Final = 5   #If the gap between blorbs is less than or equal to this they will attatch when gripping

blockWidth: Final = 150
blockHeightPercent: Final = 0.4 #Percent from the bottom
blockColor: Final = [100, 100, 115]

xSpawn: Final = 60
yPercentSpawn: Final = 0.7 #Percent from the bottom
secsPerSpawn = 1

pygame.init()
screenSize = pygame.display.get_desktop_sizes()[0]
screenSize = (screenSize[0], screenSize[1] - 60)
screenFlags = pygame.RESIZABLE
screen = pygame.display.set_mode(screenSize, screenFlags)
timer = pygame.time.Clock()
frameRate: Final = 90
width:Final = screen.get_width()
height:Final = screen.get_height()