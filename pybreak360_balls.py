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

import pybreak360_bats as bats

#################################################
class Ball(pygame.sprite.Sprite):
	""" object ball who's moving on screen
	Return: objet ball
	Fonctions: update, calcnewpos
	Attributs: img, image, rect, porteur, porteurOrigin, rayon, vector"""

	def __init__(self, (xy), vector, th_E, idx, img, porteur):
		pygame.sprite.Sprite.__init__(self)
		self.th_E = th_E
		self.idx = idx
		self.porteurOrigin = porteur # ball owner, original
		self.porteur = porteur # ball owner, last shoot bat
		self.img = img
		if img == 0:
			#self.image, self.rect = load_png('ballNone.png')
			self.image = g_ballnone
			self.rect = g_ballnoneRect
		if img == 1:
			#self.image, self.rect = load_png('ball1yellow.png')
			self.image = g_ball1yellow
			self.rect = g_ball1yellowRect
		if img == 2:
			#self.image, self.rect = load_png('ball2green.png')
			self.image = g_ball2green
			self.rect = g_ball2greenRect
		if img == 3:
			#self.image, self.rect = load_png('ball3blue.png')
			self.image = g_ball3blue
			self.rect = g_ball3blueRect
		if img == 4:
			#self.image, self.rect = load_png('ball4red.png')
			self.image = g_ball4red
			self.rect = g_ball4redRect
		# convert Surfaces for faster bliting to the screen
		#self.image.convert()

		#newpos = self.calcnewpos(self.rect,self.vector)
		#self.rect = newpos
		#self.rect.move(xy[0], xy[1]) # initpos
		self.rect.x=(xy)[0] # initpos
		self.rect.y=(xy)[1] # initpos

		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.center = self.area.center
		self.rayon = varglob.rayon +2000 #rayon where is ball, +1000 to be sur it start from far

		self.rads = 0 # angle / rapport center fenetre
		self.vector = vector # movement vector in fenetre
		self.hit = 0
		
		self.speedTime = 0
		self.nuclearTime = 0
		self.bigBallTime = 0
 
	def updatefenetre(self):
		"""Update change when resize screen fenetre"""
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.center = self.area.center
		self.rayon = varglob.rayon +2000 #rayon where is ball, +1000 to be sur it start from far

	def update(self):
		"""Update ball position"""
		#global ParBallSpeedSlow, ParBallSpeedFast
		#global ParDwngrdBrick, ParBallSpeedSlow, ParBallSpeedFast 
		
		# if rebond, start from old position
		oldrayon = self.rayon
		oldpos = self.rect
		oldvector = self.vector
		
		# calculate next position
		newpos = self.calcnewpos(self.rect,self.vector)
		self.rect = newpos
		(angle,z) = self.vector

		# test if distance to centre bigger than rayon (perimetre bat's trajectory)
		self.center = self.rect.center
		bx = self.center[0]
		by = self.center[1]
		fx = varglob.fenetre_center[0]
		fy = varglob.fenetre_center[1]
		#calculate distance to center
		dbfx = bx - fx
		dbfy = by - fy
		#rayon ball will be
		rayonball = math.sqrt(dbfx*dbfx+dbfy*dbfy) #pythagore a²+b²=c²
		#calculate angle
		rads = math.atan2(-dbfy,dbfx)
		
		#print ("rads: %s\n" %(rads) )
		# need signe ?
		rads %= (math.pi*2) # en radians

		self.rads = rads #angle rapport fenetre center

		#print (varglob.rayon)
		#print (varglob.fenetre_center)
		#print (self.center)
		#print (rayonbullet)
		#print ("rads %s" %(rads) )
		#print ("vector %s" %(self.vector[0]) )
		
		self.hit = 0
		has_changed = False

		#raise down Speed Ball Bonus
		if self.speedTime < time.time() and self.speedTime != 0:
			self.speedTime = 0
			if (z != 0) and (z != ParBallSpeedSlow): #only if ball is moving
				z = ParBallSpeedSlow
				self.setimg(self.img - 4)
				self.setspeed(ParBallSpeedSlow)
				print ("ball speed down")
				#has_changed = True # don't need, and got issues with laters check has_changed
		#raise down Nuclear Ball Bonus
		if self.nuclearTime < time.time() and self.nuclearTime != 0:
			self.nuclearTime = 0
			#Warning: may not need to send over network
			print ("ball nuclear down")
			if self.th_E != 0:
				self.th_E.sendMsg("A%s:NUCLEAROFF\n" %(self.porteur-1))
		#raise down Big Ball Bonus
		if self.bigBallTime < time.time() and self.bigBallTime != 0:
			self.bigBallTime = 0
			self.setimg(self.img)
			#Warning: may not need to send over network
			print ("big ball down")
			if self.th_E != 0:
				self.th_E.sendMsg("A%s:BIGBALLOFF\n" %(self.porteur-1))

		if self.vector[1] != 0: #check collid only if ball is mouving and doesn't follow bat
			# if poste isn't server, calculate only movement
			# angles changes and collide will be send by server broadcast (idx,x,y,angle,speed)
			if self.th_E == 0:
				# update new rayon and vector
				self.rayon = rayonball
				angle %= (math.pi*2)
				angle = round(angle,5)
				self.vector = (angle,z)
			else: # poste is serveur
				# test if touch side aera display game screen
				if not self.area.contains(newpos):
					tl = not self.area.collidepoint(newpos.topleft)
					tr = not self.area.collidepoint(newpos.topright)
					bl = not self.area.collidepoint(newpos.bottomleft)
					br = not self.area.collidepoint(newpos.bottomright)
					if tr and tl or (br and bl): # up/down
						print ("SIDE UP/DOWN")
						angle = -angle
						has_changed = True
					if tl and bl: # cotes
						print ("SIDE LEFT")
						angle = math.pi - angle
						has_changed = True
					if tr and br: # cotes
						print ("SIDE RIGHT")
						angle = math.pi - angle
						has_changed = True
						
					#player lose ball when he lose own ball (porteurOrigin)
					if has_changed: # before all tests, has_changed => ball out
						z=0
						if self.porteurOrigin !=0: # if ball is player's original ball
							if S_BallLose:
								S_BallLose.play()
							z = 0 # re-blit ball to porteur's bat
							
							#MULTIPLAYERS SHOULD ALWAYS HAVE BALLS, OTHERWISE IT DOESN'T FUN.
							if varglob.howplayers ==1:
								if varglob.players[self.porteurOrigin-1][5] > 0:
									varglob.players[self.porteurOrigin-1][5] -= 1 #ParLives
							# update player
							self.th_E.sendMsg("S%s:%s\n" %(self.porteurOrigin-1, varglob.players[self.porteurOrigin-1][3]))
							# redefine porteurOrigine
							self.porteur = self.porteurOrigin
							self.setimg(self.porteurOrigin)
							#V104
							if varglob.howplayers > 1:
								varglob.PenalityDelays[self.porteurOrigin-1] = time.time() + 3								
							else:
								varglob.PenalityDelays[self.porteurOrigin-1] = time.time() + 1
							#V105 update player penality: local time
							if varglob.howplayers > 1:
								self.th_E.sendMsg("X:%s:3\n" %(self.porteurOrigin-1))
							else:
								self.th_E.sendMsg("X:%s:1\n" %(self.porteurOrigin-1))
							
				else: # we are in screen game display
					# test if pos ball actual is greather then perimeter bat
					if (rayonball) > varglob.rayon - 10: # - bat size

						# test we're yet within bat trajectory
						#if (rayonball) > self.rayon: # and not self.hit:
						if (rayonball) < varglob.rayon + 10: # + bat size

							# we are in bat perimeter
							# test si on s'eloigne du centre
							if (rayonball) > self.rayon: # and not self.hit:
								print ("BALL PERIMETRE!!%s" %(rayonball))

								#self.rads = 0 #angle rapport au centre fentetre
								#self.vector = (angle,z) #vecteur de deplacement dans la fenetre

								#mur = False
								#if mur: # TODO ne rebondir sur le perimetre que s'il y a le bonus mur
									# CECI MARCHE ENFIN APRES 3 JOURS DE TESTS !!!
								#	angle =  -rads -((angle+rads)/2)
								#	has_changed = True
								
								#defini la distance angulaire limite bat en fontion de la taille fenetre
								limbat = 0.10

								if varglob.fenetre_size[0] >= 800:
									limbat = 0.09
								elif varglob.fenetre_size[0] >= 640:
									limbat = 0.14
								else:
									limbat = 0.17
								limbat2 = limbat
									
								#test angle 0
								#limbat = 6.2832

								if varglob.WallTime > time.time():
									#limbat = math.pi *2
									angle = math.pi-rads -((rads+angle)/1) #rebondir comme mirroir
									#angle -= distBallBat*2 #shift ball trajectory according bat impact
									print ("ball in wall protect")
									has_changed = True
									self.hit = 1					

								#V104: ball is prior to his owner, then check list...
								elif varglob.players[self.porteurOrigin-1][2]!="free": #check for each player connected, if angle ="free"=existe
									
									#WARNING: PASSAGE BY ZERO POSITIF/NEGATIF HAVE PROBLEMS
									angleplayer = varglob.players[self.porteurOrigin-1][2]
									distBallBat = (math.pi*2-rads - angleplayer)
									#all in positive
									angleplayer = varglob.players[self.porteurOrigin-1][2]
									distBallBat = (math.pi*2-angleplayer -rads)
									
									#WARNING: should be change according screen size
									if varglob.BatDim[self.porteurOrigin-1] == 1: #SHORT bat
										limbat2 = limbat - 0.05
									if varglob.BatDim[self.porteurOrigin-1] == 2: #LONG bat
										limbat2 = limbat + 0.04

									#TODO: verify positions with coordonnate calcul
									#if ((distBallBat < limbat) and (distBallBat >= 0)) or (distBallBat > math.pi*2-limbat): # try to fix 360° bug
									if ((distBallBat < limbat2) and (distBallBat >= 0)) or (distBallBat > math.pi*2-limbat2): # try to fix 360° bug
										angle = math.pi-rads -((rads+angle)/1) #rebondir comme mirroir
										angle -= distBallBat*2 #shift ball trajectory according bat impact
										print ("ball on bat")
										has_changed = True
										self.hit = 1					

										if self.img > 4 : #BALL SPEED
											self.setimg(self.porteurOrigin-1 + 5) #couleur du porteur
										else:
											self.setimg(self.porteurOrigin-1 + 1) # porteur colors

										self.porteur = self.porteurOrigin
										bats.load_batpng(self.porteurOrigin-1, 1) #flash light
										# if is serveur, ball's communicate to clients
										if self.th_E != 0:
											#update player
											self.th_E.sendMsg("S%s:%s\n" %(self.porteurOrigin-1, varglob.players[self.porteurOrigin-1][3]))

									#elif ((distBallBat > -limbat) and (distBallBat < 0)) or (distBallBat < -math.pi*2+limbat): # try to fix 360° bug
									elif ((distBallBat > -limbat2) and (distBallBat < 0)) or (distBallBat < -math.pi*2+limbat2): # try to fix 360° bug
										angle = math.pi-rads -((rads+angle)/1) # rebondir as mirror
										angle -= distBallBat*2 # devier tajectoire ball en fonction de l'impact bat
										print ("ball on bat")
										has_changed = True
										self.hit = 1					

										if self.img > 4 : #BALL SPEED
											self.setimg(self.porteurOrigin-1 + 5) # porteur color
										else:
											self.setimg(self.porteurOrigin-1 + 1) # porteur color

										self.porteur = self.porteurOrigin
										bats.load_batpng(self.porteurOrigin-1, 1) #flash light
										# if is serveur, ball's communicate to clients
										if self.th_E != 0:
											#update player
											self.th_E.sendMsg("S%s:%s\n" %(self.porteurOrigin-1, varglob.players[self.porteurOrigin-1][3]))
										

								if has_changed == False: #ball not on porteurOrigin, check others
									for nb, player in enumerate(varglob.players):
										if player[2]!="free": #check for each player connected, if angle ="free"=existe
										
											#WARNING: PASSAGE BY ZERO POSITIF/NEGATIF HAVE PROBLEMS
											angleplayer = varglob.players[nb][2]
											distBallBat = (math.pi*2-rads - angleplayer)

											#all in positive
											angleplayer = varglob.players[nb][2]
											distBallBat = (math.pi*2-angleplayer -rads)
											
											print ("a)BallRads: %s" %(rads) )
											print ("a)BallAngle: %s" %(angle) )
											print ("a)angleplayer %s: %s" %(nb, angleplayer) )
											print ("a)distBallBat: %s" %(distBallBat) )

											#WARNING: should be change according screen size
											if varglob.BatDim[nb] == 1: #SHORT bat
												limbat2 = limbat - 0.05
											if varglob.BatDim[nb] == 2: #LONG bat
												limbat2 = limbat + 0.04

											#TODO: verify positions with coordonnees calcul
											#if ((distBallBat < limbat) and (distBallBat >= 0)) or (distBallBat > math.pi*2-limbat): # try to fix 360° bug
											if ((distBallBat < limbat2) and (distBallBat >= 0)) or (distBallBat > math.pi*2-limbat2): # try to fix 360° bug
												print ("b)distBallBat: %s" %(distBallBat) )
												#FIXED: ZERO PASSAGE POSITIF/NEGATIF POSE PROBLEME
												#angle = -rads -((angle+rads)/2) #rebondir comme mirroir
												angle = math.pi-rads -((rads+angle)/1) #rebondir comme mirroir
												
												# have to change as FIXED 0°
												angle -= distBallBat*2 #shift ball trajectory according bat impact
												
												print ("ball on bat")
												has_changed = True
												print ("b)BallAngle: %s" %(angle) )
												
												self.hit = 1

												print ("LEFT")
												if self.img > 4 : #BALL SPEED
													self.setimg(nb + 5) #owner's color
												else:
													self.setimg(nb + 1) #owner's color

												if self.porteur != nb + 1:
													self.porteur = (nb + 1) #ball is from owner's bat (+1, 0 si None?)
													# non! varglob.players[self.porteur-1][5] += 1
													
												#load_batpng(nb, 1) #flash light
												bats.load_batpng(self.porteur-1, 1) #flash light
												# if is serveur, ball's communicate to clients
												if self.th_E != 0:
													#update player
													self.th_E.sendMsg("S%s:%s\n" %(self.porteur-1, varglob.players[self.porteur-1][3]))

												break
											
											#if ((distBallBat > -limbat) and (distBallBat < 0)) or (distBallBat < -math.pi*2+limbat): # try to fix 360° bug
											if ((distBallBat > -limbat2) and (distBallBat < 0)) or (distBallBat < -math.pi*2+limbat2): # try to fix 360° bug
												print ("c)distBallBat: %s" %(distBallBat))
												#FIXED: LE PASSAGE PAR ZERO POSITIF/NEGATIF POSE PROBLEME
												#angle = -rads -((angle+rads)/2) #rebondir comme mirroir
												angle = math.pi-rads -((rads+angle)/1) #rebondir comme mirroir
												
												# have to change as FIXED 0°
												angle -= distBallBat*2 #shift ball trajectory according bat impact
												print ("ball on bat")
												has_changed = True
												print ("c)BallAngle: %s" %(angle))
												
												self.hit = 1
												
												print ("RIGHT")
												if self.img > 4 : #BALL SPEED
													self.setimg(nb + 5) #couleur du porteur
												else:
													self.setimg(nb + 1) #couleur du porteur

												if self.porteur != nb + 1:
													self.porteur = (nb + 1) #ball is from owner's bat (+1, 0 si None?)
													#non ! varglob.players[self.porteur-1][5] += 1
													
												#load_batpng(nb, 1) #flash light
												bats.load_batpng(self.porteur-1, 1) #flash light
												# if is serveur, ball's communicate to clients
												if self.th_E != 0:
													#update player
													self.th_E.sendMsg("S%s:%s\n" %(self.porteur-1, varglob.players[self.porteur-1][3]))
													
												break
											
					# lower than perimetre, test if touch brick
					else:
						for idx, brick in enumerate(varglob.bricks):
							
							if varglob.bricks[idx][0].getstatus() != 0:

								porteur = self.porteur # owner's ball

								#collision = varglob.bricks[idx][0].check_collision(self.rect)
								collision = varglob.bricks[idx][0].check_collision(newpos)
								#list [0topleft, 1topright, 2bottomleft, 3bottomright, 4midleft, 5midright, 6midtop, 7midbottom, 8center]

								# WARNING: privilegier les angles ou les faces? faire parametre?
								# WARNING: regarder de quel coté la balle est collid (pas seulement la brique)
								
								angleNuclear = angle #1.0.7 memo Nuclear dosen't change, destroy all
								if (collision[0]):
									# print ("brick topleft")
									# voir CECI MARCHE ENFIN APRES 2 JOURS DE TESTS !!!
									# pas de quoi etre fiere: un bug m'a coute une journee suplementaire
									while angle >=  0:
										angle -= math.pi/4
									angle = angle/2
									angle =  -math.pi*3/4 - angle
									print ("ball on brick:%s collid0" %(idx) )
									has_changed = True

								if (not has_changed) and (collision[1]):
									#print ("brick topright")
									while angle >=  0:
										angle -= math.pi/4
									angle = angle/2
									angle =  -math.pi*1/4 - angle
									print ("ball on brick:%s collid1" %(idx) )
									has_changed = True

								if (not has_changed) and (collision[2]):
									#print ("brick bottomleft")
									while angle >=  0:
										angle -= math.pi/4
									angle = angle/2
									angle =  -math.pi*5/4 - angle
									print ("ball on brick:%s collid2" %(idx) )
									has_changed = True

								if (not has_changed) and (collision[3]):
									#print ("brick bottomright")
									while angle >=  0:
										angle -= math.pi/4
									angle = angle/2
									angle =  -math.pi*7/4 - angle
									print ("ball on brick:%s collid3" %(idx) )
									has_changed = True

								if (not has_changed) and (collision[4] or collision[5]):
									#print ("brick side vertical right or left")
									angle = math.pi - angle
									print ("ball on brick:%s collid4-5" %(idx) )
									has_changed = True

								if (not has_changed) and (collision[6] or collision[7]):
									#print ("brick top or bottom")
									angle = -angle
									print ("ball on brick:%s collid6-7" %(idx) )
									has_changed = True

								if has_changed == True:
									# black brick (7) doesn't count, as indestruclibles
									# WARNING: situation peut etre bloquée par rebond entre briques noires,
									# malgré un angle aléatoire supplementaire.
									# >>> recollage bat si tape BrickNoir + de 10 fois d'affilées.
									angle = angle + (random.randrange(0, 157)/100) # random pi/2
									angle %= (math.pi*2)

									if self.nuclearTime != 0:  #1.0.7 Nuclear destroy all
										angle = angleNuclear
										if (varglob.bricks[idx][0].getimg() == 7):
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											if self.th_E != 0:
												#self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, 0, 0, bricks[idx][0].getBrickScore(), bricks[idx][0].getBrickScorePlayer()))
												self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, 0, 0, 0, 0))
										
									if (varglob.bricks[idx][0].getimg() != 7): #BLACK brick
										
										if varglob.bricks[idx][0].getimg() == 10: #LIVE brick
											print ('ball hit LIVES brick bonus')
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											#ball+ player
											if porteur !=0:
												varglob.players[porteur-1][5] += 1
											
										elif varglob.bricks[idx][0].getimg() == 11: #BULLETS brick
											print ('ball hit BULLETS brick bonus')
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											#bullet+10 player
											if porteur !=0:
												varglob.players[porteur-1][4] += 10
											
										elif varglob.bricks[idx][0].getimg() == 12: #SPEED brick
											print ('ball hit SPEED brick bonus')
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											#ball set speedfast
											z = ParBallSpeedFast
											self.setimg(self.img + 4)
											self.speedTime = time.time() + 10
											
										elif varglob.bricks[idx][0].getimg() == 13: #GLUE brick
											print ("ball hit GLUE brick:%s bonus" %(idx))
											# warning: do not wait until ball return to bat
											# ask: logic to glue all porteur ball(s) to original porteur?
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)

											# exist if porteur exist
											if self.porteur != 0:
												#ball is from owner's bat
												self.setporteurorigin()
												self.setimg(self.porteurOrigin)
												#glue ball to bat
												bx, by, bvector = self.getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
												bang = bvector[0]
												bspeed = 0 #bvector[1]
												bvector = (bang, bspeed)
												self.setposxyvect((bx, by), bvector)
												
												if self.th_E != 0:
													self.th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(self.porteur-1, self.getimg(), bx, by, bang, 0))
												
												z = 0 # for actual ball
															
										elif varglob.bricks[idx][0].getimg() == 14: #BOMB brick
											print ("ball hit BOMB brick:%s bonus" %(idx))
											if S_bomb:
												S_bomb.play()
											checkbombs=[idx]
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
															#destruction by bomb
															if (varglob.bricks[idx2][0].getimg() < 7):
																varglob.bricks[idx2][0].showBrickScore(varglob.bricks[idx2][0].getimg(), porteur)
																#increase score player for each brick destroyed
																if porteur !=0:
																	varglob.players[porteur-1][3] += varglob.bricks[idx2][0].getimg()

															#warning: if bonus brick no bonus for player
															varglob.bricks[idx2][0].setimg(0)
															varglob.bricks[idx2][0].setstatus(0)
															# if is server, broadcast (idx brick)
															if self.th_E != 0:
																self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx2, 0, 0, varglob.bricks[idxLast][0].getBrickScore(), varglob.bricks[idxLast][0].getBrickScorePlayer()))
																#self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, 0, 0, 0, 0))

										elif varglob.bricks[idx][0].getimg() == 15: #WALL brick
											print ("ball hit WALL brick:%s bonus" %(idx))
											varglob.WallTime = time.time() + 7
											varglob.anouncetexte.append("WALL")
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:WALL\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 16: #Random brick
											ylevel = random.randrange(0, 7)
											varglob.bricks[idx][0].setimg(ylevel)
											varglob.bricks[idx][0].setstatus(ylevel)
											if self.th_E != 0:
												self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, varglob.bricks[idx][0].getimg(), varglob.bricks[idx][0].getstatus(), \
												varglob.bricks[idx][0].getBrickScore(), varglob.bricks[idx][0].getBrickScorePlayer()))
											#break

										elif varglob.bricks[idx][0].getimg() == 17: #INVERT brick
											print ("ball hit INVERT brick:%s bonus" %(idx))
											varglob.InvertTime[self.porteur-1] = time.time() + 5
											varglob.anouncetexte.append("INVERT")
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:INVERT\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 18: #SHORT brick
											print ("ball hit SHORT brick:%s bonus" %(idx))
											varglob.BatDim[porteur-1] = 1 #SHORT bat
											varglob.BatDimTime[porteur-1] = time.time() + 10
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											bats.load_batpng(self.porteur-1, 2) #flash dark
											varglob.anouncetexte.append("SHORT")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:SHORT\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 19: #LONG brick
											print ("ball hit LONG brick:%s bonus" %(idx))
											varglob.BatDim[porteur-1] = 2 #LONG bat
											varglob.BatDimTime[porteur-1] = time.time() + 10
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											bats.load_batpng(self.porteur-1, 1) #flash light
											varglob.anouncetexte.append("LONG")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:LONG\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 20: #V1.0.7 NUCLEAR brick
											print ("ball hit NUCLEAR brick:%s bonus" %(idx))
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											self.nuclearTime = time.time() + 10
											varglob.anouncetexte.append("NUCLEARON")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:NUCLEARON\n" %(self.porteur-1))
												
										elif varglob.bricks[idx][0].getimg() == 21: #V1.0.7 BIG BALL brick
											print ("ball hit BIG BALL brick:%s bonus" %(idx))
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											self.bigBallTime = time.time() + 7
											self.setbigball(self.bigBallTime)
											varglob.anouncetexte.append("BIG_BALL")
											if self.th_E != 0:
												self.th_E.sendMsg("A%s:BIGBALLON\n" %(self.porteur-1))

										else:
											if ParDwngrdBrick:
												if varglob.bricks[idx][0].getimg() >= 1:
													varglob.bricks[idx][0].showBrickScore(varglob.bricks[idx][0].getimg(), porteur)
													if porteur !=0:
														varglob.players[porteur-1][3] += varglob.bricks[idx][0].getimg()
														
													varglob.bricks[idx][0].setimg(varglob.bricks[idx][0].getimg() - 1)
													if varglob.bricks[idx][0].getimg() == 0:
														varglob.bricks[idx][0].setstatus(0)
											else:
												varglob.bricks[idx][0].showBrickScore(varglob.bricks[idx][0].getimg(), porteur)
												if porteur !=0:
													# score increase as brick color showBrickScore()
													varglob.players[porteur-1][3] += varglob.bricks[idx][0].getimg()

												varglob.bricks[idx][0].setimg(0)
												varglob.bricks[idx][0].setstatus(0)


									# if is serveur, BROADCAST serveur (idx brick)
									if self.th_E != 0:
										# warning if black brick (th_E Score and Hit not util)
										if S_HitBrick:
											S_HitBrick.play()
										self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, varglob.bricks[idx][0].getimg(), varglob.bricks[idx][0].getstatus(), \
										varglob.bricks[idx][0].getBrickScore(), varglob.bricks[idx][0].getBrickScorePlayer()))
										self.th_E.sendMsg("S%s:%s\n" %(porteur-1, varglob.players[porteur-1][3]))
									break
									
						self.hit = 0 # not util, may be yes... or not...

		# update new rayon
		self.rayon = rayonball

		# if is serveur, BROADCAST only changes (idx,x,y,angle,speed)
		if self.th_E != 0:
			# if rebond, restart from old position
			if has_changed == True:
				#TODO: recalculate only when not glue.
				self.rect = oldpos
				self.rayon = oldrayon
				#oldvector = self.vector
		
				angle %= (2*math.pi)
				angle = round(angle,5)
				self.vector = (angle,z)
			
				# and recalcuate mouvement !!!
				newpos = self.calcnewpos(self.rect,self.vector)
				self.rect = newpos
				#(angle,z) = self.vector
				print ("ball.update=B:%s:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z))
				self.th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z))
 
	def setth_E(self, th_E):
		"""define emit thread server for ball communication"""
		self.th_E = th_E
		
	def calcnewpos(self,rect,vector):
		"""calculate next ball position"""
		(angle,z) = vector
		(dx,dy) = (z*math.cos(angle),z*math.sin(angle))
		return rect.move(round(dx,1),round(dy,1))
		
	def getnuclear(self):
		"""return nuclearTime"""
		return (self.nuclearTime)

	def setnuclear(self, nuclearTime):
		"""set nuclearTime"""
		self.nuclearTime = nuclearTime

	def getbigball(self):
		"""return bigBallTime"""
		return (self.bigBallTime)

	def setbigball(self, bigBallTime):
		"""set bigBallTime"""
		#test big ball
		#g_ball1yellow = pygame.transform.scale(g_ball1yellow, HexaEmpty.get_size())
		#g_ball1yellowRect = HexaEmptyRect
		if bigBallTime !=0:
			self.bigBallTime = bigBallTime
			self.image = pygame.transform.scale(self.image, HexaEmpty.get_size())
			self.rect = HexaEmptyRect
		else:
			self.setimg(self.img)

	def getimg(self):
		"""return image number"""
		return (self.img)

	def setimg(self, img):
		"""define ball image"""

		if (img >= 9) or (img < 0):
			print ("WARNING CHANGING BALL IMG: %s" %(img))
		else:
			self.img = img
			if img == 0:
				self.image = g_ballNone
			if img == 1:
				self.image = g_ball1yellow
			if img == 2:
				self.image = g_ball2green
			if img == 3:
				self.image = g_ball3blue
			if img == 4:
				self.image = g_ball4red

			if img == 5:
				self.image = g_ball1yellowdark
			if img == 6:
				self.image = g_ball2greendark
			if img == 7:
				self.image = g_ball3bluedark
			if img == 8:
				self.image = g_ball4reddark
		#V1.0.7 alls same size or big ball bonus size
		if self.bigBallTime == 0:
			normalrect = g_ball1yellowRect
			normalrect[0] = self.rect[0]
			normalrect[1] = self.rect[1]
			self.rect = normalrect
		else:
			self.image = pygame.transform.scale(self.image, HexaEmpty.get_size())
			#self.rect = HexaEmptyRect
			bigrect = HexaEmptyRect
			bigrect[0] = self.rect[0]
			bigrect[1] = self.rect[1]
			self.rect = bigrect

	def getporteur(self):
		"""return le porteur de la ball"""
		return (self.porteur)

	def getporteurorigin(self):
		"""return original ball porteur"""
		return (self.porteurOrigin)

	def setporteur(self, porteur):
		"""define actual ball porteur"""
		self.porteur = porteur

	def setporteurorigin(self):
		"""redefine to original ball porteur"""
		self.porteur = self.porteurOrigin

	def setspeed(self, speed):
		"""define ball speed"""
		self.vector = (self.vector[0],speed) #(angle,z)

	def getpos(self):
		"""return rayon-centre, movement vector, and angle-to-center"""
		return (self.rayon, self.vector, self.rads)

	def getrads(self):
		"""return angle-to-center"""
		return (self.rads)

	def getposxyvect(self):
		"""return position (x, y) and vector"""
		return (self.rect.x, self.rect.y, self.vector)

	def getrect(self):
		"""return surface rect"""
		return (self.rect)

	def setposxyvect(self, (xy), vector):
		"""define position (x, y) and vector"""
		self.rect.x=(xy)[0] # initpos
		self.rect.y=(xy)[1] # initpos
		self.vector = vector #(angle,z)
		
