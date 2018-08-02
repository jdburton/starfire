#!/usr/bin/env python3
import pygame
import random
import math
import Starfire.utils.spritesheet as spritesheet
 

SPRITESHEET='images/newsprites.bmp'
CK=(255,0,255)


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
   
   OBJECT_WIDTH = 0
   OBJECT_HEIGHT = 0
   FRAME_HOLD = 5
   POINT_VALUE = 0

   def __init__(self,images = [],rect_x=0,rect_y=0,s_width=800,s_height=600):
      super().__init__()
      self.object_images = []
      self.object_frame = 0
      self.vel_x = 0
      self.vel_y = 0
      self.hit_points = 1
      self.damage = 0
      self.setImages(images, rect_x, rect_y)

   # Constrain: Keep the images within the bounds of the screen 

   def constrain(self,width, height):
      self.max_x = width - self.OBJECT_WIDTH
      self.max_y = height - self.OBJECT_HEIGHT
      #print("Max x: %d Max y: %d" % (self.max_x, self.max_y))
      

   # setImages: "Private" method to set the image and position of the sprite.

   def setImages(self,images,rect_x,rect_y):
      self.object_images = images
      self.image = self.object_images[self.object_frame]
      self.rect = self.image.get_rect()
      self.rect.x = rect_x
      self.rect.y = rect_y
   
   # I'm sure there is a better way to do this, but it works well enough.
   def animate(self):
      
      self.object_frame += 1 
      self.image = self.object_images[int(self.object_frame/self.FRAME_HOLD) % len(self.object_images) ]
  
   # Change the velocity of the object
   def changeVelocity(self,x=0,y=0):
      self.vel_x = x
      self.vel_y = y
      
   # Move the object by adding the current velocity to the position.
   def move(self):
      self.rect.x += self.vel_x
      self.rect.y += self.vel_y
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
      return self.hit_points
   

# Class for Player Sprite
class Player(GameObject):
   
   # Constants
      
   OBJECT_WIDTH = 72
   OBJECT_HEIGHT = 73
   SS_COORDINATES = [(1, 1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (74,1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (147,1, OBJECT_WIDTH, OBJECT_HEIGHT) ]
   
   CENTER_CANNON = ((OBJECT_WIDTH/2)-4,-12)
   RIGHT_CANNON = (1, 17)
   LEFT_CANNON =  (OBJECT_WIDTH-9,17)
   
   MAX_HIT_POINTS = 10  
   BASE_FIRE_RATE = 500
   MIN_FIRE_RATE = 125
   POINT_VALUE = 0
  
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y)
      
      # Starting position
      self.start_x = rect_x
      self.start_y = rect_y
      
      # Time created
      self.time_created = pygame.time.get_ticks()
      
      # Collision damage to other objects
      self.damage = 10
      
      # Hit points
      self.hit_points = self.MAX_HIT_POINTS
      
      self.warned = 0
   
      
      # TODO: Implement fire levels:

      # Level 0: Single fire
      # Level 1: Dual fire
      # Level 2: Triple fire
      # Level 3: Rapid (2x) fire
      # Level 4: Turbo (4x) fire

      self.fire_level = 0
      self.active_cannons = (False,True,False)
      self.fire_rate = self.BASE_FIRE_RATE
      self.last_fired = 0
     
      # Constrain to the screen.
      self.constrain(s_width,s_height)
      
   # Fire your weapon   
   def fireWeapon(self):
      
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
         if self.active_cannons[0] is True:
            shots.append(Shot("PlayerBlaster",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],0,-5))
         if self.active_cannons[1] is True:
            shots.append(Shot("PlayerBlaster",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,-5))
         if self.active_cannons[2] is True:
            shots.append(Shot("PlayerBlaster",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],0,-5))

         self.last_fired = now         
         

      return shots
       
   
   def powerUp(self):
     
      if self.fire_level >= 4:
         return
      
      
      self.fire_level += 1
      if self.fire_level == 1:
         self.active_cannons = (True,False,True) 
      else:
         self.active_cannons = (True,True,True)
         if self.fire_level >= 3:
            self.fire_rate /= 2
      
      print("Fire level=%d, Fire rate=%d" % (self.fire_level,self.fire_rate))
 
   
   def reset(self):
      
      self.hit_points = self.MAX_HIT_POINTS
      self.fire_rate = self.BASE_FIRE_RATE
      self.fire_level = 0
      self.rect.x = self.start_x
      self.rect.y = self.start_y
      self.active_cannons = (False,True,False)
      self.time_created = pygame.time.get_ticks()
      pygame.mouse.set_pos([self.start_x,self.start_y])
      self.warned = 0
      
   def hit(self,colliding_object):
      
      now = pygame.time.get_ticks()
      # Five second delay for damage
      #print ("now: %d created %d age %d" % (now, self.time_created, now - self.time_created))
  
      super().hit(colliding_object)
      if colliding_object.damage == 0:
         return -1
      else:
         return self.hit_points 
            
   
      
   # Keep the player on the screen.
   def validateMove(self):
      
      if self.rect.x > self.max_x:
         self.rect.x = self.max_x
         self.vel_x = 0
      elif self.rect.x < 0:
         self.rect.x = 0
         self.vel_x = 0
         
      if self.rect.y > self.max_y:
         self.rect.y = self.max_y
         self.vel_y = 0
      elif self.rect.y < 0:
         self.rect.y = 0
         self.vel_y = 0
      

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
      super().animate()
      # If we've been through one cycle, kill the explosion.
      if self.object_frame/self.FRAME_HOLD >= len(self.object_images):
         self.kill()
         self.object_frame = 0
      
   # Explosions don't care about being hit.
   def hit(self,colliding_object):
      return 0




# Generic Enemy Class
# This has functionality common to multiple enemies

class Enemy(GameObject):
   
   

   # All enemies are constrained to screen by default.
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y)
      self.constrain(s_width,s_height)
      
 
   def move(self):
      #return
      #self.vel_x += random.randint(-1,1)
      #self.vel_y += random.randint(-1,1)
      #super().changeVelocity(self.vel_x,self.vel_y)
      super().move()

   # kill and explode   
   def kill(self):
      super().kill()

    
   # Returns empty list so python won't complain. To be overridden in subclasses.  
   def fireWeapon(self):
      return []
    
   # Acquire the target.
   def acquireTarget(self,starfire):
      self.target_x = starfire.rect.x
      self.target_y = starfire.rect.y  
      
    
   # Aims the shot at (x_dir,y_dir) at s_vel speed.
   # returns shot velocity vector in x,y coordinates.
   def aim(self,x_dir,y_dir,s_vel):  
      
      # Find the angle
      theta = math.atan2(y_dir,x_dir)
   
      
      x_vel = int((s_vel*math.cos(theta))+0.5)
      y_vel = int((s_vel*math.sin(theta))+0.5)
      
 
      return (x_vel,y_vel)
   
   # Standard enemy move validation: Keep the enemy on the screen.
   
   def validateMove(self):
      
      if self.rect.x > self.max_x:
         self.rect.x = self.max_x
         self.vel_x = 0
      elif self.rect.x < 0:
         self.rect.x = 0
         self.vel_x = 0
         
      if self.rect.y > self.max_y:
         self.rect.y = self.max_y
         self.vel_y = 0
      elif self.rect.y < 0:
         self.rect.y = 0
         self.vel_y = 0
   
   # Enemies bounce off each other when they collide. 
   def bounce(self):
      return



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
   
   MAX_HIT_POINTS = 8  
   BASE_FIRE_RATE = 1500

  

   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.hit_points = self.MAX_HIT_POINTS
      self.damage = 5
      self.fire_rate = self.BASE_FIRE_RATE
      self.last_fired = 0
      self.target_x = s_width/2
      self.target_y = s_height-50
      
   
   
      
   def fireWeapon(self):
      
      
      x_dir  = self.target_x-self.rect.x+self.CENTER_CANNON[0]
      y_dir = self.target_y-self.rect.y+self.CENTER_CANNON[1]

      (x_vel,y_vel) = self.aim(x_dir,y_dir,3)
      
      #print("Gunship: Aiming from (%d,%d) to (%d, %d) at (%d,%d)" % (self.rect.x+self.CENTER_CANNON[0],self.target_y-self.rect.y+self.CENTER_CANNON[1],self.target_x,self.target_y,x_vel,y_vel) )
   
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         shots.append(Shot("EnemyBlaster",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],0,5))
         shots.append(Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],x_vel,y_vel))
         shots.append(Shot("EnemyBlaster",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],0,5))

         self.last_fired = now         
      
      return shots
   
   def move(self):
      
      self.vel_x += random.randint(-1,1)
      self.vel_y += random.randint(-1,1)
      super().changeVelocity(self.vel_x,self.vel_y)
      super().move()
   


      
# Enemy Dart Fighter

class Dart(Enemy):

   
   OBJECT_WIDTH = 71
   OBJECT_HEIGHT = 68
   CANNON = OBJECT_WIDTH / 2, OBJECT_HEIGHT
   POINT_VALUE = 400
   

   SS_COORDINATES = [(1, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (147, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (74, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (220, 306, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
   MAX_HIT_POINTS = 3  
   BASE_FIRE_RATE = 1500  
   
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.hit_points = self.MAX_HIT_POINTS
      self.damage = 5
      self.fire_rate = self.BASE_FIRE_RATE
      self.last_fired = 0
      self.max_y = s_height+self.OBJECT_HEIGHT
      
   def fireWeapon(self):
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate:          
         shots.append( Shot("EnemyBullet",self.rect.x+self.CANNON[0],self.rect.y+self.CANNON[1],random.randint(-3,3),random.randint(1,3)))
         self.last_fired = now
      
      return shots
   
   # Attempt to ram the player
   def move(self):
      
      self.vel_x = (self.target_x-self.rect.x+self.CANNON[0])/40

      #dir_y = self.target_y-self.rect.y+self.CANNON[1]
      
      #(self.vel_x,discard) = self.aim(dir_x,dir_y,8)
       
      self.vel_y = 15
      
      #print("Moving (%d,%d)" % (self.vel_y,self.vel_y))
      
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
   
   MAX_HIT_POINTS = 6 
   BASE_FIRE_RATE = 1000  
  
  
   
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      
      self.damage = 3
      self.fire_rate = 3000
      self.last_fired = 0
      
   
   
   def fireWeapon(self):
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         shots.append( Shot("EnemyBullet",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],-2,2))
         shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,3))
         shots.append( Shot("EnemyBullet",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],2,2))
         
         self.last_fired = now         
         # Play the sound
      
      return shots
   
   def move(self):
      #return
      self.vel_x += random.randint(-1,1)
      self.vel_y += random.randint(-1,1)
      super().changeVelocity(self.vel_x,self.vel_y)
      super().move()
      


     
# Enemy Boss

class Boss(Enemy):
   
   '''
   g_pSprite[BOSS_OBJECT] = new CClippedSprite(4,182,169);
   '''
   
   OBJECT_WIDTH = 180
   OBJECT_HEIGHT = 169
   
   LEFT_CANNON = (48, OBJECT_HEIGHT-10)
   RIGHT_CANNON =  (OBJECT_WIDTH-60,OBJECT_HEIGHT-10)
   CENTER_CANNON = (OBJECT_WIDTH / 2, OBJECT_HEIGHT-35)
   POINT_VALUE = 1600
   
   
   '''
      //********** Boss *********
   result = result && g_pSprite[BOSS_OBJECT]->load(&g_cSpriteImages,0,293,236);
   '''
   
   SS_COORDINATES = [(296, 236, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.hit_points = 30
      self.damage = 100
      self.fire_rate = 1500
      self.last_fired = 0
      self.vel_y = 5
      self.last_move = 0
      self.move_rate = 3000
   

   def fireWeapon(self):
      
      
      x_dir  = self.target_x-self.rect.x+self.CENTER_CANNON[0]
      y_dir = self.target_y-self.rect.y+self.CENTER_CANNON[1]

      (x_vel,y_vel) = self.aim(x_dir,y_dir,3)
      
      #print("Aiming from (%d,%d) to (%d, %d) at (%d,%d)" % (self.rect.x+self.CENTER_CANNON[0],self.target_y-self.rect.y+self.CENTER_CANNON[1],self.target_x,self.target_y,x_vel,y_vel) )
   
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         shots.append(Shot("EnemyBlaster",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],0,5))
         shots.append(Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],x_vel,y_vel))
         shots.append(Shot("EnemyBlaster",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],0,5))

         self.last_fired = now         
         # Play the sound
      
      return shots


   def move(self):
      
      dir_x  = self.target_x-self.rect.x+self.CENTER_CANNON[0]
      dir_y = self.target_y-self.rect.y+self.CENTER_CANNON[1]
      
      now = pygame.time.get_ticks()
      
      #TODO: Ram if you can
      if False:
         pass
#      if abs(self.target_x - self.rect.x) <= self.OBJECT_WIDTH:
#         if dir_y >= 0:
#            self.vel_y = 5
#            self.vel_x = 0
#         else:
#            self.vel_y = -3
#            self.vel_x = 0
      
      # otherwise, conventional move
      
      else:
         
         if now - self.last_move >= self.move_rate:
            self.vel_y= random.randint(-3,3)
            self.vel_x = random.randint(-3,3)
            self.last_move = now

         if self.rect.y >= self.max_y:
            self.vel_y = -3
      
         elif self.rect.y <= 0:
            self.vel_y = 3
         
         
               
         if self.rect.x >= self.max_x:
            self.vel_x = -3
      
         elif self.rect.x <= 0:
            self.vel_x = 3
         
         
      
      
      #print("Moving (%d,%d)" % (self.vel_x,self.vel_y))
      
      super().move()

# Enemy Blaster. We know it's bad because it's red.
class EnemyBlaster(GameObject):
   
   '''
   g_pSprite[ENEMY_BLASTER_OBJECT] = new CClippedSprite(1,9,20);
   '''
   
   OBJECT_WIDTH = 9
   OBJECT_HEIGHT = 20
   '''
   result = result && g_pSprite[ENEMY_BLASTER_OBJECT]->load(&g_cSpriteImages,0,220,33);
   '''
   SS_COORDINATES = [(220, 33, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   def __init__(self,images,rect_x,rect_y,s_width,s_height,vel_x=0,vel_y=5):
      
      super().__init__(images,rect_x,rect_y)
      self.damage = 2
      self.vel_x = vel_x
      self.vel_y = vel_y
      self.max_x = s_width
      self.max_y = s_height
   

   def validateMove(self):
      if self.rect.y > 600:
         self.kill()
   

# Enemy Bullet. Weak shot, but is fired at an angle.
class EnemyBullet(GameObject):
   
   '''
   g_pSprite[BULLET_OBJECT] = new CClippedSprite(1,9,9);
   '''
   
   OBJECT_WIDTH = 9
   OBJECT_HEIGHT = 9
   
   '''
   result = result && g_pSprite[BULLET_OBJECT]->load(&g_cSpriteImages,0,220,1);
   '''
   
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
      if self.rect.x <= 0 or self.rect.y <= 0 or self.rect.y >= self.max_y or self.rect.x >= self.max_x: 
         
         self.kill()

# Player Blaster. We know it's good because it's blue.
class PlayerBlaster(GameObject):
   
   '''
   g_pSprite[BLASTER_OBJECT] = new CClippedSprite(1,9,20);
   '''
   
   OBJECT_WIDTH = 9
   OBJECT_HEIGHT = 20
   '''
   result = result && g_pSprite[BLASTER_OBJECT]->load(&g_cSpriteImages,0,220,11);
   '''
   SS_COORDINATES = [(220, 11, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   def __init__(self,images,rect_x,rect_y,vel_x=0,vel_y=5):
      
      super().__init__(images,rect_x,rect_y)
      self.damage = 2      
      self.vel_x = vel_x
      self.vel_y = vel_y
      self.min_x = 0
      self.min_y = 0
   
   
   
   
   def validateMove(self):
      if self.rect.y < 0:
         self.kill()

# Generic class for power ups.
class PowerUp(GameObject):
   
   
   '''
   g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
   '''
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
  
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.vel_x = 0
      self.vel_y = 2
      self.damage = 0
      self.hit_points = 0
      
   
   def hit(self,colliding_object):
      pass

# Refill shields 
class ShieldPU(PowerUp):
   
   '''
   g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
   '''
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   
   
   '''
   result = result && g_pSprite[SHIELD_OBJECT]->load(&g_cSpriteImages,0,231,1);
   '''
    
   SS_COORDINATES = [(231, 1, OBJECT_WIDTH, OBJECT_HEIGHT) ]
     
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
      self.damage = -9
      
   
   def hit(self,colliding_object):
      pass

# Bonus points     
class BonusPU(PowerUp):
   
   '''
   g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
   '''
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   POINT_VALUE = 2000
   
   '''
   result = result && g_pSprite[BONUS_OBJECT]->load(&g_cSpriteImages,0,290,1);
   '''
   
   SS_COORDINATES = [(290, 1, OBJECT_WIDTH, OBJECT_HEIGHT) ] 
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
    
   
   def hit(self,colliding_object):
      pass
 

# Extra blasters
class PowerPU(PowerUp):
   
   '''
   g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
   '''
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   

   '''
   result = result && g_pSprite[POWER_OBJECT]->load(&g_cSpriteImages,0,231,30);
   '''
   

   SS_COORDINATES = [(231, 30, OBJECT_WIDTH, OBJECT_HEIGHT) ]
   
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)

    
   
   def hit(self,colliding_object):
      if type(colliding_object) is Player:
         colliding_object.powerUp()
      



# X Weapon - Destroys all enemies on screen.
class XWeaponPU(PowerUp):
   
   '''
   g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
   '''
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   
   '''
   result = result && g_pSprite[X_OBJECT]->load(&g_cSpriteImages,0,290,30);
   '''
   
   SS_COORDINATES = [(290, 30, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
 
   def __init__(self,images,rect_x,rect_y,s_width,s_height):
      
      super().__init__(images,rect_x,rect_y,s_width,s_height)
     
   
   def hit(self,colliding_object):
      pass