#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys #, platform, threading, math, time
import pygame
from pygame.locals import *

from reader import Reader
from pybreak360_config import *
from pybreak360_varglob import *

#################################################	
def menu_hiscores(hiscores, fenetre_size):
	#global hiscores
	message = \
"""           --- HI SCORES ---   

"""
	for idx, line in enumerate(hiscores):
		message += """LevelPackName: %s\n""" %(line[0])
		message += """PlayerName: %s, Score: %s\n""" %(line[1], line[2])
		message += """in LevelName: %s\n\n""" %(line[3])
	
	message += \
"""      (H, SPACE OR ENTER TO RESUME)      
"""
	texte = Reader(message, pos=((fenetre_size[0]-450)/2,(fenetre_size[1]-400)/2), width=450, fontsize=16, height=420, bg=(200,200,200), fgcolor=(20,20,20))
	texte.show()

	ev = pygame.event.wait()
	while 1:
		ev = pygame.event.wait()
		if ev.type == KEYDOWN:
			if ev.key==K_SPACE or ev.key==K_RETURN or ev.key==K_h:
				break
	
#################################################	
def menuupdate(no_message):
	from reader import Reader
	global fenetre
	global IPaddressPublic, IPhostname, IPaddressLocal
	
	global ParPlayerName, ParFPS, ParScreenSize, ParLockMouse, ParShowMouse, ParDwngrdBrick, ParBallSpeedSlow, ParBallSpeedFast
	global ParLives, ParBulletQty, ParBulletSpeed
	global ParMusicYN, ParMusicVol, ParLevelPack, ParIPServer, ParPlayerName
	global ParFPS, ParAllowMulti360, ParLockMouse, ParShowMouse, ParDwngrdBrick, ParBallSpeedSlow, ParBallSpeedFast, ParLives
	
	global serveur1, is_serveur
	global players
	
	if players[0][0] != "free": p1name = players[0][1]
	if players[0][0] == "free": p1name = "Free"
	if players[1][0] != "free": p2name = players[1][1]
	if players[1][0] == "free": p2name = "Free"
	if players[2][0] != "free": p3name = players[2][1]
	if players[2][0] == "free": p3name = "Free"
	if players[3][0] != "free": p4name = players[3][1]
	if players[3][0] == "free": p4name = "Free"
	f10 = "SERVER IS DISTANT, CONNECT TO LOCAL"
	if is_serveur: f10 = "SERVER IS LOCAL, CONNECT TO DISTANT"

	message0 = \
"""   --- SETTINGS ---   
YOUR LOCAL IP IS: %s
hostname: %s
CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s

F1)SERVER IP: %s
F2)PLAYER NAME: %s
F3)ALL PLAYERS 360: %s
F4)FPS LIMITE: %s
F5)LOCK MOUSE: %s
F6)SHOW MOUSE: %s
F7)SOUND: %s
F8)SOUND VOLUME: %s
F9)LEVEL PACK: %s
F10)%s

see other parameters in pybreak360.cfg

      (SPACE OR ENTER TO RESUME)      
      (S TO SAVE pybreak360.cfg)      """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, \
   ParIPServer, ParPlayerName, ParAllowMulti360, ParFPS, ParLockMouse, ParShowMouse, ParMusicYN, ParMusicVol, ParLevelPack, f10)

	message1 = \
"""   --- SETTINGS ---   


CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s


F2)PLAYER NAME: %s



Only letters and numerics allows.
Somes problems with internationnal
numeric keymap...



see other parameters in pybreak360.cfg

    (F2, SPACE OR ENTER TO RESUME)      
                                      """ \
   %(p1name, p2name, p3name, p4name, ParPlayerName)

	message2 = \
"""   --- SETTINGS ---   
YOUR LOCAL IP IS: %s
hostname: %s
CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s

F1)SERVER IP: %s



Somes problems with internationnal
numeric keymap...





see other parameters in pybreak360.cfg

    (F1, SPACE OR ENTER TO RESUME)      
                                     """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, ParIPServer,)

	message3 = \
"""   --- SETTINGS ---   
YOUR LOCAL IP IS: %s
hostname: %s
CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s

F1)SERVER IP: %s
F2)PLAYER NAME: %s
F3)ALL PLAYERS 360: %s
F4)FPS LIMITE: %s
F5)LOCK MOUSE: %s
F6)SHOW MOUSE: %s
F7)SOUND: %s
F8)SOUND VOLUME: %s
F9)LEVEL PACK: %s
F10)%s

see other parameters in pybreak360.cfg

      (SPACE OR ENTER TO RESUME)      
      SAVED  on  pybreak360.cfg       """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, \
   ParIPServer, ParPlayerName, ParAllowMulti360, ParFPS, ParLockMouse, ParShowMouse, ParMusicYN, ParMusicVol, ParLevelPack, f10)

	message4 = \
"""   --- SETTINGS ---   
YOUR LOCAL IP IS: %s
hostname: %s
CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s

F1)SERVER IP: %s
F2)PLAYER NAME: %s
F3)ALL PLAYERS 360: %s
F4)FPS LIMITE: %s
F5)LOCK MOUSE: %s
F6)SHOW MOUSE: %s
F7)SOUND: %s
F8)SOUND VOLUME: %s
F9)LEVEL PACK: %s
F10)%s

see other parameters in pybreak360.cfg

      (SPACE OR ENTER TO RESUME)      
        CONNECTED  TO  SERVER         """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, \
   ParIPServer, ParPlayerName, ParAllowMulti360, ParFPS, ParLockMouse, ParShowMouse, ParMusicYN, ParMusicVol, ParLevelPack, f10)

	message5 = \
"""   --- SETTINGS ---   
YOUR LOCAL IP IS: %s
hostname: %s
CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s

F1)SERVER IP: %s
F2)PLAYER NAME: %s
F3)ALL PLAYERS 360: %s
F4)FPS LIMITE: %s
F5)LOCK MOUSE: %s
F6)SHOW MOUSE: %s
F7)SOUND: %s
F8)SOUND VOLUME: %s
F9)LEVEL PACK: %s
F10)%s

see other parameters in pybreak360.cfg

      (SPACE OR ENTER TO RESUME)      
      DISCONNECTED  FROM  SERVER      """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, \
   ParIPServer, ParPlayerName, ParAllowMulti360, ParFPS, ParLockMouse, ParShowMouse, ParMusicYN, ParMusicVol, ParLevelPack, f10)

	message6 = \
"""   --- SETTINGS ---   
YOUR LOCAL IP IS: %s
hostname: %s
CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s

F1)SERVER IP: %s
F2)PLAYER NAME: %s
F3)ALL PLAYERS 360: %s
F4)FPS LIMITE: %s
F5)LOCK MOUSE: %s
F6)SHOW MOUSE: %s
F7)SOUND: %s
F8)SOUND VOLUME: %s
F9)LEVEL PACK: %s
F10)%s

see other parameters in pybreak360.cfg

      (SPACE OR ENTER TO RESUME)      
     CONNEXION WITH SERVER FAILED       """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, \
   ParIPServer, ParPlayerName, ParAllowMulti360, ParFPS, ParLockMouse, ParShowMouse, ParMusicYN, ParMusicVol, ParLevelPack, f10)

	# TODO place message menu in list, with parameters
	if no_message == 0: message = message0
	if no_message == 1: message = message1
	if no_message == 2: message = message2
	if no_message == 3: message = message3
	if no_message == 4: message = message4
	if no_message == 5: message = message5
	if no_message == 6: message = message6

	#texte = Reader(message, pos=(10,10), width=450, fontsize=16, height=420, bg=(200,200,200), fgcolor=(20,20,20))
	texte = Reader(message, pos=((fenetre_size[0]-450)/2,(fenetre_size[1]-400)/2), width=450, fontsize=16, height=420, bg=(200,200,200), fgcolor=(20,20,20))
	texte.show()
	#anti-rebond-keyboard
	global mem_evkey, mem_evtype
	mem_evkey = None
	mem_evtype = None

