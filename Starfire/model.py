import Starfire.utils.background as background
import Starfire.utils.spritesheet as spritesheet
import Starfire.gameobjects as gameobjects
import pygame

class Model():

   
   def __init__(self,width,height):

      self.screen_width = width
      self.screen_height = height
      
      # Because PyGame ties data and images together in pygame.sprite.Sprite, the images need
      # to be with the data in the model, not in the view.
      self.sprite_images = {}
      
      
      # sprite group for all objects
      # sprite group for player
      # sprite group for enemies
      # sprite group for shots
      # sprite group for enemy shots
      # sprite group for power ups
      self.all_objects = pygame.sprite.Group() #Is this redundant?
      self.player_objects = pygame.sprite.Group()
      self.enemy_objects = pygame.sprite.Group()
      self.enemy_shot_objects = pygame.sprite.Group()
      self.shot_objects = pygame.sprite.Group()
      self.powerup_objects = pygame.sprite.Group()
      self.explosion_objects = pygame.sprite.Group()
      
      self.lives = 3
      

   
   def initGame(self):
      
    
      self.loadImagesFromSheet()
      self.createPlayerOne()
      self.createEnemies()
      
   def loadImagesFromSheet(self):
      
      self.ss = spritesheet.spritesheet(gameobjects.SPRITESHEET)
   
      self.sprite_images['Player'] = self.ss.images_at( gameobjects.Player.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['Explosion'] = self.ss.images_at( gameobjects.Explosion.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['Gunship'] = self.ss.images_at( gameobjects.Gunship.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['Dart'] = self.ss.images_at( gameobjects.Dart.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['Drone'] = self.ss.images_at( gameobjects.Drone.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['Boss'] = self.ss.images_at( gameobjects.Boss.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['PlayerBlaster'] = self.ss.images_at( gameobjects.PlayerBlaster.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['EnemyBlaster'] = self.ss.images_at( gameobjects.EnemyBlaster.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['EnemyBullet'] = self.ss.images_at( gameobjects.EnemyBullet.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['XWeaponPU'] = self.ss.images_at( gameobjects.XWeaponPU.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['BonusPU'] = self.ss.images_at( gameobjects.BonusPU.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['PowerPU'] = self.ss.images_at( gameobjects.PowerPU.SS_COORDINATES, gameobjects.CK)
      self.sprite_images['ShieldPU'] = self.ss.images_at( gameobjects.ShieldPU.SS_COORDINATES, gameobjects.CK)
      
      
   def createPlayerOne(self):   
      
      self.playerOne = gameobjects.Player(self.screen_width,self.screen_height);
      self.playerOne.setImages(self.sprite_images['Player'],400,500)
      self.playerOne.reset(400,500);
      
      
      self.all_objects.add(self.playerOne)
      self.player_objects.add(self.playerOne)                 

   
   
   def createEnemies(self):   
      
      enemy_types = [ 'Gunship', 'Drone', 'Boss', 'Dart' ]
      enemy = None
      
      for i in range(0,4):
         type = enemy_types[i]
          
      
         if type == "Gunship":
            enemy = gameobjects.Gunship(self.screen_width,self.screen_height)
         elif type == "Drone":
            enemy = gameobjects.Drone(self.screen_width,self.screen_height)
         elif type == "Dart":
            enemy = gameobjects.Dart(self.screen_width,self.screen_height)
         elif type == "Boss":
            enemy = gameobjects.Boss(self.screen_width,self.screen_height)
         
         enemy.setImages(self.sprite_images[type],50+(i*180),100)
         #enemy.constrain(self.screen_width,self.screen_height)
         self.all_objects.add(enemy)
         self.enemy_objects.add(enemy)                 

   
   def animate(self):
      for object in self.all_objects:
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
               blast = gameobjects.EnemyBlaster(self.screen_width,self.screen_height,cannon.x_vel,cannon.y_vel)
               blast.setImages(self.sprite_images[cannon.name],cannon.x_pos,cannon.y_pos)
               self.enemy_shot_objects.add(blast)    
            elif cannon.name == "EnemyBullet":
               blast = gameobjects.EnemyBullet(self.screen_width,self.screen_height,cannon.x_vel,cannon.y_vel)
               blast.setImages(self.sprite_images[cannon.name],cannon.x_pos,cannon.y_pos)
               self.enemy_shot_objects.add(blast)       
 
   
   def fireWeapon(self):
      
      # fire the weapon
      shots = self.playerOne.fireWeapon()
      
      for cannon in shots:
         if cannon is not None:
            blast = gameobjects.PlayerBlaster(cannon.x_vel,cannon.y_vel)
            blast.setImages(self.sprite_images["PlayerBlaster"],cannon.x_pos,cannon.y_pos)
            self.shot_objects.add(blast)
      
   def collisionDetection(self):
      
      # enemy vs enemy = Bounce
      collided_enemies = pygame.sprite.groupcollide(self.enemy_objects, self.enemy_objects, False, False)
      for enemy in collided_enemies:
         if len(collided_enemies[enemy]) > 1: 
            enemy.vel_x = int(-enemy.vel_x/2)
            enemy.vel_y = int(-enemy.vel_y/2)

      # Player vs enemy = damage to both            
      player_hits = pygame.sprite.groupcollide(self.enemy_objects, self.player_objects, False, False)
      for enemy in player_hits:
         enemy.hit(self.playerOne)
         self.playerOne.hit(enemy)
         self.checkDeath(enemy)
      
      
         
      
      # Blaster vs enemy: Kill blaster, damage enemy
      blaster_hits = pygame.sprite.groupcollide(self.shot_objects, self.enemy_objects, True, False )
      for hit in blaster_hits.keys():
         enemy = blaster_hits[hit][0]
         enemy.hit(hit)
         self.checkDeath(enemy)
         
      # enemy shot vs player: Kill blaster, damage enemy
      blaster_hits = pygame.sprite.groupcollide(self.enemy_shot_objects, self.player_objects, True, False )
      for hit in blaster_hits.keys():
         player = blaster_hits[hit][0]
         player.hit(hit)
      
      self.checkDeath(self.playerOne)
   
   def checkDeath(self,object):
         # Is the object dead?
         if object.hitPoints <= 0 and object.alive():
            explosion = gameobjects.Explosion()
            explosion.setImages(self.sprite_images['Explosion'],object.rect.x,object.rect.y)
            self.explosion_objects.add(explosion)
            object.kill()
            return True
         return False
   
   def checkGameOver(self):
      
      if len(self.player_objects.sprites()) == 0:
         if self.lives > 0:

            self.lives -= 1
            print("lives remaining %d" % self.lives)
            self.playerOne.reset(400,500);
            self.player_objects.add(self.playerOne)
            
         else:

            return True
      return False
      