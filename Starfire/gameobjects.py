#!/usr/bin/env python3
import pygame
import random
import math

   
SPRITESHEET='images/newsprites.bmp'
CK=(255,0,255)

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

   def __init__(self):
      super().__init__()
      self.object_images = []
      self.object_frame = 0
      self.vel_x = 0
      self.vel_y = 0
      self.hitPoints = 1
      self.damage = 0
      

   def constrain(self,width, height):
      self.max_x = width - self.OBJECT_WIDTH
      self.max_y = height - self.OBJECT_HEIGHT
      #print("Max x: %d Max y: %d" % (self.max_x, self.max_y))
      

   def setImages(self,images,x_pos,y_pos,d_images=[]):
      self.object_images = images
      self.image = self.object_images[self.object_frame]
      self.rect = self.image.get_rect()
      self.rect.x = x_pos
      self.rect.y = y_pos
   
   # I'm sure there is a better way to do this, but it works well enough.
   def animate(self):
      
      self.object_frame += 1 
      self.image = self.object_images[int(self.object_frame/self.FRAME_HOLD) % len(self.object_images) ]
  
   def changeVelocity(self,x=0,y=0):
      self.vel_x = x
      self.vel_y = y
      
   
   def move(self):
      self.rect.x += self.vel_x
      self.rect.y += self.vel_y
      self.validateMove()
   
   def moveTo(self,x_coord,y_coord):
      self.rect.x = x_coord
      self.rect.y = y_coord
      self.validateMove()
   
   def validateMove(self):
      #print ("Validating (%d,%d)" % (self.rect.x,self.rect.y))
      pass
   
    
      
   def hit(self,colliding_object):
      self.hitPoints -= colliding_object.damage
   
# Object for Player Sprite

class Player(GameObject):
   
   
   
   OBJECT_WIDTH = 72
   OBJECT_HEIGHT = 73
   SS_COORDINATES = [(1, 1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (74,1, OBJECT_WIDTH, OBJECT_HEIGHT),
                     (147,1, OBJECT_WIDTH, OBJECT_HEIGHT) ]
   
   CENTER_CANNON = ((OBJECT_WIDTH/2)-4,-12)
   RIGHT_CANNON = (1, 17)
   LEFT_CANNON =  (OBJECT_WIDTH-9,17)
  
  
   
   
   def __init__(self,s_width,s_height):
      
      super().__init__()
      self.damage = 10
      self.hitPoints = 10
      self.time_created = pygame.time.get_ticks()
      self.fire_rate = 500
      self.last_fired = 0
      self.constrain(s_width,s_height)
      
      
   def fireWeapon(self):
      
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         shots.append(Shot("PlayerBlaster",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],0,-5))
         shots.append(Shot("PlayerBlaster",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,-5))
         shots.append(Shot("PlayerBlaster",self.rect.x+self.RIGHT_CANNON[0],self.rect.y+self.RIGHT_CANNON[1],0,-5))

         self.last_fired = now         
         # Play the sound

         sound = pygame.mixer.Sound('sounds/blaster.wav')
         sound.play()
      
      return shots
       
   
   def reset(self,x,y):
      self.hitPoints = 10
      self.rect.x = x
      self.rect.y = y
      self.time_created = pygame.time.get_ticks()
      pygame.mouse.set_pos([x,y])
      
   def hit(self,colliding_object):
      
      now = pygame.time.get_ticks()
      # Five second delay for damage
      print ("now: %d created %d age %d" % (now, self.time_created, now - self.time_created))
      if now - self.time_created > 300:
         super().hit(colliding_object)
      if colliding_object.damage > 0:
         if self.hitPoints > 1: 
            sound = pygame.mixer.Sound('sounds/ehitshield.wav')
            sound.play()
         elif self.hitPoints == 1: 
            sound = pygame.mixer.Sound('sounds/killed2.wav')
            sound.play()
      
   def kill(self):
      super().kill()
      
      sound = pygame.mixer.Sound('sounds/dying.wav')
      sound.play()
      
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
   
   def animate(self):
      super().animate()
      if self.object_frame/self.FRAME_HOLD >= len(self.object_images):
         self.kill()
         self.object_frame = 0
      
   
   def hit(self,colliding_object):
      pass




# Generic Enemy Class

class Enemy(GameObject):
   
   

   
   def __init__(self,s_width,s_height):
      
      super().__init__()
      self.constrain(s_width,s_height)
      
   
   

   
   def move(self):
      #return
      #self.vel_x += random.randint(-1,1)
      #self.vel_y += random.randint(-1,1)
      #super().changeVelocity(self.vel_x,self.vel_y)
      super().move()

   
   def kill(self):
      super().kill()
      sound = pygame.mixer.Sound('sounds/EXPLOSION.WAV')
      sound.play()
      
   def fireWeapon(self):
      return []
    
   def acquireTarget(self,starfire):
      self.target_x = starfire.rect.x
      self.target_y = starfire.rect.y  
      
    
   # Use trig to aim the shot.
   def aim(self,x_dir,y_dir,s_vel):  
      theta = math.atan2(y_dir,x_dir)
      
      if (theta == 0):
         x_vel = s_vel
         y_vel = 0
      elif (theta == 1):
         y_vel = s_vel
         x_vel = 0
      else:
         x_vel = int((s_vel/math.sin(theta))+0.5)
         y_vel = int((s_vel/math.cos(theta))+0.5)
      
      if (y_vel < 0):
         x_vel = -x_vel
         y_vel = -y_vel  
      
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
   
# Enemy Gunship

class Gunship(Enemy):
   
   '''
   g_pSprite[GUNSHIP_OBJECT]= new CClippedSprite(4,73,58);
   '''
   
   OBJECT_WIDTH = 73
   OBJECT_HEIGHT = 58
   CENTER_CANNON = None
   LEFT_CANNON = (5, OBJECT_HEIGHT-10)
   RIGHT_CANNON =  (OBJECT_WIDTH-13,OBJECT_HEIGHT-10)
   CENTER_CANNON = OBJECT_WIDTH / 2, OBJECT_HEIGHT-15
   
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
  

   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
      self.hitPoints = 7
      self.damage = 5
      self.fire_rate = 1500
      self.last_fired = 0
      self.target_x = 400
      self.target_y = 500
      
   
   
      
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
      #return
      self.vel_x += random.randint(-1,1)
      self.vel_y += random.randint(-1,1)
      super().changeVelocity(self.vel_x,self.vel_y)
      super().move()
   


      
# Enemy Dart Fighter

class Dart(Enemy):
   
   '''
   g_pSprite[DART_OBJECT] = new CClippedSprite(4,71,68);
   '''
   
   OBJECT_WIDTH = 71
   OBJECT_HEIGHT = 68
   CANNON = OBJECT_WIDTH / 2, OBJECT_HEIGHT
   
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
  
  
   
   
   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
      self.hitPoints = 2
      self.damage = 4
      self.fire_rate = 2000
      self.last_fired = 0
      self.max_y = s_height+self.OBJECT_HEIGHT
      
   def fireWeapon(self):
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         
         shots.append( Shot("EnemyBullet",self.rect.x+self.CANNON[0],self.rect.y+self.CANNON[1],random.randint(-3,3),random.randint(1,3)))

         self.last_fired = now         
         # Play the sound
      
      return shots
   
   def move(self):
      
      dir_x  = self.target_x-self.rect.x+self.CANNON[0]
      dir_y = self.target_y-self.rect.y+self.CANNON[1]
      
      (self.vel_x,discard) = self.aim(dir_x,dir_y,8)
      self.vel_y = 8
      
      print("Moving (%d,%d)" % (self.vel_y,self.vel_y))
      
      super().move()
      
   # Darts fly off the screen. Override Enemy.validateMove() here.
   def validateMove(self):
      if self.rect.y >= self.max_y:
         self.kill()
 
# Enemy Drone Fighter

class Drone(Enemy):
   
   '''
   g_pSprite[DRONE_OBJECT] = new CClippedSprite(4,79,68);
   '''
   
   OBJECT_WIDTH = 79
   OBJECT_HEIGHT = 68
   
   
   LEFT_CANNON = (1, OBJECT_HEIGHT-17)
   RIGHT_CANNON =  (OBJECT_WIDTH-9,OBJECT_HEIGHT-17)
   CENTER_CANNON = OBJECT_WIDTH / 2, OBJECT_HEIGHT
   
   '''
   //Drone

   result = result && g_pSprite[DRONE_OBJECT]->load(&g_cSpriteImages,0,1,236);
   '''
   
   SS_COORDINATES = [(1, 236, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
      self.hitPoints = 3
      self.damage = 3
      self.fire_rate = 3000
      self.last_fired = 0
      
   
   
   def fireWeapon(self):
       
      now = pygame.time.get_ticks()
      
      shots = []
      
      if now - self.last_fired > self.fire_rate: 
   
         shots.append( Shot("EnemyBullet",self.rect.x+self.LEFT_CANNON[0],self.rect.y+self.LEFT_CANNON[1],-2,2))
         shots.append( Shot("EnemyBullet",self.rect.x+self.CENTER_CANNON[0],self.rect.y+self.CENTER_CANNON[1],0,2))
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
   
   
   '''
      //********** Boss *********
   result = result && g_pSprite[BOSS_OBJECT]->load(&g_cSpriteImages,0,293,236);
   '''
   
   SS_COORDINATES = [(296, 236, OBJECT_WIDTH, OBJECT_HEIGHT) ]
  
  
   
   
   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
      self.hitPoints = 30
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
      
      # Ram if you can
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
         
         
      
      
      print("Moving (%d,%d)" % (self.vel_x,self.vel_y))
      
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
  
  
   def __init__(self,s_width,s_height,vel_x=0,vel_y=5):
      
      super().__init__()
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
  
   
   def __init__(self,s_width,s_height,vel_x=0,vel_y=5):
      
      super().__init__()
      self.damage = 2
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
  
  
   def __init__(self,vel_x=0,vel_y=5):
      
      super().__init__()
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
  
   def __init__(self,s_width,s_height):
      
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
     
   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
      
   
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
   
   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
    
   
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
   
   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
    
   
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
  
 
   def __init__(self,s_width,s_height):
      
      super().__init__(s_width,s_height)
     
   
   def hit(self,colliding_object):
      pass