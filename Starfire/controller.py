import pygame, sys
from pygame.locals import *
import random
import Starfire.utils.spritesheet as spritesheet
import Starfire.view as view
import Starfire.model as model

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

class Controller():
   
   
   def __init__(self):
      self.clock = pygame.time.Clock()
      self.V = view.View(SCREEN_WIDTH,SCREEN_HEIGHT)
      self.M = model.Model(SCREEN_WIDTH,SCREEN_HEIGHT)
      self.fire = False
      self.last_fired = 0
      
   
   
   def processInput(self):
      move_x = 0
      move_y = 0
      for event in pygame.event.get():
         if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            sys.exit()
         elif (event.type == KEYDOWN):
            if (event.key == K_UP):
               move_y -= 10
         
            elif (event.key == K_DOWN):
               move_y += 10
            
            elif (event.key == K_LEFT):
               move_x -= 10
            elif (event.key == K_RIGHT):
               move_x += 10 
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

            

   def drawObjects(self):
      self.M.player_objects.draw(self.V.screen)
      self.M.enemy_objects.draw(self.V.screen)
      self.M.explosion_objects.draw(self.V.screen)
      self.M.shot_objects.draw(self.V.screen)
      self.M.enemy_shot_objects.draw(self.V.screen)
      
   def moveObjects(self):
      self.processInput()
      self.M.moveObjects()
      self.M.animate()
      self.M.collisionDetection()
   
         
         
      
   def fireWeapon(self):
      self.M.fireWeapon()

   
   def playIntro(self):
      sound = pygame.mixer.Sound('sounds/begin2.wav')
      sound.play()
   
   def playTheme(self):
      pygame.mixer.music.load('music/boss.mid')
      pygame.mixer.music.play(-1)

   def mainLoop(self):
      self.M.initGame()
      
      self.playTheme()
      self.playIntro()
      
      while True:
         
         self.V.drawBackground()
         self.moveObjects()
         self.drawObjects()
         self.V.updateDisplay()
         self.V.postProcessing()
         if self.M.checkGameOver():
            sound = pygame.mixer.Sound('sounds/gameover.wav')
            sound.play()
         
    
         self.clock.tick(60)
   