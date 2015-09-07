#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys, math, time, random
import pygame

from pybreak360_sprites import *
import pybreak360_varglob as varglob #just need for colors ?

#################################################
class Brick(pygame.sprite.Sprite):
	"""brick HEXA object
	Return: objet brick
	Fonctions: check_collision, get or set, status, posxy, rect, img
	Attributs: img, image, rect, score"""

	def __init__(self, (xy), th_E, idx, img, status):
	#def __init__(self, (xy), th_E, idx, img, status, bcolor, brect):
		
		pygame.sprite.Sprite.__init__(self)
		self.th_E = th_E
		self.idx = idx #NOT USED ACTUALLY ?!!!
		self.status = status

		self.collision = [False] * 9

		#Loading bricks image
		self.img = img

		self.image = BricksColor[img]
		
		self.img = img
		#print ("brick img: %s" %(img))
		if img == 0:
			self.image, self.rect = load_png('H_NONE.PNG')
		if img == 1:
			self.image, self.rect = load_png('H_YELLOW.PNG')
		if img == 2:
			self.image, self.rect = load_png('H_GREEN.PNG')
		if img == 3:
			self.image, self.rect = load_png('H_BLUE.PNG')
		if img == 4:
			self.image, self.rect = load_png('H_RED.PNG')
		if img == 5:
			self.image, self.rect = load_png('H_BROWN.PNG')
		if img == 6:
			self.image, self.rect = load_png('H_GREY.PNG')
		if img == 7:
			self.image, self.rect = load_png('H_BLACK.PNG')
		#bonus
		if img == 10:
			self.image, self.rect = load_png('H_BALLS.PNG')
		if img == 11:
			self.image, self.rect = load_png('H_BULLETS.PNG')
		if img == 12:
			self.image, self.rect = load_png('H_BALLSPEED.PNG')
		if img == 13:
			self.image, self.rect = load_png('H_GLUE.PNG')
		if img == 14:
			self.image, self.rect = load_png('H_BOMB.PNG')
		if img == 15:
			self.image, self.rect = load_png('H_WALL.PNG')
		if img == 16:
			self.image, self.rect = load_png('H_RANDOM.PNG')
		if img == 17:
			self.image, self.rect = load_png('H_INVERT.PNG')
		if img == 18:
			self.image, self.rect = load_png('H_REDUCE.PNG')
		if img == 19:
			self.image, self.rect = load_png('H_ENLARGE.PNG')
		if img == 20:
			self.image, self.rect = load_png('H_NUCLEAR.PNG')
		if img == 21:
			self.image, self.rect = load_png('H_BIGBALL.PNG')
		if img == 22:
			self.image, self.rect = load_png('H_EMPTY.PNG')
		if img == 23:
			self.image, self.rect = load_png('H_EMPTY2.PNG')

		#BricksRect[img].move(-BricksRect[img].x, -BricksRect[img].y) #= 0
		#BricksRect[img].move(0, 0) #= 0
		#BricksRect[img].move_ip(-BricksRect[img].x, -BricksRect[img].y) #= 0
		
		#brect2 = list(BricksRect)
		#self.rect = list(brect2)[img]
		#self.rect.move(-(self.rect.x), -(self.rect.y)) #= 0
		#self.rect.move(0, 0) #= 0
		
		#self.rect.move(0, 0)
		self.rect = self.image.get_rect()
		
		# !!! WARNING: why does BricksRect[img] change when self.rect.x/y change? it must not be the same namespace...? !!!
		#print (self.rect)
		
		# convert Surfaces for faster bliting to the screen into load_png()

		#newpos = self.calcnewpos(self.rect,self.vector)
		#self.rect = newpos
		#self.rect.move(xy[0], xy[1]) # initpos
		self.rect.x = (xy)[0] # initpos
		self.rect.y = (xy)[1] # initpos
		
		#BricksRect[img].move(-BricksRect[img].x, -BricksRect[img].y) #= 0
		#BricksRect[img].move(0, 0) #= 0
		#BricksRect[img].move_ip(-BricksRect[img].x, -BricksRect[img].y) #= 0

		#print ("set brick img: %s, (xy)=%s, %s" %(img, self.rect.x, self.rect.y))

		#screen = pygame.display.get_surface()
		#self.area = screen.get_rect()
		
		#global rayon, fenetre_center
		#self.screencenter = self.area.center
		#self.rayon = rayon +1000

		#self.rads = 0
		#self.hit = 0
		
		# show score during hit
		# V101 showBrickScore
		self.time = time.time()
		self.player = 0
		self.score = "0"
		
		a="""
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
		a="""
		self.colors = (varglob.Black, varglob.DeepYellow, varglob.DeepGreen, varglob.DeepBlue, varglob.DeepRed)

		font = pygame.font.Font("freesansbold.ttf", 20)
		self.textBrickScore = font.render(self.score, 1, self.colors[0])
		self.textBrickScorePos = self.textBrickScore.get_rect()
		self.textBrickScorePos[0] = self.rect.center[0]-self.textBrickScorePos[2]/2
		self.textBrickScorePos[1] = self.rect.center[1]-self.textBrickScorePos[3]/2
		#for contrast
		self.textBrickScore2 = font.render(self.score, 1, self.colors[0])
		self.textBrickScore2Pos = self.textBrickScore2.get_rect()
		self.textBrickScore2Pos[0] = self.rect.center[0]-self.textBrickScore2Pos[2]/2
		self.textBrickScore2Pos[1] = self.rect.center[1]-self.textBrickScore2Pos[3]/2
		
	def getimg(self):
		"""return image number"""
		return (self.img)

	def setimg(self, img):
		"""define image brick"""
		self.img = img

		global BricksColor
		#BricksColor = (HexaNone, HexaYellow, HexaGreen, HexaBlue, HexaRed, HexaBrown, HexaGrey, HexaBlack, None, None, \
		#HexaLive, HexaBullets, HexaSpeed, HexaGlue, HexaBomb, HexaWall, HexaRand, HexaInvert, HexaReduce, HexaEnlarge, \
		#HexaNuclear,  HexaBigBall, HexaEmpty, HexaEmpty2)
		if img == 8 or img == 9 or img > 23 or img < 0 :
			print ("Warning: ERROR CHANGING BRICK IMG: %s" %(img) )
		else:
			self.image = BricksColor[img]
			self.img = img

	def getrect(self):
		"""return surface(x, y, x1, y1) """
		return (self.rect)

	def getposxy(self):
		"""return position (x, y) """
		return (self.rect.x, self.rect.y)

	def setposxy(self, (xy)):
		"""define position xy"""
		self.rect.x=(xy)[0] # initpos
		self.rect.y=(xy)[1] # initpos
		
	def getstatus(self):
		"""return status 0=absent, 1=present"""
		return (self.status)

	def getBrickScore(self):
		"""function Brick Score, return Brick hit score messages"""
		#return (self.time, self.player, self.score)
		return (self.score)

	def getBrickScorePlayer(self):
		"""function Brick Score Player, return Brick hit score messages"""
		#return (self.time, self.player, self.score)
		return (self.player)

	def setstatus(self, status):
		"""define status 0=absent, 1=present"""
		self.status = status

	def setth_E(self, th_E):
		"""define thread emit server"""
		self.th_E = th_E
		
	def check_collision(self, rect):
		self.collision[0] = rect.collidepoint(self.rect.topleft)
		self.collision[1] = rect.collidepoint(self.rect.topright)
		self.collision[2] = rect.collidepoint(self.rect.bottomleft)
		self.collision[3] = rect.collidepoint(self.rect.bottomright)

		self.collision[4] = rect.collidepoint(self.rect.midleft)
		self.collision[5] = rect.collidepoint(self.rect.midright)
		self.collision[6] = rect.collidepoint(self.rect.midtop)
		self.collision[7] = rect.collidepoint(self.rect.midbottom)

		self.collision[8] = rect.collidepoint(self.rect.center)
		return (self.collision)

	def showBrickScore(self, score, player):
		"""function Brick Score, display Brick hit score messages"""

		global fenetre
		self.time = time.time()
		self.player = player
		#self.score = "7" #test
		self.score = str(score)
		
		self.color = self.colors[self.player]

		print ("BrickScore: %s, player: %s\n" %(self.score, self.player) )

		font = pygame.font.Font("freesansbold.ttf", 20)
		
		self.textBrickScore = font.render(self.score, 1, self.color)
		self.textBrickScorePos = self.textBrickScore.get_rect()
		self.textBrickScorePos[0] = self.rect.center[0]-self.textBrickScorePos[2]/2
		self.textBrickScorePos[1] = self.rect.center[1]-self.textBrickScorePos[3]/2

		#for contrast
		self.textBrickScore2 = font.render(self.score, 1, self.colors[0])
		self.textBrickScore2Pos = self.textBrickScore2.get_rect()
		self.textBrickScore2Pos[0] = self.rect.center[0]-self.textBrickScore2Pos[2]/2 + 2
		self.textBrickScore2Pos[1] = self.rect.center[1]-self.textBrickScore2Pos[3]/2 + 2

		#self.image, self.rect = textBrickScore, textBrickScorePos

		self.time = time.time() + 0.7

	def showBrickScoreUpdate(self, fenetre):
		"""function Brick Score Update, non-thread timing to display Brick hit score messages"""
		#global fenetre
		if self.score != "0":
			if self.time >= time.time():
				try:
					fenetre.blit(self.textBrickScore2, self.textBrickScore2Pos) # for contrast
					fenetre.blit(self.textBrickScore, self.textBrickScorePos)
					#fenetre.blit(self.image, self.rect)
				except:
					pass
			else:
				self.score = "0" #avoid display in main loop
				#self.setimg(0)
				print ("stopping BrickScore: %s, player: %s\n" %(self.score, self.player) )

	def updatefenetre(self, fenetre):
		"""update change fenetre size"""
		#screen = pygame.display.get_surface()
		self.area = fenetre.get_rect()
		#global rayon, fenetre_center
		#self.screencenter = self.area.center
		#don't need:
		#self.rayon = rayon +1000 #radius where is ball, +1000 to be sur starting from far
