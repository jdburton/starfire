import pygame, sys
from pygame.locals import *
import Starfire.model as model
import Starfire.utils.background as background


import random

BG_FILE='images/starfield800.bmp'

class View:

   def __init__(self,screen_width,screen_height):
      
      self.screen = pygame.display.set_mode((screen_width, screen_height))
      self.background = background.DownScrollingBackground(BG_FILE)
   
     
   def updateDisplay(self):   
      
      pygame.display.update()
   
   def drawBackground(self):
      
      for bgimage in self.background.images:
         pass
         self.screen.blit(bgimage.image,(bgimage.x_coord,bgimage.y_coord))
   
   def postProcessing(self):
      self.background.scroll()
    

      


 
