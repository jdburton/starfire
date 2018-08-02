import Starfire.utils.background as background

import Starfire.gameobjects as gameobjects
import pygame
import random


class Model():

   
   def __init__(self,width,height):
      
      self.sound_state = {}
      
       

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
      self.player_objects = pygame.sprite.Group()
      self.enemy_objects = pygame.sprite.Group()
      self.enemy_shot_objects = pygame.sprite.Group()
      self.shot_objects = pygame.sprite.Group()
      self.powerup_objects = pygame.sprite.Group()
      self.explosion_objects = pygame.sprite.Group()
      

      

   
   def initGame(self):

      self.lives = 0
      self.enemy_rate = 0
      self.last_enemy = 0
      self.points = 0      
      self.player_objects.empty()
      self.enemy_objects.empty()
      self.enemy_shot_objects.empty()
      self.shot_objects.empty()
      self.powerup_objects.empty()
      self.explosion_objects.empty()
      self.createPlayerOne()
      

      
   
   def createPlayerOne(self):   
      
      self.playerOne = gameobjects.Player(self.sprite_images['Player'],self.screen_width/2,(self.screen_height-gameobjects.Player.OBJECT_HEIGHT),self.screen_width,self.screen_height);
      self.playerOne.reset();
      self.player_objects.add(self.playerOne)                 

   
   
   def createEnemies(self): 
      
      enemy_types = [ 'Gunship', 'Drone', 'Dart','Boss' ]
      
      now = pygame.time.get_ticks()
      
      if now - self.last_enemy < self.enemy_rate:  
         return
      
      
      type_idx = int(random.randint(0,9) / 3) ;
   
      type = enemy_types[type_idx]
      
      pos_x = random.randint(50,self.screen_width - 50)
      
      if type == "Gunship":
         enemy = gameobjects.Gunship(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "Drone":
         enemy = gameobjects.Drone(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "Dart":
         enemy = gameobjects.Dart(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "Boss":
         enemy = gameobjects.Boss(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      
      self.enemy_objects.add(enemy)  
      
      self.last_enemy = now
      self.enemy_rate = random.randint(1000,5000)       

   
   def animate(self):
      self.playerOne.animate()
      for object in self.enemy_objects:
         object.animate()
      for explosion in self.explosion_objects:
         explosion.animate()
 
         
   def movePlayer(self,x,y):   
      self.playerOne.moveTo(self.playerOne.rect.x+x,self.playerOne.rect.y+y)     
   
   def movePlayerTo(self,x,y): 
      self.playerOne.moveTo(x,y)
   
   def moveObjects(self):
      for enemy in self.enemy_objects:
         enemy.acquireTarget(self.playerOne)
         enemy.move()
         self.fireEnemyWeapons(enemy)
      for sprite in self.shot_objects:
         sprite.move()
      for sprite in self.enemy_shot_objects:
         sprite.move()

   def fireEnemyWeapons(self,enemy):
      
      shots = enemy.fireWeapon()
      for cannon in shots:
         if cannon is not None:
            if cannon.name == "EnemyBlaster":
               blast = gameobjects.EnemyBlaster(self.sprite_images[cannon.name],cannon.x_pos,cannon.y_pos,self.screen_width,self.screen_height,cannon.x_vel,cannon.y_vel)   
            elif cannon.name == "EnemyBullet":
               blast = gameobjects.EnemyBullet(self.sprite_images[cannon.name],cannon.x_pos,cannon.y_pos,self.screen_width,self.screen_height,cannon.x_vel,cannon.y_vel)

         self.enemy_shot_objects.add(blast)       
         self.sound_state['EnemyBlaster'] = True
   
   def fireWeapon(self):
      
      # fire the weapon
      shots = self.playerOne.fireWeapon()
      
      for cannon in shots:
         if cannon is not None:
            blast = gameobjects.PlayerBlaster(self.sprite_images["PlayerBlaster"],cannon.x_pos,cannon.y_pos,cannon.x_vel,cannon.y_vel)
            self.shot_objects.add(blast)
         self.sound_state['Blaster'] = True
      
      
      # Restrict blaster fire to three sound channels.
      
      #for id in range(0,2):
      #   channel = pygame.mixer.Channel(id)
      #   if not channel.get_busy():
      #      channel.play(self.sound_manager['Blaster'])
      
   def collisionDetection(self):
      hp = -1 
      # enemy vs enemy = Bounce
      collided_enemies = pygame.sprite.groupcollide(self.enemy_objects, self.enemy_objects, False, False)
      for enemy in collided_enemies:
         if len(collided_enemies[enemy]) > 1: 
            enemy.bounce()



      
      # Blaster vs enemy: Kill blaster, damage enemy
      blaster_hits = pygame.sprite.groupcollide(self.shot_objects, self.enemy_objects, True, False )
      for hit in blaster_hits.keys():
         enemy = blaster_hits[hit][0]
         enemy.hit(hit)
         self.checkDeath(enemy)
      
      
      now = pygame.time.get_ticks()
      # 1000 tick grace period. 
      if now - self.playerOne.time_created > 1000:  
         # Player vs enemy = damage to both         
         player_hits = pygame.sprite.groupcollide(self.enemy_objects, self.player_objects, False, False)
         for enemy in player_hits:
            enemy.hit(self.playerOne)
            self.playerOne.hit(enemy)
            self.checkDeath(enemy)
         
         # enemy shot vs player: Kill blaster, damage self
         blaster_hits = pygame.sprite.groupcollide(self.enemy_shot_objects, self.player_objects, True, False )
         for hit in blaster_hits.keys():
            player = blaster_hits[hit][0]
            hp = player.hit(hit)
      
      if self.checkDeath(self.playerOne):
         self.sound_state['Dying'] = True
      elif hp == 1 and self.playerOne.warned == 0:
         if random.randint(0,1):
            
            self.sound_state['Warn1'] = True
         else:
            
            self.sound_state['Warn1'] = True
         self.playerOne.warned = 1
      elif hp > 1:
         self.sound_state['Hit'] = True
         
      
          
   
   def checkDeath(self,object):
         # Is the object dead?
         if object.hit_points <= 0 and object.alive():
            self.points += object.POINT_VALUE
            self.createExplosion(object.rect.x,object.rect.y)
            object.kill()
            return True
         return False
      
   def createExplosion(self,x,y):
      explosion = gameobjects.Explosion(self.sprite_images['Explosion'],x,y)
      self.explosion_objects.add(explosion)
      self.sound_state['Explosion'] = True
   
   def checkGameOver(self):
      
      if len(self.player_objects.sprites()) == 0:
         if self.lives > 0:

            self.lives -= 1
            print("lives remaining %d" % self.lives)
            self.playerOne.reset();
            self.sound_state['NewShip1'] = True
            self.player_objects.add(self.playerOne)
            
         else:

            return True
      return False
      