#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *
import Starfire.controller as controller
 
pygame.init()
C = controller.Controller()

C.mainLoop() 
sys.exit()
    