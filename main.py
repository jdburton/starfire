import pygame, sys
from pygame.locals import *
import view
import controller
 
pygame.init()
C = controller.Controller()

C.mainLoop() 

    