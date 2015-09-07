#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys, time, random #, platform, threading, math
import pygame
from pygame.locals import *

from reader import Reader

from pybreak360_sounds import *
from pybreak360_config import *
from pybreak360_sprites import *
from pybreak360_bricks import *
from pybreak360_cursors import WAIT_CURSOR, HAND_CURSOR
import pybreak360_kbd #as kbdi18n

import pybreak360_varglob as varglob

#WARNING: music_play & music_stop should be removed
#################################################
def music_play(song, times=-1):
	"""play start background music"""

	if ParMusicYN:
		path = os.path.join("sounds", song)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(times)
		pygame.mixer.music.set_volume(ParMusicVol)
#################################################
def music_stop():
	"""play stop background music"""

	if ParMusicYN:
		pygame.mixer.music.stop()
    
#################################################
def get_alpha_surface( surf, alpha=128, red=128, green=128, blue=128, mode=pygame.BLEND_RGBA_MULT):
	"""returns a copy of a surface object with user-defined 
	   values for red, green, blue and alpha. 
	   Values from 0-255. 
	   thanks to Claudio Canepa <ccanepacc@gmail.com>
	   for this function."""
  
	tmp = pygame.Surface( surf.get_size(), pygame.SRCALPHA, 32)
	tmp.fill( (red,green,blue,alpha) )
	tmp.blit(surf, (0,0), surf.get_rect(), mode)
	return tmp

#################################################
def load_backgnd(name):
	"""Load image from levels directory, and return image rect objet"""
	fullname = os.path.join('levels', name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
		image = pygame.transform.scale(image, varglob.fenetre.get_size())

	except pygame.error, message:
		print ("Warning: Load image %s FAIL: " %(fullname) )
		# if fail, Default background white
		image = pygame.Surface(varglob.fenetre.get_size())
		image = image.convert()
		image.fill((0, 0, 0))
		image.fill((255, 255, 255))

	return image, image.get_rect()

#################################################	
def level_blit(_levelNumber):
	"""blit level on screen fenetre """
	
	varglob.levelName, varglob.levelBackGnd, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, varglob.levelClient = level_select(_levelNumber)
	varglob.background, toto = load_backgnd(varglob.levelBackGnd)
	#Re-blit balls
	for idx, ball in enumerate(varglob.balls):
		varglob.balls[idx][0].updatefenetre()
		try: # thread may lock bilt
			varglob.balls[idx][1].draw(varglob.fenetre)
		except:
			pass
	#Re-blit bricks
	for idx, brick in enumerate(varglob.bricks):
		varglob.bricks[idx][0].updatefenetre(varglob.fenetre)
		try: # thread may lock bilt
			varglob.bricks[idx][1].draw(varglob.fenetre)
		except:
			pass
	#Re-blit bullets
	for idx, bullet in enumerate(varglob.bullets):
		varglob.bullets[idx][0].updatefenetre()
		try: # thread may lock bilt
			varglob.bullets[idx][1].draw(varglob.fenetre)
		except:
			pass
	#Refresh Pygame screen display
	try: # thread may lock bilt
		pygame.display.flip()
	except:
		time.sleep(0.1)
		pygame.display.flip()

#################################################	
def level_select(_levelNumber):
	"""return parameters and bricks level from levelpack list"""

	_levelNumber = _levelNumber
	varglob.levelName = varglob.levels[_levelNumber][0]
	varglob.levelBackGnd = varglob.levels[_levelNumber][1]
	levelBackSound = varglob.levels[_levelNumber][2]
	ParBallSpeedSlow = eval(varglob.levels[_levelNumber][3]) # is level parameter
	ParBallSpeedFast = eval(varglob.levels[_levelNumber][4]) # is level parameter
	ParDwngrdBrick = eval(varglob.levels[_levelNumber][5]) # is level parameter
	ParShiftBrick = eval(varglob.levels[_levelNumber][6]) # is level parameter
	ParBrickSpace = eval(varglob.levels[_levelNumber][7]) # is level parameter
	ParScreenSize = eval(varglob.levels[_levelNumber][8]) # is level parameter
	varglob.levelClient = varglob.levels[_levelNumber][9:] #bricks list for actual level
	
	# Pygame main screen display
	ParScreenSize = (ParScreenSize, ParScreenSize)		
	varglob.fenetre_size = ParScreenSize
	print ("fenetre_size: %s, %s" %(varglob.fenetre_size))
	varglob.fenetre_center = (varglob.fenetre_size[0] / 2 , varglob.fenetre_size[1] / 2)
	#print ("fenetre_center: %s, %s" %(varglob.fenetre_center))
	varglob.fenetre = pygame.display.set_mode(varglob.fenetre_size)
	varglob.background = pygame.transform.scale(varglob.background, varglob.fenetre.get_size())
	BckGndWall2 = pygame.transform.scale(BckGndWall, varglob.fenetre.get_size())
	varglob.fenetre.blit(varglob.background, (0,0))
	varglob.rayon = varglob.fenetre_center[1] - varglob.playersbat[0][3][1] # remove size bat sprite

	#bakground music before levels, continus
	if levelBackSound!="" and levelBackSound.upper()!="NONE":
		music_play(levelBackSound, -1)
	else:
		music_stop()

	#space within bricks depend levels file option
	#level = 9 x 18 brick de 32 pixel
	bspacex = ParBrickSpace #fenetre_size[0]/30 #15 #20 #40
	bspacey = bspacex * 2 #30 #40 #30 
	#print ('brickspace x:%s, y:%s' %(bspacex, bspacey))
	
	th_E = 0 # server isn't started yet
	# bricks doesn't communicate, it's ball which emit events
	varglob.bricks = []
	for xlevelPos, xlevel in enumerate(varglob.levelClient):
		for ylevelPos, ylevel in enumerate(xlevel):
			#V106: display random bricks as brick(?)
			if ylevel != 0:
				linelenght = len(xlevel)
				if ParShiftBrick:
					if xlevelPos%2 == 0: #line even
						brick = Brick((varglob.fenetre_center[0]-bspacey*linelenght/2+bspacey/4+bspacey*ylevelPos, \
						varglob.fenetre_center[1]-bspacex*linelenght+bspacex*xlevelPos), \
						th_E, 0, ylevel, 1)
					else: #line odd
						brick = Brick((varglob.fenetre_center[0]-bspacey*linelenght/2-bspacey/4+bspacey*ylevelPos, \
						varglob.fenetre_center[1]-bspacex*linelenght+bspacex*xlevelPos), \
						th_E, 0, ylevel, 1)
				else: # don't shift brick in level
					brick = Brick((varglob.fenetre_center[0]-ParBrickSpace*linelenght/2+ParBrickSpace*ylevelPos, \
					varglob.fenetre_center[1]-ParBrickSpace*linelenght/2+ParBrickSpace*xlevelPos), \
					th_E, 0, ylevel, 1)
	
				bricksprite = pygame.sprite.RenderPlain(brick)
				varglob.bricks.append([brick, bricksprite])
				#del brick

	return (varglob.levelName, varglob.levelBackGnd, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, varglob.levelClient)

#################################################	
def designer_blit_level_array(_levelNumber, designer_bricks_select, designer_bricks_array, MenuBottom):
	"""blit level for designer on screen fenetre """
	
	#varglob.levelName, varglob.levelBackGnd, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, varglob.levelClient = level_select(_levelNumber)
	varglob.background, toto = load_backgnd(varglob.levelBackGnd)
	varglob.fenetre.blit(varglob.background, (0,0))

	#Re-blit bricks select MenuBottom
	for idx, MenuBottomItem in enumerate(MenuBottom):
		try: # thread may lock bilt
			varglob.fenetre.blit(MenuBottom[idx][0], (MenuBottom[idx][1][0],MenuBottom[idx][1][1]) )
		except:
			pass

	#Re-blit bricks select menu
	for idx, brick in enumerate(designer_bricks_select):
		designer_bricks_select[idx][0].updatefenetre(varglob.fenetre)
		try: # thread may lock bilt
			designer_bricks_select[idx][1].draw(varglob.fenetre)
		except:
			pass

	#Re-blit bricks
	for idx, brick in enumerate(designer_bricks_array):
		for idx2, brick2 in enumerate(brick):
			designer_bricks_array[idx][idx2][0].updatefenetre(varglob.fenetre)
			try: # thread may lock bilt
				designer_bricks_array[idx][idx2][1].draw(varglob.fenetre)
			except:
				pass

	#blit parameters
	designer_LEVELNAME = "URANUS"
	designer_LEVELBACKGND = "uranus.jpg"
	designer_LEVELSOUND = "TimothyPinkhamStillAnotherWanderer.ogg"
	designer_ParBallSpeedSlow = 4
	designer_ParBallSpeedFast = 6
	designer_ParDwngrdBrick = True
	designer_ParShiftBrick = True
	designer_ParBrickSpace = 18
	designer_ParScreenSize = 480
	designer_array_X = 9
	designer_array_Y = 9
	
	#Refresh pygame.display.flip() screen display on designer_level

#################################################	
def designer_level_get_array(levelClient, ParShiftBrick, ParBrickSpace, th_E):
	"""return level bricks and array for designer"""
	#space within bricks depend levels file option
	bspacex = ParBrickSpace #fenetre_size[0]/30 #15 #20 #40
	bspacey = bspacex * 2 #30 #40 #30 
	
	# remap all bricks for actual level
	designer_bricks = []
	designer_bricks_array = []
	for xlevelPos, xlevel in enumerate(levelClient):
		designer_bricks_array1 = []
		for ylevelPos, ylevel in enumerate(xlevel):

			ylevel2 = ylevel
			if ylevel2 == 0:
				ylevel2 = 22 #design empty brick
			if ylevel2 != 0:
				linelenght = len(xlevel)
				if ParShiftBrick:
					if xlevelPos%2 == 0: #line even
						brick = Brick((varglob.fenetre_center[0]-bspacey*linelenght/2+bspacey/4+bspacey*ylevelPos, \
						varglob.fenetre_center[1]-bspacex*linelenght+bspacex*xlevelPos), \
						th_E, 0, ylevel2, 1)
					else: #line odd
						brick = Brick((varglob.fenetre_center[0]-bspacey*linelenght/2-bspacey/4+bspacey*ylevelPos, \
						varglob.fenetre_center[1]-bspacex*linelenght+bspacex*xlevelPos), \
						th_E, 0, ylevel2, 1)
				else: # don't shift brick in level
					brick = Brick((varglob.fenetre_center[0]-ParBrickSpace*linelenght/2+ParBrickSpace*ylevelPos, \
					varglob.fenetre_center[1]-ParBrickSpace*linelenght/2+ParBrickSpace*xlevelPos), \
					th_E, 0, ylevel2, 1)
	
				bricksprite = pygame.sprite.RenderPlain(brick)
				designer_bricks.append([brick, bricksprite])
				#del brick
			if ylevel2 == 22: designer_bricks_array1.append([brick, bricksprite, 0])
			else:designer_bricks_array1.append([brick, bricksprite, ylevel2])
		designer_bricks_array.append(designer_bricks_array1)
		designer_bricks_array1 = []
		
	return (designer_bricks, designer_bricks_array)


#################################################	
def designer_level(_levelNumber, th_E):
	"""level bricks designer"""

	varglob.background, toto = load_backgnd(varglob.levelBackGnd)

	# stop the game
	varglob.anouncetexte.append("!ABORTED!")
	th_E.sendMsg("!ABORTED!\n" )
	#stop ball and missils
	for idx, ball in enumerate(varglob.balls):
		varglob.balls[idx][0].setspeed(0)
		varglob.balls[idx][0].setporteur(idx+1)
		varglob.balls[idx][0].setimg(idx+1)
		# in thread reception
		th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0))
	for idx, bullet in enumerate(varglob.bullets):
		varglob.bullets[idx][0].setspeed(0)
		varglob.bullets[idx][0].setporteur(idx+1)
		varglob.bullets[idx][0].setimg(idx+1)
		# in thread reception
		th_E.sendMsg("T:%s:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0, varglob.players[idx][2]))
		#th_E.sendMsg("T:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.bullets[idx][0].getimg(), bx, by, math.pi+varglob.players[bporteur-1][2], 0))

		# raz score, setback Qty ball & bullets
		varglob.players[idx][3] = 0
		varglob.players[idx][4] = ParBulletQty
		varglob.players[idx][5] = ParLives
		if varglob.players[idx][2] != "free":
			# update player
			th_E.sendMsg("S%s:%s\n" %(idx, varglob.players[idx][3]))

	#redesign level and bricksmap

	_levelNumber = _levelNumber
	varglob.levelName = varglob.levels[_levelNumber][0]
	varglob.levelBackGnd = varglob.levels[_levelNumber][1]
	levelBackSound = varglob.levels[_levelNumber][2]
	ParBallSpeedSlow = eval(varglob.levels[_levelNumber][3]) # is level parameter
	ParBallSpeedFast = eval(varglob.levels[_levelNumber][4]) # is level parameter
	ParDwngrdBrick = eval(varglob.levels[_levelNumber][5]) # is level parameter
	ParShiftBrick = eval(varglob.levels[_levelNumber][6]) # is level parameter
	ParBrickSpace = eval(varglob.levels[_levelNumber][7]) # is level parameter
	ParScreenSize = eval(varglob.levels[_levelNumber][8]) # is level parameter
	varglob.levelClient = varglob.levels[_levelNumber][9:] #bricks list for actual level
	
	# Pygame main screen display
	ParScreenSize = (ParScreenSize, ParScreenSize)		
	varglob.fenetre_size = ParScreenSize
	print ("fenetre_size: %s, %s" %(varglob.fenetre_size))
	varglob.fenetre_center = (varglob.fenetre_size[0] / 2 , varglob.fenetre_size[1] / 2)
	varglob.fenetre = pygame.display.set_mode(varglob.fenetre_size)
	varglob.background = pygame.transform.scale(varglob.background, varglob.fenetre.get_size())
	BckGndWall2 = pygame.transform.scale(BckGndWall, varglob.fenetre.get_size())
	varglob.fenetre.blit(varglob.background, (0,0))
	varglob.rayon = varglob.fenetre_center[1] - varglob.playersbat[0][3][1] # remove size bat sprite

	#bakground music before levels, continus
	if levelBackSound!="" and levelBackSound.upper()!="NONE":
		music_play(levelBackSound, -1)
	else:
		music_stop()

	designer_bricks, designer_bricks_array = designer_level_get_array(varglob.levelClient, ParShiftBrick, ParBrickSpace, th_E)

	#menu top for brick select
	designer_bricks_select = []
	for idx, brick in enumerate(BricksColor):
		#2 last bricks empty and highlight are for designer
		if idx < len(BricksColor) -2:
			if brick != None:
				brickpos = brick.get_rect() #(0,0,32,32)
				if idx < 10:
					brickpos[0] = brickpos[3] * idx
				else:
					brickpos[0] = brickpos[3] * (idx-10)
					brickpos[1] = brickpos[3]
				#varglob.fenetre.blit(brick, brickpos)
				brick = Brick((brickpos[0], brickpos[1]), th_E, 0, idx, 1)
				bricksprite = pygame.sprite.RenderPlain(brick)
				designer_bricks_select.append([brick, bricksprite])
	
	mouseX,mouseY = 0, 0
	brickSelected = 0
	designer_running = True
	while designer_running:
		MenuBottom =[]
		font = pygame.font.Font("freesansbold.ttf", 14)			
		font.set_bold(True)
		#varglob.levelname
		text = font.render("%s, right/left click change Parameters, S to save" %(varglob.levelName), 1, (0, 0, 0)) #RGBA
		#text = get_alpha_surface(text, 200, 200, 200, 200, pygame.BLEND_RGBA_MULT) # get current alpha
		textpos = text.get_rect()
		textpos.x = varglob.fenetre.get_rect()[0]
		textpos.y = varglob.fenetre.get_rect()[2]-(textpos[3]*2)
		MenuBottom.append((text,textpos))
		#ParBallSpeedSlow
		text = font.render("Slow:%s" %(ParBallSpeedSlow), 1, (0, 0, 0)) #RGBA
		#text = get_alpha_surface(text, 200, 200, 200, 200, pygame.BLEND_RGBA_MULT) # get current alpha
		textpos = text.get_rect()
		#textpos.x = MenuBottom[0][1][0]+MenuBottom[0][1][2]+5 #
		textpos.x = varglob.fenetre.get_rect()[0]
		textpos.y = varglob.fenetre.get_rect()[2]-textpos[3]
		MenuBottom.append((text,textpos))
		#ParBallSpeedFast
		text = font.render("Fast:%s" %(ParBallSpeedFast), 1, (0, 0, 0)) #RGBA
		#text = get_alpha_surface(text, 200, 200, 200, 200, pygame.BLEND_RGBA_MULT) # get current alpha
		textpos = text.get_rect()
		textpos.x = MenuBottom[1][1][0]+MenuBottom[1][1][2]+10 #
		textpos.y = varglob.fenetre.get_rect()[2]-textpos[3]
		MenuBottom.append((text,textpos))
		#ParDwngrdBrick
		text = font.render("Dwngrd:%s" %(ParDwngrdBrick), 1, (0, 0, 0)) #RGBA
		#text = get_alpha_surface(text, 200, 200, 200, 200, pygame.BLEND_RGBA_MULT) # get current alpha
		textpos = text.get_rect()
		textpos.x = MenuBottom[2][1][0]+MenuBottom[2][1][2]+10 #
		textpos.y = varglob.fenetre.get_rect()[2]-textpos[3]
		MenuBottom.append((text,textpos))
		#ParShiftBrick
		text = font.render("ShftBrk:%s" %(ParShiftBrick), 1, (0, 0, 0)) #RGBA
		#text = get_alpha_surface(text, 200, 200, 200, 200, pygame.BLEND_RGBA_MULT) # get current alpha
		textpos = text.get_rect()
		textpos.x = MenuBottom[3][1][0]+MenuBottom[3][1][2]+10 #
		textpos.y = varglob.fenetre.get_rect()[2]-textpos[3]
		MenuBottom.append((text,textpos))
		#ParBrickSpace
		text = font.render("BrkSpc:%s" %(ParBrickSpace), 1, (0, 0, 0)) #RGBA
		#text = get_alpha_surface(text, 200, 200, 200, 200, pygame.BLEND_RGBA_MULT) # get current alpha
		textpos = text.get_rect()
		textpos.x = MenuBottom[4][1][0]+MenuBottom[4][1][2]+10 #
		textpos.y = varglob.fenetre.get_rect()[2]-textpos[3]
		MenuBottom.append((text,textpos))
		#print MenuBottom
	
		designer_blit_level_array(_levelNumber, designer_bricks_select, designer_bricks_array, MenuBottom)

		for event in pygame.event.get():    # Waiting for events
			#if (event.type == QUIT):
			#	designer_running = False
			#	break
			if (event.type == KEYDOWN):
				if (event.key == K_d): #exit from designer
					designer_running = False
				if (event.key == K_ESCAPE): #exit from designer
					designer_running = False
				if (event.key == K_s): #save levelpack
					font = pygame.font.Font("freesansbold.ttf", 20)			
					font.set_bold(True)
					bgd = 20, 20, 20

					text = font.render("LevelPack Saved", 1, (0, 0, 0)) #RGBA
					text = get_alpha_surface(text, varglob.anouncealphaactu, varglob.anouncealphaactu, varglob.anouncealphaactu, \
					varglob.anouncealphaactu, pygame.BLEND_RGBA_MULT) # get current alpha
					textpos = text.get_rect()
					textpos.centerx = varglob.background.get_rect().centerx
					textpos.centery = varglob.background.get_rect().centery
					try: # thread may lock bilt
						varglob.fenetre.blit(text, textpos)
						pygame.display.flip()
					except:
						time.sleep(0.1)
						try:
							varglob.fenetre.blit(text, textpos)
							pygame.display.flip()
						except:
							pass
					time.sleep(0.5)
					
					designer_level = []
					designer_sublevel = []
					#print len(designer_bricks_array)
					for idx, designer_bricks_array1 in enumerate(designer_bricks_array):
						designer_sublevel = []
						for idx2, brick in enumerate(designer_bricks_array1):
							#designer_sublevel.append(designer_bricks_array[idx][idx2][2])
							designer_sublevel.append(brick[2])
						#print designer_sublevel
						designer_level.append(designer_sublevel)
						designer_sublevel = []
					#print designer_level
					#print "\n"
					#print varglob.levels[_levelNumber]
					#print varglob.levelClient
					varglob.levels[_levelNumber] = []
					varglob.levels[_levelNumber].append(varglob.levelName)# = levels[levelNumber][0]
					varglob.levels[_levelNumber].append(varglob.levelBackGnd)# = levels[levelNumber][1]
					varglob.levels[_levelNumber].append(levelBackSound)# = levels[levelNumber][2]
					varglob.levels[_levelNumber].append(str(ParBallSpeedSlow))# = eval(levels[levelNumber][3]) # is level parameter
					varglob.levels[_levelNumber].append(str(ParBallSpeedFast))# = eval(levels[levelNumber][4]) # is level parameter
					varglob.levels[_levelNumber].append(str(ParDwngrdBrick))# = eval(levels[levelNumber][5]) # is level parameter
					varglob.levels[_levelNumber].append(str(ParShiftBrick))# = eval(levels[levelNumber][6]) # is level parameter
					varglob.levels[_levelNumber].append(str(ParBrickSpace))# = eval(levels[levelNumber][7]) # is level parameter
					varglob.levels[_levelNumber].append(str(ParScreenSize[0]))# = eval(levels[levelNumber][8]) # is level parameter
					varglob.levelClient = [tuple(b) for b in designer_level] #bricks list for actual level
					for lines in varglob.levelClient:
						varglob.levels[_levelNumber].append(lines)# = levels[levelNumber][9:] #bricks list for actual level
					#tuple(tuple(b) for b in designer_level)
					#print varglob.levels[_levelNumber]
					
					#finally save levelpack
					designer_level_save(ParLevelPack)

			if event.type == MOUSEMOTION:
				mouseX,mouseY = event.pos

			if event.type == MOUSEBUTTONDOWN:
				if event.button == 3: #right button erase blick
					# check if mouse brick level click
					for idx, designer_bricks_array1 in enumerate(designer_bricks_array):
						for idx2, designerBrick in enumerate(designer_bricks_array1):
							#designer_bricks_array1.append([brick, bricksprite, ylevel2])
							designerBrickRect = designer_bricks_array1[idx2][0].getrect()
							designerBrickRectCenter = designerBrickRect.center
							
							if (abs(mouseX - designerBrickRectCenter[0]) < 10) and (abs(mouseY - designerBrickRectCenter[1]) < 10):
								print ("ClearBrick")
								designer_bricks_array1[idx2][2] = 0
								designer_bricks_array1[idx2][0].setimg(22)

					# check if mouse click menuBottom
					for idx, MenuBottomItem in enumerate(MenuBottom):
						#if MenuBottom[idx][0].rect.collidepoint(mouseX,mouseY):
						if MenuBottom[idx][1].collidepoint(mouseX,mouseY):
							#levelname, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, ParShiftBrick, ParBrickSpace
							print ("MenuBottom:%s" %(idx))
							if idx == 1:
								if ParBallSpeedSlow >3:
									ParBallSpeedSlow -=1
							if idx == 2:
								if ParBallSpeedFast >3:
									ParBallSpeedFast -=1
							if idx == 3:
								ParDwngrdBrick = not ParDwngrdBrick
							if idx == 4:
								ParShiftBrick = not ParShiftBrick
								designer_bricks, designer_bricks_array = designer_level_get_array(varglob.levelClient, ParShiftBrick, ParBrickSpace, th_E)
							if idx == 5:
								if ParBrickSpace >10:
									ParBrickSpace -=1
									designer_bricks, designer_bricks_array = designer_level_get_array(varglob.levelClient, ParShiftBrick, ParBrickSpace, th_E)
							
				if event.button == 1: #left button
					# check if mouse click menuBottom
					for idx, MenuBottomItem in enumerate(MenuBottom):
						#if MenuBottom[idx][0].rect.collidepoint(mouseX,mouseY):
						if MenuBottom[idx][1].collidepoint(mouseX,mouseY):
							#levelname, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, ParShiftBrick, ParBrickSpace
							print ("MenuBottom:%s" %(idx))
							if idx == 1:
								if ParBallSpeedSlow <9:
									ParBallSpeedSlow +=1
							if idx == 2:
								if ParBallSpeedFast <9:
									ParBallSpeedFast +=1
							if idx == 3:
								ParDwngrdBrick = not ParDwngrdBrick
							if idx == 4:
								ParShiftBrick = not ParShiftBrick
								designer_bricks, designer_bricks_array = designer_level_get_array(varglob.levelClient, ParShiftBrick, ParBrickSpace, th_E)
							if idx == 5:
								if ParBrickSpace <40:
									ParBrickSpace +=1
									designer_bricks, designer_bricks_array = designer_level_get_array(varglob.levelClient, ParShiftBrick, ParBrickSpace, th_E)
								
					# update on level array
					EndUpdateArray = False
					for idx, designer_bricks_array1 in enumerate(designer_bricks_array):
						for idx2, designerBrick in enumerate(designer_bricks_array1):
							#designer_bricks_array1.append([brick, bricksprite, ylevel2])
							designerBrickRect = designer_bricks_array1[idx2][0].getrect()
							designerBrickRectCenter = designerBrickRect.center
							
							if (abs(mouseX - designerBrickRectCenter[0]) < 10) and (abs(mouseY - designerBrickRectCenter[1]) < 10):
								print 'yay!'
								#if brickSelected == None or brickSelected == 8 or brickSelected == 9:
								if brickSelected == 0:
									designer_bricks_array1[idx2][2] = 0
									designer_bricks_array1[idx2][0].setimg(22)
									EndUpdateArray = True
								elif brickSelected >= 8:
									designer_bricks_array1[idx2][2] = brickSelected + 2
									designer_bricks_array1[idx2][0].setimg(brickSelected + 2)
									EndUpdateArray = True
								else:
									designer_bricks_array1[idx2][2] = brickSelected
									designer_bricks_array1[idx2][0].setimg(brickSelected)
									EndUpdateArray = True
								break
						if EndUpdateArray == True:
							print designer_bricks_array1[idx2][2]
							break
							
					# check if mouse click brick select menu
					for idx, brick in enumerate(designer_bricks_select):
					    if designer_bricks_select[idx][0].rect.collidepoint(mouseX,mouseY):
							brickSelected = idx
					
		#highlight on mouse pos
		for idx, designerBrick in enumerate(designer_bricks):
			designerBrickRect = designer_bricks[idx][0].getrect()
			designerBrickRectCenter = designerBrickRect.center			
			if (abs(mouseX - designerBrickRectCenter[0]) < 10) and (abs(mouseY - designerBrickRectCenter[1]) < 10):
				varglob.fenetre.blit(BricksColor[23], (designerBrickRect[0],designerBrickRect[1]) )
		#highlight brickSelected
		for idx, designerBrick in enumerate(designer_bricks_select):
			designerBrickRect = designer_bricks_select[idx][0].getrect()
			designerBrickRectCenter = designerBrickRect.center			
			if brickSelected == idx:
				varglob.fenetre.blit(BricksColor[23], (designerBrickRect[0],designerBrickRect[1]) )

		#finally Refresh Pygame screen display
		try: # thread may lock bilt
			pygame.display.flip()
		except:
			time.sleep(0.1)
			pygame.display.flip()

	level_select(_levelNumber)
	#time.sleep(0.3)

#################################################	
def designer_level_save(levelpack):
	"""save modified level from designer"""

	fullname = os.path.join("levels", "%s.level" %(levelpack))
	try:
		fichier = open(fullname, "w")
		
		fichier.write("# pybreak360 version: %s\n" %(varglob.pybreak360version))
		fichier.write("# EACH LEVEL SHOULD BE A SQUARE\n")
		fichier.write("#\n")
		fichier.write("# NUMBER OF LINES DEPEND OF ParBrickSpace TO BE CORRECT\n")
		fichier.write("# 0 = NONE, 1 = YELLOW, 2 = GREEN, 3 = BLUE, 4 = RED\n")
		fichier.write("# 5 = BROWN, 6 = GREY, 7 = BLACK\n")
		fichier.write("# 8, 9 = NOT USED\n")
		fichier.write("# BONUS:\n")
		fichier.write("# A = BALLS, B = BULLETS, C = BALLSPEED, D = GLUE, E = BOMB\n")
		fichier.write("# F = WALL\n")
		fichier.write("# G = RANDOM (0-6)\n")
		fichier.write("# H = INVERT COMMAND, I = REDUCE, J = ENLARGE, K= NUCLEAR\n")
		fichier.write("# L = BIGBALL\n")
		fichier.write("#\n")
		fichier.write("# if ParAllowMulti360 = False, don't use brick H = INVERT COMMAND.\n")
		fichier.write("# if ParDwngrdBrick = False, Bricks explose immediately, otherwise brick descrease until 0, except blacks.\n")
		fichier.write("\n")
		
		for idx, line in enumerate(varglob.levels):
			#print (idx)
			fichier.write("[LEVELNAME]\n")
			fichier.write(line[0]+"\n")
			fichier.write("[LEVELBACKGND]\n")
			fichier.write(line[1]+"\n")
			fichier.write("[LEVELSOUND]\n")
			fichier.write(line[2]+"\n")
			fichier.write("[ParBallSpeedSlow]\n")
			fichier.write(line[3]+"\n")
			fichier.write("[ParBallSpeedFast]\n")
			fichier.write(line[4]+"\n")
			fichier.write("[ParDwngrdBrick]\n")
			fichier.write(line[5]+"\n")
			fichier.write("[ParShiftBrick]\n")
			fichier.write(line[6]+"\n")
			fichier.write("[ParBrickSpace]\n")
			fichier.write(line[7]+"\n")
			fichier.write("[ParScreenSize]\n")
			fichier.write(line[8]+"\n")
			fichier.write("[LevelValue]\n")
			end_level_line = len(line)
			print end_level_line
			print line[9]
			for level_line in xrange(9, end_level_line):
				if eval(line[6]): #ParShiftBrick
					if level_line%2 != 0:
						fichier.write(" ") # only for visual shift presentation
				
				#fichier.write(str(line[level_line])+"\n")
				fichier.write("(")
				for idx2, level_line_item in enumerate(line[level_line]):
					ll=level_line_item
					if ll==16 : ll = "G" #Random
					elif ll==17 : ll = "H" #Invert
					elif ll==18 : ll = "I" #Reduce
					elif ll==19 : ll = "J" #Enlarge
					elif ll==20 : ll = "K" #Nuclear
					elif ll==21 : ll = "L" #BigBall
					else: ll = hex(ll)[-1:].upper()
					fichier.write(ll)
					if idx2+1 < len(line[level_line]): fichier.write(",")
				fichier.write(")\n")

			fichier.write("[LEVELEND]\n")
			fichier.write("\n")

		fichier.close()

		print ("%s saved" %(fullname))
	except pygame.error, message:
		print ("Warning: unable to save %s" %(fullname))
	
