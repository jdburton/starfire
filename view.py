import pygame, sys
from pygame.locals import *

class View:

   def __init__(self):
      self.screen = pygame.display.set_mode((800, 600))
       
      self.image1 = pygame.image.load('images/starfield800.bmp')
      self.image2 = pygame.image.load('images/starfield800.bmp')
       
      self.coordinate_image1 = -self.image2.get_height()
      self.coordinate_image2 = 0
    
   
   def processScreen(self):
      self.preProcessing()
      self.updateDisplay()
      self.postProcessing() 
   
   def preProcessing(self):
      self.blitImages()
   
   def blitImages(self):
      self.screen.blit(self.image1, (0,self.coordinate_image1))
      self.screen.blit(self.image2, (0,self.coordinate_image2))
 
      
   def updateDisplay(self):   
      
      pygame.display.update()
   
   
   def postProcessing(self):
      self.scrollImage()
    
   def scrollImage(self):
 
    self.coordinate_image1 += 1
    self.coordinate_image2 += 1
    
    # if imaage 1 has gone off the screen
    if self.coordinate_image1 >= self.image1.get_height():
        self.coordinate_image1 = self.coordinate_image2 - self.image2.get_height()
    if self.coordinate_image2 >= self.image2.get_height():
        self.coordinate_image2 = self.coordinate_image1 - self.image1.get_height()
 
