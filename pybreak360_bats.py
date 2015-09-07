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

#################################################
def load_batpng(bat, png):
	"""change bat picture (No_Bat[0-3], No_png[0-2])"""

	if bat==0:
		if png==0:
			if varglob.BatDim[0] == 0:
				varglob.playersbat[bat][0] = g_bat_yellow2
			if varglob.BatDim[0] == 1:
				varglob.playersbat[bat][0] = g_bat_yellow3short
			if varglob.BatDim[0] == 2:
				varglob.playersbat[bat][0] = g_bat_yellow4long
		if png==1:
			if varglob.BatDim[0] == 0:
				varglob.playersbat[bat][0] = g_bat_yellow2light
			if varglob.BatDim[0] == 1:
				varglob.playersbat[bat][0] = g_bat_yellow3shortlight
			if varglob.BatDim[0] == 2:
				varglob.playersbat[bat][0] = g_bat_yellow4longlight
		if png==2:
			if varglob.BatDim[0] == 0:
				varglob.playersbat[bat][0] = g_bat_yellow2dark
			if varglob.BatDim[0] == 1:
				varglob.playersbat[bat][0] = g_bat_yellow3shortdark
			if varglob.BatDim[0] == 2:
				varglob.playersbat[bat][0] = g_bat_yellow4longdark

	if bat==1:
		if png==0:
			if varglob.BatDim[1] == 0:
				varglob.playersbat[bat][0] = g_bat_green2
			if varglob.BatDim[1] == 1:
				varglob.playersbat[bat][0] = g_bat_green3short
			if varglob.BatDim[1] == 2:
				varglob.playersbat[bat][0] = g_bat_green4long
		if png==1:
			if varglob.BatDim[1] == 0:
				varglob.playersbat[bat][0] = g_bat_green2light
			if varglob.BatDim[1] == 1:
				varglob.playersbat[bat][0] = g_bat_green3shortlight
			if varglob.BatDim[1] == 2:
				varglob.playersbat[bat][0] = g_bat_green4longlight
		if png==2:
			if varglob.BatDim[1] == 0:
				varglob.playersbat[bat][0] = g_bat_green2dark
			if varglob.BatDim[1] == 1:
				varglob.playersbat[bat][0] = g_bat_green3shortdark
			if varglob.BatDim[1] == 2:
				varglob.playersbat[bat][0] = g_bat_green4longdark

	if bat==2:
		if png==0:
			if varglob.BatDim[2] == 0:
				varglob.playersbat[bat][0] = g_bat_blue2
			if varglob.BatDim[2] == 1:
				varglob.playersbat[bat][0] = g_bat_blue3short
			if varglob.BatDim[2] == 2:
				varglob.playersbat[bat][0] = g_bat_blue4long
		if png==1:
			if varglob.BatDim[2] == 0:
				varglob.playersbat[bat][0] = g_bat_blue2light
			if varglob.BatDim[2] == 1:
				varglob.playersbat[bat][0] = g_bat_blue3shortlight
			if varglob.BatDim[2] == 2:
				varglob.playersbat[bat][0] = g_bat_blue4longlight
		if png==2:
			if varglob.BatDim[2] == 0:
				varglob.playersbat[bat][0] = g_bat_blue2dark
			if varglob.BatDim[2] == 1:
				varglob.playersbat[bat][0] = g_bat_blue3shortdark
			if varglob.BatDim[2] == 2:
				varglob.playersbat[bat][0] = g_bat_blue4longdark

	if bat==3:
		if png==0:
			if varglob.BatDim[3] == 0:
				varglob.playersbat[bat][0] = g_bat_red2
			if varglob.BatDim[3] == 1:
				varglob.playersbat[bat][0] = g_bat_red3short
			if varglob.BatDim[3] == 2:
				varglob.playersbat[bat][0] = g_bat_red4long
		if png==1:
			if varglob.BatDim[3] == 0:
				varglob.playersbat[bat][0] = g_bat_red2light
			if varglob.BatDim[3] == 1:
				varglob.playersbat[bat][0] = g_bat_red3shortlight
			if varglob.BatDim[3] == 2:
				varglob.playersbat[bat][0] = g_bat_red4longlight
		if png==2:
			if varglob.BatDim[3] == 0:
				varglob.playersbat[bat][0] = g_bat_red2dark
			if varglob.BatDim[3] == 1:
				varglob.playersbat[bat][0] = g_bat_red3shortdark
			if varglob.BatDim[3] == 2:
				varglob.playersbat[bat][0] = g_bat_red4longdark

	try:
		#print ("load bat %s, image:%s" %(bat, png) )
		varglob.playersbat[bat][5] = png # animation
	except:
		print ("Warning: unable to load bat %s, image:%s !!!" %(bat, png) )


#################################################
#TODO: right now, not used, this is just a copy of bullet class
class Bat(pygame.sprite.Sprite):
	"""Object Bat moving on screen
	Return: objet Bat
	Fonctions: update, calcnewpos
	Attributs: img, image, rect, porteur, center(xy), rayon, animation"""

	def __init__(self, (xy), angle, th_E, idx, img, porteur):

		#[0 objOriBatImage, 1 objBatImageAngle, 2 objOriBatPos(posx, posy), 3 center(posx, posy), 4 objBatAnglePos(posx, posy), 5 animation]
		#playersbat = [[g_bat_yellow2, "free", "free", "free", "free", 0], [g_bat_green2, "free", "free", "free", "free", 0], \
		#[g_bat_blue2, "free", "free", "free", "free", 0], [g_bat_red2, "free", "free", "free", "free", 0]]

		pygame.sprite.Sprite.__init__(self)
		self.angle = angle
		self.th_E = th_E
		self.idx = idx
		self.porteur = porteur #player owner, 0=none

		self.img = img
		if img == 0:
			self.image = g_bat_None2
			self.rect = g_bat_None2Rect
		if img == 1:
			self.image = g_bat_yellow2
			self.rect = g_bat_yellow2Rect
		if img == 2:
			self.image = g_bat_green2
			self.rect = g_bat_green2Rect
		if img == 3:
			self.image = g_bat_blue2
			self.rect = g_bat_blue2Rect
		if img == 4:
			self.image = g_bat_red2
			self.rect = g_bat_red2Rect

		self.imageOri = self.image
		self.rectOri = self.rect
		self.rect.x=(xy)[0] # initpos
		self.rect.y=(xy)[1] # initpos

		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.center = self.area.center
		self.rayon = varglob.fenetre_center[1] - self.rect[1] # remove bat size sprite #rayon where is bat

		self.rads = 0

	def updatefenetre(self):
		""" Update Change fenetre size"""
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.center = self.area.center
		self.rayon = +2000 #rayon +1000 #rayon where is bullet, +1000 to be sur it start from far

	def update(self):
		""" Update bullet position"""
		#if varglob.pdb_debug: pdb.set_trace()

		# calculate next position
		newpos = self.calcnewpos(self.rect,self.vector)
		self.rect = newpos
		(angle,z) = self.vector

		# test if distance to center is bigger then rayon (perimeter trajectory's bats)
		self.center = self.rect.center
		bx = self.center[0]#+self.rect.x
		by = self.center[1]#+self.rect.y
		fx = varglob.fenetre_center[0]
		fy = varglob.fenetre_center[1]
		#calculate distance
		dbfx = bx - fx
		dbfy = by - fy
		rayonbullet = math.sqrt(dbfx*dbfx+dbfy*dbfy) #pythagore a²+b²=c²
		#calculate angle
		rads = math.atan2(-dbfy,dbfx)
		
		#print ("rads: %s\n" %(rads) )
		# g besoin du signe ?
		rads %= (math.pi*2) # en radians

		self.rads = rads

		#degs = math.degrees(rads) # en degres
		
		#print (varglob.rayon)
		#print (varglob.fenetre_center)
		#print (self.center)
		#print (rayonbullet)
		#print ("rads %s" %(rads))
		#print ("vector %s" %(self.vector[0]))
		
		has_changed = False

		if self.vector[1] != 0: #check collid only if bullet mouving and don't follow bat
			# poste isn't server, only movement is calculated
			# changes angle and collid will be check by broadcast server (idx,x,y,angle,speed)
			
			if self.th_E == 0:
				# update new rayon and vector
				self.rayon = rayonbullet
				angle %= (math.pi*2)
				angle = round(angle,5)
				self.vector = (angle,z)
			else: # if poste is server bullets communicate just on change events
				# test if touch side screen
				if not self.area.contains(newpos):
					tl = not self.area.collidepoint(newpos.topleft)
					tr = not self.area.collidepoint(newpos.topright)
					bl = not self.area.collidepoint(newpos.bottomleft)
					br = not self.area.collidepoint(newpos.bottomright)
					if tr and tl or (br and bl): # up/down
						print ("SIDE UP/DOWN")
						#angle = -angle
						#self.vector[1] = 0
						z = 0
						has_changed = True
					if tl and bl: # cotes
						print ("SIDE LEFT")
						#angle = math.pi - angle
						#self.vector[1] = 0
						z = 0
						has_changed = True
					if tr and br: # cotes
						print ("SIDE RIGHT")
						#angle = math.pi - angle
						#self.vector[1] = 0
						z = 0
						has_changed = True
				else: # we are within game screen
					# test if actual pos is greather than rayon
					#if (rayonbullet) > varglob.rayon:
					if (rayonbullet) > varglob.rayon - 10: #bat size
						#test we're yet within bat's trajectory
						#if (rayonbullet) > self.rayon: # and not self.hit:
						if (rayonbullet) < varglob.rayon + 10: # and not self.hit:
							#print ("!!!BULLET PERIMETRE: %s" %(rayonbullet) )
							#print (varglob.rayon)
							#print (varglob.fenetre_center)
							#print (self.center)
							#print ("rads %s" %(rads) )
							#print ("vector %s" %(self.vector[0]) )

							# CECI MARCHE ENFIN APRES 2 JOURS DE TESTS !!!
							#angle =  -rads -((angle+rads)/2)
							#self.vector[1] = 0
							
							# check if bat present
							
							# define angle distance limit bat according screen size (fenetre)
							limbat = 0.10
							if varglob.fenetre_size[0] >= 800:
								limbat = 0.09
							elif varglob.fenetre_size[0] >= 640:
								limbat = 0.14
							else:
								limbat = 0.17
							limbat2 = limbat
								
							for nb, player in enumerate(varglob.players):
								if player[2]!="free": #check all, for each players # and nb!=playerno:
									
									angleplayer = varglob.players[nb][2]
									distBallBat = (math.pi*2-rads - angleplayer)
										
									#V106 BONUS SIZE BAT
									#WARNING: should be change according screen size
									if varglob.BatDim[nb] == 1: #SHORT bat
										limbat2 = limbat-0.05
									if varglob.BatDim[nb] == 2: #LONG bat
										limbat2 = limbat+0.04

									if distBallBat < limbat2:
										#print ("angleplayer %s: %s" %(nb, angleplayer))
										#print ("distBallBat: %s" %(distBallBat))

										#if distBallBat > -limbat:
										if distBallBat > -limbat2:
											#print ("bullet %s touche player %s" %(self.porteur-1, nb))
											#self.vector[1] = 0
											z = 0
											has_changed = True
											#increase player score, update client will be later on update pos
											porteur = self.porteur #celui a qui appartien le tir, sauf 0

											#check if porteur isn't launcher
											if porteur != 0 and porteur != (nb+1) :
												varglob.players[porteur-1][3] += 10
												load_batpng(porteur-1, 1) #flash light
												#decrease hitted player score
												varglob.players[nb][3] -= 10
												load_batpng(nb, 2) #flash dark
												if S_glassbreak:
													S_glassbreak.play()
												#print ("bullet update bats %s and %s" %(porteur-1, nb) )
											
											if self.th_E != 0:
												# Warning: double emploi si on a deja touche, mais necessaire maj bullets
												#self.th_E.sendMsg("S%s:%s\n" %(porteur-1, varglob.players[porteur-1][3]))
												self.th_E.sendMsg("S%s:%s\n" %(nb, varglob.players[nb][3]))
												#update client will be later on update pos
												
											break
										else:
											#print ("MISSED LEFT")
											toto = 1
									else:
										#print ("MISSED RIGHT")
										toto = 1
										
									#time.sleep(1)

							self.hit = 1					
							# update new rayon
							self.rayon = rayonbullet
						else:
							self.hit = 0
							
					else:
						# test if brick touch
						for idx, brick in enumerate(varglob.bricks):
							
							if varglob.bricks[idx][0].getstatus()!=0:
								porteur = self.porteur # bullet owner
								#collision1 = we check for bullet, not for brick!
								collision = self.check_collision(varglob.bricks[idx][0].getrect())
								#0topleft, 1topright, 2bottomleft, 3bottomright, 4midleft, 5midright, 6midtop, 7midbottom, 8center)

								if collision[0] or collision[1] or collision[2] or collision[3] or collision[4] \
								or collision[5] or collision[6] or collision[7] or collision[8]:
									z = 0
									has_changed = True

									# black brick (7) doesn't count as indestruclibles
									if varglob.bricks[idx][0].getimg() != 7:
										
										print ("brick img: %s") %(varglob.bricks[idx][0].getimg())
										if varglob.bricks[idx][0].getimg() == 10: #LIVE brick
											#print ("bullet hit LIVES brick bonus")
											#ball+ player
											if porteur !=0:
												varglob.players[porteur-1][5] += 1
											
										elif varglob.bricks[idx][0].getimg() == 11: #BULLETS brick
											#print ("bullet hit BULLETS brick bonus")
											#bullet+10 player
											if porteur !=0:
												varglob.players[porteur-1][4] += 10
												
										elif varglob.bricks[idx][0].getimg() == 12: #SPEED brick
											print ("bullet hit SPEED brick bonus")
											#do nothink, bullet set speedfast no sense

										elif varglob.bricks[idx][0].getimg() == 13: #GLUE brick
											print ("bullet hit GLUE brick bonus")
											# warning: do not wait until ball return to bat
											# ask: logic to glue all porteur ball(s) to original porteur?
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)

											# exist if porteur exist
											if porteur !=0:
												# player got any balls?
												if (varglob.players[porteur-1][5] !=0 ) or True:
													for idx2, ball2 in enumerate(varglob.balls):
														#if varglob.balls[idx2][0].getporteur() == porteur:
														if varglob.balls[idx2][0].getporteurorigin() == porteur:
															# decrease ball old porteur
															varglob.players[idx2][5] -= 1
															# if is serveur, broadcast serveur change old porteur
															if self.th_E != 0:
																self.th_E.sendMsg("S%s:%s\n" %(idx2, varglob.players[idx2][3]))
															
															varglob.balls[idx2][0].setporteurorigin()
															varglob.balls[idx2][0].setimg(varglob.balls[idx2][0].getporteurorigin())

															#increase ball new porteur
															varglob.players[self.porteur-1][5] += 1
															# if is serveur, broadcast serveur change new porteur
															if self.th_E != 0:
																self.th_E.sendMsg("S%s:%s\n" %(self.porteur-1, varglob.players[self.porteur-1][3]))

															bx, by, bvector = varglob.balls[idx2][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
															bang = bvector[0]
															bspeed = 0 #bvector[1]
															bvector = (bang, bspeed)
															varglob.balls[idx2][0].setposxyvect((bx, by), bvector)

															# if is serveur, broadcast change old porteur
															if self.th_E != 0:
																#self.th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(self.porteur, self.getimg(), bx, by, bang, 0))
																self.th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(idx2, varglob.balls[idx2][0].getimg(), bx, by, bang, 0))

										elif varglob.bricks[idx][0].getimg() == 14: #BOMB brick
											print ("bullet hit BOMB brick bonus")
											if S_bomb:
												S_bomb.play()
											checkbombs=[idx]
											#check for all other bombs to explode
											while len(checkbombs)!=0:
												idxLast = checkbombs.pop()
												for idx2, brick2 in enumerate(varglob.bricks):
													#check only for existing bricks
													if (varglob.bricks[idx2][0].getstatus()!=0):
														collision2 = varglob.bricks[idxLast][0].check_collision(varglob.bricks[idx2][0].getrect())
														if collision2[0] or collision2[1] or collision2[2] or collision2[3] or collision2[4] \
														or collision2[5] or collision2[6] or collision2[7] or collision2[8]:
															#append other bombs to explode
															if (varglob.bricks[idx2][0].getimg() == 14) and (idxLast!=idx2) and (idx2 not in checkbombs):
																checkbombs.append(idx2)
															#increase score player for each brick destroyed
															if porteur != 0:
																if varglob.bricks[idx2][0].getimg() < 7: # only thoses have points scores
																	varglob.players[porteur-1][3] += varglob.bricks[idx2][0].getimg()
																	varglob.bricks[idx2][0].showBrickScore(varglob.bricks[idx2][0].getimg(), porteur)

															#warning: if bonus brick no bonus for player
															varglob.bricks[idx2][0].setimg(0)
															varglob.bricks[idx2][0].setstatus(0)
															# if is serveur, broadcast serveur (idx brick)
															if self.th_E != 0:
																self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx2, varglob.bricks[idx2][0].getimg(), varglob.bricks[idx2][0].getstatus(), \
																varglob.bricks[idx2][0].getBrickScore(), varglob.bricks[idx2][0].getBrickScorePlayer()))
	

										elif varglob.bricks[idx][0].getimg() == 15: #WALL brick
											varglob.WallTime = time.time() + 7
											varglob.anouncetexte.append("WALL")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:WALL\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 16: #Random brick
											ylevel = random.randrange(0, 7)
											varglob.bricks[idx][0].setimg(ylevel)
											varglob.bricks[idx][0].setstatus(ylevel)
											if self.th_E != 0:
												self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, varglob.bricks[idx][0].getimg(), varglob.bricks[idx][0].getstatus(), \
												varglob.bricks[idx][0].getBrickScore(), varglob.bricks[idx][0].getBrickScorePlayer()))
											break

										elif varglob.bricks[idx][0].getimg() == 17: #INVERT brick
											varglob.InvertTime[self.porteur-1] = time.time() + 5
											varglob.anouncetexte.append("INVERT")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:INVERT\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 18: #SHORT brick
											varglob.BatDim[self.porteur-1] = 1
											varglob.BatDimTime[self.porteur-1] = time.time() + 10
											load_batpng(self.porteur-1, 2) #flash dark
											varglob.anouncetexte.append("SHORT")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:SHORT\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 19: #LONG brick
											varglob.BatDim[self.porteur-1] = 2
											varglob.BatDimTime[self.porteur-1] = time.time() + 10
											load_batpng(self.porteur-1, 1) #flash light
											varglob.anouncetexte.append("LONG")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:LONG\n" %(self.porteur-1))

										else:
											#increase score player as brick value, update client with update pos
											if porteur != 0:
												varglob.players[porteur-1][3] += varglob.bricks[idx][0].getimg()
												varglob.bricks[idx][0].showBrickScore(varglob.bricks[idx][0].getimg(), porteur)
										
										#destruction by bullet
										varglob.bricks[idx][0].setimg(0)
										varglob.bricks[idx][0].setstatus(0)

									# if is serveur, broadcast serveur (idx brick)
									if self.th_E != 0:
										self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, varglob.bricks[idx][0].getimg(), varglob.bricks[idx][0].getstatus(), \
										varglob.bricks[idx][0].getBrickScore(), varglob.bricks[idx][0].getBrickScorePlayer()))

										# Warning: double case if already hited, but nedeed update bullets
										#self.th_E.sendMsg("S%s:%s\n" %(porteur-1, varglob.players[porteur-1][3]))
									# explode one brick per time, then exit for
									break
								
		# if poste is server, broadcast only changes to server (idx,x,y,angle,speed,oriented)
		if self.th_E != 0:
			if has_changed == True: # test not nedeed as in else
				angle = round(angle, 5)
				self.vector = (angle,z)
				# decrease bullets when tarjectory ended in update
				porteur = self.porteur
				#varglob.players[porteur-1][4] = varglob.players[porteur-1][4] - 1
				varglob.players[porteur-1][4] -= 1
				#print ("UpdateBullet T:%s:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z))
				#self.th_E.sendMsg("T:%s:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z))
				self.th_E.sendMsg("T:%s:%s:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z, varglob.players[porteur-1][2]))
				# update porteur
				# Warning: double emploi si on a deja touche, but nedeed update bullets
				self.th_E.sendMsg("S%s:%s\n" %(porteur-1, varglob.players[porteur-1][3]))

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

	def setth_E(self, th_E):
		"""define thread emit for server communication"""
		self.th_E = th_E
		
	def calcnewpos(self,rect,vector):
		"""calculate next position bullet"""
		(angle,z) = vector
		(dx,dy) = (z*math.cos(angle),z*math.sin(angle))
		return rect.move(round(dx,1),round(dy,1))
		
	def getpos(self):
		"""return rayon-centre, vector mouvment, and angle-centre"""
		return (self.rayon, self.vector, self.rads)

	def getimg(self):
		"""return bullet image number"""
		return (self.img)

	def setimg(self, img):
		"""define bullet image"""
		global g_bulletNone, g_bulletYellow, g_bulletGreen, g_bulletBlue, g_bulletRed
		if img == 0:
			self.image = g_bulletNone
		if img == 1:
			self.image = g_bulletYellow
		if img == 2:
			self.image = g_bulletGreen
		if img == 3:
			self.image = g_bulletBlue
		if img == 4:
			self.image = g_bulletRed
		if img >= 5:
			print ("ERROR CHANGING BULLET IMG: %s" %(img))
		else:
			self.img = img

	def getporteur(self):
		"""return bullet owner"""
		return (self.porteur)

	def setporteur(self, porteur):
		"""define bullet owner"""
		self.porteur = porteur

	def setspeed(self, speed):
		"""define bullet speed"""
		self.vector = (self.vector[0],speed) #(angle,z)

	def getposxyvect(self):
		"""return position (x, y) and vector"""
		return (self.rect.x, self.rect.y, self.vector)

	def getrect(self):
		"""return surface rect"""
		return (self.rect)

	def setposxyvect(self, (xy), vector, angle):
		"""define position (x,y), vector, and oriented angle"""
				
		#WARNING: if players[idx][2] not existe, angle value is string "free"
		#if varglob.players[self.porteur-1][2] != "free":
		if angle != "free":
			#self.image, self.rect = self.rot_center(self.imageOri, self.rectOri, 90 - math.degrees(float(angle)))
			self.rot_center(self.imageOri, self.rectOri, 90 - math.degrees(float(angle)))
		else:
			print ("WARNING: players[%s][2] == 'free'" %([self.porteur-1]))
		
		self.rect.x=(xy)[0] # initpos
		self.rect.y=(xy)[1] # initpos
		
		#self.vector = vector #(angle,z)
		angle = vector[0]
		angle %= (math.pi*2)
		self.vector = (angle, vector[1]) #(angle,z)
		
	def rot_center(self, image, rect, angle):
		"""rotate an image while keeping its center"""
		self.image = pygame.transform.rotate(image, angle)
		w = math.sqrt(rect.width**2 + rect.height**2)
		self.rect = self.image.get_rect(center=rect.center, size=(w,w))
		
