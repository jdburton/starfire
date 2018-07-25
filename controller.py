import pygame, sys
from pygame.locals import *
import random
import spritesheet
import view
import model

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

class Controller():
   
   
   def __init__(self):
      self.clock = pygame.time.Clock()
      self.V = view.View(SCREEN_WIDTH,SCREEN_HEIGHT)
      self.M = model.Model(SCREEN_WIDTH,SCREEN_HEIGHT)
      
   
   
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
            self.M.movePlayer(move_x,move_y)    
         elif (event.type == MOUSEMOTION):
            #print("pos: %r, rel: %r, buttons: %r" % (event.pos,event.rel,event.buttons))

            self.M.movePlayerTo(event.pos[0],event.pos[1])

   def drawObjects(self):
      pass
   

   def mainLoop(self):
      self.M.initGame()
      while True:
         
         self.V.drawBackground()
         self.processInput()
         self.M.moveEnemies()
         self.M.animate()
         self.M.all_objects.draw(self.V.screen)
         self.V.updateDisplay()      
    
         self.clock.tick(300)
   