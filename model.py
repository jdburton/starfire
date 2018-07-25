import background
import spritesheet
import gameobjects
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
      
      self.playerOne = gameobjects.Player();
      self.playerOne.setImages(self.sprite_images['Player'],400,500)
      self.playerOne.constrain(self.screen_width,self.screen_height)
      
      self.all_objects.add(self.playerOne)
      self.player_objects.add(self.playerOne)                 

   
   
   def createEnemies(self):   
      
      enemy_types = [ 'Gunship', 'Drone', 'Boss', 'Dart' ]
      enemy = None
      
      for i in range(0,4):
         type = enemy_types[i] 
      
         if type == "Gunship":
            enemy = gameobjects.Gunship()
         elif type == "Drone":
            enemy = gameobjects.Drone()
         elif type == "Dart":
            enemy = gameobjects.Dart()
         elif type == "Boss":
            enemy = gameobjects.Boss()
         
         enemy.setImages(self.sprite_images[type],50+(i*180),100)
         enemy.constrain(self.screen_width,self.screen_height)
         self.all_objects.add(enemy)
         self.enemy_objects.add(enemy)                 

   
   def animate(self):
      for object in self.all_objects:
         object.animate()
         
   def movePlayer(self,x,y):
      self.playerOne.move(x,y)     
   
   def movePlayerTo(self,x,y): 
      self.playerOne.moveTo(x,y)
   
   def moveEnemies(self):
      for sprite in self.enemy_objects:
         sprite.move()
      