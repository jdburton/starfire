#!/usr/bin/env python3
#
# James Burton
# jburto2@clemson.edu
# CPSC 8700
# August 3, 2018
# Final Project
#
# Starfire/utils/background.py
#
# This module is a utility for displaying backgrounds. Down scrolling and static backgrounds have been implemented.
#
#

import pygame

class Background():
   
    
   class BgImage():
      
      def __init__(self,image,x,y):
         self.image = image
         self.x_coord = x
         self.y_coord = y
       
        
   def __init__(self,filename):
      self.images = []
      self.image_coordinates = [ 0 ]

   # implement scroll in the derived classes
   def scroll(self,speed):
      pass

   

class DownScrollingBackground(Background):
   
   
   def __init__(self,filename,direction=1):

      # load the file twice
      image1 = pygame.image.load(filename)
      image2 = pygame.image.load(filename) 
      
      self.images = [ Background.BgImage(image1, 0, -image2.get_height()) , Background.BgImage(image2,0,0) ]
   
   
   
   def scroll(self, speed=1):
      
      # increment the y coordinates to scroll down
      self.images[0].y_coord += speed
      self.images[1].y_coord += speed
    
      # check to see if the image has gone off the screen.  
      # if the coordinate of image 0 is below the screen
      if self.images[0].y_coord >= self.images[1].image.get_height():
         # The new coordinate of image 0 will be the top of image 1 - the height of image 1.
         self.images[0].y_coord = self.images[1].y_coord - self.images[1].image.get_height()
      # if the coordinate of image 1 is below the screen
      if self.images[1].y_coord >= self.images[0].image.get_height():
         # The new coordinate of image 1 will be the top of image 0 - the height of image 0.
         self.images[1].y_coord = self.images[0].y_coord - self.images[0].image.get_height()
   


   
# background from a single frame
class StaticBackground(Background):
   def __init__(self,filename):
      
      # load the file once
      image =  pygame.image.load(filename) 
      self.images = [ Background.BgImage(image, 0,0) ]

   
   # scroll does nothing. 
      
      

      
   
   