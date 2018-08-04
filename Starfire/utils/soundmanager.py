#!/usr/bin/env python3
#
# James Burton
# jburto2@clemson.edu
# CPSC 8700
# August 3, 2018
# Final Project
#
# Starfire/utils/soundmanager.py
#
# This module is a utility for playing game sounds. 
# This does not include game music, which is covered by the built-in pygame.mixer.music.
#
#

import pygame

class SoundManager():
   
   def __init__(self):
      self.sounds = {}
      self.q_channels = []
   
   def loadSounds(self):
      
      self.sounds['Blaster'] = pygame.mixer.Sound('sounds/blaster.wav')
      self.sounds['Splash1'] = pygame.mixer.Sound('sounds/Monkey.wav')
      self.sounds['Splash2'] = pygame.mixer.Sound('sounds/typewriter.wav')
      self.sounds['EnemyBlaster'] = pygame.mixer.Sound('sounds/laser.wav')
      self.sounds['Gameover1'] = pygame.mixer.Sound('sounds/gameover1.wav')
      self.sounds['Gameover2'] = pygame.mixer.Sound('sounds/gameover.wav')
      self.sounds['Flyby'] = pygame.mixer.Sound('sounds/flyby.wav')
      self.sounds['Warn1'] = pygame.mixer.Sound('sounds/killed0.wav')
      self.sounds['Warn2'] = pygame.mixer.Sound('sounds/killed2.wav')
      self.sounds['Begin'] = pygame.mixer.Sound('sounds/begin2.wav')
      self.sounds['Dying'] = pygame.mixer.Sound('sounds/dying.wav')
      self.sounds['Hit'] = pygame.mixer.Sound('sounds/HITSHIELD.WAV')
      self.sounds['EnemyHit'] = pygame.mixer.Sound('sounds/ehitshield.wav')
      self.sounds['Gameover0'] = pygame.mixer.Sound('sounds/killed1.wav')
      self.sounds['Start'] = pygame.mixer.Sound('sounds/begin2.wav')
      self.sounds['NewShip1'] = pygame.mixer.Sound('sounds/begin0.wav')
      self.sounds['NewShip2'] = pygame.mixer.Sound('sounds/begin1.wav')
      self.sounds['Explosion'] = pygame.mixer.Sound('sounds/EXPLOSION.WAV')

   # Play sounds from a dictionary of active sounds. 
   # The keys of the active sounds are the same as the keys of the loaded sound in the manager.
   def playActiveSounds(self,active_sounds = {}):
      for sound in active_sounds.keys():
         if active_sounds[sound]:
            # Limit to 3 channels to keep a single sound (usually the player blaster) from overwhelming the system.
            if self.sounds[sound].get_num_channels() < 3:
               self.sounds[sound].play()
            active_sounds[sound] = False
    

   def playActiveSoundsInQueue(active_sounds = {}):
      for sound in active_sounds.keys():
         if active_sounds[sound]:  
            sound_q.append(sound)
            active_sounds[sound] = False
      self.playQueuedSounds(sound_q)
   
   
   # Play sounds consecutively.
   def playQueuedSounds(self,sound_q = []):
      q_channel = pygame.mixer.find_channel()
      for sound in sound_q:
         q_channel.queue(self.sounds[sound])      
      
      self.q_channels.append(q_channel)
      
   def checkQueueChannels(self):
      for channel in self.q_channels:
         if not channel.get_busy():
            self.q_channels.remove(channel) 
      return len(self.q_channels)
   
   # play sounds concurrently.
   def playConcurrentSounds(self,sounds = []):
      for sound in sounds:
         self.sounds[sound].play()
    
   # stop concurrent sounds     
   def stopConcurrentSounds(self,sounds = None):
      if sounds is None:
         sounds = self.sounds.keys()
      for sound in sounds:
         self.sounds[sound].stop()
         