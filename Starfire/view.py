#!/usr/bin/env python3
#
# James Burton
# jburto2@clemson.edu
# CPSC 8700
# August 3, 2018
# Final Project
#
# Starfire/view.py
#
# This implements the view of the program. 
# This includes the game screen and the auxiliary screens.


import pygame, sys
from pygame.locals import *
import Starfire.model as model
import Starfire.utils.background as background


import random

BG_FILE='images/starfield800.bmp'
LOGO_FILE='images/logo.bmp'
TITLE_FILE='images/title.bmp'
GAMEOVER_FILE='images/game_over.bmp'
MENU_FILE='images/menu.bmp'
FONT_SIZE = 26
FONT_FILE = 'fonts/stonehen.ttf'
FONT_COLOR = (254,249,215)
HELP_FILES =[ 'images/help_new.bmp', 'images/enemies.bmp' ]
SCROLL_SPEED = 1.5

class View:

   def __init__(self,screen_width,screen_height,display_fps):
      
      pygame.display.set_caption('Starfire')
      self.screen = pygame.display.set_mode((screen_width, screen_height))
      self.help_index = 0
      self.display_fps = display_fps
      self.last_scroll = pygame.time.get_ticks()
   
   # Logo, title, menu, and game over are simply static backgrounds.   
   def displayLogo(self):
      self.background = background.StaticBackground(LOGO_FILE)
      self.drawBackground()
      pygame.display.flip()
   
   def displayTitle(self):
      self.background = background.StaticBackground(TITLE_FILE)
      self.drawBackground()
      pygame.display.flip()
   
   def displayMenu(self):
      self.background = background.StaticBackground(MENU_FILE)
      self.drawBackground()
      pygame.display.flip()

   def displayGameOver(self):
      self.background = background.StaticBackground(GAMEOVER_FILE)
      self.drawBackground()
      pygame.display.flip()
   
   # Two help screens
   def displayHelp(self):
      
      if self.help_index < len(HELP_FILES):
         self.background = background.StaticBackground(HELP_FILES[self.help_index])
         self.drawBackground()
         pygame.display.flip()
         self.help_index = ( self.help_index + 1 )         
      else:
         self.help_index = 0
         
      return self.help_index
   
   # Start the background scrolling and initialize the text. 
   def initGame(self):
      self.background = background.DownScrollingBackground(BG_FILE)
      self.initText()
   
   # blit the text to the screen and update the image. Text will be on top.
   # Most drawing is done in the pygame.sprite.Group instances in the model class
    
   def updateDisplay(self):   
      
      for line in range(len(self.text_msg)):
         self.screen.blit(self.text_msg[line],(0,(line*FONT_SIZE)+((10)) ) )
      pygame.display.update()
      
   # Draw the background. This must be done before anything else is drawn.
   def drawBackground(self):
      
      for bgimage in self.background.images:
         self.screen.blit(bgimage.image,(bgimage.x_coord,bgimage.y_coord))
   
   # calculate scroll speed and scroll the background.
   def postProcessing(self):
      now = pygame.time.get_ticks()
      speed = int( SCROLL_SPEED * (now - self.last_scroll ) * self.display_fps * 0.001)
      self.background.scroll(speed)
      self.last_scroll = now
   
   # initialize the font  
   def initText(self):
      self.myfont = pygame.font.Font(FONT_FILE, FONT_SIZE)
   
   # draw the current game state to a text message.   
   def drawState(self,level,lives,shield,points):
      self.text_msg = []
      self.text_msg.append(self.myfont.render("Level: %d" % level, True, FONT_COLOR))
      self.text_msg.append(self.myfont.render("Lives: %d" % lives, True, FONT_COLOR))
      self.text_msg.append(self.myfont.render("Shield: %d" % shield, True, FONT_COLOR))
      self.text_msg.append(self.myfont.render("Points: %d" % points, True, FONT_COLOR))
      
      
    

      


 
