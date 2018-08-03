#!/usr/bin/env python3
#
# James Burton
# jburto2@clemson.edu
# CPSC 8700
# August 3, 2018
# Final Project
#
# Starfire/model.py
#
# This contains the data model for the game and much of the business logic.
# 
# This class contains 
#   1. Several lists of sprites 
#   2. Screen dimensions
#   3. State of available sounds
#   4. Sprite images
#   5. A series of timers
#   6. Global state information, like level, lives, and points
#
#  Information and business logic for the individual game objects is
#  in gameobjects.py
#

import pygame
import random
import Starfire.utils.background as background
import Starfire.gameobjects as gameobjects

INIT_LIVES = 3
INIT_LEVEL = 1

class Model():

   
   def __init__(self,width,height):
      
      # should this sound be played?
      self.sound_state = {}
      
      # screen dimensions
      self.screen_width = width
      self.screen_height = height
      
      # Because PyGame ties data and images together in pygame.sprite.Sprite, the images need
      # to be with the data in the model, not in the view.
      self.sprite_images = {}
      
      
      # sprite group for player
      # sprite group for enemies
      # sprite group for shots
      # sprite group for enemy shots
      # sprite group for power ups
      # sprite group for explosions
      self.player_objects = pygame.sprite.Group()
      self.enemy_objects = pygame.sprite.Group()
      self.enemy_shot_objects = pygame.sprite.Group()
      self.shot_objects = pygame.sprite.Group()
      self.powerup_objects = pygame.sprite.Group()
      self.explosion_objects = pygame.sprite.Group()
      

   # start a new game   
   def initGame(self):

      self.lives = INIT_LIVES
      self.level = INIT_LEVEL
      self.enemy_rate = 1000
      self.boss_interval = 40000
      self.last_enemy = pygame.time.get_ticks()
      self.last_pu = pygame.time.get_ticks()
      self.last_boss = pygame.time.get_ticks()
      self.pu_rate = 10000
      self.points = 0  
      
      # empty the sprite groups    
      self.player_objects.empty()
      self.enemy_objects.empty()
      self.enemy_shot_objects.empty()
      self.shot_objects.empty()
      self.powerup_objects.empty()
      self.explosion_objects.empty()
      
      # create playerOne and boss
      self.createPlayerOne()
      self.createBossSprite()

   # Create the boss and reset it to default     
   def createBossSprite(self):
      self.theBoss = gameobjects.Boss(self.sprite_images['Boss'],0,0,self.screen_width,self.screen_height)
      self.theBoss.reset()
      
   # Create player One and add it to the player_objects
   def createPlayerOne(self):   
      
      self.playerOne = gameobjects.Player(self.sprite_images['Player'],self.screen_width/2,(self.screen_height-gameobjects.Player.OBJECT_HEIGHT),self.screen_width,self.screen_height);
      self.playerOne.reset();
      self.player_objects.add(self.playerOne)

   
   # create enemies
   def createEnemies(self): 
      
      # Stop creating enemies if a boss is alive
      if self.createBoss() is True:
         return
      
      now = pygame.time.get_ticks()
      
      #print("model.createEnemies() boss_mode=%r, enemy_rate=%d, now=%d,last_enemy=%d" % (self.boss_mode,self.enemy_rate,now,self.last_enemy))
      
      # if we have recently created an enemy, don't create another one
      if now - self.last_enemy < self.enemy_rate:  
         return
          
      # Which enemy?
      type_idx = random.randint(0,5)
      
      # 0 is a gunship
      if type_idx % 6 == 0:
         type = "Gunship"
      # 2, 4, are darts
      elif type_idx % 2 == 0:
         type = "Dart"
      # 1, 3, 5 is a drone
      else:
         type = "Drone"
      
      # place randomly at the top of the screen
      pos_x = random.randint(50,self.screen_width - 50)
      
      #TODO: Recycle sprites instead of creating new ones. Or does python's GC do it better?
      
      if type == "Gunship":
         enemy = gameobjects.Gunship(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "Drone":
         enemy = gameobjects.Drone(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "Dart":
         enemy = gameobjects.Dart(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
         self.sound_state['Flyby'] = True
      
      # Add to the sprite group
      self.enemy_objects.add(enemy)  
      
      # When do we make the next enemy? Sooner on higher levels!
      self.last_enemy = now
      rate_max = 5000 - (500 * (self.level-1))
      rate_min = 2000 - (200 * (self.level-1))
      if rate_min > rate_max:
         self.enemy_rate = rate_min
      else:   
         self.enemy_rate = random.randint(rate_min,rate_max)       


   # Create the boss
   def createBoss(self):
      
         # if we have a boss already, we don't need another one!
         if self.theBoss.alive():
            #print("The boss is alive!")
            return True
         
         # is it time to create the boss?
         now = pygame.time.get_ticks()
         if now - self.last_boss < self.boss_interval:
            return False
         
         # reset the boss for this level and add it to the enemies list
         self.theBoss.reset(self.level)
         self.enemy_objects.add(self.theBoss)
         return True
  
      
   # Create power ups
   def createPowerUps(self): 
      
      pu_types = [ 'BonusPU', 'PowerPU', 'ShieldPU','XWeaponPU' ]

      
      now = pygame.time.get_ticks()
      
      if now - self.last_pu < self.pu_rate:  
         return
      
      # Shield, Bonus, and Power are common. Weapon X is not.
      type_idx = int(random.randint(0,9) / 3) ;
   
      type = pu_types[type_idx]

      # Place randomly at top of screen.
      pos_x = random.randint(50,self.screen_width - 50)
      
      if type == "BonusPU":
         pu = gameobjects.BonusPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "PowerPU":
         pu = gameobjects.PowerPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "ShieldPU":
         pu = gameobjects.ShieldPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "XWeaponPU":
         pu = gameobjects.XWeaponPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      
      # Place power up on screen
      self.powerup_objects.add(pu)  
      
      # Next power up? Later on higher levels
      self.last_pu = now
      rate_max = 20000 + (1000 * (self.level-1))
      rate_min = 7000 + (1000 * (self.level-1))
      self.pu_rate = random.randint(rate_min,rate_max)    
   
   # Animate the sprites
   def animate(self):
      self.playerOne.animate()
      for object in self.enemy_objects:
         object.animate()
      for explosion in self.explosion_objects:
         explosion.animate()
 
   # Move the player x,y distance. For keyboard/joystick control.      
   def movePlayer(self,x,y):   
      self.playerOne.moveTo(self.playerOne.rect.x+x,self.playerOne.rect.y+y)     
   
   # Move the player to point (x,y) on the screen. For mouse control.
   def movePlayerTo(self,x,y): 
      self.playerOne.moveTo(x,y)
   
   # Move the objects
   def moveObjects(self):
      for enemy in self.enemy_objects:
         # Spot player one and react
         enemy.acquireTarget(self.playerOne)
         enemy.move()
         self.fireEnemyWeapons(enemy)
      for sprite in self.shot_objects:
         sprite.move()
      for sprite in self.enemy_shot_objects:
         sprite.move()
      for sprite in self.powerup_objects:
         sprite.move()

   # Helper method to fire enemy weapons.
   def fireEnemyWeapons(self,enemy):    
      # shots come from the enemy
      shots = enemy.fireWeapon(self.level)
      # process them and create sprites
      for cannon in shots:
         if cannon is not None:
            if cannon.name == "EnemyBlaster":
               blast = gameobjects.EnemyBlaster(self.sprite_images[cannon.name],cannon.x_pos,cannon.y_pos,self.screen_width,self.screen_height,cannon.x_vel,cannon.y_vel)   
            elif cannon.name == "EnemyBullet":
               blast = gameobjects.EnemyBullet(self.sprite_images[cannon.name],cannon.x_pos,cannon.y_pos,self.screen_width,self.screen_height,cannon.x_vel,cannon.y_vel)
         # Add to the list
         self.enemy_shot_objects.add(blast)
         # Pew! Pew!    
         self.sound_state['EnemyBlaster'] = True
   
   # fire the player's weapon
   def fireWeapon(self):
      
      # fire the weapon
      shots = self.playerOne.fireWeapon()
      # process shots and create sprites
      for cannon in shots:
         if cannon is not None:
            blast = gameobjects.PlayerBlaster(self.sprite_images["PlayerBlaster"],cannon.x_pos,cannon.y_pos,cannon.x_vel,cannon.y_vel)
            self.shot_objects.add(blast)
         self.sound_state['Blaster'] = True
      

   # Collision detection: The fun stuff!
   def collisionDetection(self):
      
      hp = gameobjects.NO_DAMAGE 
      kill_em_all = False
  
      # Blaster vs enemy: Kill blaster, damage enemy
      blaster_hits = pygame.sprite.groupcollide(self.shot_objects, self.enemy_objects, True, False )
      for hit in blaster_hits.keys():
         enemy = blaster_hits[hit][0]
         enemy.hit(hit)
         self.checkDeath(enemy)
         
      
      # Power ups! 
      powerup_hits = pygame.sprite.groupcollide(self.powerup_objects,self.player_objects, False, False)
      for powerup in powerup_hits:
         powerup.hit(self.playerOne)
         self.playerOne.hit(powerup)
         # Is this Weapon X? 
         if type(powerup) is gameobjects.XWeaponPU:
            kill_em_all = True
         self.checkDeath(powerup)
      
      # Why yes, it IS Weapon X. Kill 'em all!
      if kill_em_all:
         for enemy in self.enemy_objects.sprites():
            # Weapon X does not kill bosses, but does 20 points of damage.
            # Play the exposion sound, even if it did not kill the boss.
            enemy.hit_points -= 20
            self.checkDeath(enemy)
            self.sound_state['Explosion'] = True
               
        
      
      now = pygame.time.get_ticks()
      # 2 second grace period for player damage. 
      if now - self.playerOne.time_created > 2000:  
         # Player vs enemy = damage to both         
         player_hits = pygame.sprite.groupcollide(self.enemy_objects, self.player_objects, False, False)
         for enemy in player_hits:
            enemy.hit(self.playerOne)
            self.playerOne.hit(enemy)
            # If the enemy is still alive, we have a hit.
            if enemy.alive():
               self.sound_state['EnemyHit'] = True
         
         # enemy shot vs player: Kill blaster, damage self
         blaster_hits = pygame.sprite.groupcollide(self.enemy_shot_objects, self.player_objects, True, False )
         for hit in blaster_hits.keys():
            player = blaster_hits[hit][0]
            hp = player.hit(hit)
            
      #print("hp=%d warned=%d" % (hp,self.playerOne.warned))
      # Aaaaaaaaagh!
      if self.checkDeath(self.playerOne):
         self.sound_state['Dying'] = True
      
      # One more hit and you're dead. Probably should know.   
      elif hp <= 2 and hp != gameobjects.NO_DAMAGE and self.playerOne.warned == 0:
         if random.randint(0,1):
            self.sound_state['Warn1'] = True
         else:   
            self.sound_state['Warn2'] = True
         self.playerOne.warned = 1
      # Otherwise, play shield hit.
      elif hp > 1:
         self.sound_state['Hit'] = True
      
      # Reset warning if you got a shield PU
      if hp > 2 and self.playerOne.warned == 1:
          self.playerOne.warned = 0
      
          
   # Did the object just die?
   def checkDeath(self,object):
         
      # Nope, already dead.
      if not object.alive():
         return False
      
      # Nope, still have hit points
      if object.hit_points > 0:
         return False
      
      # If I'm here, I must have just died.
      
      # Add up the points
      self.points += object.POINT_VALUE
      # Bosses have big explosions and reset boss mode
      if type(object) is gameobjects.Boss:
         # TODO: Make one big explosion instead of five little ones.
         self.createExplosion(object.rect.x,object.rect.y)
         self.createExplosion(object.rect.x+object.OBJECT_WIDTH,object.rect.y)
         self.createExplosion(object.rect.x,object.rect.y+object.OBJECT_HEIGHT)
         self.createExplosion(object.rect.x+object.OBJECT_WIDTH,object.rect.y+object.OBJECT_HEIGHT)
         self.createExplosion(object.rect.x+object.OBJECT_WIDTH/2,object.rect.y+object.OBJECT_HEIGHT/2)
         
         # Reset boss information.
         self.last_boss = pygame.time.get_ticks()
         self.last_enemy = self.last_boss
         self.level += 1
      # If the object explodes, blow it up!
      elif object.explodes():
         self.createExplosion(object.rect.x,object.rect.y)
      object.kill()
      return True
 
   # Boom!  
   def createExplosion(self,x,y,type="Explosion"):
      # Explosion only type implemented for now.
      type = "Explosion"
      explosion = gameobjects.Explosion(self.sprite_images[type],x,y)
      self.explosion_objects.add(explosion)
      self.sound_state[type] = True
   
   # Is this really the end?
   def checkGameOver(self):
      
      # If the player is dead, check for more lives.
      if len(self.player_objects.sprites()) == 0:
         # No more lives. Game over.
         if self.lives <= 0:
            return True
         
         # Lose a life and reset player
         self.lives -= 1
         #print("lives remaining %d" % self.lives)
         self.playerOne.reset();
         self.sound_state['NewShip1'] = True
         self.player_objects.add(self.playerOne)

      return False
   
   

      