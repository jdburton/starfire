#!/usr/bin/env python3
import pygame
import random

   
SPRITESHEET='images/newsprites.bmp'
CK=(255,0,255)

# Generic GameObject class. 
# All GameObjects are Sprites with game specific data and functionality.


class GameObject(pygame.sprite.Sprite):
   
   OBJECT_WIDTH = 0
   OBJECT_HEIGHT = 0
   FRAME_HOLD = 5

   def __init__(self):
      super().__init__()
      self.object_images = []
      self.object_frame = 0
      self.vel_x = 0
      self.vel_y = 0


   def constrain(self,width, height):
      self.max_x = width - self.OBJECT_WIDTH
      self.max_y = height - self.OBJECT_HEIGHT
      #print("Max x: %d Max y: %d" % (self.max_x, self.max_y))
      
   def init(self):
      pass

   def setImages(self,images,x_pos,y_pos,d_images=[]):
      self.object_images = images
      self.image = self.object_images[self.object_frame]
      self.rect = self.image.get_rect()
      self.rect.x = x_pos
      self.rect.y = y_pos
   
   def animate(self):
      
      self.object_frame += 1 
      self.image = self.object_images[int(self.object_frame/self.FRAME_HOLD) % len(self.object_images) ]
  
   
   def move(self,delta_x=0,delta_y=0):
      self.rect.x += delta_x
      self.rect.y += delta_y
      self.validateMove()
   
   def moveTo(self,x_coord,y_coord):
      self.rect.x = x_coord
      self.rect.y = y_coord
      self.validateMove()
   
   def validateMove(self):
      #print ("Validating (%d,%d)" % (self.rect.x,self.rect.y))
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
         
      #print ("Validated to (%d,%d)" % (self.rect.x,self.rect.y))
   
# Object for Player Sprite

class Player(GameObject):
   
   
   
   OBJECT_WIDTH = 72
   OBJECT_HEIGHT = 73
   SS_COORDINATES = [(1, 1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (74,1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (147,1, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass
   
class Explosion(GameObject):
   
   
   '''
   g_pSprite[EXPLOSION_OBJECT] = new CClippedSprite(5,99,99);
   '''
   
   OBJECT_WIDTH = 99
   OBJECT_HEIGHT = 99
   
   '''
   
   result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,0,1,136);
   result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,1,101,136);
   result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,2,301,136);
   result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,3,201,136);
   result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,4,401,136);
   '''
   
   SS_COORDINATES = [   (1,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (101,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (301,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (201,136,OBJECT_WIDTH, OBJECT_HEIGHT),
                            (401,136,OBJECT_WIDTH, OBJECT_HEIGHT)]
   
   
   
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass


# Generic Enemy Class

class Enemy(GameObject):
   
   def __init__(self):
      
      super().__init__()

      
   
   def hit(self,colliding_object):
      pass
   
   def move(self):
      self.vel_x += random.randint(-1,1)
      self.vel_y += random.randint(-1,1)
      super().move(self.vel_x,self.vel_y)

   
# Enemy Gunship

class Gunship(Enemy):
   
   '''
   g_pSprite[GUNSHIP_OBJECT]= new CClippedSprite(4,73,58);
   '''
   
   OBJECT_WIDTH = 73
   OBJECT_HEIGHT = 58
   
   '''
   result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,0,1,75);
   result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,1,76,75);
   result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,2,150,75);
   result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,3,226,75);
   '''
   
   SS_COORDINATES = [(1, 75, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (76,75, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (150,75, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (226,75, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  

   def __init__(self):
      
      super().__init__()
      

   
   def hit(self,colliding_object):
      pass
      
# Enemy Dart Fighter

class Dart(Enemy):
   
   '''
   g_pSprite[DART_OBJECT] = new CClippedSprite(4,71,68);
   '''
   
   OBJECT_WIDTH = 71
   OBJECT_HEIGHT = 68
   
   '''
      //========= Dart =======//
   result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,0,1,306);
   result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,1,147,306);
   result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,2,74,306);
   result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,3,220,306);
   
   '''
   SS_COORDINATES = [(1, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (147, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (74, 306, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (220, 306, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass
 
# Enemy Drone Fighter

class Drone(Enemy):
   
   '''
   g_pSprite[DRONE_OBJECT] = new CClippedSprite(4,79,68);
   '''
   
   OBJECT_WIDTH = 79
   OBJECT_HEIGHT = 68
   
   '''
   //Drone

   result = result && g_pSprite[DRONE_OBJECT]->load(&g_cSpriteImages,0,1,236);
   '''
   
   SS_COORDINATES = [(1, 236, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass
   
     
# Enemy Boss

class Boss(Enemy):
   
   '''
   g_pSprite[BOSS_OBJECT] = new CClippedSprite(4,182,169);
   '''
   
   OBJECT_WIDTH = 182
   OBJECT_HEIGHT = 169
   
   '''
      //********** Boss *********
   result = result && g_pSprite[BOSS_OBJECT]->load(&g_cSpriteImages,0,293,236);
   '''
   
   SS_COORDINATES = [(296, 236, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass
   

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
  
  
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass

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
  
   
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass

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
  
  
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass

# Generic class for power ups.
class PowerUp(GameObject):
   
   
   '''
   g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
   '''
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
  
   def __init__(self):
      
      super().__init__()
      
   
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
     
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass

# Bonus points     
class BonusPU(PowerUp):
   
   '''
   g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
   '''
   
   OBJECT_WIDTH = 57
   OBJECT_HEIGHT = 27
   
   '''
   result = result && g_pSprite[BONUS_OBJECT]->load(&g_cSpriteImages,0,290,1);
   '''
   
   SS_COORDINATES = [(290, 1, OBJECT_WIDTH, OBJECT_HEIGHT) ] 
   
   def __init__(self):
      
      super().__init__()
      
   
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
   
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass



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
  
 
   def __init__(self):
      
      super().__init__()
      
   
   def hit(self,colliding_object):
      pass