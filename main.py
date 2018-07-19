import pygame, sys
from pygame.locals import *
import view
 
pygame.init()
V = view.View()
 
while True:
   
    clock = pygame.time.Clock()
    
    V.processScreen()
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            sys.exit()
 
    clock.tick(300)
    