import pygame, sys
from pygame.locals import *
import spritesheet
import random

class View:

   def __init__(self):
      self.screen = pygame.display.set_mode((800, 600))
       
      self.image1 = pygame.image.load('images/starfield800.bmp')
      self.image2 = pygame.image.load('images/starfield800.bmp')
       
      self.coordinate_image1 = -self.image2.get_height()
      self.coordinate_image2 = 0
   
      
      # load the spritesheet  
      ss = spritesheet.spritesheet('images/newsprites.bmp')
      # Sprite is 16x16 pixels at location 0,0 in the file...
      
      # load the images from the spritesheet
      ck=(255,0,255)
      self.starfire_images = ss.images_at( [(1, 1, 72, 73), (74,1,72,73), (147,1,72,73)], ck)
      self.gunship_images = ss.images_at(  [(1, 75, 73,58), (76,75,73,58), (150,75,73,58),(226,75,73,58)], ck)
      self.drone_images = ss.images_at(  [(1,236, 79,68)], ck)
      self.dart_images = ss.images_at(   [(1,306, 71,68), (147,306 ,71,68), (74,306 ,71,68),(220,306,71,68)],ck) 
      self.boss_images = ss.images_at(  [(293,236, 182,169)], ck)
      
      self.bullet_images = ss.images_at([(220,1,9,9)],ck)
      self.blaster_images = ss.images_at([(220,1,9,20)],ck)
      self.enemy_blaster_images = ss.images_at([(220,33,9,20)],ck)
      self.explosion_images = ss.images_at([(101,136,99,99),(301,136,99,99),(201,136,99,99),(401,136,99,99)],ck)
      self.shield_images=ss.images_at([(231,1,57,27)],ck)
      self.power_images=ss.images_at([(231,30,57,27)],ck)
      self.bonus_images=ss.images_at([(290,1,57,27)],ck)
      self.x_images=ss.images_at([(290,30,57,27)],ck)
      

      self.frame = 0
    
      # Create the sprite for the object
      self.starfire_sprite = pygame.sprite.Sprite()
      
      # Set the image of the sprite.
      self.starfire_sprite.image = self.starfire_images[0]
      # Get the rectangle of the sprite
      self.starfire_sprite.rect = self.starfire_sprite.image.get_rect()
      # set the position of the sprite.
      self.starfire_sprite.rect.x = 300   
      self.starfire_sprite.rect.y = 300
   
      # Add the sprite to a Group. Groups manage sprites.
      self.sprite_group = pygame.sprite.Group()
      self.sprite_group.add([ self.starfire_sprite ])
      
      self.dir_x = 0
      self.dir_y = 0
   
   def processScreen(self):
      self.preProcessing()
      self.updateDisplay()
      self.postProcessing() 
   
   def preProcessing(self):
      self.blitImages()
   
   def blitImages(self):
      
      # Drwaw the background.
      self.screen.blit(self.image1, (0,self.coordinate_image1))
      self.screen.blit(self.image2, (0,self.coordinate_image2))
      
      self.screen.blit(self.gunship_images[int(self.frame / 5) % len(self.gunship_images)],(200,200))
      self.screen.blit(self.drone_images[int(self.frame / 5) % len(self.drone_images)],(400,100))
      self.screen.blit(self.dart_images[int(self.frame / 5) % len(self.dart_images)],(300,100))
      self.screen.blit(self.boss_images[int(self.frame / 5) % len(self.boss_images)],(500,300))
      self.screen.blit(self.explosion_images[int(self.frame / 5) % len(self.explosion_images)],(500,200))
      
   
      # Draw all sprites.
      self.sprite_group.draw(self.screen)
      
      # Update each sprite.
      self.starfire_sprite.image = self.starfire_images[int(self.frame / 5) % len(self.starfire_images)]

   
      if self.frame % 30 == 0:
         self.dir_x = random.randint(-2,2)
         self.dir_y = random.randint(-2,2)
   
      self.starfire_sprite.rect.x += self.dir_x  
      self.starfire_sprite.rect.y += self.dir_y
      self.frame += 1
 
      
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
 
