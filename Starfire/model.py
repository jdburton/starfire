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

      self.lives = 3
      self.level = 1
      self.enemy_rate = 1000
      self.boss_interval = 40000
      self.last_enemy = pygame.time.get_ticks()
      self.last_pu = pygame.time.get_ticks()
      self.last_boss = pygame.time.get_ticks()
      self.pu_rate = 10000
      self.points = 0      
      self.player_objects.empty()
      self.enemy_objects.empty()
      self.enemy_shot_objects.empty()
      self.shot_objects.empty()
      self.powerup_objects.empty()
      self.explosion_objects.empty()
      self.createPlayerOne()
      self.createBossSprite()
    
      
                       

      

      
      
   def createBossSprite(self):
      self.theBoss = gameobjects.Boss(self.sprite_images['Boss'],0,0,self.screen_width,self.screen_height)
      self.theBoss.reset()
      
   
   def createPlayerOne(self):   
      
      self.playerOne = gameobjects.Player(self.sprite_images['Player'],self.screen_width/2,(self.screen_height-gameobjects.Player.OBJECT_HEIGHT),self.screen_width,self.screen_height);
      self.playerOne.reset();
      self.player_objects.add(self.playerOne)

   
   
   def createEnemies(self): 
      
      # Stop creating enemies if a boss is alive
      if self.createBoss() is True:
         return
      
      now = pygame.time.get_ticks()
      
      #print("model.createEnemies() boss_mode=%r, enemy_rate=%d, now=%d,last_enemy=%d" % (self.boss_mode,self.enemy_rate,now,self.last_enemy))
      if now - self.last_enemy < self.enemy_rate:  
         return
          
      
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
      
      
      
      pos_x = random.randint(50,self.screen_width - 50)
      
      if type == "Gunship":
         enemy = gameobjects.Gunship(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "Drone":
         enemy = gameobjects.Drone(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "Dart":
         enemy = gameobjects.Dart(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
         self.sound_state['Flyby'] = True
      
      self.enemy_objects.add(enemy)  
      
      self.last_enemy = now
      rate_max = 5000 - (500 * (self.level-1))
      rate_min = 2000 - (200 * (self.level-1))
      if rate_min > rate_max:
         self.enemy_rate = rate_min
      else:   
         self.enemy_rate = random.randint(rate_min,rate_max)       


   def createBoss(self):
      
      
         if self.theBoss.alive():
            #print("The boss is alive!")
            return True
         
         now = pygame.time.get_ticks()
         if now - self.last_boss <= self.boss_interval:
            return False
         
         self.theBoss.reset(self.level)
         self.enemy_objects.add(self.theBoss)
         return True

         
      

   def createPowerUps(self): 
      
      pu_types = [ 'BonusPU', 'PowerPU', 'ShieldPU','XWeaponPU' ]

      
      now = pygame.time.get_ticks()
      
      if now - self.last_pu < self.pu_rate:  
         return
      
      
      type_idx = int(random.randint(0,9) / 3) ;
   
      type = pu_types[type_idx]

      
      pos_x = random.randint(50,self.screen_width - 50)
      
      if type == "BonusPU":
         pu = gameobjects.BonusPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "PowerPU":
         pu = gameobjects.PowerPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "ShieldPU":
         pu = gameobjects.ShieldPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      elif type == "XWeaponPU":
         pu = gameobjects.XWeaponPU(self.sprite_images[type],pos_x,0,self.screen_width,self.screen_height)
      
      self.powerup_objects.add(pu)  
      
      self.last_pu = now
      rate_max = 20000 + (1000 * (self.level-1))
      rate_min = 7000 + (1000 * (self.level-1))
 

      self.pu_rate = random.randint(rate_min,rate_max)    
   
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
      for sprite in self.powerup_objects:
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
      kill_em_all = False


      
      # Blaster vs enemy: Kill blaster, damage enemy
      blaster_hits = pygame.sprite.groupcollide(self.shot_objects, self.enemy_objects, True, False )
      for hit in blaster_hits.keys():
         enemy = blaster_hits[hit][0]
         enemy.hit(hit)
         self.checkDeath(enemy)
      
      powerup_hits = pygame.sprite.groupcollide(self.powerup_objects,self.player_objects, False, False)
      for powerup in powerup_hits:
         powerup.hit(self.playerOne)
         self.playerOne.hit(powerup)
         if type(powerup) is gameobjects.XWeaponPU:
            kill_em_all = True
         self.checkDeath(powerup)
      
      
      if kill_em_all:
         for enemy in self.enemy_objects.sprites():
            # Weapon X does not kill bosses, but does 20 points of damage.
            # Play the exposion sound, even if it did not kill the boss.
            enemy.hit_points -= 20
            self.checkDeath(enemy)
            self.sound_state['Explosion'] = True
               
               
               
         
      
      now = pygame.time.get_ticks()
      # 2000 tick grace period. 
      if now - self.playerOne.time_created > 2000:  
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
            
            self.sound_state['Warn2'] = True
         self.playerOne.warned = 1
      elif hp > 1:
         self.sound_state['Hit'] = True
         
      
          
   
   def checkDeath(self,object):
         # Is the object dead?
         if not object.alive():
            return False
         
         if object.hit_points <= 0:
            self.points += object.POINT_VALUE
            # Bosses have big explosions and reset boss mode
            if type(object) is gameobjects.Boss:
               self.createExplosion(object.rect.x,object.rect.y)
               self.createExplosion(object.rect.x+object.OBJECT_WIDTH,object.rect.y)
               self.createExplosion(object.rect.x,object.rect.y+object.OBJECT_HEIGHT)
               self.createExplosion(object.rect.x+object.OBJECT_WIDTH,object.rect.y+object.OBJECT_HEIGHT)
               self.createExplosion(object.rect.x+object.OBJECT_WIDTH/2,object.rect.y+object.OBJECT_HEIGHT/2)
               self.last_boss = pygame.time.get_ticks()
               self.last_enemy = self.last_boss
               self.level += 1
               
            elif object.explodes():
               self.createExplosion(object.rect.x,object.rect.y)
            object.kill()
            return True
         
         elif isinstance(object,gameobjects.Enemy):
            self.sound_state['EnemyHit'] = True
         
         return False
      
   def createExplosion(self,x,y,type="Explosion"):
      # Explosion only type implemented for now.
      type = "Explosion"
      explosion = gameobjects.Explosion(self.sprite_images[type],x,y)
      self.explosion_objects.add(explosion)
      self.sound_state[type] = True
   
   def checkGameOver(self):
      
      if len(self.player_objects.sprites()) == 0:
         if self.lives > 1:

            self.lives -= 1
            print("lives remaining %d" % self.lives)
            self.playerOne.reset();
            self.sound_state['NewShip1'] = True
            self.player_objects.add(self.playerOne)
            
         else:

            return True
      return False
      