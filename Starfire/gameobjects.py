#!/usr/bin/env python3
#
# James Burton
# jburto2@clemson.edu
# CPSC 8700
# August 3, 2018
# Final Project


import pygame
import random
import math
import Starfire.utils.spritesheet as spritesheet


SPRITESHEET='images/newsprites.bmp'
CK=(255,0,255)

# Number of FPS
MAX_FPS = 60

# How long to hold an animation. The smaller the number, the faster the animation
FRAME_HOLD = int ( MAX_FPS / 10 )

# How fast the objects move on the screen. The bigger, the faster enemies move.
MOVE_SCALE = (1.0 * MAX_FPS * 0.001) 

# Constant that indicates no damage occured from a hit.
NO_DAMAGE = -999999

# How big is the explosion?
NO_EXPLOSION = 0
SMALL_EXPLOSION = 1
BIG_EXPLOSION = 2

# Utility to load images from the sprite sheet.
# returns a dictionary of images.

def loadImagesFromSheet():
   
   ss = spritesheet.spritesheet(SPRITESHEET)
   
   sprite_images = {}

   sprite_images['Player'] = ss.images_at( Player.SS_COORDINATES, CK)
   sprite_images['Explosion'] = ss.images_at( Explosion.SS_COORDINATES, CK)
   sprite_images['Gunship'] = ss.images_at( Gunship.SS_COORDINATES, CK)
   sprite_images['Dart'] = ss.images_at( Dart.SS_COORDINATES, CK)
   sprite_images['Drone'] = ss.images_at( Drone.SS_COORDINATES, CK)
   sprite_images['Boss'] = ss.images_at( Boss.SS_COORDINATES, CK)
   sprite_images['PlayerBlaster'] = ss.images_at( PlayerBlaster.SS_COORDINATES, CK)
   sprite_images['EnemyBlaster'] = ss.images_at( EnemyBlaster.SS_COORDINATES, CK)
   sprite_images['EnemyBullet'] = ss.images_at( EnemyBullet.SS_COORDINATES, CK)
   sprite_images['XWeaponPU'] = ss.images_at( XWeaponPU.SS_COORDINATES, CK)
   sprite_images['BonusPU'] = ss.images_at( BonusPU.SS_COORDINATES, CK)
   sprite_images['PowerPU'] = ss.images_at( PowerPU.SS_COORDINATES, CK)
   sprite_images['ShieldPU'] = ss.images_at( ShieldPU.SS_COORDINATES, CK)
   
   return sprite_images

# Data structure for shots fired.
class Shot():

   def __init__(self,name,x_pos,y_pos,x_vel,y_vel):
      self.name = name
      self.x_pos = x_pos
      self.y_pos = y_pos
      self.x_vel = x_vel
      self.y_vel = y_vel

# Generic GameObject class. 
# All GameObjects are Sprites with game specific data and functionality.

class GameObject(pygame.sprite.Sprite):
   
   # Should get overridden in derived classes
   OBJECT_WIDTH = 0
   OBJECT_HEIGHT = 0
   POINT_VALUE = 0
   MAX_VELOCITY_X = 1
   MIN_VELOCITY_X = -1
   MAX_VELOCITY_Y = 1
   MIN_VELOCITY_Y = -1
  

   def __init__(self,images = [],rect_x=0,rect_y=0,s_width=800,s_height=600):
      super().__init__()
    
      self.object_images = []
      self.object_frame = 0
      
      # Starting position
      self.start_x = rect_x
      self.start_y = rect_y
      
      # Default values
      self.vel_x = 0
      self.vel_y = 0
      self.hit_points = 1
      self.damage = 0
      
      # Can't think of a case where a constrained object has a min that isn't zero.
      self.min_x = 0
      self.min_y = 0
      
      self.setImages(images, rect_x, rect_y)
      self.last_move = pygame.time.get_ticks()
   
   # setImages: "Private" method to set the image and position of the sprite.
   def setImages(self,images,rect_x,rect_y):
      self.object_images = images
      self.image = self.object_images[self.object_frame]
      self.rect = self.image.get_rect()
      self.rect.x = rect_x
      self.rect.y = rect_y

   # Constrain: Keep the images within the bounds of the screen 
   def constrain(self,width, height):
      self.max_x = width - self.OBJECT_WIDTH
      self.max_y = height - self.OBJECT_HEIGHT
      #print("Max x: %d Max y: %d" % (self.max_x, self.max_y))
      
  
   # There is probably a better way to do this, but it works well enough.
   def animate(self,hold=FRAME_HOLD):
      
      self.object_frame += 1 
      self.image = self.object_images[int(self.object_frame/hold) % len(self.object_images) ]
  
   # Accelerate the object
   def accelerate(self,x=0,y=0):
      self.vel_x += x
      self.vel_y += y
   
   # Change the velocity of the object
   def changeDirection(self,x=0,y=0):
      self.vel_x = x
      self.vel_y = y
      
   # Move the object by adding the current velocity to the position.
   def move(self):
      now = pygame.time.get_ticks()
      ticks = now - self.last_move
      self.rect.x += int((self.vel_x * ticks * MOVE_SCALE))
      self.rect.y += int((self.vel_y * ticks * MOVE_SCALE))
      self.last_move = now
      self.validateMove()
   
   # Move the object directly to (x,y)
   def moveTo(self,x_coord,y_coord):
      self.rect.x = x_coord
      self.rect.y = y_coord
      self.validateMove()
   
   # Validate that the next move is valid. Will be overridden in subclasses
   def validateMove(self):
      pass
 
   # Calculate damage from being hit by a colliding object.     
   def hit(self,colliding_object):
      
      self.hit_points -= colliding_object.damage

      if colliding_object.damage == 0:
         return NO_DAMAGE
      else:
         return self.hit_points 
   
   # Does this object explode? No, unless explicitly specified in subclass.
   def explodes(self):
      return NO_EXPLOSION

# Class for Player Sprite
class Player(GameObject):
   
   # Constants
      
   OBJECT_WIDTH = 72
   OBJECT_HEIGHT = 73
   SS_COORDINATES = [(1, 1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (74,1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (147,1, OBJECT_WIDTH, OBJECT_HEIGHT) ]
   
   # Cannon positions for firing.
   # Also useful for locating the object.
   CENTER_CANNON = ((OBJECT_WIDTH/2)-4,-12)
   RIGHT_CANNON = (1, 17)
   LEFT_CANNON =  (OBJECT_WIDTH-9,17)
   
   # More values
   MAX_HIT_POINTS = 20  
   BASE_FIRE_RATE = 400
   MIN_FIRE_RATE = 100
   POINT_VALUE = 0
   DAMAGE = 10
  
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y)
     
      # Collision damage to other objects
      self.damage = self.DAMAGE
     
      # Constrain to the screen.
      self.constrain(s_width,s_height)
      
      # reset to default values
      self.reset()
      
   # Fire your weapon   
   def fireWeapon(self):
      
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      # if you are ready to fire, fire active cannons
      if now - self.last_fired > self.fire_rate: 
         if self.active_cannons[0] is True:
            shots.append(Shot("PlayerBlaster",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],0,-5))
         if self.active_cannons[1] is True:
            shots.append(Shot("PlayerBlaster",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,-5))
         if self.active_cannons[2] is True:
            shots.append(Shot("PlayerBlaster",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],0,-5))

         self.last_fired = now         
         
      # return shot data to the model
      return shots
       
   # Increase firepower
   def powerUp(self):
      
      # Level 0: Single fire
      # Level 1: Dual fire
      # Level 2: Triple fire
      # Level 3: Rapid (2x) fire
      # Level 4: Turbo (4x) fire
    
      # Max level is 4
      if self.fire_level >= 4:
         return
      
      # Increase the fire level
      self.fire_level += 1
      
      # Turn on side cannons at level 1
      if self.fire_level == 1:
         self.active_cannons = (True,False,True)
      # Turn on all cannons at level 2 and higher 
      else:
         self.active_cannons = (True,True,True)
         # Half the fire delay for level 3 and 4
         if self.fire_level >= 3:
            self.fire_rate /= 2
      
      #print("Fire level=%d, Fire rate=%d" % (self.fire_level,self.fire_rate))
 
   # Reset to defaults
   def reset(self):
      
      self.hit_points = self.MAX_HIT_POINTS
      self.fire_rate = self.BASE_FIRE_RATE
      
      self.rect.x = self.start_x
      self.rect.y = self.start_y      
      
      self.fire_level = 0
      self.active_cannons = (False,True,False)
      self.time_created = pygame.time.get_ticks()
      self.last_fired = self.time_created
      
      # reset the mouse
      pygame.mouse.set_pos([self.start_x,self.start_y])
      
      # Low shield warning
      self.warned = 0
   
           
   
      
   # Keep the player on the screen.
   def validateMove(self):
      
      if self.rect.x > self.max_x:
         self.rect.x = self.max_x
         self.vel_x = 0
      elif self.rect.x < self.min_x:
         self.rect.x = self.min_x
         self.vel_x = 0
         
      if self.rect.y > self.max_y:
         self.rect.y = self.max_y
         self.vel_y = 0
      elif self.rect.y < self.min_y:
         self.rect.y = 0
         self.vel_y = 0
   
   def explodes(self):
      return SMALL_EXPLOSION
      

# Class for the explosion   
class Explosion(GameObject):
   

   OBJECT_WIDTH = 99
   OBJECT_HEIGHT = 99

   
   SS_COORDINATES = [   (1,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (101,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (301,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (201,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (401,136,OBJECT_WIDTH, OBJECT_HEIGHT)]
   
   
   
   def __init__(self,images,rect_x,rect_y):
      
      super().__init__(images,rect_x,rect_y)
   
   def animate(self):
      super().animate(hold = FRAME_HOLD/2)
      # If we've been through one cycle, kill the explosion.
      if self.object_frame/(FRAME_HOLD/2) >= len(self.object_images):
         self.kill()
         self.object_frame = 0
      
   # Explosions don't care about being hit.
   def hit(self,colliding_object):
      return NO_DAMAGE




# Generic Enemy Class
# This has functionality common to multiple enemies

class Enemy(GameObject):
   
   

   # All enemies are constrained to screen by default.
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y)
      self.constrain(s_width,s_height)
      self.move_interval =  random.randint(500,1000) 
      self.last_ai_move = 0
      self.damage = 10
      
    
   # Returns empty list so python won't complain. To be overridden in subclasses.  
   def fireWeapon(self, level = 1):
      return []
    
   # Acquire the target. Aim for the center
   def acquireTarget(self,starfire):
      self.target_x = starfire.rect.x + starfire.OBJECT_WIDTH/2
      self.target_y = starfire.rect.y + starfire.OBJECT_HEIGHT/2 
      
    
   # Aims the shot at (x_dir,y_dir) at s_vel speed.
   # returns shot velocity vector in x,y coordinates.
   def aim(self,x_dir,y_dir,s_vel):  
      
      # Find the angle
      theta = math.atan2(y_dir,x_dir)
  
      # find the velocity    
      x_vel = int((s_vel*math.cos(theta))+0.5)
      y_vel = int((s_vel*math.sin(theta))+0.5)
   
      return (x_vel,y_vel)
   
   # Enemies bounce off each other when they collide. Not implemented. 
   def bounce(self):
      return

   # Enemies explode
   def explodes(self):
      return SMALL_EXPLOSION

# Enemy Gunship
class Gunship(Enemy):
   
   
   OBJECT_WIDTH = 73
   OBJECT_HEIGHT = 58
   POINT_VALUE = 800
   
   LEFT_CANNON = (5, OBJECT_HEIGHT-10)
   RIGHT_CANNON =  (OBJECT_WIDTH-13,OBJECT_HEIGHT-10)
   CENTER_CANNON = OBJECT_WIDTH / 2, OBJECT_HEIGHT-15
   
   
   SS_COORDINATES = [(1, 75, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (76,75, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (150,75, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (226,75, OBJECT_WIDTH, OBJECT_HEIGHT) ]
   
   MAX_HIT_POINTS = 6  
   BASE_FIRE_RATE = 1500
   MIN_FIRE_RATE = 750

   MAX_VELOCITY_X = 2
   MIN_VELOCITY_X = -2
   MAX_VELOCITY_Y = 2
   MIN_VELOCITY_Y = -2
  

   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.hit_points = self.MAX_HIT_POINTS
      self.fire_rate = random.randint(self.MIN_FIRE_RATE,self.BASE_FIRE_RATE)
      self.last_fired = 0
      self.target_x = s_width/2
      self.target_y = s_height-50
   
      
   def fireWeapon(self, level = 1):
      
      
      x_dir  = self.target_x-self.rect.x+self.CENTER_CANNON[0]
      y_dir = self.target_y-self.rect.y+self.CENTER_CANNON[1]

      (x_vel,y_vel) = self.aim(x_dir,y_dir,3)
      
      #print("Gunship: Aiming from (%d,%d) to (%d, %d) at (%d,%d)" % (self.rect.x+self.CENTER_CANNON[0],self.target_y-self.rect.y+self.CENTER_CANNON[1],self.target_x,self.target_y,x_vel,y_vel) )
   
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         shots.append(Shot("EnemyBlaster",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],0,5))
         if (level >= 4):
            shots.append(Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],x_vel,y_vel))
         shots.append(Shot("EnemyBlaster",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],0,5))

         self.fire_rate = random.randint(self.MIN_FIRE_RATE,self.BASE_FIRE_RATE)
         self.last_fired = now    
         
      
      return shots
   
   def move(self):
      
      now = pygame.time.get_ticks()
      
      if now - self.last_ai_move < self.move_interval:
         super().move()
         return
      
      # Distance from target to object 
      distance_y = self.target_y-self.rect.y+self.OBJECT_HEIGHT/2
      distance_x = self.target_x-self.rect.x+self.OBJECT_WIDTH/2
      
      # Adapted from legacy Ai.cpp
      
      # if we are above the player, check to see if we need to move.
      # TODO: Replace hardcoded constants with global values.
      if distance_y < 0:
         if abs(distance_x) < 50:
            if distance_x > 0:
               self.vel_x = self.MIN_VELOCITY_X
            else:
               self.vel_x = self.MAX_VELOCITY_X
         elif abs(distance_x) > 200:
            if distance_x > 0:
               self.vel_x = self.MAX_VELOCITY_X
            else:
               self.vel_x = self.MIN_VELOCITY_X
         else:
            self.vel_x = random.randint(self.MIN_VELOCITY_X,self.MAX_VELOCITY_X)
      else:
         self.vel_x = random.randint(self.MIN_VELOCITY_X,self.MAX_VELOCITY_X)

         
      if self.rect.y < 200:
         self.vel_y = random.randint(1,self.MAX_VELOCITY_Y)
      elif self.rect.y < (self.max_y - 200):
         self.vel_y = random.randint(self.MIN_VELOCITY_Y,-1)
      else:
         self.vel_y = random.randint(self.MIN_VELOCITY_Y,self.MAX_VELOCITY_Y)
            

      self.move_interval = random.randint(1500,2500)
         
      self.last_ai_move = now   
      super().changeDirection(self.vel_x,self.vel_y)
      super().move()

   # Standard enemy move validation: Keep the enemy on the screen.
   def validateMove(self):
      

      if self.rect.x > self.max_x:
         self.rect.x = self.max_x
         self.vel_x = self.MIN_VELOCITY_X
         
      elif self.rect.x < self.min_x:
         self.rect.x = self.min_x
         self.vel_x = self.MAX_VELOCITY_X
         
         
      if self.rect.y > self.max_y:
         self.rect.y = self.max_y
         self.vel_y = self.MIN_VELOCITY_Y
         # Keep backing up. 
         # This makes for a boring game if enemies stay at the bottom of the screen
         self.move_interval = 2000
         
         
      elif self.rect.y < self.min_y:
         self.rect.y = self.min_y
         self.vel_y = self.MAX_VELOCITY_Y
         


      
# Enemy Dart Fighter

class Dart(Enemy):

   
   OBJECT_WIDTH = 71
   OBJECT_HEIGHT = 68
   CENTER_CANNON = OBJECT_WIDTH / 2, OBJECT_HEIGHT
   POINT_VALUE = 400
   

   SS_COORDINATES = [(1, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (147, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (74, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (220, 306, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
   MAX_HIT_POINTS = 4  
   BASE_FIRE_RATE = 500 
   
   MAX_VELOCITY_X = 2
   MIN_VELOCITY_X = -2
   MAX_VELOCITY_Y = 6
   MIN_VELOCITY_Y = 6 
   
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.hit_points = self.MAX_HIT_POINTS
      self.fire_rate = self.BASE_FIRE_RATE
      self.last_fired = 0
      self.max_y = s_height+self.OBJECT_HEIGHT
      
   def fireWeapon(self,level=1):
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate:          
         shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],random.randint(-3,3),random.randint(1,3)))
         self.last_fired = now
      
      return shots
   
   # Attempt to ram the player
   def move(self):
      
      now = pygame.time.get_ticks()
      
      if now - self.last_ai_move < self.move_interval:
         super().move()
         return
       
      # Distance from target to object 
      distance_y = self.target_y-self.rect.y+self.OBJECT_HEIGHT/2
      distance_x = self.target_x-self.rect.x+self.OBJECT_WIDTH/2
      
      # Adapted from legacy Ai.cpp
   
      
      # if we are above the player, check to see if we need to move.
      # TODO: Replace hardcoded constants with global values.
      # Are we above the player
      if distance_y > 0:
         # Do we need to adjust course?
         if abs(distance_x) > 50:
            if distance_x > 0:
               self.vel_x = self.MAX_VELOCITY_X
            else:
               self.vel_x = self.MIN_VELOCITY_X
         # If not, ramming speed!
         else:
            self.vel_x = 0
      else:
         self.vel_x = random.randint(-1,1)
      
      self.vel_y = self.MAX_VELOCITY_Y
       
      self.move_interval = random.randint(500,1000)
         
      self.last_ai_move = now   
      super().changeDirection(self.vel_x,self.vel_y)
      super().move()
      
   # Darts fly off the screen. Override Enemy.validateMove() here.
   def validateMove(self):
      if self.rect.y >= self.max_y:
         self.kill()


# Enemy Drone Fighter
class Drone(Enemy):
   

   
   OBJECT_WIDTH = 79
   OBJECT_HEIGHT = 68
   POINT_VALUE = 200
   
   
   LEFT_CANNON = (1, OBJECT_HEIGHT-17)
   RIGHT_CANNON =  (OBJECT_WIDTH-9,OBJECT_HEIGHT-17)
   CENTER_CANNON = OBJECT_WIDTH / 2, OBJECT_HEIGHT
   

   
   SS_COORDINATES = [(1, 236, OBJECT_WIDTH, OBJECT_HEIGHT) ]
   
   MAX_HIT_POINTS = 4 
   BASE_FIRE_RATE = 2500 
   MIN_FIRE_RATE = 1000 
   MAX_VELOCITY_X = 3
   MIN_VELOCITY_X = -3
   MAX_VELOCITY_Y = 4
   MIN_VELOCITY_Y = -4
  
  
   
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      
      self.fire_rate = random.randint(self.MIN_FIRE_RATE,self.BASE_FIRE_RATE)
      self.last_fired = 0
      self.hit_points = self.MAX_HIT_POINTS
      
   
   # Fire weapon
   def fireWeapon(self,level = 1):
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      # 3 cannon spread shot
      if now - self.last_fired > self.fire_rate: 
   
         shots.append( Shot("EnemyBullet",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],-3,4))
         shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,5))
         shots.append( Shot("EnemyBullet",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],3,4))
         self.fire_rate = random.randint(self.MIN_FIRE_RATE,self.BASE_FIRE_RATE)
         self.last_fired = now         
         # Play the sound
      
      return shots
   
   
   def move(self):

      now = pygame.time.get_ticks()
      
      if now - self.last_ai_move < self.move_interval:
         super().move()
         return
       
       # Distance from target to object 
      distance_y = self.target_y-self.rect.y+self.OBJECT_HEIGHT/2
      distance_x = self.target_x-self.rect.x+self.OBJECT_WIDTH/2
      
      # Adapted from legacy Ai.cpp
   
      
      # if we are above the player, check to see if we need to move.
      # TODO: Replace hardcoded constants with global values.
      if distance_y > 0:
         if abs(distance_x) < 50:
            if distance_x > 0:
               self.vel_x = random.randint(self.MIN_VELOCITY_X,-1)
            else:
               self.vel_x = random.randint(1,self.MAX_VELOCITY_X)
         elif abs(distance_x) > 200:
            if distance_x > 0:
               self.vel_x = self.MAX_VELOCITY_X
            else:
               self.vel_x = self.MIN_VELOCITY_X
         else:
            self.vel_x = random.randint(self.MIN_VELOCITY_X,self.MAX_VELOCITY_X)
      
         
      self.vel_y = random.randint(0,self.MAX_VELOCITY_Y)
            
       
      self.move_interval = random.randint(500,2000)
         
      self.last_ai_move = now   
      super().changeDirection(self.vel_x,self.vel_y)
      super().move()
      
   
   def validateMove(self):
      
      if self.rect.x > self.max_x:
         self.rect.x = self.max_x
         self.vel_x = self.MIN_VELOCITY_X
         self.move_interval = 1000
         
      elif self.rect.x < self.min_x:
         self.rect.x = self.min_x
         self.vel_x = self.MAX_VELOCITY_X
         self.move_interval = 1000
         
      if self.rect.y > self.max_y:
         self.rect.y = self.max_y
         self.vel_y = self.MIN_VELOCITY_Y
         self.move_interval = 1500
         
      elif self.rect.y < self.min_y:
         self.rect.y = self.min_y
         self.vel_y = self.MAX_VELOCITY_Y
      


# Enemy Boss
class Boss(Enemy):
   

   OBJECT_WIDTH = 180
   OBJECT_HEIGHT = 169
   
   LEFT_CANNON = (48, OBJECT_HEIGHT-10)
   RIGHT_CANNON =  (OBJECT_WIDTH-60,OBJECT_HEIGHT-10)
   CENTER_CANNON = (OBJECT_WIDTH / 2, OBJECT_HEIGHT/2)
   POINT_VALUE = 10000


   MAX_VELOCITY_X = 2
   MIN_VELOCITY_X = -2
   MAX_VELOCITY_Y = 3
   MIN_VELOCITY_Y = -2
   MAX_HIT_POINTS = 80
   DAMAGE = 100
   BASE_FIRE_RATE = 2000 
   MIN_FIRE_RATE = 500
   
   
   SS_COORDINATES = [(296, 236, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)

      self.reset()
   

   def reset(self,level=1):
      
      self.hit_points = self.MAX_HIT_POINTS + ( (level-1) * 20 )
      
      self.time_created = pygame.time.get_ticks()
      self.damage = self.DAMAGE
      
      # Calculate current fire rate.
      rate_max = 2000 -  ( (level-1) * 100 )
      rate_min = 1200 - ( (level-1) * 100 )
      if rate_min < 0:
         rate_min = 0
      if rate_max < 500:
         self.fire_rate = 500   
      else:       
         self.fire_rate = random.randint(rate_min,rate_max) + 500
      
      self.last_fired = pygame.time.get_ticks()
      self.last_move = self.last_fired
      
      start_x = random.randint(0,self.max_x)
      self.vel_y = self.MAX_VELOCITY_Y
      self.moveTo(start_x,0)
      self.move_interval =  random.randint(2500,4000) 

   def fireWeapon(self,level = 1):
      
      

      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         shots.append(Shot("EnemyBlaster",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],0,4))
         shots.append(Shot("EnemyBlaster",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],0,4))
         
         # Add spread for level 2
         if level >= 2:
            shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],-3,3))
            shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,4))
            shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],3,3))
           
         # Fire sideways on level 3.    
         if level >= 3:      
               shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],-4,0))
               shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],4,0))
   
         # Fire backwards on higher levels
         if level >= 4:
               shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],-3,-3))
               shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,-4))
               shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],3,-3))
         
         # Aimed shot on higher levels
         if level >= 5:
            x_dir  = self.target_x-self.rect.x+self.CENTER_CANNON[0]
            y_dir = self.target_y-self.rect.y+self.CENTER_CANNON[1]

            # shot gets faster the higher you go.
            (x_vel,y_vel) = self.aim(x_dir,y_dir,level-1)
      
            #print("Aiming from (%d,%d) to (%d, %d) at (%d,%d)" % (self.rect.x+self.CENTER_CANNON[0],self.target_y-self.rect.y+self.CENTER_CANNON[1],self.target_x,self.target_y,x_vel,y_vel) )
   
            shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],x_vel,y_vel))


         self.fire_rate = random.randint(self.MIN_FIRE_RATE,self.BASE_FIRE_RATE)
         self.last_fired = now         
         # Play the sound
      
      return shots


   def move(self):
      
      # Distance from target to object 
      distance_y = self.target_y-self.rect.y+self.OBJECT_HEIGHT/2
      distance_x = self.target_x-self.rect.x+self.OBJECT_WIDTH/2
      
      now = pygame.time.get_ticks()
      
      if now - self.last_ai_move < self.move_interval:
         super().move()
         return
      
      # Adapted from legacy Ai.cpp
      
      # RAM IF YOU CAN 
      if abs(distance_x) < 70 and 2 * self.rect.y < self.max_y: 
         self.vel_x = 0
         self.vel_y = self.MAX_VELOCITY_Y
      else:
               
         self.vel_x = random.randint(self.MIN_VELOCITY_X,self.MAX_VELOCITY_X)
  
      self.move_interval =  random.randint(2500,4000) 
      self.last_ai_move = now   
      super().changeDirection(self.vel_x,self.vel_y)
      super().move()
   
   # Standard enemy move validation: Keep the enemy on the screen.
   def validateMove(self):
      
      if self.rect.x > self.max_x:
         self.rect.x = self.max_x
         self.vel_x = self.MIN_VELOCITY_X
      elif self.rect.x < self.min_x:
         self.rect.x = self.min_x
         self.vel_x = self.MAX_VELOCITY_X
         
      if self.rect.y > self.max_y:
         self.rect.y = self.max_y
         self.vel_y = self.MIN_VELOCITY_Y
      elif self.rect.y < 0:
         self.rect.y = 0
         self.vel_y = self.MAX_VELOCITY_Y
         
   def explodes(self):
      return BIG_EXPLOSION      


# Enemy Blaster. We know it's bad because it's red.
class EnemyBlaster(GameObject):
   

   
   OBJECT_WIDTH = 9
   OBJECT_HEIGHT = 20

   SS_COORDINATES = [(220, 33, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   def __init__(self,images,rect_x,rect_y,s_width,s_height,vel_x=0,vel_y=4):
      
      super().__init__(images,rect_x,rect_y)
      self.damage = 2
      self.vel_x = vel_x
      self.vel_y = vel_y
      self.max_x = s_width
      self.max_y = s_height
   

   def validateMove(self):
      if self.rect.y > self.max_y:
         self.kill()
   

# Enemy Bullet. Weak shot, but is fired at an angle and can be targeted.
class EnemyBullet(GameObject):
   
   
   OBJECT_WIDTH = 9
   OBJECT_HEIGHT = 9

   
   SS_COORDINATES = [(220, 1, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height,vel_x=0,vel_y=5):
      
      super().__init__(images,rect_x,rect_y)
      self.damage = 1
      self.vel_x = vel_x
      self.vel_y = vel_y
      self.max_x = s_width
      self.max_y = s_height

   def validateMove(self):
      # If the bullet has gone off the screen, kill it.
      if self.rect.x <= self.min_x or self.rect.y <= self.min_y or self.rect.y >= self.max_y or self.rect.x >= self.max_x: 
         self.kill()

# Player Blaster. We know it's good because it's blue.
class PlayerBlaster(GameObject):
   
   OBJECT_WIDTH = 9
   OBJECT_HEIGHT = 20

   SS_COORDINATES = [(220, 11, OBJECT_WIDTH, OBJECT_HEIGHT) ]
    
   def __init__(self,images,rect_x,rect_y,vel_x=0,vel_y=10):
      
      super().__init__(images,rect_x,rect_y)
      self.damage = 2      
      self.vel_x = vel_x
      self.vel_y = vel_y
      self.min_x = 0
      self.min_y = 0

   def validateMove(self):
      if self.rect.y < self.min_y:
         self.kill()

# Generic class for power ups.
class PowerUp(GameObject):
   
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
  
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.vel_x = 0
      self.vel_y = 2
      self.damage = 0
      self.hit_points = 0
      
   


# Refill shields 
class ShieldPU(PowerUp):
   
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   
    
   SS_COORDINATES = [(231, 1, OBJECT_WIDTH, OBJECT_HEIGHT) ]
     
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      # Shields do negative damage.
      self.damage = -10
      
   


# Bonus points     
class BonusPU(PowerUp):
   
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   
   # Bonus PUs have a point value
   POINT_VALUE = 2000

   
   SS_COORDINATES = [(290, 1, OBJECT_WIDTH, OBJECT_HEIGHT) ] 
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
    
   

 

# Extra blasters
class PowerPU(PowerUp):
   
  
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   

   SS_COORDINATES = [(231, 30, OBJECT_WIDTH, OBJECT_HEIGHT) ]
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)

    
   # Power PUs call the powerUp() method.
   def hit(self,colliding_object):
      if type(colliding_object) is Player:
         colliding_object.powerUp()
      super().hit(colliding_object)
      



# X Weapon - Destroys all enemies on screen.
class XWeaponPU(PowerUp):
   

   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   

   
   SS_COORDINATES = [(290, 30, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
 
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
     
   
   # Business logic for XWeapon is taken care of in the Model class.