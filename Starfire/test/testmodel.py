#!/usr/bin/env python3
#
# James Burton
# jburto2@clemson.edu
# CPSC 8700
# August 3, 2018
# Final Project
#
# testModel.py
#
# This module tests the Model class.


import sys

import unittest
import Starfire.model as model
import Starfire.gameobjects as gameobjects
import pygame
import time

class TestModel(unittest.TestCase):

   def setUp(self):
      
      pygame.init()
      self.screen_width = 800
      self.screen_height = 600
      self.myModel = None
      

   
   def testModelInit(self):
      self.myModel = model.Model(self.screen_width, self.screen_height)
      
      self.assertEqual(self.myModel.screen_width,self.screen_width, "Did not save screen width!")
      self.assertEqual(self.myModel.screen_height,self.screen_height, "Did not save screen height!")
      # 
      self.assertFalse(self.myModel.sound_state, "sound_state not empty!")
      self.assertFalse(self.myModel.sprite_images, "sprite_images is empty!")
      
      
      self.assertEqual(len(self.myModel.player_objects),0,"player_object not empty!")
      self.assertEqual(len(self.myModel.enemy_objects),0,"enemy_objects not empty!")
      self.assertEqual(len(self.myModel.enemy_shot_objects),0,"enemy_shot_objects not empty!")
      
      self.assertEqual(len(self.myModel.powerup_objects),0,"powerup_objects not empty!")
      self.assertEqual(len(self.myModel.explosion_objects),0,"explosion_objects not empty!")
      self.assertEqual(len(self.myModel.shot_objects),0,"shot_objects not empty!")
      
   def testLoadImages(self):
      self.testModelInit()
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
      self.myModel.sprite_images = gameobjects.loadImagesFromSheet()
      # Make sure the images loaded. Or at least something loaded.
      for image_name in self.myModel.sprite_images.keys():
         self.assertGreater(len(self.myModel.sprite_images[image_name]),0,"Image %s did not load!" % image_name)
         # test image count
         
         for image in self.myModel.sprite_images[image_name]:
            self.assertTrue(type(image),pygame.Surface)
            self.assertGreater(image.get_bytesize(),0,"Image in " + image_name + "is 0 bytes")
            
      
    
   def testInitGame(self):
      self.testModelInit()
      self.testLoadImages()
      now = pygame.time.get_ticks()
      self.myModel.initGame()
      
      self.assertEqual(self.myModel.lives,model.INIT_LIVES)
      self.assertEqual(self.myModel.level,model.INIT_LEVEL)
      self.assertAlmostEqual(self.myModel.last_enemy, now, delta=10)
      self.assertAlmostEqual(self.myModel.last_pu, now, delta=10)
      self.assertAlmostEqual(self.myModel.last_boss, now, delta=10)
      self.assertEqual(self.myModel.points, 0)
      
      
      self.assertEqual(len(self.myModel.enemy_objects),0,"enemy_objects not empty!")
      self.assertEqual(len(self.myModel.enemy_shot_objects),0,"enemy_shot_objects not empty!")
      
      self.assertEqual(len(self.myModel.powerup_objects),0,"powerup_objects not empty!")
      self.assertEqual(len(self.myModel.explosion_objects),0,"explosion_objects not empty!")
      self.assertEqual(len(self.myModel.shot_objects),0,"shot_objects not empty!")
      
      self.assertGreaterEqual(len(self.myModel.player_objects),1,"Player one not in player_objects")
      self.assertLessEqual(len(self.myModel.player_objects),1,"More than one object in player_objects")
      
      
      self.assertTrue(self.myModel.playerOne.alive(),"Player should be alive")
      self.assertFalse(self.myModel.theBoss.alive(),"Boss should not be alive at init")
      


      
   def testCreatePowerUps(self):
      self.testInitGame()
      self.myModel.last_pu = 0
      # Empty all power ups
      self.myModel.powerup_objects.empty() 
      time_check = pygame.time.get_ticks()
      self.assertGreater(time_check, 0, "Timer not working %d" % time_check)
      self.myModel.pu_rate = 0
      old_rate = self.myModel.pu_rate
      
      self.assertGreaterEqual(time_check - self.myModel.last_pu,self.myModel.pu_rate,"Failed initial assertion %d - %d < %d" % (time_check,self.myModel.last_pu,self.myModel.pu_rate))  
         
      
      self.myModel.createPowerUps()
      last_pu = pygame.time.get_ticks()
      
      self.assertGreater(self.myModel.last_pu,0,"last_pu time is zero or negative")
      self.assertAlmostEqual(self.myModel.last_pu, last_pu, delta=10, msg="last_pu not updated")
      self.assertNotEqual(self.myModel.pu_rate, old_rate, "powerup_rate not updated")

      
      self.assertGreaterEqual(len(self.myModel.powerup_objects),1,"Did not create power up")
      self.assertLessEqual(len(self.myModel.powerup_objects),1,"Created more than one power up")
      
      for sprite in self.myModel.powerup_objects:
         self.assertTrue(isinstance(sprite,pygame.sprite.Sprite),"Object is not a Sprite")
         self.assertTrue(isinstance(sprite,gameobjects.GameObject),"Object is not a GameObject")
         self.assertTrue(isinstance(sprite,gameobjects.PowerUp),"Object is not a PowerUp")
         self.assertIsNot(type(sprite),gameobjects.PowerUp,"Object is a generic PowerUp and not a subclass")
         self.assertGreaterEqual(sprite.rect.x,50, "Sprite too far to the left")
         self.assertLessEqual(sprite.rect.x,self.screen_width-50, "Sprite too far to the right")
         self.assertEqual(sprite.rect.y,0, "Sprite not at top of screen")
      
            
   def testCreateEnemies(self):
      self.testInitGame()
      self.myModel.last_enemy = 0
      
      self.myModel.enemy_objects.empty() 
      time_check = pygame.time.get_ticks()
      self.assertGreater(time_check, 0, "Timer not working %d" % time_check)
      self.myModel.enemy_rate = 0
      old_rate = self.myModel.enemy_rate
      self.myModel.boss_interval = 40000
      
      self.assertFalse(self.myModel.createBoss(),"Boss present or being created.")
      
      
      self.assertGreaterEqual(time_check - self.myModel.last_enemy,self.myModel.enemy_rate,"Failed initial assertion %d - %d < %d" % (time_check,self.myModel.last_enemy,self.myModel.enemy_rate))  
         
      
      self.myModel.createEnemies()
      last_enemy = pygame.time.get_ticks()
      
      self.assertGreater(self.myModel.last_enemy,0,"last_enemy time is zero or negative")
      self.assertAlmostEqual(self.myModel.last_enemy, last_enemy, delta=10, msg="last_enemy not updated")
      self.assertNotEqual(self.myModel.enemy_rate, old_rate, "enemy_rate not updated")

      
      
      self.assertGreaterEqual(len(self.myModel.enemy_objects),1,"Did not create enemy")
      self.assertLessEqual(len(self.myModel.enemy_objects),1,"Created more than one enemy")
      
      self.assertFalse(self.myModel.enemy_objects.has(self.myModel.theBoss),"theBoss in enemy list!")
      
      for sprite in self.myModel.powerup_objects:
         self.assertTrue(isinstance(sprite,pygame.sprite.Sprite),"Object is not a Sprite")
         self.assertTrue(isinstance(sprite,gameobjects.GameObject),"Object is not a GameObject")
         self.assertTrue(isinstance(sprite,gameobjects.Enemy),"Object is not an Enemy")
         self.assertIsNot(type(sprite),gameobjects.Enemy,"Object is a generic Enemy and not a subclass") 
         self.assertIsNot(type(sprite),gameobjects.Boss,"Object is a Boss") 
         self.assertGreaterEqual(sprite.rect.x,50, "Sprite too far to the left")
         self.assertLessEqual(sprite.rect.x,self.screen_width-50, "Sprite too far to the right")
         self.assertEqual(sprite.rect.y,0, "Sprite not at top of screen")    
      
   def testCreateBoss(self):
      self.testCreateEnemies()
      self.myModel.boss_interval = 40000
      self.assertFalse(self.myModel.createBoss(),"Created boss before interval")
      self.myModel.boss_interval = 0
      self.assertTrue(self.myModel.createBoss(),"Could not create boss.")
      self.assertTrue(self.myModel.createBoss(),"Boss did not lock out enemy creation.")
      
      self.assertTrue(self.myModel.enemy_objects.has(self.myModel.theBoss),"theBoss in enemy list!")
      
      self.assertGreaterEqual(len(self.myModel.enemy_objects),2,"Less than 2 enemies have been created. Should have regular enemy and boss.")
      self.assertLessEqual(len(self.myModel.enemy_objects),2,"Created too many enemies")
      
      
      for sprite in self.myModel.powerup_objects:
         self.assertTrue(isinstance(sprite,pygame.sprite.Sprite),"Object is not a Sprite")
         self.assertTrue(isinstance(sprite,gameobjects.GameObject),"Object is not a GameObject")
         self.assertTrue(isinstance(sprite,gameobjects.Enemy),"Object is not an Enemy")
         self.assertIsNot(type(sprite),gameobjects.Enemy,"Object is a generic Enemy and not a subclass") 
         self.assertGreaterEqual(sprite.rect.x,50, "Sprite too far to the left")
         self.assertLessEqual(sprite.rect.x,self.screen_width-50, "Sprite too far to the right")
         self.assertEqual(sprite.rect.y,0, "Sprite not at top of screen")    
                               
      num_enemies = len(self.myModel.enemy_objects)
      self.myModel.createEnemies()
      self.assertEqual(len(self.myModel.enemy_objects),num_enemies,"createEnemies created new enemy while boss active.")
      
      self.assertTrue(self.myModel.createBoss(),"Boss not active")
      
   
   def testMovePlayer(self):
      self.testInitGame()
      
      self.myModel.playerOne.rect.x = 100
      self.myModel.playerOne.rect.y = 100
      self.myModel.movePlayer(100,100)
      self.assertEqual(self.myModel.playerOne.rect.x, 200, "Error moving player in X direction. Player(x) at %d! " % self.myModel.playerOne.rect.x)
      self.assertEqual(self.myModel.playerOne.rect.y, 200, "Error moving player in Y direction. Player(y) at %d! " % self.myModel.playerOne.rect.y)
      
      self.myModel.movePlayer(1000,1000)
      self.assertNotEqual(self.myModel.playerOne.rect.x, 1200, "Player not confined to screen (too right). rect.x = %d! " % self.myModel.playerOne.rect.x)
      self.assertNotEqual(self.myModel.playerOne.rect.y, 1200, "Player not confined to screen (too down). rect.y = %d! " % self.myModel.playerOne.rect.y)

      self.assertLessEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.max_x, "Player above max_x (right) max_x = %d. rect.x = %d! " % (self.myModel.playerOne.max_x,self.myModel.playerOne.rect.x))
      self.assertLessEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.max_y, "Player above max_y (down)  max_y = %d. rect.y = %d! " % (self.myModel.playerOne.max_y,self.myModel.playerOne.rect.y))
      self.assertEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.max_x, "Player not at max_x (right) max_x = %d. rect.x = %d! " % (self.myModel.playerOne.max_x,self.myModel.playerOne.rect.x))
      self.assertEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.max_y, "Player not at max_y (down)  max_y = %d. rect.y = %d! " % (self.myModel.playerOne.max_y,self.myModel.playerOne.rect.y))
      
      self.myModel.movePlayer(-2000,-2000)
      self.assertNotEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.max_x-2000, "Player not confined to screen (too right). rect.x = %d! " % self.myModel.playerOne.rect.x)
      self.assertNotEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.max_x-2000, "Player not confined to screen (too down). rect.y = %d! " % self.myModel.playerOne.rect.y)

    
      self.assertGreaterEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.min_x, "Player above min_x (right) min_x = %d. rect.x = %d! " % (self.myModel.playerOne.min_x,self.myModel.playerOne.rect.x))
      self.assertGreaterEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.min_y, "Player above min_y (down)  min_y = %d. rect.y = %d! " % (self.myModel.playerOne.min_y,self.myModel.playerOne.rect.y))
      self.assertEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.min_x, "Player not at min_x (right) min_x = %d. rect.x = %d! " % (self.myModel.playerOne.min_x,self.myModel.playerOne.rect.x))
      self.assertEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.min_y, "Player not at min_y (down)  min_y = %d. rect.y = %d! " % (self.myModel.playerOne.min_y,self.myModel.playerOne.rect.y))
      
   def testMovePlayerTo(self):
      
      self.testInitGame()
      self.myModel.playerOne.rect.x = 100
      self.myModel.playerOne.rect.y = 100
      self.myModel.movePlayerTo(300,300)
      self.assertEqual(self.myModel.playerOne.rect.x, 300, "Error moving player in X direction. Player(x) at %d! " % self.myModel.playerOne.rect.x)
      self.assertEqual(self.myModel.playerOne.rect.y, 300, "Error moving player in Y direction. Player(y) at %d! " % self.myModel.playerOne.rect.y)
      
      self.myModel.movePlayer(2000,2000)
      self.assertNotEqual(self.myModel.playerOne.rect.x, 2000, "Player not confined to screen (too right). rect.x = %d! " % self.myModel.playerOne.rect.x)
      self.assertNotEqual(self.myModel.playerOne.rect.y, 2000, "Player not confined to screen (too down). rect.y = %d! " % self.myModel.playerOne.rect.y)

      self.assertLessEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.max_x, "Player above max_x (right) max_x = %d. rect.x = %d! " % (self.myModel.playerOne.max_x,self.myModel.playerOne.rect.x))
      self.assertLessEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.max_y, "Player above max_y (down)  max_y = %d. rect.y = %d! " % (self.myModel.playerOne.max_y,self.myModel.playerOne.rect.y))
      self.assertEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.max_x, "Player not at max_x (right) max_x = %d. rect.x = %d! " % (self.myModel.playerOne.max_x,self.myModel.playerOne.rect.x))
      self.assertEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.max_y, "Player not at max_y (down)  max_y = %d. rect.y = %d! " % (self.myModel.playerOne.max_y,self.myModel.playerOne.rect.y))
      
      self.myModel.movePlayer(-2000,-2000)
      self.assertNotEqual(self.myModel.playerOne.rect.x, -2000, "Player not confined to screen (too right). rect.x = %d! " % self.myModel.playerOne.rect.x)
      self.assertNotEqual(self.myModel.playerOne.rect.y, -2000, "Player not confined to screen (too down). rect.y = %d! " % self.myModel.playerOne.rect.y)

    
      self.assertGreaterEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.min_x, "Player above min_x (right) min_x = %d. rect.x = %d! " % (self.myModel.playerOne.min_x,self.myModel.playerOne.rect.x))
      self.assertGreaterEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.min_y, "Player above min_y (down)  min_y = %d. rect.y = %d! " % (self.myModel.playerOne.min_y,self.myModel.playerOne.rect.y))
      self.assertEqual(self.myModel.playerOne.rect.x, self.myModel.playerOne.min_x, "Player not at min_x (right) min_x = %d. rect.x = %d! " % (self.myModel.playerOne.min_x,self.myModel.playerOne.rect.x))
      self.assertEqual(self.myModel.playerOne.rect.y, self.myModel.playerOne.min_y, "Player not at min_y (down)  min_y = %d. rect.y = %d! " % (self.myModel.playerOne.min_y,self.myModel.playerOne.rect.y))

      
'''  
  
TODO: Test the other game functions.

   def animate(self):
   def moveObjects(self):
   def fireEnemyWeapons(self,enemy):
   def fireWeapon(self):
   def collisionDetection(self):
   def checkDeath(self,object):
   def createExplosion(self,x,y,type="Explosion"):
   def checkGameOver(self):
   
Plus the gamemodel objects.
'''
      

 
   

if __name__ == "__main__":
   unittest.main()
