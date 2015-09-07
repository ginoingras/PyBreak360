#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys, time, random #, platform, threading, math
import pygame
from pygame.locals import *

from pybreak360_sounds import *
from pybreak360_config import *
from pybreak360_sprites import *

pybreak360version = "1.0.7rc2"

pdb_debug = False
#pdb_debug = True

#Colors RGB
Aqua=(0, 255, 255)
Black=(0, 0, 0)
Blue=(0, 0, 255)
#DeepBlue=(0, 0, 210)
DeepBlue=(0, 0, 160)
Fuchsia=(255, 0, 255)
Gray=(128, 128, 128)
Green=(0, 255, 0)
#DeepGreen=(0, 164, 0)
DeepGreen=(0, 140, 0)
Lime=(0, 255, 0)
Brown=(128, 0, 0)
NavyBlue=(0, 0, 128)
Olive=(128, 128, 0)
Purple=(128, 0, 128)
Red=(255, 0, 0)
#DeepRed=(200, 0, 0)
DeepRed=(160, 0, 0)
Silver=(192, 192, 192)
Teal=(0, 128, 128)
White=(255, 255, 255)
Yellow=(255, 255, 0)
#DeepYellow=(210, 210, 0)
DeepYellow=(160, 160, 0)


players = [["free", "player1", 0, 0, ParBulletQty, ParLives], ["free", "player2", "free", 0, ParBulletQty, ParLives], \
["free", "player3", "free", 0, ParBulletQty, ParLives], ["free", "player4", "free", 0, ParBulletQty, ParLives]]

# client know if player exist if angle != "free"
#[0 objOriBatImage, 1 objBatImageAngle, 2 objOriBatPos(posx, posy), 3 center(posx, posy), 4 objBatAnglePos(posx, posy), 5 animation]
playersbat = [[g_bat_yellow2, "free", "free", "free", "free", 0], [g_bat_green2, "free", "free", "free", "free", 0], \
[g_bat_blue2, "free", "free", "free", "free", 0], [g_bat_red2, "free", "free", "free", "free", 0]]

playerno = 0 # actual number of player in local game

balls = [["free", (0,0,0,0), 0], ["free", (0,0,0,0), 0], ["free", (0,0,0,0), 0], ["free", (0,0,0,0), 0]]
bullets = []
bricks = []

#background, toto = load_backgnd(levelBackGnd)
background = pygame.Surface((480,480))
background = background.convert()
background.fill((255, 255, 255))

BatDim = [0, 0, 0, 0]
BatDimTime = [0, 0, 0, 0]
InvertTime = [0, 0, 0, 0]

#allowed for all players
WallTime = 0

rayon = 240 #default 480 screen size
fenetre_center = (240, 240) #default 480 screen size
fenetre_size = ParScreenSize #default 480
fenetre = pygame.display.set_mode(fenetre_size)

nb_levels = 1
levels = []
levelNumber = 0
#nb_levels, levels = load_levels(ParLevelPack)

#global levelName, levelBackGnd, levelClient
levelName = "Unknow"
levelBackGnd = "Unknow"
levelClient =  [(0,6,4,3,2), (0,0,6,0,0), (1,2,3,0,0), (7,0,0,2,0), (0,0,3,0,0), (2,3,4,5,6)]


#global PenalityDelays   # when lose ball
PenalityDelayP1 = time.time() + 2
PenalityDelayP2 = time.time() + 2
PenalityDelayP3 = time.time() + 2
PenalityDelayP4 = time.time() + 2
PenalityDelays = [PenalityDelayP1, PenalityDelayP2, PenalityDelayP3, PenalityDelayP4]

anouncetexte = ["PyBreak360 V%s" %(pybreak360version)]
anouncetime = 4
anouncetimeactu = 0
anouncealpha = 180 #128
anouncealphaactu = 1

howplayers = 1
