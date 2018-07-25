import pygame, sys
from pygame.locals import *
import model
import background
import spritesheet

import random

class View:

   def __init__(self,screen_width,screen_height):
      
      #self.model = gameModel
      self.screen = pygame.display.set_mode((screen_width, screen_height))
      self.background = background.DownScrollingBackground(background.BG_FILE)
   

      
   def updateDisplay(self):   
      
      pygame.display.update()
   
   def drawBackground(self):
      
      for bgimage in self.background.images:
         self.screen.blit(bgimage.image,(bgimage.x_coord,bgimage.y_coord))
   
   def postProcessing(self):
      self.background.scroll()
    

      


 
