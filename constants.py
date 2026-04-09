from typing import *
from math import *
import pygame

mass: Final = 1
gravity: Final = 0.5
speedGoal: Final = 1
horizontalAccPercent: Final = 0.1
blorbRadius: Final = 15
colideForce: Final = 0.1

xSpawn: Final = 60
yPercentSpawn: Final = 0.3 #Percent from the top
secsPerSpawn = 1

pygame.init()
screenSize = pygame.display.get_desktop_sizes()[0]
screenSize = (screenSize[0], screenSize[1] - 60)
screenFlags = pygame.RESIZABLE
screen = pygame.display.set_mode(screenSize, screenFlags)
timer = pygame.time.Clock()
frameRate: Final = 90