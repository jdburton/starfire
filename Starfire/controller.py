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
GAME_OVER = 1

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
      
   
   def pauseLoop(self):
      (x,y) = self.releaseMouse()

      m_pos = pygame.mixer.music.get_pos()
      print("Pausing at ",m_pos)
      pygame.mixer.music.stop()
      # wait to unpause
      while True:
         for unpause in pygame.event.get():
            if unpause.type == QUIT or (unpause.type == KEYUP and unpause.key == K_ESCAPE):
               sys.exit()
            elif unpause.type == KEYDOWN and unpause.key == K_p:
               self.grabMouse(x,y)
               try:
                  pygame.mixer.music.set_pos(m_pos)
               except:
                  print("Warning: Setting music position not supported for this file type. Restarting")
               pygame.mixer.music.play(-1)
               
               return
               

         time.sleep(1)     
   
   
   
   def processGameInput(self):
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
            elif (event.key == K_p):
               self.pauseLoop()
               
               
               
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
      self.M.powerup_objects.draw(self.V.screen)
      
      self.V.drawState(self.M.lives,self.M.playerOne.hit_points,self.M.points)
      
   def moveObjects(self):
      self.processGameInput()
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
   
   def grabMouse(self,x=0,y=0):
      pygame.mouse.set_visible(False)
      pygame.event.set_grab(True)
      pygame.mouse.set_pos([x,y])
      
   def releaseMouse(self):
      pygame.mouse.set_visible(True)
      pygame.event.set_grab(False)
      return pygame.mouse.get_pos()
   
   
   def displayLogo(self):
      
      self.V.displayLogo()
      self.sound_manager.playConcurrentSounds(["Splash1","Splash2"])

      start = pygame.time.set_timer(pygame.TIMER_RESOLUTION, 5000)
      while True:
         for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
               sys.exit()
            elif event.type == pygame.TIMER_RESOLUTION or (event.type == KEYUP and event.key == K_RETURN):
               #self.sound_manager.stopSounds(["Splash1","Splash2"])
               self.sound_manager.stopConcurrentSounds()

               return
            
         self.clock.tick(60)
   
   
   def displayTitle(self):
      
      self.V.displayTitle()
      while True:
         for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
               sys.exit()
            elif (event.type == KEYUP):
               if (event.key == K_RETURN):
                  return
            
         self.clock.tick(60)
         
   def displayHelp(self):
      
      # Help index is the current help panel, starting at 1. 0 if no more.
      help_idx = self.V.displayHelp()
      while help_idx:
         for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
               sys.exit()
            elif (event.type == KEYUP):
               if (event.key == K_RETURN):
                  help_idx = self.V.displayHelp()
            
         self.clock.tick(60)
   
   def mainMenu(self):
      
      self.V.displayMenu()
      while True:
         
         for event in pygame.event.get():
            if event.type == QUIT: 
               sys.exit()
            elif (event.type == KEYUP):
               if (event.key == K_ESCAPE or  event.key == K_q):
                  sys.exit()
               elif (event.key == K_RETURN or event.key == K_n):
                  self.gameLoop()
                  self.V.displayMenu()
               elif (event.key == K_h):
                  self.displayHelp()   
                  self.V.displayMenu()
            
         self.clock.tick(60)

   def mainLoop(self):
      self.displayLogo()
      self.displayTitle()
  
      self.grabMouse(SCREEN_WIDTH/2,SCREEN_HEIGHT-100)
      self.mainMenu()
      sys.exit()
      
   def gameOver(self):
      self.stopMusic()
      #self.sound_manager.stopConcurrentSounds()
      
      start = pygame.time.set_timer(pygame.TIMER_RESOLUTION, 2000)
      wait = True
      while wait:
         for event in pygame.event.get():
            if event.type == pygame.TIMER_RESOLUTION:
               wait = False
               break
            
         self.clock.tick(60)
      
      self.V.displayGameOver()
      
      self.sound_manager.playQueuedSounds(sound_q = ["Gameover2","Gameover1"])

      start = pygame.time.set_timer(pygame.TIMER_RESOLUTION, 8000)
      
      while True:
         for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
               sys.exit()
            elif event.type == pygame.TIMER_RESOLUTION or (event.type == KEYUP and event.key == K_RETURN):
               return True

            
         self.clock.tick(60)
   
   

   def gameLoop(self):
      self.M.initGame()
      self.V.initGame()
      self.playTheme()
      self.sound_manager.playQueuedSounds(["Start"])
      #self.playIntro()
      
      die = 0

      while True:
         
         self.V.drawBackground()
         self.M.createEnemies()
         self.M.createPowerUps()
         self.moveObjects()
         self.drawObjects()
         self.V.updateDisplay()
         self.sound_manager.playActiveSounds(self.M.sound_state)
         self.V.postProcessing()
         if self.M.checkGameOver():

            return self.gameOver()
    
         self.clock.tick(60)
   