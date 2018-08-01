import pygame, sys
from pygame.locals import *
import Starfire.model as model
import Starfire.utils.background as background


import random

BG_FILE='images/starfield800.bmp'
FONT_SIZE = 26
FONT_FILE = 'fonts/stonehen.ttf'
FONT_COLOR = (254,249,215)

class View:

   def __init__(self,screen_width,screen_height):
      
      pygame.display.set_caption('Starfire')
      self.screen = pygame.display.set_mode((screen_width, screen_height))
      self.background = background.DownScrollingBackground(BG_FILE)
      self.initText()
   
     
   def updateDisplay(self):   
      
      for line in range(len(self.text_msg)):
         self.screen.blit(self.text_msg[line],(0,(line*FONT_SIZE)+((10)) ) )
      pygame.display.update()
      
   
   def drawBackground(self):
      
      for bgimage in self.background.images:
         pass
         self.screen.blit(bgimage.image,(bgimage.x_coord,bgimage.y_coord))
   
   def postProcessing(self):
      self.background.scroll()
      
   def initText(self):
      #pygame.font.init()
      self.myfont = pygame.font.Font(FONT_FILE, FONT_SIZE)
      
   def drawState(self,lives,shield,points):
      self.text_msg = []
      self.text_msg.append(self.myfont.render("Lives: %d" % lives, True, FONT_COLOR))
      self.text_msg.append(self.myfont.render("Shield: %d" % shield, True, FONT_COLOR))
      self.text_msg.append(self.myfont.render("Points: %d" % points, True, FONT_COLOR))
      
      
    

      


 
