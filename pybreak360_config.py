#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys #, platform, threading, math, time

#################################################	
def load_config(name):
	"""Load file pybreak360.cfg and return config paramters
	return (ParPlayerName, ParFPS, ParScreenSize, ParLockMouse, ParShowMouse, ParLives, ParBulletQty, ParBulletSpeed, ParMusicYN, ParMusicVol)"""

	#DEFAULT VALUES IF NOT FOUND IN CONFIG FILE
	ParPlayerName = "Gino"
	ParFPS = 60 #60	
	ParGrabMouse =False
	ParLockMouse = False
	ParShowMouse = True
	ParLives = 5
	ParBulletQty = 15
	ParBulletSpeed = 10
	ParMusicYN = True
	ParMusicVol = 0.9
	ParLevelPack = "Classic"
	ParIPServer = "127.0.0.1"
	ParIPServerPort = 50000
	ParIPaddressLocal = "127.0.0.1"
	
	ParAllowMulti360 = True
	ParKeybUnicode = True
	ParKeybi18n = "fr"

	ParBallSpeedSlow = 4 # is level parameter
	ParBallSpeedFast = 6 # is level parameter
	ParDwngrdBrick = True # is level parameter
	ParScreenSize = (640, 640)# is level parameter
		
	try:
		#open config file extension ".cfg" in correct directory.
		fullname = os.path.join('', name)
		configstext = []
		fichier = open(fullname,'r')
		# pass on each lines with command for
		for ligne in fichier.readlines() :
			# split line in words - split remove spaces and carriage return
			donnees = ligne.split()
			# finally add to config array 
			configstext.extend(donnees)
		# end of loop for, close config file
		fichier.close()
		
		#print (configstext)
		#WARNING: somes parameters in v10x only, have to check version header file!
		for idx, line in enumerate(configstext):
			#print idx
			if line =="[ParPlayerName]":
				ParPlayerName = (configstext[idx+1])
				print ("ParPlayerName: %s" %(ParPlayerName))
			if line =="[ParFPS]":
				ParFPS = eval(configstext[idx+1])
				print ("ParFPS: %s" %(ParFPS))
			if line =="[ParScreenSize]":
				ParScreen = eval(configstext[idx+1])
				ParScreenSize = (ParScreen, ParScreen)
				print ("ParScreenSize: %s x %s" %(ParScreen, ParScreen))
			if line =="[ParGrabMouse]":
				ParGrabMouse = eval(configstext[idx+1])
				print ("ParGrabMouse: %s" %(ParGrabMouse))
			if line =="[ParLockMouse]":
				ParLockMouse = eval(configstext[idx+1])
				print ("ParLockMouse: %s" %(ParLockMouse))
			if line =="[ParShowMouse]":
				ParShowMouse = eval(configstext[idx+1])
				print ("ParShowMouse: %s" %(ParShowMouse))
			if line =="[ParBulletQty]":
				ParBulletQty = eval(configstext[idx+1])
				print ("ParBulletQty: %s" %(ParBulletQty))
			if line =="[ParBulletSpeed]":
				ParBulletSpeed = eval(configstext[idx+1])
				print ("ParBulletSpeed: %s" %(ParBulletSpeed))
			if line =="[ParLives]":
				ParLives = eval(configstext[idx+1])
				print ("ParLives: %s" %(ParLives))
			if line =="[ParMusicYN]":
				ParMusicYN = eval(configstext[idx+1])
				print ("ParMusicYN: %s" %(ParMusicYN))
			if line =="[ParMusicVol]":
				ParMusicVol = eval(configstext[idx+1])
				print ("ParMusicVol: %s" %(ParMusicVol))
			if line =="[ParLevelPack]":
				ParLevelPack = (configstext[idx+1])
				print ("ParLevelPack: %s" %(ParLevelPack))
			if line =="[ParIPServer]":
				ParIPServer = (configstext[idx+1])
				print ("ParIPServer: %s" %(ParIPServer))
			if line =="[ParIPServerPort]":
				ParIPServerPort = eval(configstext[idx+1])
				print ("ParIPServerPort: %s" %(ParIPServerPort))
			if line =="[ParIPaddressLocal]":
				ParIPaddressLocal =(configstext[idx+1])
				print ("ParIPaddressLocal: %s" %(ParIPaddressLocal))
			if line =="[ParAllowMulti360]":
				ParAllowMulti360 = eval(configstext[idx+1])
				print ("ParAllowMulti360: %s" %(ParAllowMulti360))
			if line =="[ParKeybUnicode]":
				ParKeybUnicode = eval(configstext[idx+1])
				print ("ParKeybUnicode: %s" %(ParKeybUnicode))
			if line =="[ParKeybi18n]":
				ParKeybi18n = (configstext[idx+1])
				print ("ParKeybi18n: %s" %(ParKeybi18n))
				
	except:
		print "Warning: INVALIDE PARAMETERS IN pybreak360.cfg !!!"

	return (ParPlayerName, ParFPS, ParScreenSize, ParGrabMouse, ParLockMouse, ParShowMouse, ParLives, ParBulletQty, ParBulletSpeed, \
	ParMusicYN, ParMusicVol, ParLevelPack, ParIPServer, ParIPServerPort, ParIPaddressLocal, ParAllowMulti360, ParKeybUnicode, ParKeybi18n) 

#DEFAULT VALUES IF NOT FOUND IN CONFIG FILE
ParPlayerName = "Gino"
ParFPS = 60 #60	
ParGrabMouse =False
ParLockMouse = False
ParShowMouse = True
ParLives = 5
ParBulletQty = 15
ParBulletSpeed = 10
ParMusicYN = True
ParMusicVol = 0.9
ParLevelPack = "Classic"
ParIPServer = "127.0.0.1"
ParIPaddressLocal = "127.0.0.1"
ParIPServerPort = 50000

ParAllowMulti360 = True
ParKeybUnicode = True
ParKeybi18n = "fr"

ParBallSpeedSlow = 4 # is level parameter
ParBallSpeedFast = 6 # is level parameter
ParDwngrdBrick = True # is level parameter
ParScreenSize = (640, 640)# is level parameter
	
ParBallSpeedSlow = 4 # is level parameter
ParBallSpeedFast = 6 # is level parameter
ParDwngrdBrick = True # is level parameter
ParScreenSize = (640, 640)# is level parameter

print ("Loading pybreak360.cfg file parameters")
ParPlayerName, ParFPS, ParScreenSize, ParGrabMouse, ParLockMouse, ParShowMouse, ParLives, ParBulletQty, ParBulletSpeed, ParMusicYN, ParMusicVol, \
	ParLevelPack, ParIPServer, ParIPServerPort, ParIPaddressLocal, ParAllowMulti360, ParKeybUnicode, ParKeybi18n = load_config('pybreak360.cfg')

