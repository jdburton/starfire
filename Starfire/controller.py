import pygame, sys
from pygame.locals import *
import random
import Starfire.utils.spritesheet as spritesheet
import Starfire.utils.soundmanager as soundmanager
import Starfire.view as view
import Starfire.model as model
import Starfire.gameobjects as gameobjects

import time

SCREEN_WIDTH=800
SCREEN_HEIGHT=600


class Controller():
   
   
   def __init__(self):
      self.clock = pygame.time.Clock()
      self.V = view.View(SCREEN_WIDTH,SCREEN_HEIGHT)
      self.M = model.Model(SCREEN_WIDTH,SCREEN_HEIGHT)
      self.M.sprite_images = gameobjects.loadImagesFromSheet()
      self.sound_manager = soundmanager.SoundManager()
      self.sound_manager.loadSounds()
      self.fire = False
      self.last_fired = 0
      self.move_up = False
      self.move_down = False
      self.move_left = False
      self.move_right = False
      
      
   
   
   
   def processInput(self):
      move_x = 0
      move_y = 0
      MOVE_SIZE = 4

      for event in pygame.event.get():
         if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            sys.exit()
         elif (event.type == KEYDOWN):
            if (event.key == K_UP):
               self.move_up = True
         
            elif (event.key == K_DOWN):
               self.move_down = True
            
            elif (event.key == K_LEFT):
               self.move_left = True
            elif (event.key == K_RIGHT):
               self.move_right = True
            elif (event.key == K_SPACE):
               self.fire = True

         elif (event.type == KEYUP):
            if (event.key == K_UP):
               self.move_up = False
         
            elif (event.key == K_DOWN):
               self.move_down = False
            
            elif (event.key == K_LEFT):
               self.move_left = False
            elif (event.key == K_RIGHT):
               self.move_right = False
            elif (event.key == K_SPACE):
               self.fire = False

            #self.M.movePlayer(move_x,move_y)    
         elif (event.type == MOUSEMOTION):
            #print("pos: %r, rel: %r, buttons: %r" % (event.pos,event.rel,event.buttons))

            self.M.movePlayerTo(event.pos[0],event.pos[1])
         
         elif (event.type == MOUSEBUTTONDOWN):
            self.fire = True
         elif (event.type == MOUSEBUTTONUP):
            self.fire = False
   
      #print("now: %r lastfired %r" % (now,self.last_fired))
      if self.fire:
         self.fireWeapon();
      
      if self.move_up:
         move_y -= MOVE_SIZE

      if self.move_down:
         move_y += MOVE_SIZE
         
      if self.move_left:
         move_x -= MOVE_SIZE
         
      if self.move_right:
         move_x += MOVE_SIZE
         
      self.M.movePlayer(move_x,move_y)
            

   def drawObjects(self):
      self.M.player_objects.draw(self.V.screen)
      self.M.enemy_objects.draw(self.V.screen)
      self.M.explosion_objects.draw(self.V.screen)
      self.M.shot_objects.draw(self.V.screen)
      self.M.enemy_shot_objects.draw(self.V.screen)
      self.V.drawState(self.M.lives,self.M.playerOne.hit_points,self.M.points)
      
   def moveObjects(self):
      self.processInput()
      self.M.moveObjects()
      self.M.animate()
      self.M.collisionDetection()
   
         
         
      
   def fireWeapon(self):
      self.M.fireWeapon()

   
   def playIntro(self):
      self.M.music_manager['Intro'].play(-1)
   
   def playTheme(self):
      pygame.mixer.music.load('music/boss.mid')
      pygame.mixer.music.play(-1)
     

   def stopMusic(self):
      pygame.mixer.music.fadeout(1000)
   

   def mainLoop(self):
      pygame.mouse.set_visible(False)
      pygame.event.set_grab(True)
      self.gameLoop()

   def gameLoop(self):
      self.M.initGame()
      
      self.playTheme()
      #self.playIntro()
      
      die = 0
      play_gameover = 0
      while True:
         
         self.V.drawBackground()
         self.M.createEnemies()
         self.moveObjects()
         self.drawObjects()
         self.V.updateDisplay()
         self.sound_manager.playActiveSounds(self.M.sound_state)
         self.V.postProcessing()
         if self.M.checkGameOver() and die == 0:
            print("Died!")
            die = pygame.time.get_ticks()
            self.stopMusic()
            
            
         if die > 0:
            now = pygame.time.get_ticks()
            if now - die > 2000 and self.sound_manager.checkQueueChannels() == 0:
               if play_gameover == 0:
                  self.sound_manager.playQueuedSounds(sound_q = ["Gameover2","Gameover1"])
                  play_gameover = 1
               else:
                  sys.exit()
            
    
         self.clock.tick(60)
   