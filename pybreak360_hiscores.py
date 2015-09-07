#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys, time, random #, platform, threading, math
import pygame
from pygame.locals import *

from reader import Reader

from pybreak360_sounds import *
from pybreak360_config import *
from pybreak360_sprites import *

import pybreak360_varglob as varglob


#################################################	
def load_hiscores():
	"""load file pybreak360.hiscores and return hiscores list"""

	#DEFAULT VALUES IF NOT FOUND IN CONFIG FILE
	#hiscores = [LevelPackName,PlayerName,Hiscore,Level]
	hiscores = [["Classic480","Gino","0","URANUS"], ["Classic480Fast","Delf","765","LUNA"]]

	try:
		#open config file "pybreak360.hiscores" in correct directory.
		fullname = os.path.join('', "pybreak360.hiscores")
		hiscorestext = []
		fichier = open(fullname,'r')
		# pass on each lines with command for
		for ligne in fichier.readlines() :
			# split line in words - split remove spaces and carriage return
			donnees = ligne.split()
			# finally add to config array 
			hiscorestext.extend(donnees)
		# end of loop for, close hiscores file
		fichier.close()
		
		#print (hiscorestext)

		nbhiscores = 0
		hiscores = []
		subscore = []
		#WARNING: if somes parameters in v10x only, have to check version header file!
		for idx, line in enumerate(hiscorestext):
			#print (idx)
			if line =="[LevelPackName]":
				subscore.append(hiscorestext[idx+1])
			if line =="[PlayerName]":
				subscore.append(hiscorestext[idx+1])
			if line =="[LevelPackScore]":
				subscore.append(hiscorestext[idx+1])
			if line =="[LevelName]":
				subscore.append(hiscorestext[idx+1])
			if line =="[EndLevelPack]":
				hiscores.append(subscore)
				nbhiscores += 1
				subscore = []
			
	except:
		print ("Warning: INVALIDE PARAMETERS IN pybreak360.hiscores !!!")

	return (hiscores) 

#################################################	
def save_hiscores(hiscores):
	"""save file pybreak360.hiscores from list"""

	fullname = os.path.join("", "pybreak360.hiscores")
	#print (hiscores)
	try:
		fichier = open(fullname, "w")
		
		fichier.write("# pybreak360.hiscores version: %s\n" %(varglob.pybreak360version))
		fichier.write("# only the 1st line just downside paramater is checked\n")
		
		#hiscores = [["Classic480","Gino","0","URANUS"], ["Classic480Fast","Delf","765","LUNA"]]
		for idx, line in enumerate(hiscores):
			#print (idx)
			fichier.write("[LevelPackName]\n")
			fichier.write(line[0]+"\n")
			fichier.write("[PlayerName]\n")
			fichier.write(line[1]+"\n")
			fichier.write("[LevelPackScore]\n")
			fichier.write(line[2]+"\n")
			fichier.write("[LevelName]\n")
			fichier.write(line[3]+"\n")
			fichier.write("[EndLevelPack]\n")
			fichier.write("\n")

		fichier.close()

		print ("pybreak360.hiscores saved")
	except pygame.error, message:
		print ("Warning: unable to save pybreak360.hiscores")
	
#################################################	
def menu_hiscores(hiscores):
	"""Display HiScores Message """
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
	texte = Reader(message, pos=((varglob.fenetre_size[0]-450)/2, (varglob.fenetre_size[1]-400)/2), width=450, fontsize=16, height=420, bg=(200,200,200), fgcolor=(20,20,20))
	texte.show()

	ev = pygame.event.wait()
	while 1:
		ev = pygame.event.wait()
		if ev.type == KEYDOWN:
			if ev.key==K_SPACE or ev.key==K_RETURN or ev.key==K_h:
				break
	
#################################################	
hiscores = [["Classic480","Gino","0","URANUS"], ["Classic480Fast","Delf","765","LUNA"]]
