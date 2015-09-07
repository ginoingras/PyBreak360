#!/usr/bin/env python
# -*- coding: utf8 -*-

#    PyBreak360, an arkanoid breakout multi player network game at 360 degree
#    Copyright (C) 2015  Jean Ingrasciotta
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    see COPYING file.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# i apologize that code certainly doesn't Pythonic.
# some comments are already fixed or outdated/incoherente...
# i have to clean it (a lot).
#
# How to contribute:
# see README.TXT
# check "FIXME:" in code
# check "WARNING:" in code
# check "TODO:" in code
# github: git clone git://git.code.sf.net/p/pybreak360/code pybreak360-code
#
# report bug, send your levelpack at adresse below
# ginoingras@gmail.com 


try:
	import os, sys, math, time, random
	import platform, threading
	import getopt
	import textwrap
	import glob

	import pygame
	from pygame.locals import *

	import socket
	import urllib

	#import Queue
	#from decimal import *
	
	import pdb

	os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
	
	#local game import
	from reader import Reader
	from pybreak360_sounds import *
	from pybreak360_config import *
	from pybreak360_sprites import *
	from pybreak360_cursors import WAIT_CURSOR, HAND_CURSOR
	from pybreak360_bricks import *
	import pybreak360_kbd #as kbdi18n
	
	import pybreak360_varglob as varglob
	import pybreak360_hiscores as HS
	import pybreak360_designer as designer

	import pybreak360_bats as bats

	import pybreak360_bullets as bullets
	#print bullets

except ImportError, message:
	print ("ERROR IMPORTING MODULES: %s" % message)
	raise SystemExit,  "Unable to load module. %s" % message
	sys.exit()
	
try:
	import netifaces
except ImportError, message:
	print ("WARNING IMPORTING MODULES %s" % message)
	print ("netifaces is more efficient to resolve ip adresses")
	
varglob.pdb_debug = False
#varglob.pdb_debug = True

global serveur1
global conn_client #"free" or conn
global conn_client_name #"player1" aliasname

#global BricksColor, BricksRect, BricksCenter #imported from sprites

#global players, playersbat, playerbat, playerno #imported from varglob

#global bullets, balls #imported from varglob

varglob.pybreak360version = "1.0.7rc2"


#############################################
def getIP():
	'''Return IPaddressPublic, IPhostname, IPaddressLocal, IPaddressLocal_all'''
	#adresse ip externe
	try:
		#page = urllib.urlopen("http://www.monip.org/").read()
		#IPaddressPublic = page.split("IP : ")[1].split("<br>")[0]
		#print ("PUBLIC IP: " + IPaddressPublic)
		# disable reason: too long, and not needed
		IPaddressPublic = "HOSTNAME NOT RESOLVED"
	except:
		print ("PUBLIC IP NOT RESOLVED")
		IPaddressPublic = "PUBLIC_IP_NOT_RESOLVED"
		varglob.anouncetexte.append(IPaddressPublic)
	#hostname
	try:
		IPhostname = socket.gethostname()
		#print ("HOSTNAME: " + IPhostname)
	except:
		print ("HOSTNAME NOT RESOLVED")
		IPhostname = "HOSTNAME_NOT_RESOLVED"
		varglob.anouncetexte.append(IPhostname)

	LinuxIP="/sbin/ifconfig"
	LinuxIP="ifconfig eth1 | grep 'inet ad' | awk '{print $2}' | sed -e 's/adr://'"
	LinuxIP="ifconfig | grep 'inet ad' | awk '{print $2}' | sed -e 's/adr://'"
	#LinuxIP="ifconfig"
	Win32IP="ipconfig /all"
	Win32IP="ipconfig"

	#print (os.name) #nt
	#print (sys.platform) #'Win32' 'linux2'
	#print (platform.system() ) #Windows
	#print (platform.release() ) #'7' 'XP' 'version du noyau'

	IPaddressLocal_all = []
	#adresse ip local
	try:
		#if sys.platform == "win32": #XP
		if platform.release() == "XP": #XP
			#fichier=os.system(Win32IP)
			fichier=os.popen(Win32IP).read()
			#IPaddressLocal = fichier.split('IP')[2].split(':')[1].split()[0]
			#for addresse in fichier.split('IP')[2].split(':')[1].split():
			IPaddressLocal_all.append(fichier.split('IP')[2].split(':')[1].split()[0])
			#print ("os: XP, IP: " + IPaddressLocal)
		elif platform.release() == "7": #SEVEN
			#fichier=os.system(Win32IP)
			fichier=os.popen(Win32IP).read()
			#IPaddressLocal = fichier.split('IPv4')[1].split(':')[1].split()[0]
			#for addresse in fichier.split('IPv4')[1].split(':')[1].split()[0]:
			IPaddressLocal_all.append(fichier.split('IPv4')[1].split(':')[1].split()[0])
			#print ("os: Seven, IPv4: " + IPaddressLocal)
		else: #linux
			#fichier=os.system(LinuxIP)
			fichier=os.popen(LinuxIP).read()
			#IPaddressLocal = fichier.split()[0]
			for addresse in fichier.split():
				IPaddressLocal_all.append(addresse)
			#print ("os: Linux, IPv4: " + IPaddressLocal)
	except:
		print ("METHODE 0:ipconfig/ifconfig, LOCAL IP NOT RESOLVED")

	try:
		#IPaddressLocal = (socket.gethostbyname(socket.gethostname()))
		IPaddressLocal_all2 = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
		for addresse in IPaddressLocal_all2:
			IPaddressLocal_all.append(addresse)
		#IPaddressLocal_all.append(IPaddressLocal_all2)
		#print ("IPaddressLocal_all: %s" %(IPaddressLocal_all))
		#print ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])
		#print ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")])
	except:
		print ("METHODE 1:socket.gethostbyname_ex, LOCAL IP NOT RESOLVED")
	
	# an other way to get ip
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#s.connect(("google.com",80))
		s.connect(("8.8.8.8",80)) #work only with external access
		IPaddressLocal_all.append(s.getsockname()[0])
		#print (s.getsockname()[0])
		s.close()
	except:
		print ("METHODE 2:socket.connect(external_ip), LOCAL IP NOT RESOLVED")

	# an other way to get ip: import netifaces
	try:
		for ifaceName in netifaces.interfaces():
			addresses = [i['addr'] for i in netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr':'No IP addr'}] )]
			#print ('%s: %s' % (ifaceName, ', '.join(addresses)) )
		for addresse in addresses:
			IPaddressLocal_all.append(addresse)
			
	except:
		print ("METHODE 3:netifaces.interfaces(), LOCAL IP NOT RESOLVED" )

	IPaddressLocal_all.append('127.0.0.1')
	IPaddressLocal_all.append('localhost')
	#clean duplicate lines
	IPaddressLocal_all2 = []
	for addresse in IPaddressLocal_all:
		if (not addresse in IPaddressLocal_all2) and (addresse != []) and (addresse[:2] != "No"):
			IPaddressLocal_all2.append(addresse)
	IPaddressLocal_all = IPaddressLocal_all2
	IPaddressLocal = IPaddressLocal_all[0]

	#varglob.anouncetexte.append(IPaddressLocal)
	#print ("IPaddressLocal_all: %s" %(IPaddressLocal_all))

	return(IPaddressPublic, IPhostname, IPaddressLocal, IPaddressLocal_all)

################################################
class ThreadServeurClient(threading.Thread):
	'''derivation thread object SERVEUR CLIENT to manage connexion with EACH client'''
	def __init__(self, conn, no):
		global conn_client, conn_client_name

		threading.Thread.__init__(self)
		self.connexion = conn
		self.no = no
		
		global serveur1
		#self.qServeurClient = Queue.Queue() # don't use queue, too long timing
		self.qServeurClient2 = ""
		
		self.running = True
		
	def run(self):
		#Dialogue with client :
		global conn_client, conn_client_name
		global is_serveur

		#global ParBulletSpeed, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick
		#global ParScreenSize, ParFPS
		#global ParAllowMulti360
		
		# if not deleted, we need to readjust that on restart
		self.running = True
		self.qServeurClient2 =""
		
		nom = self.getName()        # Each thread have a name
		print ("launch th_SerCli: %s\n" %(self.getName()))

		while self.running:
			try: # connexion my be interrupt for any reasons
				#msgClient = self.connexion.recv(8192)
				msgClient = self.connexion.recv(16384)
				self.qServeurClient2 += msgClient
				
				#if msgClient[-1] == '\n':
				if self.qServeurClient2.count('\n') > 0:

					try:
						value = self.qServeurClient2

						for xligne, ligne in enumerate(value.split()): # we may recive several trames in one recive
							if xligne >= value.count("\n"): # last line may be not finished with "\n"
								self.qServeurClient2 = ligne
								break
							else:
								print ("Th_ServClient >>> %s> %s" % (nom, ligne))
								if ligne[:3] == "FIN": # or ligne =='':
									self.running = False
									self.qServeurClient2 = ""
									break

								message = "%s> %s" % (nom, ligne)
								#print ("Th_ServClient >>>" + message)
								
								#BROADCAST message balls position
								if ligne[:2] == "B:":
									#print (ligne)
									for nb, player in enumerate(varglob.players):
										if player[0]!="free" and nb != self.no:
											conn = player[0]
											#conn.send("B:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z))
											conn.send(ligne+"\n")
									#continue

								#BROADCAST message bricks hit
								if ligne[:2] == "H:":
									#print (ligne)
									for nb, player in enumerate(varglob.players):
										if player[0]!="free" and nb != self.no:
											conn = player[0]
											#print ("Th_SerCli: %s" %(ligne))
											conn.send(ligne+"\n")
									#continue

								if ligne[:6] == "angle:":
									varglob.players[self.no][2] = eval(ligne[6:])
									#BROADCAST systematically all infos bat's
									for nb, player in enumerate(varglob.players):
										if (player[0] != "free") and (nb != self.no):
											conn = player[0]
											# no spaces in msg's.+fast, secure split
											conn.send("P" + str(self.no) + ":" + varglob.players[self.no][1] + ":" + str(varglob.players[self.no][2]) \
											+ ":" + str(varglob.players[self.no][3]) + ":" + str(varglob.players[self.no][4]) + ":" \
											+ str(varglob.players[self.no][5]) + ":" + str(varglob.playersbat[self.no][5]) + "\n" )
									# update bat's animation
									#load_batpng(self.no, varglob.playersbat[self.no][5])
									bats.load_batpng(self.no, varglob.playersbat[self.no][5])
									#continue

								if ligne[:1] == "S": # "S1:score"
									varglob.playerno = eval(ligne[1])
									#varglob.players[self.no][3] = eval(ligne[6:])
									#BROADCAST systematically all infos bat's
									for nb, player in enumerate(varglob.players):
										if player[0]!="free" and nb != self.no:
											conn = player[0]
											# no spaces in msg's.+fast, secure split
											conn.send("P" + str(varglob.playerno) + ":" + varglob.players[varglob.playerno][1] + ":" + str(varglob.players[varglob.playerno][2]) \
											+ ":" + str(varglob.players[varglob.playerno][3]) + ":" + str(varglob.players[varglob.playerno][4]) + ":" \
											+ str(varglob.players[varglob.playerno][5]) + ":" + str(varglob.playersbat[varglob.playerno][5]) + "\n" )

									# update bat's animation
									# maj des animation bat a faire ici ?
									# TODO check if inutile ??? update dans Th-R et Bullet, see also for balls?
									#load_batpng(varglob.playerno, varglob.playersbat[varglob.playerno][5])
									bats.load_batpng(varglob.playerno, varglob.playersbat[varglob.playerno][5])
									#continue

								#V105 update player penality: local time
								#BROADCAST update player penality: local time
								if ligne[:1] == "X":
									varglob.playerno = eval(ligne[2])
									if varglob.players[varglob.playerno][0] != "free" and varglob.playerno != self.no:
										conn = varglob.players[varglob.playerno][0]
										conn.send(ligne+"\n")
										print ("Th_ServClient >>> %s\n" %(ligne) )

								#BROADCAST message position missil
								if ligne[:2] == "T:":
									#print ligne
									for nb, player in enumerate(varglob.players):
										if player[0]!="free" and nb != self.no:
											conn = player[0]
											#conn.send("T:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z))
											conn.send(ligne+"\n")
											print ("Th_ServClient >>> %s\n" %(ligne) )
									#continue

								if ligne[:1] == "N": # bleft launch missils porteur
									varglob.playerno = eval(ligne[1])
									#print ("mouse_button right")
									#th_E.sendMsg("N%s\n" %(varglob.playerno))

									for idx, bullet in enumerate(varglob.bullets): # if speed == 0, missil must follow bat's porteur
										bporteur = varglob.bullets[idx][0].getporteur()
										if (bporteur-1) == varglob.playerno:
											bx, by, bvector = varglob.bullets[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
											bang = bvector[0]
											bspeed = bvector[1]
											if bspeed == 0:
												#setposxyvect((xy), vector)
												bx = math.cos(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[0] - varglob.balls[idx][0].getrect()[2]/2
												by = math.sin(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[1] - varglob.balls[idx][0].getrect()[3]/2
												varglob.bullets[idx][0].setposxyvect((bx,by), (math.pi+varglob.players[bporteur-1][2], ParBulletSpeed), varglob.players[bporteur-1][2])
								
												for nb, player in enumerate(varglob.players): # broadcast, informe clients
													if player[0]!="free" and nb != self.no:
														conn = player[0]
														bx, by, bvector = varglob.bullets[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
														bang = bvector[0]
														bspeed = bvector[1]
														conn.send("T:%s:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.bullets[idx][0].getimg(), bx, by, bang, ParBulletSpeed,varglob.players[bporteur-1][2]))
									#continue

								if ligne[:5] == "name:":
									print (nom)
									print (ligne[5:])
									#varglob.players[self.no][1] = ligne[5:-1]
									varglob.players[self.no][1] = ligne[5:]
									for cle2 in conn_client:
										conn_client[cle2].send(ligne)
									#continue

								if ligne[:1] == "M": # bright launch balls porteur
									varglob.playerno = eval(ligne[1])
									#print ("mouse_button left")
									# informe serveur
									#th_E.sendMsg("M%s\n" %(varglob.playerno))
									
									for idx, ball in enumerate(varglob.balls): # if speed == 0, ball must lollow bat's porteur
										bporteur = varglob.balls[idx][0].getporteur()
										if (bporteur-1) == varglob.playerno:
											bx, by, bvector = varglob.balls[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
											bang = bvector[0]
											bspeed = bvector[1]
											if bspeed == 0:
												#setposxyvect((xy), vector)
												bx = math.cos(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[0] - varglob.balls[idx][0].getrect()[2]/2
												by = math.sin(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[1] - varglob.balls[idx][0].getrect()[3]/2
												varglob.balls[idx][0].setposxyvect((bx,by), (math.pi+varglob.players[bporteur-1][2], ParBallSpeedSlow))
								
												for nb, player in enumerate(varglob.players): # BROADCAST, message for clients
													if player[0]!="free" and nb != self.no:
														conn = player[0]
														bx, by, bvector = varglob.balls[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
														bang = bvector[0]
														bspeed = bvector[1]
														conn.send("B:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.balls[idx][0].getimg(), bx, by, bang, bspeed))
														#conn.send(ligne+"\n")
									#continue

								#BROADCAST GAME ABORTED
								if ligne[:9] == "!ABORTED!":
									#print (ligne)
									for nb, player in enumerate(varglob.players):
										if player[0]!="free" and nb != self.no:
											conn = player[0]
											conn.send(ligne+"\n")
									#continue

								#BROADCAST MESSAGE ANNONCE
								if ligne[0][0] == 'A': # conn (maintenu by serveur) or P1, P2, P3, P4 (broadcast)
									#print (ligne)
									for nb, player in enumerate(varglob.players):
										if player[0]!="free" and nb != self.no:
											conn = player[0]
											conn.send(ligne+"\n")
											#varglob.anouncetexte.append(ligne[1])
									#continue

								# send level in progress only to client who's requested
								# (send levelActu/nombreLevels got no sens here)
								if ligne[:2] == "L?":
									levelServeurEncours = "L:"
									levelServeurEncours += varglob.levelName + ":"
									levelServeurEncours += varglob.levelBackGnd + ":"
									levelServeurEncours += str(ParBallSpeedSlow) + ":"
									levelServeurEncours += str(ParBallSpeedFast) + ":"
									levelServeurEncours += str(ParDwngrdBrick) + ":"
									levelServeurEncours += str(ParScreenSize[0]) + ":"
									levelServeurEncours += str(ParFPS) + ":"
									levelServeurEncours += str(ParAllowMulti360) + ":"
									
									levelServeurEncours += str(len(varglob.bricks)) + ":"
									#"px:py:img:status"
									for idx, brick in enumerate(varglob.bricks):
										ll = varglob.bricks[idx][0].getposxy()
										levelServeurEncours += str(ll[0]) + ":" + str(ll[1]) + ":"
										ll = varglob.bricks[idx][0].getimg()
										levelServeurEncours += str(ll) +":"
										ll = varglob.bricks[idx][0].getstatus()
										levelServeurEncours += str(ll) +":"

									levelServeurEncours = levelServeurEncours[:-1]
									#print ('SEND LEVEL TO CLIENT:'+levelServeurEncours)
									self.connexion.send(levelServeurEncours+"\n")

								#impose level in progress for all clients
								# (send levelActu/nombreLevels got no sens here)
								if ligne[:2] == "!L":
									levelServeurEncours = "L:"
									levelServeurEncours += varglob.levelName + ":"
									levelServeurEncours += varglob.levelBackGnd + ":"
									levelServeurEncours += str(ParBallSpeedSlow) + ":"
									levelServeurEncours += str(ParBallSpeedFast) + ":"
									levelServeurEncours += str(ParDwngrdBrick) + ":"

									# not need to send parBrickSpace nor parShiftBrick as these already defined as position in server
									# but need to send parScreenSize and parFPS
									#print ('NEW PAR TO SEND')
									#print ('parFPS: %s' %ParFPS)
									#print ('parScreenSize: %s' %ParScreenSize)
									levelServeurEncours += str(ParScreenSize[0]) + ":"
									levelServeurEncours += str(ParFPS) + ":"
									levelServeurEncours += str(ParAllowMulti360) + ":"

									levelServeurEncours += str(len(varglob.bricks)) + ":"
									#"px:py:img:status"
									A,B,C,D,E,F,G,H,I,J,K,L = 10,11,12,13,14,15,16,17,18,19,20,21
									a,b,c,d,e,f,g,h,i,j,k,l = 10,11,12,13,14,15,16,17,18,19,20,21

									for idx, brick in enumerate(varglob.bricks):
										ll = varglob.bricks[idx][0].getposxy()
										levelServeurEncours += str(ll[0]) + ":" + str(ll[1]) + ":"
										ll = varglob.bricks[idx][0].getimg()
										#levelServeurEncours += str(ll) +":"
										#ll = hex(ll)[-1:].upper()
										if ll==16 : ll = "G" #Random
										elif ll==17 : ll = "H" #invert
										elif ll==18 : ll = "I" #reduce
										elif ll==19 : ll = "J" #Enlarge
										elif ll==20 : ll = "K" #Nuclear
										elif ll==21 : ll = "L" #BigBall
										else: ll = hex(ll)[-1:].upper()
										levelServeurEncours += ll +":"
										ll = varglob.bricks[idx][0].getstatus()
										levelServeurEncours += str(ll) +":"

									levelServeurEncours = levelServeurEncours[:-1]

									for nb, player in enumerate(varglob.players):
										if player[0]!="free" and nb != self.no:
											conn = player[0]
											# WARNNING network paquet size and level string
											#print ('BRAODCAST SEND LEVEL: '+levelServeurEncours)
											conn.send(levelServeurEncours+"\n")

								#conn.send("D%s\n" %(self.no))
								if ligne[0][0] == 'D': # deconnect (maintenu by server) or P1, P2, P3, P4 (broadcast)
									global serveur1
									playerdis = eval(ligne[0][1])
									#FIXME: Windows/linux not same. TODO !!!!
									print ("Th_SerClient > playerno: %s disconnect\n" %(playerdis) )

									#varglob.players[playerdis] = ["free", "free", "free", 0, ParBulletQty, ParLives]
									
									# not util here, must be done from client ?
									#varglob.balls[playerdis][0].setth_E(0)
									#varglob.bullets[playerdis][0].setth_E(0)

									#serveur1.delclient(playerdis)

							self.qServeurClient2 = ""

					#except message:
					except:
						#print ("Th_ServClient except !!!%s!!!\n" %message)
						print ("Th_ServClient except1 !!!\n")
						sys.stdout.flush()
						self.qServeurClient2 = ""
						self.running = False

			#except message:
			except:
				#print ("Th_ServClient except !!!%s!!!\n" %message)
				print ("Th_ServClient except2 !!!\n")
				sys.stdout.flush()
				self.qServeurClient2 = ""
				self.running = False
			
		print ("stopping th_SerCli: %s\n" %(self.getName()) )
		#print ("Th_ServClient Close %s connexion server-> client\n" %(nom) )
		self.qServeurClient2 = ""
		#BROADCAST informe disconnexion
		for nb, player in enumerate(varglob.players):
			if player[0]!="free" and nb != self.no:
				conn = player[0]
				conn.send("A" + str(nb) + ":" + ("!!PLAYER%s(%s)DISCONNECT!!" %(self.no+1, varglob.players[self.no][1])) + "\n" )
				conn.send("D%s\n" %(self.no))
		
		#varglob.players[self.no] = ["free", "free", "free", 0, ParBulletQty, ParLives]
		#varglob.balls[self.no+1][0].setth_E(0)
		#varglob.bullets[self.no+1][0].setth_E(0)
		
		# stop connexion from serveur
		#self.connexion.shutdown(socket.SHUT_RDWR)
		#self.connexion.close
		
		print ("informe ThreadServer to delete client from List entry")
		serveur1.delClient(self.no)

		# thread end here

	def sendMsg(self, message_emis):
		"""End Thread Serveur Client, wait to close connexions"""
		if message_emis[:3] == "FIN":
			self.running = False

	def stop(self):
		"""Stop Thread Serveur Client immediatly, don't wait"""
		self.connexion.shutdown(socket.SHUT_RDWR)
		self.connexion.close()
		self.running = False
 
################################################
class ThreadServeur(threading.Thread):
	'''derivation thread object SERVEUR for launch serveur'''

	def __init__(self, HOST, PORT):
		threading.Thread.__init__(self)
		global conn_client, conn_client_name
	
		conn_client = {}               # dictionnary name connexions clients
		conn_client_name = {}          # dictionnary alias name connexions clients
		self.HOST=HOST
		self.PORT=PORT
		self.mySocket = 0
		
		self.running = True
		
		#list of 4 threads clients
		self.th_SerCli = ["free", "free", "free", "free"]
 
	def run(self):
		global conn_client, conn_client_name

		# if not deleted, we need to readjust that on restart
		self.running = True
		#list of 4 threads clients
		self.th_SerCli = ["free", "free", "free", "free"]

		# Initialisation server - Start socket :
		self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.mySocket.bind((self.HOST, self.PORT))
			print ("Server %s:%s ready, waiting for requests ..." %(self.HOST, self.PORT) )
			self.mySocket.listen(5) # max 5 connexions
		except socket.error:
			print ("Warning: Socket connexion to server at adress %s:%s FAILED.\n" %(self.HOST, self.PORT) )
			# 2nd try
			try:
				self.PORT += 1
				self.mySocket.bind((self.HOST, self.PORT))
				print ("Server %s:%s ready, waiting for requests ...\n" %(self.HOST, self.PORT) )
				self.mySocket.listen(5)
			except socket.error:
				print ("Warning: Socket connexion to serveur at adress %s:%s FAILED.\n" %(self.HOST, self.PORT) )
				self.running = False

		print ("launch thread_Server: %s\n" %(self.getName()) )
		#self.mySocket.settimeout(100)
		
		global continuer # need to know if game's stopping in threads
		
		while self.running:
			try:
				# waitting for client connexions request :
				connexion, adresse = self.mySocket.accept()
				#print ("connected adresse %s:%s" %(adresse[0], adresse[1]) )
				
				if not continuer:
					break
				# Create thread object to manage connexion :
				accepted = False
				for no, player in enumerate(varglob.players):
					if player[0]=="free":
						varglob.players[no][0]=connexion
						#varglob.players[no][0].settimeout(10)
						#varglob.players[no][0].settimeout(None)
						# update list of connected threads
						self.th_SerCli[no] = ThreadServeurClient(connexion, no)
						self.th_SerCli[no].start()
						time.sleep(1) # secure to be done
						it = self.th_SerCli[no].getName()        # identifiant thread
						print ("%s Client %s connected, adresse IP %s, port %s.\n" %(it, no, adresse[0], adresse[1]) )
						# Dialogue with client who request connexion:
						connexion.send("SERV>ConnectionAcceptedClient:%sClient.\n" %no) # IMPERATIF !!! no spaces in msg's.+fast, secure split
						accepted = True

						# send to new client actual list of clients connected
						# TODO check if must also send to clients connected ?
						for nb, player in enumerate(varglob.players):
							if player[0]!="free" and nb != no:
								# no spaces in msg's.+fast, secure split
								connexion.send("P" + str(nb) + ":" + varglob.players[nb][1] + ":" + str(varglob.players[nb][2]) \
								+ ":" + str(varglob.players[nb][3]) + ":" + str(varglob.players[nb][4]) + ":" \
								+ str(varglob.players[nb][5]) + ":" + str(varglob.playersbat[nb][5]) + "\n" )

						# send to clients connected announce message
						#varglob.anouncetexte.append("P%s_IP_%s_,_%s" %(no+1, adresse[0], adresse[1]))
						# we don't know yet player name
						# WARNING: double emploi avec le thread is_serveur
						varglob.anouncetexte.append("PLAYER_%s_FROM_IP_%s" %(no+1, adresse[0]))
						for nb, player in enumerate(varglob.players):
							if player[0]!="free" and nb != no:
								# no spaces in msg's.+fast, secure split
								varglob.players[no][0].send("A%s:PLAYER_%s_FROM_IP_%s\n" %(nb, no+1, adresse[0]))

						# stop loop search free player
						break
				
				if accepted == False :
					try: # connexion may be shutdown
						# if we arrive here, there is no possible connexion player free (>4)
						connexion.send("SERV>ConnectionRefusedTooMuchClients(>4).\n") # pas d'espaces dans msg's.+rapide, secu split
						connexion.close()
						#break non!!!
					except:
						pass
			except:
				pass
		
		#is running = False, stop serveur
		print ("stopping Main Server: %s\n" %(self.getName()) )
		#print ("Main Server: shutting down, close connexions ...\n")
		for no, player in enumerate(varglob.players):
			if varglob.players[no][0]!="free" or True:
				try:
					connexion = player[no]
					connexion.send("FIN\n")
					connexion.close()
					print ("connexion %s closed\n" %(no) )
					self.delClient(no)
					print ("client %s deleted\n" %(no) )
				except:
					print ("ERROR DEL CLIENT %s NOT EXIST.\n" %(no) )
					pass
		self.th_SerCli = ["free", "free", "free", "free"]
				
		print ("Stop threads...\n")
		for no, sercli in enumerate(self.th_SerCli):
			try:
				if sercli != "free" or True:
					self.th_SerCli[no].stop()
					print ("Stop threads ServerClient %s ...\n" %(no) )
			except:
				pass
		
		try:
			self.mySocket.close()
			del self.mySocket
			del connexion
			print ("connexion and socket closed\n")
		except:
			pass

		print ("Main Server Stopped\n")
					
	def is_running(self):
		"""return if server is running or not"""
		return (self.running)

	def getConnClient(self):
		"""return dictionnary connected clients{}"""
		global conn_client, conn_client_name

		return (conn_client)
		
	def getPlayers(self):
		"""return list players connected {}"""
		global conn_client, conn_client_name

		return (varglob.players)
		
	def delClient(self, idx):
		"""delete client connected from list"""
		global conn_client, conn_client_name
		
		try:
			if varglob.players[idx][0] != "free":
				print ("THSERVER: Stop connexion client %s...\n" %(idx) )
				# envoi au thread reception client
				connexion = varglob.players[idx][0]
				try:
					connexion.send("FIN\n")
					#connexion.shutdown(socket.SHUT_RDWR)
				except:
					pass
				try:
					connexion.close()
				except:
					pass
				print ("Server Send Stop Thread SerCli %s...\n" %(self.th_SerCli[idx].getname()) )
				# arrete le thread coté serveur
				try:
					#self.th_SerCli[idx].shutdown(socket.SHUT_RDWR)
					self.th_SerCli[idx].stop()
					self.th_SerCli[idx].close()
					self.th_SerCli[idx] = "free"
				except:
					pass
				print ("Server delete player %s from list" %(idx) )
				varglob.players[idx] = ["free", "free", "free", 0, ParBulletQty, ParLives]
				varglob.balls[idx+1][0].setth_E(0)
				varglob.bullets[idx+1][0].setth_E(0)
				
				varglob.players[idx][0] = "free"
				varglob.players[idx][1] = "free"
				varglob.players[idx][2] = "free"
		
		except:
			print ("Warning: DEL CLIENT %s NOT EXIST.\n" %(idx) )
			varglob.players[idx] = ["free", "free", "free", 0, ParBulletQty, ParLives]
			varglob.balls[idx+1][0].setth_E(0)
			varglob.bullets[idx+1][0].setth_E(0)
			
			varglob.players[idx][0] = "free"
			varglob.players[idx][1] = "free"
			varglob.players[idx][2] = "free"
		
	def stop(self):
		"""Stop Thread Serveur Master"""
		# need to unlock running
		#self.mySocket.shutdown(socket.SHUT_RDWR)
		self.mySocket.close()
		print ("Main Server Stop(): connexion and socket closed\n")
		self.running = False
		
	def changeIP(self, HOST, PORT):
		"""Thread Serveur Master Close socket and reconnect to an other ip"""
		global conn_client, conn_client_name
		# need to unlock running
		#self.mySocket.shutdown(socket.SHUT_RDWR)
		
		#for idx in xrange(0,3):
		#	try:
		#		self.delClient(idx)
		#	except:
		#		pass
		#self.mySocket.close()
		#self.th_SerCli = ["free", "free", "free", "free"]
		
		for no, player in enumerate(varglob.players):
			if varglob.players[no][0]!="free" or True:
				try:
					connexion = player[no]
					connexion.send("FIN\n")
					connexion.close()
					print ("connexion %s closed\n" %(no) )
					self.delClient(no)
					print ("client %s deleted\n" %(no) )
				except:
					print ("ERROR DEL CLIENT %s NOT EXIST.\n" %(no) )
					pass
		#self.th_SerCli = ["free", "free", "free", "free"]
			
		print ("Stop threads...\n")
		for no, sercli in enumerate(self.th_SerCli):
			try:
				if sercli != "free" or True:
					self.th_SerCli[no].stop()
					print ("Stop threads ServerClient %s ...\n" %(no) )
			except:
				pass
		
		try:
			self.mySocket.close()
			try:
				connexion, adresse = self.mySocket.accept()
			except:
				pass
			del self.mySocket
			del connexion, adresse
			print ("connexion and socket closed\n")
		except:
			pass

		self.HOST = HOST
		self.PORT = PORT
		# Initialisation server - Start socket :
		self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.mySocket.bind((self.HOST, self.PORT))
			print ("Server %s:%s ready, waiting for requests ..." %(self.HOST, self.PORT) )
			self.mySocket.listen(5) # max 5 connexions
		except socket.error:
			print ("Warning: Socket connexion to server at adress %s:%s FAILED.\n" %(self.HOST, self.PORT) )
			# 2nd try
			try:
				self.PORT += 1
				self.mySocket.bind((self.HOST, self.PORT))
				print ("Server %s:%s ready, waiting for requests ...\n" %(self.HOST, self.PORT) )
				self.mySocket.listen(5)
			except socket.error:
				print ("Warning: Socket connexion to serveur at adress %s:%s FAILED.\n" %(self.HOST, self.PORT) )
				self.running = False

		print ("thread_Server: %s\n" %(self.getName()) )
		#self.mySocket.settimeout(100)

		#print ("Main Server Change(): %s:%s\n" %(self.HOST, self.PORT) )
		
		#self.running = False
		
################################################
class ThreadReception(threading.Thread):
	"""objet thread CLIENT manage reception messages"""
	def __init__(self, conn, no):
		threading.Thread.__init__(self)
		self.connexion = conn           # ref. du socket de connexion
		self.no = no
		self.recivedMessages = "test self.recivedMessages()"
		self.qReception2 = ""
		
		self.running = True
 
	def run(self):
		global conn_client, conn_client_name, serveur1

		#global ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick
		#global ParScreenSize, ParFPS, ParAllowMulti360

		self.running = True
		self.qReception2 = ""
		nom = self.getName()        # each thread got a name
		print ("launch th_R: %s\n" %(self.getName()) )

		while self.running:
			try:
				#message_recu = self.connexion.recv(8192)
				message_recu = self.connexion.recv(16384)
				self.qReception2 += message_recu
				
				#TODO WINDOWS SLOW? SI MESSAGE PAS COMPLET? FIXED: lenteur de la fonction Queue.
				self.connexion.send('\n') #pb win7, xp, slow recive if not that , why!? see pydoc socket, win/linux
				#if message_recu[-1] == '\n' or True:
				if self.qReception2.count('\n') > 0:
				
					try:
						value = self.qReception2
						print ("Th_Recive %s >>> %s\n" %(nom, value))

						#we may recive severals lines in one block
						for xligne, ligne in enumerate(value.split()):
							if xligne >= value.count("\n"): # if line not ended, may be the last line
								self.qReception2 = ligne
								break
							else:
								if ligne[:3] == "FIN": #or ligne =='':
									self.running = False
									break

								# Bcast:"Px:name:angle:score"
								ligne = ligne.split(":")
								print (ligne)

								# manage messages priority H>S/P>B>T, clause "continue"
								# message brick hited 
								#self.th_E.sendMsg("H:%s:%s:%s:%s:%s\n" %(idx, varglob.bricks[idx][0].getimg(), varglob.bricks[idx][0].getstatus(), \
								#varglob.bricks[idx][0].getBrickScore(), varglob.bricks[idx][0].getBrickScorePlayer()))
								if ligne[0][0] == 'H': # conn (maintenu par serveur) ou P:1:image_ball:x:y:angle:speed (broadcast)
									#print ("Th_R: %s" %(ligne) )
									idx = eval(ligne[1])
									img = eval(ligne[2])
									status = eval(ligne[3])
									brickscore = eval(ligne[4])
									brickscoreplayer = eval(ligne[5])
									varglob.bricks[idx][0].setstatus(status)
									varglob.bricks[idx][0].setimg(img)
									varglob.bricks[idx][0].showBrickScore(brickscore, brickscoreplayer)

									# warning: to much sounds in multiplayers?
									if S_HitBrick:
										S_HitBrick.play()
									continue

								#message update player 
								if ligne[0][0] == 'P': # P1, P2, P3, P4 (broadcast)
									nb = eval(ligne[0][1])
									varglob.players[nb][1] = ligne[1] #nom
									varglob.players[nb][2] = eval(ligne[2]) #angle
									varglob.players[nb][3] = eval(ligne[3]) #score
									varglob.players[nb][4] = eval(ligne[4]) #ParBulletQty
									varglob.players[nb][5] = eval(ligne[5]) #ParLives
									varglob.playersbat[nb][5] = eval(ligne[6]) #animation bat
									#print ("FROM TH-Recive")
									bats.load_batpng(nb, varglob.playersbat[nb][5])
									continue
									
								#message update ball 
								#self.th_E.sendMsg("B:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z))
								if ligne[0][0] == 'B': # B:1:image_ball:x:y:angle:speed (broadcast) 
									idx = eval(ligne[1])
									#print ("th_R_B:%s\n" %(ligne[0]) )
									while idx+1 > len(varglob.balls): #idx start from 0, add ball if necessary
										varglob.balls.append([ball, ballsprite])
									newimg = eval(ligne[2])
									newx = eval(ligne[3])
									newy = eval(ligne[4])
									newangle = eval(ligne[5])
									newz = eval(ligne[6])
									varglob.balls[idx][0].setimg(newimg)
									varglob.balls[idx][0].setposxyvect((newx,newy), (newangle,newz))
									print ("th_R_B:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.balls[idx][0].getimg(), newx, newy, newangle, newz) )
									continue
									
								#message update bullet missil
								#self.th_E.sendMsg("T:%s:%s:%s:%s:%s:%s:%s\n" %(self.idx, self.img, self.rect.x, self.rect.y, angle, z, oriented))
								if ligne[0][0] == 'T': # T:1:image_bullet:x:y:angle:speed (broadcast)
									idx = eval(ligne[1])
									while idx+1 > len(varglob.bullets): #idx start from 0, add bullet if necessary
										varglob.bullets.append([bullet, bulletsprite])
									newimg = eval(ligne[2])
									newx = eval(ligne[3])
									newy = eval(ligne[4])
									newangle = eval(ligne[5])
									#print ("angle shoot: %s" %(ligne[5]))
									newz = eval(ligne[6])
									#neworiented = eval(ligne[7])
									neworiented = ligne[7]
									if neworiented != "free": neworiented = eval(neworiented)
									varglob.bullets[idx][0].setimg(newimg) #avant setposxyvect coz rot_center
									varglob.bullets[idx][0].setposxyvect((newx,newy), (newangle,newz), neworiented)
									#print ("update bullet T:%s:%s:%s:%s:%s:%s\n" %(idx, newimg, newx, newy, newangle, newz))
									continue
									
								#V105 update player penality: local time
								if ligne[0][0] == "X":
									print (ligne)
									#self.th_E.sendMsg("X%s:%s\n" %(self.porteurOrigin-1, varglob.PenalityDelays[self.porteurOrigin-1]))
									#self.th_E.sendMsg("X:%s:3\n" %(self.porteurOrigin-1))
									print (ligne[1])
									varglob.playerno = eval(ligne[1]) #normaly you're!
									print ("playerno: %s" %(varglob.playerno))
									print (ligne[2])
									PenalityTime = eval(ligne[2])
									print ("playerno: %s" %(PenalityTime))
									varglob.PenalityDelays[varglob.playerno] = time.time() + PenalityTime
									continue

								if ligne[0][:9] == "!ABORTED!": # conn (maintenu par serveur) ou P1, P2, P3, P4 (broadcast)
									#varglob.players[no][0].send("A" + str(nb) + ":" + ("PLAYER%s(%s)CONNECTED" %(no+1, varglob.players[no][1])) + "\n" )
									#varglob.players[no][0].send("A" + str(nb) + ":" + ("%s,%s" %(adresse[0], adresse[1])) + "\n" )
									varglob.anouncetexte.append("!GAME ABORTED!")
									print ("!GAME ABORTED!")
									for idx, ball in enumerate(varglob.balls):
										varglob.balls[idx][0].setspeed(0)
										varglob.balls[idx][0].setporteur(idx+1)
										varglob.balls[idx][0].setimg(idx+1)
										# in thread reception
										#th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0))
									for idx, bullet in enumerate(varglob.bullets):
										varglob.bullets[idx][0].setspeed(0)
										varglob.bullets[idx][0].setporteur(idx+1)
										varglob.bullets[idx][0].setimg(idx+1)
										# in thread reception
										#th_E.sendMsg("T:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0, 0))
										
									# level must be impose by server

								if ligne[0][0] == 'A': # conn (maintenu par serveur) ou P1, P2, P3, P4 (broadcast)
									#varglob.players[no][0].send("A" + str(nb) + ":" + ("PLAYER%s(%s)CONNECTED" %(no+1, varglob.players[no][1])) + "\n" )
									#th_E.sendMsg("A%s:WALL\n" %(porteur-1))

									if varglob.pdb_debug: pdb.set_trace()

									if ligne[1] == "WALL" :
										varglob.WallTime = time.time() + 7
									if ligne[1] == "INVERT" :
										idx = eval(ligne[0][1])
										varglob.InvertTime[idx] = time.time() + 5
									if ligne[1] == "SHORT" :
										idx = eval(ligne[0][1])
										varglob.BatDim[idx] = 1
										varglob.BatDimTime[idx] = time.time() + 10
										bats.load_batpng(idx, 2) #flash dark
									if ligne[1] == "LONG" :
										idx = eval(ligne[0][1])
										varglob.BatDim[idx] = 2
										varglob.BatDimTime[idx] = time.time() + 10
										bats.load_batpng(idx, 1) #flash light
									if ligne[1] == "NUCLEARON" :
										idx = eval(ligne[0][1])
										varglob.balls[idx][0].setnuclear(time.time() + 10)
									if ligne[1] == "NUCLEAROFF" :
										idx = eval(ligne[0][1])
										varglob.balls[idx][0].setnuclear(0)
									if ligne[1] == "BIGBALLON" :
										idx = eval(ligne[0][1])
										varglob.balls[idx][0].setbigball(time.time() + 7)
									if ligne[1] == "BIGBALLOFF" :
										idx = eval(ligne[0][1])
										varglob.balls[idx][0].setbigball(0)
										
									varglob.anouncetexte.append(ligne[1])
									
								#conn.send("D%s\n" %(self.no))
								if ligne[0][0] == 'D': # deconnect (maintain by serveur) ou D1, D2, D3, D4 (broadcast)
									playerdis = eval(ligne[0][1])
									print ("Th_R playerdis: %s disconnect" %(playerdis) )
									print ("Th_R playerno: %s" %(varglob.playerno) )
									varglob.players[playerdis] = ["free", "free", "free", 0, ParBulletQty, ParLives]
									# if 'DO' recived => serveur is disconnected !!!
									# but we can't reconnect local in th_R, see in mainloop										

								if ligne[0] == 'SERV>ConnectionAcceptedClient': # (SERVEUR>ConnectionAcceptedClient:%sLogged.\n" %1) (broadcast no spaces)
									varglob.playerno = eval(ligne[1][0])
									print ("i am playerno: %s logged" %(varglob.playerno) )
									varglob.players[varglob.playerno][1] = ParPlayerName

								# message levelInProgress
								#ll="L:nb:px:py:img:status:px:py:img:status:...
								if ligne[0][0] == 'L': # L:nb:px:py:img:status:px:py:img:status:... (broadcast)
									#TODO lock this step in thread ?
									# recive levelInProgress from server
									# (recive levelActu/nombreLevels got no sens here)
									varglob.levelName = ligne[1]
									varglob.levelBackGnd = ligne[2]
									ParBallSpeedSlow = eval(ligne[3])
									ParBallSpeedFast = eval(ligne[4])
									ParDwngrdBrick = eval(ligne[5])

									ParScreenSize = eval(ligne[6])
									ParFPS = eval(ligne[7])

									ParAllowMulti360 = eval(ligne[8])

									A,B,C,D,E,F,G,H,I,J,K,L = 10,11,12,13,14,15,16,17,18,19,20,21
									a,b,c,d,e,f,g,h,i,j,k,l = 10,11,12,13,14,15,16,17,18,19,20,21
									varglob.bricks = []
									print ("nb bricks: %s" %(ligne[9]))
									for idx in xrange(0, eval(ligne[9])*4,4):
										th_E = 0 # we"re never server here!
										#((px,py), threadEmission, idx, imgbrick, status)
										#brick = Brick((eval(ligne[idx+2]), eval(ligne[idx+3])), th_E, 0, eval(ligne[idx+4]), eval(ligne[idx+5]))
										#brick = Brick((eval(ligne[idx+9]), eval(ligne[idx+10])), th_E, 0, eval(ligne[idx+11]), eval(ligne[idx+12]))
										brick = Brick((eval(ligne[idx+10]), eval(ligne[idx+11])), th_E, 0, eval(ligne[idx+12]), eval(ligne[idx+13]))
										bricksprite = pygame.sprite.RenderPlain(brick)
										varglob.bricks.append([brick, bricksprite])

									#load level background
									varglob.background, toto = designer.load_backgnd(varglob.levelBackGnd)
									print ("LEVEL RECIVED")
									
									ParScreenSize = (ParScreenSize, ParScreenSize)		
									#resize Pygame screen
									varglob.fenetre_size = ParScreenSize
									print ("fenetre_size: %s, %s" %(varglob.fenetre_size) )
									varglob.fenetre_center = (varglob.fenetre_size[0] / 2 , varglob.fenetre_size[1] / 2)
									
									#resize Pygame backgroung
									varglob.background = pygame.transform.scale(varglob.background, varglob.fenetre.get_size())
									# WARNING: blit have to be done outside thread (main loop, or menu)
									varglob.fenetre.blit(varglob.background, (0,0))
									varglob.rayon = varglob.fenetre_center[1] - varglob.playersbat[0][3][1] # retirer la taille du sprite bat									

						# if reception doesn't finished, no '\n' left
						# see 1st if in for
						if self.qReception2.count('\n') > 0:
							self.qReception2 = ""

					except message:
						#raise
						print ("Thread reception except !!!THREAD %s, CLIENT RECEPTION 1 !!!\n" %(nom) )
						print (message)

						if varglob.pdb_debug: pdb.set_trace()
						
						sys.stdout.flush()
						self.qReception2 = ""
						self.running = False

			except:
			#except message:
				#raise
				print ("Thread reception except !!!THREAD %s, CLIENT RECEPTION 2 !!!\n" %(nom))
				#print (message)

				if varglob.pdb_debug: pdb.set_trace()
				
				sys.stdout.flush()
				self.qReception2 = ""
				self.running = False
							
		print ("stopping th_R: %s\n" %(self.getName()))
		#print ("Client %s Stoped By Serveur. Connexion closed.\n" %(nom))
		#self.connexion.shutdown(socket.SHUT_RDWR)
		#self.connexion.close
		serveur1.delClient(self.no)
		# thread <reception> end here.
		
	def recivedMsg(self):
		return (self.recivedMessages)

	def getrunning(self):
		return (self.running)

	def stop(self):
		"""stop Thread Recive messages"""
		#self.connexion.shutdown(socket.SHUT_RDWR)
		#self.connexion.close
		self.running = False
	
################################################
class ThreadEmission(threading.Thread):
	"""objet thread CLIENT manages messages emition"""
	def __init__(self, conn, no):
		threading.Thread.__init__(self)
		self.connexion = conn           # ref. du socket de connexion
		self.no = no
		self.running = True
 
	def run(self):
		print ("launch th_E: %s\n" %(self.getName()))
		self.running = True
		while self.running:
			#message_emis = raw_input()
			
			message_emis = ""
			time.sleep(1)
			
			if message_emis[:3] == "FIN":
				self.running = False
				break
			#self.connexion.send(message_emis)

		print ("stopping th_E: %s\n" %(self.getName()))
		#self.connexion.shutdown(socket.SHUT_RDWR)
		#self.connexion.close
	
	def sendMsg(self, message_emis):
		if message_emis[:3] == "FIN":
			self.running = False
		# if FIN, sending stop also ThreadServer, local or distant
		try:
			self.connexion.send(message_emis)
		except:
			print ("Warning: th_E unable to send message")
			self.running = False

	def getrunning(self):
		return (self.running)

	def stop(self):
		#self.connexion.shutdown(socket.SHUT_RDWR)
		#self.connexion.close
		# stop associed thread server
		try:
			self.connexion.send("FIN")
		except:
			pass
		self.running = False

################################################
def rot_center(image, rect, angle):
	"""rotate an image while keeping its center"""
	rot_image = pygame.transform.rotate(image, angle)
	w = math.sqrt(rect.width**2 + rect.height**2)
	rot_rect = rot_image.get_rect(center=rect.center, size=(w,w))

	return rot_image,rot_rect

#WARNING: doublon in designer, music_play & music_stop should be removed
#################################################
def music_play(song, times=-1):
	"""play start background music"""
	#global ParMusicYN, ParMusicVol
	if ParMusicYN:
		path = os.path.join("sounds", song)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(times)
		pygame.mixer.music.set_volume(ParMusicVol)
#################################################
def music_stop():
	"""play stop background music"""
	#global ParMusicYN, ParMusicVol
	if ParMusicYN:
		pygame.mixer.music.stop()
    
#################################################
def load_batpng0(bat, png):
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
				th_E.sendMsg("A%s:NUCLEAROFF\n" %(self.porteur-1))
		#raise down Big Ball Bonus
		if self.bigBallTime < time.time() and self.bigBallTime != 0:
			self.bigBallTime = 0
			self.setimg(self.img)
			#Warning: may not need to send over network
			print ("big ball down")
			if self.th_E != 0:
				th_E.sendMsg("A%s:BIGBALLOFF\n" %(self.porteur-1))

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
												th_E.sendMsg("A%s:WALL\n" %(self.porteur-1))

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
												th_E.sendMsg("A%s:INVERT\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 18: #SHORT brick
											print ("ball hit SHORT brick:%s bonus" %(idx))
											varglob.BatDim[porteur-1] = 1 #SHORT bat
											varglob.BatDimTime[porteur-1] = time.time() + 10
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											bats.load_batpng(self.porteur-1, 2) #flash dark
											varglob.anouncetexte.append("SHORT")
											if self.th_E != 0:
												th_E.sendMsg("A%s:SHORT\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 19: #LONG brick
											print ("ball hit LONG brick:%s bonus" %(idx))
											varglob.BatDim[porteur-1] = 2 #LONG bat
											varglob.BatDimTime[porteur-1] = time.time() + 10
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											bats.load_batpng(self.porteur-1, 1) #flash light
											varglob.anouncetexte.append("LONG")
											if self.th_E != 0:
												th_E.sendMsg("A%s:LONG\n" %(self.porteur-1))

										elif varglob.bricks[idx][0].getimg() == 20: #V1.0.7 NUCLEAR brick
											print ("ball hit NUCLEAR brick:%s bonus" %(idx))
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											self.nuclearTime = time.time() + 10
											varglob.anouncetexte.append("NUCLEARON")
											if self.th_E != 0:
												th_E.sendMsg("A%s:NUCLEARON\n" %(self.porteur-1))
												
										elif varglob.bricks[idx][0].getimg() == 21: #V1.0.7 BIG BALL brick
											print ("ball hit BIG BALL brick:%s bonus" %(idx))
											varglob.bricks[idx][0].setimg(0)
											varglob.bricks[idx][0].setstatus(0)
											self.bigBallTime = time.time() + 7
											self.setbigball(self.bigBallTime)
											varglob.anouncetexte.append("BIG_BALL")
											if self.th_E != 0:
												th_E.sendMsg("A%s:BIGBALLON\n" %(self.porteur-1))

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
		
#################################################	
def load_levels(name):
	"""Load file list levels in levelPack '.level' and return levels list object"""
	#open level file extension ".level" in correct directory.
	fullname = os.path.join('levels', name+".level")
	levelstext = []
	fichier = open(fullname,'r')
	# pass on each lines with command for
	for ligne in fichier.readlines() :
		# split line in words - split remove spaces and carriage return
		donnees = ligne.split()
		# finally add to level array 
		levelstext.extend(donnees)
	# end of loop for, close level file
	fichier.close()
	
	#print (levelstext)

	varglob.levels = []
	nblevels = 0
	sublevel = []
	#WARNING: somes parameters in v10x only, have to check version header file!
	for idx, line in enumerate(levelstext):
		if line =="[LEVELNAME]":
			sublevel.append(levelstext[idx+1])
		if line =="[LEVELBACKGND]":
			sublevel.append(levelstext[idx+1])
		if line =="[LEVELSOUND]":
			sublevel.append(levelstext[idx+1])
		if line =="[ParBallSpeedSlow]":
			sublevel.append(levelstext[idx+1])
		if line =="[ParBallSpeedFast]":
			sublevel.append(levelstext[idx+1])
		if line =="[ParDwngrdBrick]":
			sublevel.append(levelstext[idx+1])
		if line =="[ParShiftBrick]":
			sublevel.append(levelstext[idx+1])
		if line =="[ParBrickSpace]":
			sublevel.append(levelstext[idx+1])
		if line =="[ParScreenSize]":
			sublevel.append(levelstext[idx+1])
		if line =="[LevelValue]":
			A,B,C,D,E,F,G,H,I,J,K,L = 10,11,12,13,14,15,16,17,18,19,20,21
			a,b,c,d,e,f,g,h,i,j,k,l = 10,11,12,13,14,15,16,17,18,19,20,21

			idx2 = 0
			while levelstext[idx+idx2+1] != "[LEVELEND]":
				idx2 += 1
				sublevel.append(eval(levelstext[idx+idx2]))

		if line =="[LEVELEND]":
			varglob.levels.append(sublevel)
			nblevels += 1
			sublevel = []
	print ("nblevels: %s" %(nblevels))
	return (nblevels, varglob.levels) 

#################################################	
def menuupdate(no_message):
	#from reader import Reader
	global IPaddressPublic, IPhostname, IPaddressLocal, IPaddressLocal2
	
	#global ParPlayerName, ParFPS, ParScreenSize, ParLockMouse, ParShowMouse, ParDwngrdBrick, ParBallSpeedSlow, ParBallSpeedFast
	#global ParAllowMulti360, ParLives, ParBulletQty, ParBulletSpeed
	#global ParMusicYN, ParMusicVol, ParLevelPack, ParIPServer
	
	global serveur1, is_serveur
	
	if varglob.players[0][0] != "free": p1name = varglob.players[0][1]
	if varglob.players[0][0] == "free": p1name = "free"
	if varglob.players[1][0] != "free": p2name = varglob.players[1][1]
	if varglob.players[1][0] == "free": p2name = "free"
	if varglob.players[2][0] != "free": p3name = varglob.players[2][1]
	if varglob.players[2][0] == "free": p3name = "free"
	if varglob.players[3][0] != "free": p4name = varglob.players[3][1]
	if varglob.players[3][0] == "free": p4name = "free"
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
F11)CHANGE LOCAL IP

see other parameters in pybreak360.cfg
(InGame:D=Designer, B=BootPlayer, H=Scores)
      (SPACE OR ENTER TO RESUME)      
      (S TO SAVE pybreak360.cfg)      """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, \
   ParIPServer, ParPlayerName, ParAllowMulti360, ParFPS, ParLockMouse, ParShowMouse, ParMusicYN, ParMusicVol, ParLevelPack, f10)

	message1 = \
"""   --- SETTINGS ---   


CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s


F2)PLAYER NAME: %s



Only letters, numerics and -_ allowed.
if problems with keymap
see pybreak360_kbd and .cfg ...



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



if problems with keymap
see pybreak360_kbd and .cfg ...





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
F11)CHANGE LOCAL IP

see other parameters in pybreak360.cfg
(InGame:D=Designer, B=BootPlayer, H=Scores)
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
F11)CHANGE LOCAL IP

see other parameters in pybreak360.cfg
(InGame:D=Designer, B=BootPlayer, H=Scores)
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
F11)CHANGE LOCAL IP

see other parameters in pybreak360.cfg
(InGame:D=Designer, B=BootPlayer, H=Scores)
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
F11)CHANGE LOCAL IP

see other parameters in pybreak360.cfg
(InGame:D=Designer, B=BootPlayer, H=Scores)
      (SPACE OR ENTER TO RESUME)      
     CONNEXION WITH SERVER FAILED       """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, \
   ParIPServer, ParPlayerName, ParAllowMulti360, ParFPS, ParLockMouse, ParShowMouse, ParMusicYN, ParMusicVol, ParLevelPack, f10)

	#IPaddressLocal_all = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
	#IPaddressLocal_all.append('127.0.0.1')
	#IPaddressLocal_all.append('localhost')
	IPaddressPublic_none, IPhostname_none, IPaddressLocal_none, IPaddressLocal_all = getIP()

	message7 = \
"""   --- SETTINGS ---   
YOUR LOCAL IP IS: %s
hostname: %s
CONNECTED PLAYERS:
P1:%s P2:%s P3:%s P4:%s


if problems with keymap
see pybreak360_kbd and .cfg ...

YOU MAY NEED TO SAVE
AND RESTART GAME...

local ip founds:
%s

F11)CHANGE LOCAL IP: %s


    (F11, SPACE OR ENTER TO RESUME)      
                                     """ \
   %(IPaddressLocal, IPhostname, p1name, p2name, p3name, p4name, IPaddressLocal_all, IPaddressLocal2)

	# TODO place message menu in list, with parameters
	if no_message == 0: message = message0
	if no_message == 1: message = message1
	if no_message == 2: message = message2
	if no_message == 3: message = message3
	if no_message == 4: message = message4
	if no_message == 5: message = message5
	if no_message == 6: message = message6
	if no_message == 7: message = message7

	#texte = Reader(message, pos=(10,10), width=450, fontsize=16, height=420, bg=(200,200,200), fgcolor=(20,20,20))
	texte = Reader(message, pos=((varglob.fenetre_size[0]-450)/2,(varglob.fenetre_size[1]-400)/2), width=450, fontsize=16, height=420, bg=(200,200,200), fgcolor=(20,20,20))
	texte.show()
	#anti-rebond-keyboard
	global mem_evkey, mem_evtype
	mem_evkey = None
	mem_evtype = None

#################################################	
def menu():
	if varglob.pdb_debug: pdb.set_trace()

	global ParPlayerName, ParFPS, ParAllowMulti360, ParGrabMouse, ParLockMouse, ParShowMouse
	global ParLives, ParBulletQty, ParBulletSpeed, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick
	global ParMusicYN, ParMusicVol, ParLevelPack, ParIPServer, ParIPServerPort
	global ParKeybUnicode
	
	global IPaddressPublic, IPhostname, IPaddressLocal, IPaddressLocal2
	global th_E, th_R, serveur1
	global serveur1, is_serveur, IPport
	
	global angle2actu
	
	IPaddressLocal2 = IPaddressLocal
	
	menulevel = 0
	menuupdate(0)
	
	# num touchs doesn't allways alls work keyboard fr (linux, windows)
	while menulevel >= 0:
		ev = pygame.event.wait()
		global mem_evkey, mem_evtype
		mem_evtype = ev.type
		mem_evkey = None
		if mem_evtype==KEYDOWN:
			mem_evkey = ev.key
			
		if mem_evtype == KEYDOWN:
			if menulevel == 0 and (mem_evkey==K_SPACE or mem_evkey==K_RETURN): # or ev.key==K_ESCAPE): # Warning conflit potential with game key
				menulevel = -1
				break
				#menuupdate(0)

			# change IPaddressLocal
			if menulevel == 0 and mem_evkey==K_F11:
				IPaddressLocal2 = IPaddressLocal
				menulevel = 7
				menuupdate(7)
			if menulevel == 7:
				#print ("len IPaddressLocal: %s"%len(IPaddressLocal2) )
				print ("Key: %s" %mem_evkey)

				if mem_evkey==K_BACKSPACE and len(IPaddressLocal2)>0:
					IPaddressLocal2 = IPaddressLocal2[:-1]
					menuupdate(7)
				if len(ParIPServer)<15:
					#TODO: check if valid syntaxe IPv4, resolve hostname
					tchPressed = pygame.key.get_pressed()
					
					# Pygame doesn't recognize all keyboards. 1st test in pybreak360_kbd
					# if mem_evkey in pybreak360_kbd.i18n_keys["fr"]:
					if mem_evkey in pybreak360_kbd.i18n_keys[ParKeybi18n]:
						if tchPressed[K_RSHIFT] or tchPressed[K_LSHIFT]:
							IPaddressLocal2 += pybreak360_kbd.i18n_keys[ParKeybi18n][mem_evkey].upper()
						else:
							IPaddressLocal2 += pybreak360_kbd.i18n_keys[ParKeybi18n][mem_evkey]
						menuupdate(7)

					elif (mem_evkey in range(K_a, K_z) or mem_evkey==K_PERIOD or mem_evkey in range(K_0, K_9) or mem_evkey==K_MINUS or mem_evkey==K_UNDERSCORE):
						#tchPressed = pygame.key.get_pressed()

						if ParKeybUnicode:
							carac= ev.dict['unicode']
							IPaddressLocal2 += carac
						else:
							if (tchPressed[K_RSHIFT] or tchPressed[K_LSHIFT]) and (mem_evkey in range(K_a, K_z)):
								IPaddressLocal2 += chr(mem_evkey).upper()
							else:
								IPaddressLocal2 += chr(mem_evkey)	
						menuupdate(7)

				if mem_evkey==K_SPACE or mem_evkey==K_RETURN or mem_evkey==K_F11:
					#need to restart local server if changed
					if IPaddressLocal2 != IPaddressLocal:
						pygame.mouse.set_cursor(*WAIT_CURSOR)
						#pygame.mouse.set_cursor(*HAND_CURSOR)
						is_serveur = False
						serverDisconnectER(serveur1)
						menuupdate(6) #msg disconnected
						print ("th_E, th_R, disconnected from server")
						time.sleep(1)

						#starting local server
						#serveur_Encours = False
						#client_Encours = False
						#is_serveur = True #allways at startup
						
						serveur1.stop()
						time.sleep(1)
						del serveur1
						#time.sleep(1)

						IPport = ParIPServerPort + 1
						IPaddressLocal = IPaddressLocal2
						ParIPaddressLocal = IPaddressLocal2
						
						#serveur1.changeIP(IPaddressLocal, IPport)
						serveur1 = ThreadServeur(IPaddressLocal, IPport)
						serveur1.start()
						time.sleep(1)
						
						print (is_serveur)
						print ("try to connect local server: %s:%s" %(IPaddressLocal, IPport))
						is_serveur = True
						th_E, th_R, sermsg = serverConnectER(serveur1)
						if sermsg == "CONNECTION ESTABLISHED":
							th_E.sendMsg("angle:%s\n" %(angle2actu))
							#th_E.sendMsg("angle:%s\n" %(varglob.players[varglob.playerno][2]))
							menuupdate(5) #msg connected
							#time.sleep(1)
						else:
							print ("Warning: unable to connect any server!!!")
							menuupdate(5) #msg connected
						a="""
							#if failed, try to reconnect local again
							#is_serveur = True
							IPaddressLocal = "127.0.0.1"
							print ("FAILD! try to reconnect local server: %s:%s" %(IPaddressLocal, IPport))
							serveur1.changeIP(IPaddressLocal, IPport)
							time.sleep(0.5)
							th_E, th_R, sermsg = serverConnectER(serveur1)
							print (sermsg)
							if sermsg != "CONNECTION ESTABLISHED":
								print ("Warning: unable to connect any server!!!")
								menuupdate(5) #msg connected
							else:
								menuupdate(6) #msg disconnected
						a="""
						time.sleep(1)

					menulevel = 0
					menuupdate(0)
					#pygame.mouse.set_cursor(*WAIT_CURSOR)
					pygame.mouse.set_cursor(*HAND_CURSOR)

			# change Distant Server IP
			if menulevel == 0 and mem_evkey==K_F1:
				menulevel = 2
				menuupdate(2)
			if menulevel == 2:
				#print ("len IP: %s"%len(ParIPServer) )
				print ("Key: %s" %mem_evkey)

				if mem_evkey==K_BACKSPACE and len(ParIPServer)>0:
					ParIPServer = ParIPServer[:-1]
					menuupdate(2)
				if len(ParIPServer)<15:
					#TODO: check if valid syntaxe IPv4, resolve hostname
					tchPressed = pygame.key.get_pressed()
					
					# Pygame doesn't recognize all keyboards. 1st test in pybreak360_kbd
					# if mem_evkey in pybreak360_kbd.i18n_keys["fr"]:
					if mem_evkey in pybreak360_kbd.i18n_keys[ParKeybi18n]:
						if tchPressed[K_RSHIFT] or tchPressed[K_LSHIFT]:
							ParIPServer = ParIPServer + pybreak360_kbd.i18n_keys[ParKeybi18n][mem_evkey].upper()
						else:
							ParIPServer = ParIPServer + pybreak360_kbd.i18n_keys[ParKeybi18n][mem_evkey]
						menuupdate(2)
						
					elif (mem_evkey in range(K_a, K_z) or mem_evkey==K_PERIOD or mem_evkey in range(K_0, K_9) or mem_evkey==K_MINUS or mem_evkey==K_UNDERSCORE):
						#tchPressed = pygame.key.get_pressed()

						if ParKeybUnicode:
							carac= ev.dict['unicode']
							ParIPServer = ParIPServer + carac
						else:
							if (tchPressed[K_RSHIFT] or tchPressed[K_LSHIFT]) and (mem_evkey in range(K_a, K_z)):
								ParIPServer = ParIPServer + chr(mem_evkey).upper()
							else:
								ParIPServer = ParIPServer + chr(mem_evkey)	
						menuupdate(2)

				if mem_evkey==K_SPACE or mem_evkey==K_RETURN or mem_evkey==K_F1:
					menulevel = 0
					menuupdate(0)

			# change Name
			if menulevel == 0 and mem_evkey==K_F2:
				menulevel = 1
				menuupdate(1)
			if menulevel == 1:
				#print ("len name: %s"%len(ParPlayerName) )
				print ("Key: %s" %mem_evkey)

				if mem_evkey==K_BACKSPACE and len(ParPlayerName)>0:
					ParPlayerName = ParPlayerName[:-1]
					menuupdate(1)
				if len(ParPlayerName)<10: #limit lengh name to 10 char
					tchPressed = pygame.key.get_pressed()
					
					# Pygame doesn't recognize all keyboards. 1st test in pybreak360_kbd
					# if mem_evkey in pybreak360_kbd.i18n_keys["fr"]:
					if mem_evkey in pybreak360_kbd.i18n_keys[ParKeybi18n]:
						if tchPressed[K_RSHIFT] or tchPressed[K_LSHIFT]:
							ParPlayerName = ParPlayerName + pybreak360_kbd.i18n_keys[ParKeybi18n][mem_evkey].upper()
						else:
							ParPlayerName = ParPlayerName + pybreak360_kbd.i18n_keys[ParKeybi18n][mem_evkey]
						menuupdate(1)
						
					elif (mem_evkey in range(K_a, K_z) or mem_evkey in range(K_0, K_9) or mem_evkey==K_MINUS or mem_evkey==K_UNDERSCORE):
						#tchPressed = pygame.key.get_pressed()

						if ParKeybUnicode:
							carac= ev.dict['unicode']
							ParPlayerName = ParPlayerName + carac
							menuupdate(1)
						else:
							if tchPressed[K_RSHIFT] or tchPressed[K_LSHIFT]:
								ParPlayerName = ParPlayerName + chr(mem_evkey).upper()
							else:
								ParPlayerName = ParPlayerName + chr(mem_evkey)						
							menuupdate(1)

				if mem_evkey==K_SPACE or mem_evkey==K_RETURN or mem_evkey==K_F2: #return to main menu
					varglob.players[varglob.playerno][1] = ParPlayerName
					menulevel = 0
					menuupdate(0)

			# ParAllowMulti360
			if menulevel == 0 and mem_evkey==K_F3:
				ParAllowMulti360 = not ParAllowMulti360
				menuupdate(0)
			# FPS
			if menulevel == 0 and mem_evkey==K_F4:
				ParFPS += 2
				if ParFPS > 60:
					ParFPS = 10
				menuupdate(0)
			# Lock Mouse
			if menulevel == 0 and mem_evkey==K_F5:
				ParLockMouse = not ParLockMouse
				menuupdate(0)
			# Show Mouse
			if menulevel == 0 and mem_evkey==K_F6:
				ParShowMouse = not ParShowMouse
				pygame.mouse.set_visible(ParShowMouse)
				menuupdate(0)
			#sound Yes / No
			if menulevel == 0 and mem_evkey==K_F7:
				ParMusicYN = not ParMusicYN
				if ParMusicYN:
					pygame.mixer.music.play()
				else:
					pygame.mixer.music.stop()
				menuupdate(0)
			#sound volume
			if menulevel == 0 and mem_evkey==K_F8:
				ParMusicVol += 0.1
				if ParMusicVol > 1:
					ParMusicVol = 0.1
				pygame.mixer.music.set_volume(ParMusicVol)
				menuupdate(0)

			#level pack
			if menulevel == 0 and mem_evkey==K_F9:
				#import glob
				print (ParLevelPack)
				fichiers = os.path.join("levels", "*.level")
				fichiers = glob.glob(fichiers)    #we list only files with "levels/*.level" extension
				if len(fichiers)>0:
					fichiers.sort()
					for idx, ligne in enumerate(fichiers):
						if (ParLevelPack+".level") == os.path.basename(ligne):
							
							if idx < (len(fichiers)-1):
								ParLevelPack = os.path.basename(fichiers[idx+1]).split('.')
								ParLevelPack = ParLevelPack[0]
								load_levels(ParLevelPack)
								varglob.nb_levels, varglob.levels = load_levels(ParLevelPack)
								varglob.levelNumber = 0
								varglob.levelName, varglob.levelBackGnd, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, varglob.levelClient = designer.level_select(varglob.levelNumber)
								varglob.background, toto = designer.load_backgnd(varglob.levelBackGnd)
								
								designer.level_blit(varglob.levelNumber)

								menuupdate(0)
								pygame.display.set_caption("PyBreak360 - V%s - LevelPack: %s" %(varglob.pybreak360version, ParLevelPack))
								break
							#begin the list
							else:
								ParLevelPack = os.path.basename(fichiers[0]).split('.')
								ParLevelPack = ParLevelPack[0]
								#print (ParLevelPack)
								load_levels(ParLevelPack)
								varglob.nb_levels, varglob.levels = load_levels(ParLevelPack)
								varglob.levelNumber = 0
								varglob.levelName, varglob.levelBackGnd, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, varglob.levelClient = designer.level_select(varglob.levelNumber)
								varglob.background, toto = designer.load_backgnd(varglob.levelBackGnd)

								designer.level_blit(varglob.levelNumber)

								menuupdate(0)
								pygame.display.set_caption("PyBreak360 - V%s - LevelPack: %s" %(varglob.pybreak360version, ParLevelPack))
								break

			#connect server
			if menulevel == 0 and mem_evkey==K_F10:
				pygame.mouse.set_cursor(*WAIT_CURSOR)
				#pygame.mouse.set_cursor(*HAND_CURSOR)
				print ("disconnecting from server....\n")
				serverDisconnectER(serveur1)

				if is_serveur:
					# we are server and become client
					# FIXME: need to disconnect all clients if we're server
					print ("try to connect distant server: %s:%s.\n" %(ParIPServer, ParIPServerPort))					
					is_serveur = False
					th_E, th_R, sermsg = serverConnectER(serveur1)
					if sermsg == "CONNECTION ESTABLISHED":
						th_E.sendMsg("angle:%s\n" %(angle2actu))
						#th_E.sendMsg("angle:%s\n" %(varglob.players[varglob.playerno][2]))
						menuupdate(4)
					else:
						#if failed, try to reconnect local
						is_serveur = True
						th_E, th_R, sermsg = serverConnectER(serveur1)
						menuupdate(6)
				else:
					# we are client and become server
					print ("try to connect local server: %s:%s" %(IPaddressLocal, ParIPServerPort+1))
					is_serveur = True
					th_E, th_R, sermsg = serverConnectER(serveur1)
					if sermsg == "CONNECTION ESTABLISHED":
						th_E.sendMsg("angle:%s\n" %(angle2actu))
						#th_E.sendMsg("angle:%s\n" %(varglob.players[varglob.playerno][2]))
						menuupdate(5)
					else:
						#if failed, try to reconnect local
						is_serveur = True
						th_E, th_R, sermsg = serverConnectER(serveur1)
						menuupdate(6)
				#pygame.mouse.set_cursor(*WAIT_CURSOR)
				pygame.mouse.set_cursor(*HAND_CURSOR)

			# save parameters
			if menulevel == 0 and mem_evkey==K_s:
				#print (ev.key)
				#print (mem_evkey)
				# erase old config, create from scratch
				fullname = os.path.join("", "pybreak360.cfg")
				try:
					fichier = open(fullname, "w")
					
					fichier.write("# pybreak360.cfg version: %s\n" %(varglob.pybreak360version))
					fichier.write("# only the 1st line just downside paramater is checked\n")
					fichier.write("[ParPlayerName]\n")
					fichier.write(ParPlayerName+"\n")

					fichier.write("[ParFPS]\n")
					fichier.write(str(ParFPS)+"\n")

					fichier.write("[ParGrabMouse]\n")
					fichier.write(str(ParGrabMouse)+"\n")
					fichier.write("True | False\n")

					fichier.write("[ParLockMouse]\n")
					fichier.write(str(ParLockMouse)+"\n")
					fichier.write("True | False\n")

					fichier.write("[ParShowMouse]\n")
					fichier.write(str(ParShowMouse)+"\n")
					fichier.write("True | False\n")

					fichier.write("[ParLives]\n")
					fichier.write(str(ParLives)+"\n")

					fichier.write("[ParBulletSpeed]\n")
					fichier.write(str(ParBulletSpeed)+"\n")

					fichier.write("[ParBulletQty]\n")
					fichier.write(str(ParBulletQty)+"\n")

					fichier.write("[ParMusicYN]\n")
					fichier.write(str(ParMusicYN)+"\n")
					fichier.write("True | False\n")

					fichier.write("[ParMusicVol]\n")
					fichier.write(str(ParMusicVol)+"\n")

					fichier.write("[ParLevelPack]\n")
					fichier.write(ParLevelPack+"\n")

					fichier.write("[ParIPServer]\n")
					fichier.write(ParIPServer+"\n")

					fichier.write("[ParIPServerPort]\n")
					fichier.write(str(ParIPServerPort)+"\n")

					fichier.write("[ParIPaddressLocal]\n")
					fichier.write(IPaddressLocal+"\n")

					fichier.write("[ParAllowMulti360]\n")
					fichier.write(str(ParAllowMulti360)+"\n")
					fichier.write("True | False : Warning:InvertCommand Brick Bonus not compliant\n")
					
					fichier.write("[ParKeybUnicode]\n")
					fichier.write(str(ParKeybUnicode)+"\n")
					fichier.write("True | False\n")
					
					fichier.write("[ParKeybi18n]\n")
					fichier.write((ParKeybi18n)+"\n")
					fichier.write("fr | us | gb - see pybreak360_kbd\n")


					# NOT USED
					fichier.write("# not need, updated by level config\n")
					fichier.write("[ParDwngrdBrick]\n")
					fichier.write(str(ParDwngrdBrick)+"\n")

					fichier.write("[ParBallSpeedSlow]\n")
					fichier.write(str(ParBallSpeedSlow)+"\n")

					fichier.write("[ParBallSpeedFast]\n")
					fichier.write(str(ParBallSpeedFast)+"\n")

					fichier.write("[ParScreenSize]\n")
					fichier.write(str(ParScreenSize[0])+"\n")
					fichier.write("480 640 800\n")

					fichier.close()

					print ("pybreak360.cfg saved")
				except pygame.error, message:
					print ("Warning: unable to save pybreak360.cfg")
				
				menuupdate(3)

#############################################
def serverDisconnectER(serveur1_toto):
	"""Disconnection from server
	Stop th_ServClient on server, then Stop local th_E, th_R"""

	# network settings
	global IPaddressPublic, IPhostname, IPaddressLocal
	#global ParIPServer, ParIPServerPort, ParPlayerName
	global serveur1, is_serveur
	global th_E, th_R
	
	# no matter if we're server or not
	print ("stop balls and bullets communication...")
	for idx, ball in enumerate(varglob.balls):
		varglob.balls[idx][0].setth_E(0)
	for idx, bullet in enumerate(varglob.bullets):
		varglob.bullets[idx][0].setth_E(0)
	print ("BALLS/BULLETS COMMUNICATION STOPPED !!!")
	time.sleep(0.2) # secure wait to be done
	
	# informe connected server (local or distant) to stop ThreadServerClient, we'll deconnecting
	# and stop th_E local
	try:
		th_E.sendMsg("D%s\n" %(varglob.playerno))
		print ("th_E sendMsg(D%s\n) !!!"%(varglob.playerno) )
	except:
		pass
	time.sleep(0.2) # secure wait to be done
	try:
		th_E.sendMsg("FIN\n")
		print ("th_E sendMsg(FIN\n) !!!")
	except:
		pass
	time.sleep(0.2) # secure wait to be done
	
	try:
		th_E.stop()
		print ("th_E STOPPED !!!")
	except:
		pass
	
	try:
		th_R.stop()
		print ("th_R STOPPED !!!")
	except:
		pass
	time.sleep(0.2) # secure wait to be done
	
	print ("is server: %s" %(is_serveur) )
	#was server and become client. stop balls and bullets communication
	if (is_serveur): # only if we was server and become client.
		# we don't need to stop local server. just reconnect th_E, th_R
		#print ("stop thread Recive")
		#th_E.stop() # don't need, as already done
	
		# th_R.stop() informe local server (that  stop ThreadServerClient local) we'll deconnecting
		# WARNING: client deleted on ServerThread
		print ("serveur1.delClient(%s) REQUEST !!!" %(varglob.playerno))
		#serveur1.delClient(varglob.playerno)
		time.sleep(0.2) # secure wait to be done
		print ("serveur1.delClient(%s) DONE ?!" %(varglob.playerno))

	# WARNING: need to del object cause _init ?
	try:
		del th_E
		print ("th_E DELETED !!!")
	except:
		pass		
	try:
		del th_R
		print ("th_R DELETED !!!")
	except:
		pass
	time.sleep(0.2) # secure wait to be done
	
	serveur_Encours = False
	connect_Encours = False
	client_Encours = False
	#NO?!:server may be distant
	#varglob.players = [["free", "free", 0, 0, ParBulletQty, ParLives], ["free", "free", "free", 0, ParBulletQty, ParLives], \
	#["free", "free", "free", 0, ParBulletQty, ParLives], ["free", "free", "free", 0, ParBulletQty, ParLives]]
	varglob.players[varglob.playerno] = ["free", "free", "free", 0, ParBulletQty, ParLives]

#############################################
def serverConnectER(serveur1_toto):
	""" th_E, th_R = serverConnectER(serveur1)
	launch th_ServClient on server, and start local th_E, th_R"""
	global is_serveur, IPaddressLocal, IPport
	#global ParIPServer, ParIPServerPort, ParPlayerName
	global client_Encours

	IPport = ParIPServerPort + 1
	# try to Establish connexion :
	try:
		connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#print ("socket.getdefaulttimeout(): ")
		#print (socket.getdefaulttimeout() )
		connexion.settimeout(5)
		if is_serveur:
			connexion.connect((IPaddressLocal, IPport))
			connexion.settimeout(None)
			print ("Connexion ESTABISHED with server %s:%s.\n" %(IPaddressLocal, IPport) )
		else:
			#connexion.connect((ParIPServer, ParIPServerPort))
			connexion.connect((ParIPServer, IPport))
			connexion.settimeout(None)
			#print ("Connexion ESTABISHED with server %s:%s.\n" %(ParIPServer, ParIPServerPort) )
			print ("Connexion ESTABISHED with server %s:%s.\n" %(ParIPServer, IPport) )
	except socket.error:
		if is_serveur:
			print ("Warning: Client connexion FAILED %s:%s.\n" %(IPaddressLocal, IPport) )
		else:
			#print ("Client connexion FAILED %s:%s.\n" %(ParIPServer, ParIPServerPort) )
			print ("Warning: Client connexion FAILED %s:%s.\n" %(ParIPServer, IPport) )
		# close connexion in case of opened
		try:
			connexion.close()
		except:
			pass
		# 2nd test on port +1
		try:
			IPport2 = IPport + 1
			ParIPServerPort2 = ParIPServerPort + 1
			connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			connexion.settimeout(5)
			if is_serveur:
				connexion.connect((IPaddressLocal, IPport2))
				connexion.settimeout(None)
				print ("Client Connexion ESTABISHED with server %s:%s.\n" %(IPaddressLocal, IPport2) )
			else:
				#connexion.connect((ParIPServer, ParIPServerPort))
				connexion.connect((ParIPServer, IPport2))
				connexion.settimeout(None)
				print ("Client Connexion ESTABISHED with server %s:%s.\n" %(ParIPServer, IPport2) )
		except socket.error:
			if is_serveur:
				print ("ERROR: Client connexion FAILED with server %s:%s and %s.\n" %(IPaddressLocal, IPport, IPport2) )
			else:
				print ("ERROR: Client connexion FAILED with server %s:%s and %s.\n" %(ParIPServer, IPport, IPport2) )
			# close connexion in case of opened
			try:
				connexion.close()
			except:
				pass
			return (0, 0, "CONNECTION FAILED")
			#sys.exit()    
	
	# Dialogue with server : launch 2 threads to manage 
	# independantly emit and recive messages :
	# WARNING: on same connexion?
	try:
		print ("Starting Thread emit.\n")
		th_E = ThreadEmission(connexion, varglob.playerno)
		th_E.start()
		print ("Thread emit started.\n")
	except:
		print ("ERROR: Thread emis is failed.\n")
		connexion.close()
		return (0, 0, "CONNECTION FAILED")
		#sys.exit()    
		
	try:
		print ("Starting Thread recive.\n")
		th_R = ThreadReception(connexion, varglob.playerno)
		th_R.start()
		print ("Thread recive started.\n")
	except:
		print ("ERROR: Thread recive is failed.\n")
		connexion.close()
		return (0, 0, "CONNECTION FAILED")
		#sys.exit()    

	client_Encours = True
	th_E.sendMsg("name:%s\n" %(ParPlayerName))
	
	if is_serveur == False: # if poste is client, ask for level before balls comunication
		th_E.sendMsg("L?\n")
		time.sleep(0.5)
	
	if is_serveur == True:
		# if poste is server, balls must communicate with clients
		for idx, ball in enumerate(varglob.balls):
			varglob.balls[idx][0].setth_E(th_E)
		# if poste is server, bullets must communicate with clients
		for idx, bullet in enumerate(varglob.bullets):
			varglob.bullets[idx][0].setth_E(th_E)
				
	return (th_E, th_R, "CONNECTION ESTABLISHED")

#hiscores = [LevelPackName,PlayerName,Hiscore,Level]
HS.hiscores = [["Classic480","Gino","0","URANUS"], ["Classic480Fast","Delf","765","LUNA"]]



#WARNING: don't need to be global?
global BotBatEnable, BotBatMovFow, BotBatMovRev, BotBatLaunchBall, BotBatLaunchMissil, BotBatLMRandomTime, BotBatMovRand, BotBatMovRandTime
BotBatEnable = False
BotBatMovFow = False
BotBatMovRev = False
BotBatLaunchBall = False
BotBatLaunchMissil = False
BotBatLMRandomTime = time.time() + (random.randrange(0, 10))
BotBatMovRand = 0
BotBatMovRandTime = 0

#################################################
def main():
	#global ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick

	global conn_client #"free" or conn
	global conn_client_name #"player1" aliasname
	global serveur1, is_serveur
	global th_E, th_R
	global BotBatEnable, BotBatMovFow, BotBatMovRev, BotBatLaunchBall, BotBatLaunchMissil, \
	BotBatLMRandomTime, BotBatMovRand, BotBatMovRandTime
	nbbricks = 0
	#global BckGndWall, BckGndWall2 # ??? why need global as from pybreak360_sprites import *
	BckGndWall, BckGndWallRect = load_png('WALL.PNG') #load_png function from pybreak360_sprites
	BckGndWall2 = pygame.transform.scale(BckGndWall, (480, 480))

	
	print ("Loading pybreak360.hiscores file")
	HS.hiscores = HS.load_hiscores()
	
	#ParAllowMulti360 = True #test
	
	#FIXME: test if sound available to enable sounds or not

	# Pygame initialisation
	#pygame.font.init()
	#pygame.key.set_repeat(30, 50)
	#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
	pygame.mixer.pre_init()
	pygame.init()
	pygame.mixer.set_num_channels(3)
	pygame.mixer.init()

	#Loading sounds
	
	#bakground music before levels, continus
	music_play("RhapsodyOfFireTornado.ogg", -1)

	#pygame.mixer.music.stop()
	#pygame.display.set_icon(pygame.image.load(os.path.join("images","pybreak360.png")))
	pygame.display.set_icon(pygame.image.load(os.path.join("images","H_BALLS.PNG")))
	pygame.display.set_caption("PyBreak360 - V%s - LevelPack: %s" %(varglob.pybreak360version, ParLevelPack))

	# Pygame main display screen
	varglob.fenetre_size = ParScreenSize
	print ("fenetre_size: %s, %s" %(varglob.fenetre_size))
	varglob.fenetre_center = (varglob.fenetre_size[0] / 2 , varglob.fenetre_size[1] / 2)
	#print ("fenetre_center: %s, %s" %(varglob.fenetre_center))

	#global fenetre #import pybreak360_varglob as varglob
	#varglob.fenetre = pygame.display.set_mode(varglob.fenetre_size)

	#global playerbat not used
	
	#loading balls from varglob

	#Loading default background, do not use load_png from sprite (need resize)
	varglob.background, toto = designer.load_backgnd('pybreak360.png')	#('none.png')
	varglob.fenetre.blit(varglob.background, (0,0))
	
	pygame.display.flip()

	#Loading bricks from import
	#global BricksColor, BricksRect, BricksCenter

	for idx, playerbat in enumerate(varglob.playersbat):
		#perso = pygame.transform.scale(perso, (20,80))
		varglob.playersbat[idx][1] = varglob.playersbat[idx][0] # playersbat[idx][1]
		varglob.playersbat[idx][2] = varglob.playersbat[idx][0].get_rect() # playersbat[idx][2]
		varglob.playersbat[idx][3] = varglob.playersbat[idx][2].center # playersbat[idx][3]
		varglob.playersbat[idx][4] = varglob.playersbat[idx][2] # playersbat[idx][4]
		varglob.playersbat[idx][5] = 0 # animation

		varglob.playersbat[idx][2].center = varglob.fenetre_center # playersbat[idx][]

	varglob.rayon = varglob.fenetre_center[1] - varglob.playersbat[0][3][1] # retirer la taille du sprite bat	
	print ("rayon: %s" %(varglob.rayon))

	#loading bullets
	print ("define players bullets")

	# Initialisation bullets
	#varglob.bullets = [["free", "free", (0,0,0,0), (0,0)], ["free", "free", (0,0,0,0), 0], ["free", "free", (0,0,0,0), 0], ["free", "free", (0,0,0,0), 0]]

	# Initialisation sprites bullets
	#a="""
	speed = 0 #3 #13
	ang = 0.47 # in rads
	#rand = ((0.1 * (random.randint(5,8))))
	th_E = 0 # server isn't started yet
	bullet1 = bullets.Bullet((50, 50), (ang, speed), th_E, 0, 1, 1) #((px,py),(angle,speed), threadEmission, idx_bullet, imgbullet, status-porteur)
	bullet2 = bullets.Bullet((40, 70), (0.88, 0), th_E, 1, 2, 2)
	bullet3 = bullets.Bullet((700, 700), (4.76, 0), th_E, 2, 3, 3)
	bullet4 = bullets.Bullet((700, 700), (2.76, 0), th_E, 3, 4, 4)

	bullet1sprite = pygame.sprite.RenderPlain(bullet1)
	bullet2sprite = pygame.sprite.RenderPlain(bullet2)
	bullet3sprite = pygame.sprite.RenderPlain(bullet3)
	bullet4sprite = pygame.sprite.RenderPlain(bullet4)

	varglob.bullets = []
	varglob.bullets.append([bullet1, bullet1sprite])
	varglob.bullets.append([bullet2, bullet2sprite])
	varglob.bullets.append([bullet3, bullet3sprite])
	varglob.bullets.append([bullet4, bullet4sprite])
	#a="""
	 
	#definition Levels

	varglob.nb_levels, varglob.levels = load_levels(ParLevelPack)
	varglob.levelNumber = 0
	varglob.levelName, varglob.levelBackGnd, ParBallSpeedSlow, ParBallSpeedFast, ParDwngrdBrick, varglob.levelClient = designer.level_select(varglob.levelNumber)
	varglob.background, toto = designer.load_backgnd(varglob.levelBackGnd)

	#Refresh screen display
	pygame.display.flip()
	 
	timebatflsash = time.time() # animation bat

	global continuer # need to know if game's stopping in threads
	continuer = 1
	x=0
	y = 0
	i = 0

	angle2 = 0 #Decimal(0) #to 2pi
	global angle2actu
	angle2actu = 0 #Decimal(0) #to 2pi

	varglob.playersbat[varglob.playerno][4][0] = varglob.fenetre_center[0] + varglob.rayon*math.cos(angle2)
	varglob.playersbat[varglob.playerno][4][1] = varglob.fenetre_center[1] + varglob.rayon*math.cos(angle2)

	angle3 = 3.14 #Decimal(3.14) #to 2pi
	angle3actu = 3.14 #Decimal(3.14) #to 2pi

	# Initialisation de l'horloge
	clock = pygame.time.Clock()

	#pygame.event.set_grab(True) # lock mouse and event inside (danger...)
	 
	# Initialisation balls
	#varglob.balls = [[objet-image, objet-sprite, position_rect, (angle,speed)], [objet-image, position, (angle,speed)]]

	speed = 0 #3 #13
	ang = 0.47 # en rads
	#rand = ((0.1 * (random.randint(5,8))))
	th_E = 0 # server isn't started yet
	ball1 = Ball((50, 50), (ang, speed), th_E, 0, 1, 1) #((px,py),(angle,speed), threadEmission, idx_ball, imgball, status-porteur)
	ball2 = Ball((40, 70), (0.88, 0), th_E, 1, 2, 2)
	ball3 = Ball((700, 700), (4.76, 0), th_E, 2, 3, 3)
	ball4 = Ball((700, 700), (2.76, 0), th_E, 3, 4, 4)

	# Initialisation balls sprites
	#playersprites = pygame.sprite.RenderPlain((player1, player2))
	ball1sprite = pygame.sprite.RenderPlain(ball1)
	ball2sprite = pygame.sprite.RenderPlain(ball2)
	ball3sprite = pygame.sprite.RenderPlain(ball3)
	ball4sprite = pygame.sprite.RenderPlain(ball4)

	varglob.balls = []
	varglob.balls.append([ball1, ball1sprite])
	varglob.balls.append([ball2, ball2sprite])
	varglob.balls.append([ball3, ball3sprite])
	varglob.balls.append([ball4, ball4sprite])
	
	# Initialisation bricks
	# done in select_level
	
	#network part
	global IPaddressPublic, IPhostname, IPaddressLocal, IPaddressLocal2
	IPaddressPublic = "127.0.0.1"
	IPhostname = "Unknow"
	IPaddressLocal= "127.0.0.1"
	IPaddressLocal_all = ["127.0.0.1", "localhost"]
	#IPport = 50000
	IPport = ParIPServerPort + 1
	IPaddressPublic, IPhostname, IPaddressLocal, IPaddressLocal_all = getIP()
	#IPaddressLocal= "192.168.0.37"
	IPaddressLocal = ParIPaddressLocal

	#starting local server
	serveur_Encours = False
	client_Encours = False
	is_serveur = True #allways at startup
	
	# allways start the local server
	serveur1 = ThreadServeur(IPaddressLocal, IPport)
	serveur1.start()
	
	time.sleep(1)
	# verify if server started effectivly, retry 2nd time in localhost
	if not serveur1.is_running():
		if IPaddressLocal != "127.0.0.1" and IPaddressLocal != "localhost":
			#try to run server in localhost
			IPaddressLocal = "127.0.0.1"
			serveur1 = ThreadServeur(IPaddressLocal, IPport)
			serveur1.start()
			time.sleep(1)
			if not serveur1.is_running():
				sys.exit()
		else:
			#nothing else we can do
			sys.exit()
	
	th_E, th_R, sermsg = serverConnectER(serveur1)
	if sermsg != "CONNECTION ESTABLISHED":
		print (sermsg)
		sys.exit()
	
	#global WAIT_CURSOR, HAND_CURSOR
	#from pybreak360_cursors import WAIT_CURSOR, HAND_CURSOR
	#pygame.mouse.set_cursor(*WAIT_CURSOR)
	pygame.mouse.set_cursor(*HAND_CURSOR)
	print ("mouse.set_visible(%s)" %ParShowMouse)
	pygame.mouse.set_visible(ParShowMouse)
	

	p2_mx0, p2_my0 = pygame.mouse.get_pos() #(0,0)
	dbfx0 = 0
	dbfy0 = 0
	rads_mouse = 0
	rads_mouse2 = 0
	angle2old = 0
	
	memoK_LEFT = False
	memoK_RIGHT = False
	memoK_LEFTvalue = 0
	memoK_RIGHTvalue = 0
	print ("STARTING GAME...")
	
	# INFINITE LOOP
	while continuer:
		# ensure that secreen size is those requested (server change for client)
		if pygame.display.get_surface().get_rect()[2] != varglob.fenetre_size[0]:
			varglob.fenetre = pygame.display.set_mode(varglob.fenetre_size)
			varglob.fenetre_center = (varglob.fenetre_size[0] / 2 , varglob.fenetre_size[1] / 2)
			varglob.background = pygame.transform.scale(varglob.background, varglob.fenetre.get_size())
			BckGndWall2 = pygame.transform.scale(BckGndWall, varglob.fenetre.get_size())
			varglob.rayon = varglob.fenetre_center[1] - varglob.playersbat[0][3][1] # retirer la taille du sprite bat

		# ensure game working at 60 FramesPerSeconde, synchro with clients
		clock.tick(ParFPS)
		
		if ParGrabMouse:
			pygame.event.set_grab(True) # lock mouse and event inside windows

		spacePressed = pygame.key.get_pressed()
		#print (spacePressed)
				
		#pb synchro between clock tiks and keyreapeat ?
		if (memoK_RIGHT and not memoK_LEFT) or (BotBatMovFow):
			memoK_LEFT = False
			memoK_LEFTvalue = 0
			memoK_RIGHTvalue += 0.01
			if memoK_RIGHTvalue > 0.2:
				memoK_RIGHTvalue = 0.2
		else:
			if memoK_RIGHTvalue > 0:
				memoK_RIGHTvalue -= 0.02
			if memoK_RIGHTvalue < 0:
				memoK_RIGHTvalue = 0
		
		if (memoK_LEFT and not memoK_RIGHT) or (BotBatMovRev):
			memoK_RIGHT = False
			memoK_RIGHTvalue = 0
			memoK_LEFTvalue -= 0.01
			if memoK_LEFTvalue < -0.2:
				memoK_LEFTvalue = -0.2
		else:
			if memoK_LEFTvalue < 0:
				memoK_LEFTvalue += 0.02
			if memoK_LEFTvalue > 0:
				memoK_LEFTvalue = 0

		p2_mx, p2_my = pygame.mouse.get_pos() #(0,0) in pixel
		
		if memoK_RIGHTvalue > 0 or memoK_LEFTvalue < 0 :
			rads_mouse = rads_mouse + memoK_RIGHTvalue + memoK_LEFTvalue
			pygame.mouse.set_pos(varglob.fenetre_center[0]+math.cos(rads_mouse)*varglob.rayon/1.5, varglob.fenetre_center[1]+math.sin(rads_mouse)*varglob.rayon/1.5)
			p2_mx, p2_my = varglob.fenetre_center[0]+math.cos(rads_mouse)*varglob.rayon/1.5, varglob.fenetre_center[1]+math.sin(rads_mouse)*varglob.rayon/1.5

		
		#position en x dans la fenetre = 360° angle de 0 a 2pi
		#angle2actu = round(Decimal(3.1416*2)*(Decimal(p2_mx)/(varglob.fenetre_size[1])), 5)
		
		#TODO: l'angle ne doit pas dependre de la coordonnee X, mais de l'angle-centre-fenetre de la souris.
		#TODO: l'angle de la coordonnee relative serai meilleur?
		
		fx = varglob.fenetre_center[0]
		fy = varglob.fenetre_center[1]
		#calcul de la distance
		dbfx = p2_mx - fx
		dbfy = p2_my - fy
		#TODO: l'angle ne doit pas dependre de l'angle-centre-fenetre de la souris, mais de va variation angulaire de la souris elle meme.
		#TODO: 1h du mat, essai pas glop, c'est mieu de confiner la souris a l'interrieur de la fenetre
		rayon_mouse = math.sqrt(dbfx*dbfx+dbfy*dbfy) #pythagore a²+b²=c²
		#calcul de l'angle
		rads_mouse = -math.atan2(-dbfy,dbfx)
		rads_mouse %= (math.pi*2)
		rads_mouse = round(rads_mouse,5)
		#print ("rads_mouse: %s" %(rads_mouse))

		# limiter l'angle de la souris en fonction du nombre de joueurs 
		#if (rayon_mouse < (varglob.rayon/3 - 3)) or (rayon_mouse > (varglob.rayon/3 + 3)):
		varglob.howplayers = 0
		# existe if angle != "free"
		if (varglob.players[0][2]!="free"):
			varglob.howplayers += 1
		if (varglob.players[1][2]!="free"):
			varglob.howplayers += 1
		if (varglob.players[2][2]!="free"):
			varglob.howplayers += 1
		if (varglob.players[3][2]!="free"):
			varglob.howplayers += 1

		#print (varglob.howplayers)
		if varglob.howplayers == 0:
			varglob.howplayers = 1
		
		#test
		#varglob.howplayers = 2
		#ParAllowMulti360 = False
			
		radsmouseplayer = math.pi*2 / varglob.howplayers
		if varglob.fenetre_size == (800, 800):
			radsmouseplayerstart = (radsmouseplayer * varglob.playerno) + 0.090
			radsmouseplayerend = (radsmouseplayerstart + radsmouseplayer) - 0.090*2
		elif varglob.fenetre_size == (640, 640):
			radsmouseplayerstart = (radsmouseplayer * varglob.playerno) + 0.125
			radsmouseplayerend = (radsmouseplayerstart + radsmouseplayer) - 0.125*2
		else:
			radsmouseplayerstart = (radsmouseplayer * varglob.playerno) + 0.160
			radsmouseplayerend = (radsmouseplayerstart + radsmouseplayer) - 0.160*2

		#WARNING: zero overflow with 3 players ?
		if (varglob.howplayers > 1) and ( not ParAllowMulti360): #v1.04
			#if (((rads_mouse) < radsmouseplayerstart)) or (rads_mouse) > (radsmouseplayerend+radsmouseplayer/2)):
			if (((rads_mouse-radsmouseplayerstart) < -0.002) or (rads_mouse > (radsmouseplayerend+radsmouseplayer/2))):
				print ('<%s' %((rads_mouse-radsmouseplayerstart)) )
				rads_mouse = radsmouseplayerstart #+0.1
				#print ('=%s' %rads_mouse)
				pygame.mouse.set_pos(varglob.fenetre_center[0]+math.cos(rads_mouse+0.002)*varglob.rayon/1.5, varglob.fenetre_center[1]+math.sin(rads_mouse+0.002)*varglob.rayon/1.5)
				p2_mx, p2_my = varglob.fenetre_center[0]+math.cos(rads_mouse+0.002)*varglob.rayon/1.5, varglob.fenetre_center[1]+math.sin(rads_mouse+0.002)*varglob.rayon/1.5

				#re calcul de la distance
				dbfx = p2_mx - fx
				dbfy = p2_my - fy
				rayon_mouse = math.sqrt(dbfx*dbfx+dbfy*dbfy) #pythagore a²+b²=c²
				#re calcul de l'angle
				rads_mouse = -math.atan2(-dbfy,dbfx)
				rads_mouse %= (math.pi*2)

			#if (((rads_mouse) > radsmouseplayerend)): # or (rads_mouse) < (radsmouseplayerstart-radsmouseplayer/2)):
			if (((rads_mouse-radsmouseplayerend) > 0.002) or (rads_mouse < (radsmouseplayerstart-radsmouseplayer/2))):
				print ('>%s' %((rads_mouse-radsmouseplayerend)) )
				rads_mouse = radsmouseplayerend#-0.1
				#print ('=%s' %rads_mouse)
				pygame.mouse.set_pos(varglob.fenetre_center[0]+math.cos(rads_mouse-0.002)*varglob.rayon/1.5, varglob.fenetre_center[1]+math.sin(rads_mouse-0.002)*varglob.rayon/1.5)
				p2_mx, p2_my = varglob.fenetre_center[0]+math.cos(rads_mouse-0.002)*varglob.rayon/1.5, varglob.fenetre_center[1]+math.sin(rads_mouse-0.002)*varglob.rayon/1.5

				#re calculate distance
				dbfx = p2_mx - fx
				dbfy = p2_my - fy
				rayon_mouse = math.sqrt(dbfx*dbfx+dbfy*dbfy) #pythagore a²+b²=c²
				#re calculate angle
				rads_mouse = -math.atan2(-dbfy,dbfx)
				rads_mouse %= (math.pi*2)

		#106 Brick Bonus Invert Time
		if varglob.InvertTime[varglob.playerno] > time.time():
			if ParAllowMulti360: # invert bonus not allowed if not 360 degree game
				if not BotBatEnable: # invert bonus not allowed for bootPlayer
					rads_mouse += math.pi
					rads_mouse %= (math.pi*2)
			
		rads_mouse = round(rads_mouse,5)

		angle2actu = rads_mouse
		
		#Warning: saturation Th_R sur station cliente Windows
		#if angle2actu != angle2: #envoyer event que sur changement
		if abs(angle2actu - angle2old) > 0.001: #envoyer event que sur changement
			
			#update own position outside server
			#angle2 = rads_mouse
			#angle2actu = rads_mouse
			varglob.players[varglob.playerno][2] = rads_mouse

			th_E.sendMsg("angle:%s\n" %(angle2actu))
			angle2old = angle2actu

		# didn't done by thread reception	
		angle2 = rads_mouse
		varglob.players[varglob.playerno][2] = rads_mouse			
		
		#angle2 = varglob.players[varglob.playerno][2]		
		#print (angle2)

		for idx, playerbat in enumerate(varglob.playersbat):
			# existe if angle != "free"
			if (varglob.players[idx][2]!="free"):
				varglob.playersbat[idx][2][0] = varglob.fenetre_center[0] + varglob.rayon*math.cos(varglob.players[idx][2]) - varglob.playersbat[idx][3][0]
				varglob.playersbat[idx][2][1] = varglob.fenetre_center[1] + varglob.rayon*math.sin(varglob.players[idx][2]) - varglob.playersbat[idx][3][1]
				varglob.playersbat[idx][1], varglob.playersbat[idx][4] = rot_center(varglob.playersbat[idx][0], varglob.playersbat[idx][2], 90 - math.degrees(varglob.players[idx][2]))
			
		#spacePressed = pygame.key.get_pressed()
		#print (spacePressed)
		
		if spacePressed[K_ESCAPE]:
			if (serveur_Encours == True) or is_serveur:
				serveur1.stop()
			th_E.sendMsg("FIN\n")
			continuer = 0

		#v1.0.4
		BotEv = pygame.event.Event(pygame.USEREVENT, {'data': 'Bot', 'value': 'BotReq'})
		if not BotBatEnable:
			#BotBatEnable = False
			BotBatMovFow = False
			BotBatMovRev = False
			BotBatLaunchBall = False
			BotBatLaunchMissil = False
		else:
			# always launch ball
			bporteur = varglob.balls[varglob.playerno][0].getporteur()
			# existe if angle != "free"
			#if varglob.balls[varglob.playerno][0].getporteurorigin().
			if (varglob.players[bporteur-1][2]!="free"):
				if (bporteur-1) == varglob.playerno: # porteur is local client and so exist, except on deconnection
					bx, by, bvector = varglob.balls[varglob.playerno][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
					bang = bvector[0]
					bspeed = bvector[1]
					if bspeed == 0:
						BotBatLaunchBall = True
						pygame.event.post(BotEv)
					else:
						BotBatLaunchBall = False
			
			# random launch missil within 10 sec
			if time.time() > BotBatLMRandomTime :
				BotBatLMRandomTime = time.time() + (random.randrange(0, 10))
				BotBatLaunchMissil = True
				pygame.event.post(BotEv)
			else:
				BotBatLaunchMissil = False
				
			#BotBatFow and BotBatRev
			# got any balls (porteurOrigine)?
			#BotBatMovRev, BotBatMovtFow = False, False

			if BotBatMovRandTime > 0:
				BotBatMovRandTime -=1
				
			# move anyway if no ball or no bricks
			if (varglob.players[varglob.playerno][5] <= 0) or (nbbricks == 0):
				# to ensure never lock
				if BotBatMovRandTime <=0 :
					BotBatMovRandTime = random.randrange(0, 5) # to ensure never lock FPS
					BotBatMovRand = random.randrange(0, 33)
					BotBatMovRev, BotBatMovtFow = False, False
					if BotBatMovRand  < 11:
						BotBatMovFow = True
						BotBatMovRev = False
						print ("BotBatMovForward\n")
						pygame.event.post(BotEv)
					if BotBatMovRand  >19:
						BotBatMovFow = False
						BotBatMovRev = True
						print ("BotBatMovReverse\n")
						pygame.event.post(BotEv)
					
			if varglob.players[varglob.playerno][5] > 0:
				BotBatMovRev, BotBatMovtFow = False, False
				# to ensure never lock
				if BotBatMovRandTime <=0 :
					BotBatMovRandTime = random.randrange(30, 120) # to ensure never lock FPS
					#BotBatMovRand = random.randrange(0, 30)/100 -0.15 # to ensure never lock
					BotBatMovRand = float(random.randrange(0, 20))
					BotBatMovRand = float((BotBatMovRand/100) - 0.10)
					#BotBatMovRand -= float(0.15) # to ensure never lock
					#print ('BotBatMovRand: %s' %(BotBatMovRand))
					#time.sleep(0.5)

				ballrads = varglob.balls[varglob.playerno][0].getrads()
				print ("ballrads: %s, angle2actu: %s\n" %(ballrads, angle2actu))
				
				#FIXED: ZERO PASSAGE POSITIF/NEGATIF GOT PROBLEMS
				#all in positive
				#distBallBat = (math.pi*2-angle2actu -ballrads)
				distBallBat = (math.pi*2-angle2actu -ballrads)

				limbat = 0.09
				if varglob.fenetre_size[0] >= 800:
					limbat = 0.09
				elif varglob.fenetre_size[0] >= 640:
					limbat = 0.14
				else:
					limbat = 0.17
				limbat -= 0.03
				limbat = 0.02 # middle atmolst at center

				
				if distBallBat < 0:
					distBallBat += BotBatMovRand
				else:
					distBallBat -= BotBatMovRand
				
				#if (distBallBat > math.pi) or (distBallBat < -math.pi):
				#	time.sleep(0.2)

				#print ("bot)BallRads: %s\n" %(rads))
				#print ("bot)BallAngle: %s\n" %(angle))
				#print ("bot)angleplayer %s: %s\n" %(nb, angleplayer))
				print ("bot)distBallBat: %s\n" %(distBallBat))
				#TODO: verifier les positions par calcul des coordonnees
				#if ((distBallBat < limbat) and (distBallBat >= 0)) or (distBallBat > math.pi*2-limbat): # try to fix 360° bug
				if (distBallBat > limbat) and (distBallBat < math.pi) or (distBallBat < -math.pi):
					BotBatMovFow = True
					BotBatMovRev = False
					print ("BotBatMovReverse\n")
					pygame.event.post(BotEv)
				#if ((distBallBat > -limbat) and (distBallBat < 0)) or (distBallBat < -math.pi*2+limbat): # try to fix 360° bug
				if (distBallBat < -limbat) and (distBallBat > -math.pi) or (distBallBat > math.pi):
					BotBatMovRev = True
					BotBatMovFow = False
					print ("BotBatMovForward\n")
					pygame.event.post(BotEv)

		for event in pygame.event.get():    # Waiting for events
			#fix test event type 1st, if event not exist
			if (event.type == KEYDOWN):
				if (event.key == K_RIGHT):
					memoK_RIGHT = True
					print ("rightdown")
			if (event.type == KEYDOWN):
				if (event.key == K_LEFT):
					memoK_LEFT = True
					print ("leftdown")
			if (event.type == KEYUP):
				if (event.key == K_RIGHT):
					memoK_RIGHT = False
					print ("rightup")
			if (event.type == KEYUP):
				if (event.key == K_LEFT):
					memoK_LEFT = False
					print ("leftup")
				
			#v1.0.4 BotBat
			if event.type == KEYDOWN:
				if event.key == K_b:
					BotBatEnable = not BotBatEnable #False
				
			if event.type == KEYDOWN:
				if (event.key == K_SPACE or event.key == K_RETURN):
					if endgame: endgame = False

			EvLaunchBall = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					EvLaunchBall = True
			if event.type == KEYDOWN:
				if event.key == K_DOWN:
					EvLaunchBall = True
					
			if (BotBatEnable and BotBatLaunchBall): # bgauche or K_DWN launch porteur bullets
				EvLaunchBall = True

			if (EvLaunchBall == True) and (time.time() > varglob.PenalityDelays[varglob.playerno]):
				print ("EvLaunchBall == True")
				# informer serveur doesn't needed, informe only ball launched
				#th_E.sendMsg("M%s\n" %(varglob.playerno))
				
				for idx, ball in enumerate(varglob.balls): #if vitesse == 0, ball must follow porteur's bat
					#bporteur = varglob.balls[idx][0].getporteur()
					# player got any own ball (porteurOrigine)?
					bporteur = varglob.balls[idx][0].getporteurorigin()
					# existe if angle != "free"
					if (varglob.players[bporteur-1][2] != "free"):
						if (bporteur-1) == varglob.playerno: # porteur is local client and so exist, except on deconnection
							bx, by, bvector = varglob.balls[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
							bang = bvector[0]
							bspeed = bvector[1]
							if bspeed == 0:
								# player got any own balls (porteurOrigine)?
								if varglob.players[idx][5] > 0:
									if S_gong:
										S_gong.play()
									#setposxyvect((xy), vector)
									bx = math.cos(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[0] - varglob.balls[idx][0].getrect()[2]/2
									by = math.sin(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[1] - varglob.balls[idx][0].getrect()[3]/2
									bx = round(bx, 5)
									by = round(by, 5)
									bangle = round(math.pi+varglob.players[bporteur-1][2], 5)
									#th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.balls[idx][0].getimg(), bx, by, math.pi+varglob.players[bporteur-1][2], ParBallSpeedSlow))
									varglob.balls[idx][0].setposxyvect((bx,by), (bangle, ParBallSpeedSlow))
									th_E.sendMsg("B:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.balls[idx][0].getimg(), bx, by, bangle, ParBallSpeedSlow))
			
			EvLaunchMissil = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 3:   # bgauche ou K_UP lancer les missiles du porteur
					EvLaunchMissil = True
			if event.type == KEYDOWN:
				if event.key == K_UP:   # bgauche ou K_UP lancer les missiles du porteur
					EvLaunchMissil = True
			if (BotBatEnable and BotBatLaunchMissil): # bgauche ou K_UP lancer les missiles du porteur
				EvLaunchMissil = True

			if (EvLaunchMissil == True):
				print ("EvLaunchMissil == True")
				# informe serveur is not utile, informe only bullet launched
				#th_E.sendMsg("N%s\n" %(varglob.playerno))
				
				for idx, bullet in enumerate(varglob.bullets): # if speed == 0, bullet follow bat's porteur
					bporteur = varglob.bullets[idx][0].getporteur()
					# exist if angle != "free"
					if (varglob.players[bporteur-1][2]!="free"):
						if (bporteur-1) == varglob.playerno: # porteur is local client and so exist, except on deconnection
							bx, by, bvector = varglob.bullets[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
							bang = bvector[0]
							bspeed = bvector[1]
							if bspeed == 0:
								# player got bullets?
								if (varglob.players[idx][4]!=0):
									if S_missil:
										S_missil.play()
									# decrement bullets when tarjectory end un bullet.update
									#varglob.players[idx][4]=varglob.players[idx][4] - 1
									#setposxyvect((xy), vector)
									bx = math.cos(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[0] - varglob.balls[idx][0].getrect()[2]/2
									by = math.sin(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[1] - varglob.balls[idx][0].getrect()[3]/2
									bx = round(bx, 5)
									by = round(by, 5)
									bangle = round(math.pi+varglob.players[bporteur-1][2], 5)
									varglob.bullets[idx][0].setposxyvect((bx,by), (bangle, ParBulletSpeed), varglob.players[bporteur-1][2])
									th_E.sendMsg("T:%s:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.bullets[idx][0].getimg(), bx, by, bangle, ParBulletSpeed, varglob.players[bporteur-1][2]))

			if event.type == QUIT:
				#th_E.sendMsg("FIN\n")
				continuer = 0

			#pygame.key.set_repeat(30, 50)
			#pygame.key.set_repeat()
			if is_serveur: # only if we're server, can change level
				if event.type == KEYDOWN:
					#if event.key == K_PLUS: # touche "+" # doesn't work with french keyboard
					if event.key == K_PAGEUP: # touche "+" # doesn't work with french keyboard
						if varglob.levelNumber+1 < varglob.nb_levels:
							# change level +
							# stop the game
							varglob.anouncetexte.append("!ABORTED!")
							th_E.sendMsg("!ABORTED!\n" )
							# stop balls and missils for all players
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
								#th_E.sendMsg("T:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0))
								th_E.sendMsg("T:%s:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0, varglob.players[idx][2]))
								#th_E.sendMsg("T:%s:%s:%s:%s:%s:%s\n" %(idx, varglob.bullets[idx][0].getimg(), bx, by, math.pi+varglob.players[bporteur-1][2], 0))

								# raz score, setback Qty ball & bullets
								varglob.players[idx][3] = 0
								varglob.players[idx][4] = ParBulletQty
								varglob.players[idx][5] = ParLives
								if varglob.players[idx][2] != "free":
									# update player
									th_E.sendMsg("S%s:%s\n" %(idx, varglob.players[idx][3]))

							varglob.levelNumber += 1
							designer.level_blit(varglob.levelNumber)

							# impose level to clients
							th_E.sendMsg("!L\n" )
							time.sleep(0.3)
							endgame = False #start a new game

					#if event.key == K_MINUS: #touch "-" work, but not "+"

				if spacePressed[K_PAGEDOWN]:
					if True:
						if varglob.levelNumber > 0:
							# change level -
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

								# raz score, setback Qty ball & bullets
								varglob.players[idx][3] = 0
								varglob.players[idx][4] = ParBulletQty
								varglob.players[idx][5] = ParLives
								if varglob.players[idx][2] != "free":
									# update player
									th_E.sendMsg("S%s:%s\n" %(idx, varglob.players[idx][3]))

							varglob.levelNumber -= 1
							designer.level_blit(varglob.levelNumber)

							# impose level to clients
							th_E.sendMsg("!L\n" )
							time.sleep(0.3)
							endgame = False #start a new game

			# MODE MENU
			# TODO: send clients to pause, clients must can change parametres
			if event.type == KEYDOWN:
				if event.key == K_SPACE or event.key == K_RETURN:
					#print ("paused")
					menu()
					#print ("resumeded")
				if event.key == K_h:
					#print ("paused")
					HS.menu_hiscores(HS.hiscores)
					#print ("resumeded")
				if event.key == K_d:
					print("entering level designer")
					designer.designer_level(varglob.levelNumber, th_E)

		#Re-blit background
		#WARNING: thread recive can change background server -> client
		try:
			varglob.fenetre.blit(varglob.background, (0,0)) # fond blanc
		except:
			pass
		try:
			if varglob.WallTime > time.time():
				varglob.fenetre.blit(BckGndWall2, (0,0)) # fond blanc
		except:
			pass			

		#Re-blit bricks		
		for idx, brick in enumerate(varglob.bricks):
			#WARNING: Thread recive can change brick count causing index out of range
			try: # thread may lock bilt
				varglob.bricks[idx][1].draw(varglob.fenetre)
				varglob.bricks[idx][0].showBrickScoreUpdate(varglob.fenetre)
			except:
				pass

		for idx, playerbat in enumerate(varglob.playersbat):
			# existe if connexion != "free"
			if (varglob.players[idx][2] != "free"):
				varglob.fenetre.blit(varglob.playersbat[idx][1], (varglob.playersbat[idx][4][0], varglob.playersbat[idx][4][1]))
		#v105 finally display top level bat owner
		if (varglob.players[varglob.playerno][2] != "free"):
			varglob.fenetre.blit(varglob.playersbat[varglob.playerno][1], (varglob.playersbat[varglob.playerno][4][0], varglob.playersbat[varglob.playerno][4][1]))

		for idx, playerbat in enumerate(varglob.playersbat):
			# return to normal dimentions
			if varglob.BatDim[idx] != 0:
				if varglob.BatDimTime[idx] < time.time(): # + 5
					varglob.BatDim[idx] = 0
					varglob.BatDimTime[idx] = 0
					bats.load_batpng(idx, 0)
			
			# return to color after a flash
			if (varglob.players[idx][2]!="free"): # if player exist
				if (varglob.playersbat[idx][5] != 0) and (varglob.playersbat[idx][5] != 10): # difup bat's player
					#print ("start anim bat")
					timebatflsash = time.time()
					varglob.playersbat[idx][5] = 10
				if (varglob.playersbat[idx][5] == 10): #animation in progress
					if time.time() > timebatflsash + 0.2: #stop animation
						#print ("stop anim bat")
						varglob.playersbat[idx][5] = 0
						bats.load_batpng(idx, 0)

		if ParLockMouse:
			# reposition mouse for synchro bat mouvement 
			if (rayon_mouse > (varglob.rayon/1.5 + 10)):
				pygame.mouse.set_pos(varglob.fenetre_center[0]+math.cos(rads_mouse)*varglob.rayon/1.5, varglob.fenetre_center[1]+math.sin(rads_mouse)*varglob.rayon/1.5)
			if (rayon_mouse < (varglob.rayon/4 - 10)):
				pygame.mouse.set_pos(varglob.fenetre_center[0]+math.cos(rads_mouse)*varglob.rayon/4, varglob.fenetre_center[1]+math.sin(rads_mouse)*varglob.rayon/4)
		
		for idx, bullet in enumerate(varglob.bullets): # if speed == 0, missil must fellow porteur's bat
			# player exist if angle != "free"
			if (varglob.players[idx][2]!="free"):
				# player got any bullets?
				if (varglob.players[idx][4]!=0):
					bx, by, bvector = varglob.bullets[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
					bang = bvector[0]
					bspeed = bvector[1]
					if bspeed == 0:
						bporteur = varglob.bullets[idx][0].getporteur()
						#setposxyvect((xy), vector)
						bx = math.cos(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[0] - varglob.bullets[idx][0].getrect()[2]/2
						by = math.sin(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[1] - varglob.bullets[idx][0].getrect()[3]/2
						varglob.bullets[idx][0].setposxyvect((bx,by), (math.pi-varglob.players[bporteur-1][2], 0), varglob.players[idx][2])
			
					#if is_serveur == True: # if serveur, les ball doivent communiquer
					#	varglob.balls[idx][1].update()
					#TODO les ball communiquent leur changement uniquement, le reste est gere par le client
					varglob.bullets[idx][1].update()
					# sinon l'update est fait par le thread reception
					try: # thread may lock bilt
						varglob.bullets[idx][1].draw(varglob.fenetre)
					except:
						pass

		for idx, ball in enumerate(varglob.balls): #si la vitesse est a 0, la ball suis la raquette du porteur
			# existe if angle != "free"
			if (varglob.players[idx][2]!="free"): # and (idx != varglob.playerno):
				# player got balls?
				if (varglob.players[idx][5]!=0):
					# player got balls own (porteurOrigine)?
					bporteur = varglob.balls[idx][0].getporteurorigin()
					if bporteur-1 == idx:

						bx, by, bvector = varglob.balls[idx][0].getposxyvect() #return (self.rect.x, self.rect.y, self.vector)
						bang = bvector[0]
						bspeed = bvector[1]
						if bspeed == 0:
							bporteur = varglob.balls[idx][0].getporteur()
							#setposxyvect((xy), vector)
							bx = math.cos(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[0] - varglob.balls[idx][0].getrect()[2]/2
							by = math.sin(varglob.players[bporteur-1][2]) * (varglob.rayon-14) + varglob.fenetre_center[1] - varglob.balls[idx][0].getrect()[3]/2
							varglob.balls[idx][0].setposxyvect((bx,by), (math.pi-varglob.players[bporteur-1][2], 0))

						# ball communicate only when event change somthink, movement managed by client
						varglob.balls[idx][1].update()
						# else update done in thread reception
						try: # thread may lock bilt
							#Warning: may not need, draw downstair
							varglob.balls[idx][1].draw(varglob.fenetre)
						except:
							pass
						#1.0.7 draw nuclear
						if varglob.balls[idx][0].getnuclear() !=0:
							ballpos = varglob.balls[idx][0].getposxyvect()
							ballpos = (ballpos[0], ballpos[1])
							try: # thread may lock bilt
								if varglob.balls[idx][0].getbigball()==0:
									varglob.fenetre.blit(g_ballnuclear, ballpos)
								else:
									varglob.fenetre.blit(g_bigballnuclear, ballpos)
							except:
								pass
						
		#v105 finally display top level ball owner
		if (varglob.players[varglob.playerno][2] != "free"):
			if (varglob.players[varglob.playerno][5]!=0): # player got balls?
				#varglob.balls[varglob.playerno][1].update()
				# else update done in thread reception
				try: # thread may lock bilt
					varglob.balls[varglob.playerno][1].draw(varglob.fenetre)
				except:
					pass
				#1.0.7 draw nuclear
				if varglob.balls[varglob.playerno][0].getnuclear() !=0:
					ballpos = varglob.balls[varglob.playerno][0].getposxyvect()
					ballpos = (ballpos[0], ballpos[1])
					try: # thread may lock bilt
						if varglob.balls[varglob.playerno][0].getbigball()==0:
							varglob.fenetre.blit(g_ballnuclear, ballpos)
						else:
							varglob.fenetre.blit(g_bigballnuclear, ballpos)
					except:
						pass
						

		# Display Announce text	
		#varglob.anouncetexte = ["PyBreak360"]
		#varglob.anouncetime = 2
		#varglob.anouncetimeactu = 0
		#varglob.anouncealpha = 128
		#varglob.anouncealphaactu = 1

		if len(varglob.anouncetexte) > 2:
			varglob.anouncetime = 0.5
		elif len(varglob.anouncetexte) > 1:
			varglob.anouncetime = 1
		else :
			varglob.anouncetime = 3

		if len(varglob.anouncetexte) > 0:
			if varglob.anouncetimeactu == 0:
				# init effect fondu
				#print (varglob.anouncetexte)
				#print (varglob.anouncetime)
				varglob.anouncetimeactu = time.time()
				varglob.anouncealphaactu = 50

			#font = pygame.font.Font(None, 48)
			font = pygame.font.Font("freesansbold.ttf", 20)
			
			font.set_bold(True)
			bgd = 20, 20, 20

			text = font.render(varglob.anouncetexte[0], 1, (0, 0, 0)) #RGBA
			#tmp = designer.get_alpha_surface(img, a, r, g, b, mode) # get current alpha
			#text = designer.get_alpha_surface(text, 128, 128, 128, 128, pygame.BLEND_RGBA_MULT) # get current alpha
			text = designer.get_alpha_surface(text, varglob.anouncealphaactu, varglob.anouncealphaactu, varglob.anouncealphaactu, \
			varglob.anouncealphaactu, pygame.BLEND_RGBA_MULT) # get current alpha

			textpos = text.get_rect()
			textpos.centerx = varglob.background.get_rect().centerx
			textpos.centery = varglob.background.get_rect().centery
			try: # thread may lock bilt
				varglob.fenetre.blit(text, textpos)
			except:
				pass
				
			if varglob.anouncealphaactu < varglob.anouncealpha: # degrader la transparence
				varglob.anouncealphaactu += 3
			if time.time() > (varglob.anouncetimeactu + varglob.anouncetime):
				varglob.anouncetimeactu = 0
				varglob.anouncealphaactu = 50 # start with some d'opacity
				del varglob.anouncetexte [0] # cancel 1st element request of text announce
				
		#font = pygame.font.Font(None, 32)
		font = pygame.font.Font("freesansbold.ttf", 16)
		#bricks left
		#text5 = font.render("Bricks: %s" %(len(bricks)), 1, (10, 10, 10))
		nbbricks = 0
		for idx, brick in enumerate(varglob.bricks):
		# don't count black bricks (7) as indestructibles
			#WARNING: Thread recive can change brick count causing index out of range
			try:
				if varglob.bricks[idx][0].getstatus()!=0:
					if varglob.bricks[idx][0].getimg()!=7:
						nbbricks += 1
			except:
				# Thread recive have changed brick count, at least one
				nbbricks += 1
				pass
		text5 = font.render("Bricks: %s" %(nbbricks), 1, (0, 0, 0))
		text5back = font.render("Bricks: %s" %(nbbricks), 1, (90, 90, 90))
		textpos5 = text5.get_rect()
		textpos5[1] = varglob.fenetre.get_rect()[3]-textpos5[3]*6
		try: # thread may lock bilt
			varglob.fenetre.blit(text5back, (textpos5[0]+1,textpos5[1]+1))
			varglob.fenetre.blit(text5, textpos5)
		except:
			pass
		# client check if end level
		if nbbricks == 0:
			# serveur check if end level
			if is_serveur:
				
				if varglob.howplayers == 1: #in one player, game finish with last level in pack
					if S_applaudissement:
						S_applaudissement.play()
					if varglob.levelNumber+1 < varglob.nb_levels:
						varglob.anouncetexte.append("NEXT_LEVEL")
						th_E.sendMsg("A%s:NEXT_LEVEL\n" %(varglob.playerno))
						varglob.levelNumber += 1

					#FIXME: balls and bullets doesn't stop for clients
					#stop balls and missils for all players
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
						#th_E.sendMsg("T:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0))
						th_E.sendMsg("T:%s:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0, varglob.players[idx][2]))

					designer.level_blit(varglob.levelNumber)

					# impose level to clients
					th_E.sendMsg("!L\n" )
					time.sleep(0.3)

		#info level with contrast
		textlevel = font.render("L:%s/%s, %s" %(varglob.levelNumber+1, varglob.nb_levels, varglob.levelName), 1, (0, 0, 0))
		textlevelback = font.render("L:%s/%s, %s" %(varglob.levelNumber+1, varglob.nb_levels, varglob.levelName), 1, (90, 90, 90))
		textlevelpos = textlevel.get_rect()
		textlevelpos[1] = varglob.fenetre.get_rect()[3]-textlevelpos[3]*5
		try: # thread may lock bilt
			varglob.fenetre.blit(textlevelback, (textlevelpos[0]+1,textlevelpos[1]+1))
			varglob.fenetre.blit(textlevel, textlevelpos)
		except:
			pass
		
		#imported from varglob
		a="""
		#render(text, antialias, color, background=None) -> Surface
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
		
		#p1name = varglob.players[0][1] #thread-name, alias-name, angle, score
		p1name = font.render("P1: %s" %(varglob.players[0][1]), 1, varglob.DeepYellow)
		p1namepos = p1name.get_rect()
		p1namepos[1] = varglob.fenetre.get_rect()[0]+0
		p1score = font.render("Score: %s" %(varglob.players[0][3]), 1, varglob.DeepYellow)
		p1scorepos = p1score.get_rect()
		p1scorepos[1] = varglob.fenetre.get_rect()[0]+p1namepos[3]
		#p1lives = font.render("Balls: %s" %(varglob.players[0][5]), 1, varglob.DeepYellow)
		p1lives = font.render("   : %s" %(varglob.players[0][5]), 1, varglob.DeepYellow)
		p1livespos = p1lives.get_rect()
		p1livespos[1] = varglob.fenetre.get_rect()[0]+p1namepos[3]+p1scorepos[3]
		#p1bullets = font.render("Bullets: %s" %(varglob.players[0][4]), 1, varglob.DeepYellow)
		p1bullets = font.render("   : %s" %(varglob.players[0][4]), 1, varglob.DeepYellow)
		p1bulletspos = p1bullets.get_rect()
		p1bulletspos[1] = varglob.fenetre.get_rect()[0]+p1namepos[3]+p1scorepos[3]+p1livespos[3]
		try: # thread may lock bilt
			varglob.fenetre.blit(p1name, p1namepos)
			varglob.fenetre.blit(p1score, p1scorepos)
			varglob.fenetre.blit(p1lives, p1livespos)
			varglob.fenetre.blit(g_livesYellow, p1livespos)
			varglob.fenetre.blit(p1bullets, p1bulletspos)
			varglob.fenetre.blit(g_bulletYellow, p1bulletspos)
		except:
			pass
		
		# exist if angle != "free"
		if (varglob.players[1][2]!="free"):# or True:
			p2name = font.render("P2: %s" %(varglob.players[1][1]), 1, varglob.DeepGreen)
			p2namepos = p2name.get_rect()
			p2namepos[0] = varglob.fenetre.get_rect()[2]-p2namepos[2] #left-longtext
			p2score = font.render("Score: %s" %(varglob.players[1][3]), 1, varglob.DeepGreen)
			p2scorepos = p2score.get_rect()
			p2scorepos[0] = varglob.fenetre.get_rect()[2]-p2scorepos[2]
			p2scorepos[1] = varglob.fenetre.get_rect()[0]+p2namepos[3] #left-longtext
			#p2lives = font.render("Balls: %s" %(varglob.players[1][5]), 1, varglob.DeepGreen)
			p2lives = font.render("   : %s" %(varglob.players[1][5]), 1, varglob.DeepGreen)
			p2livespos = p2lives.get_rect()
			p2livespos[0] = varglob.fenetre.get_rect()[2]-p2livespos[2]
			p2livespos[1] = varglob.fenetre.get_rect()[0]+p2namepos[3]+p2scorepos[3]
			#p2bullets = font.render("Bullets: %s" %(varglob.players[1][4]), 1, varglob.DeepGreen)
			p2bullets = font.render("   : %s" %(varglob.players[1][4]), 1, varglob.DeepGreen)
			p2bulletspos = p2bullets.get_rect()
			p2bulletspos[0] = varglob.fenetre.get_rect()[2]-p2bulletspos[2]
			p2bulletspos[1] = varglob.fenetre.get_rect()[0]+p2namepos[3]+p2scorepos[3]+p2livespos[3]
			try: # thread may lock bilt
				varglob.fenetre.blit(p2name, p2namepos)
				varglob.fenetre.blit(p2score, p2scorepos)
				varglob.fenetre.blit(p2lives, p2livespos)
				varglob.fenetre.blit(g_livesGreen, p2livespos)
				varglob.fenetre.blit(p2bullets, p2bulletspos)
				varglob.fenetre.blit(g_bulletGreen, p2bulletspos)
			except:
				pass
		
		# exist if angle != "free"
		if (varglob.players[2][2]!="free"):# or True:
			p3name = font.render("P3: %s" %(varglob.players[2][1]), 1, varglob.DeepBlue)
			p3namepos = p3name.get_rect()
			p3score = font.render("Score: %s" %(varglob.players[2][3]), 1, varglob.DeepBlue)
			p3scorepos = p3score.get_rect()
			#p3lives = font.render("Balls: %s" %(varglob.players[2][5]), 1, varglob.DeepBlue)
			p3lives = font.render("   : %s" %(varglob.players[2][5]), 1, varglob.DeepBlue)
			p3livespos = p3lives.get_rect()
			#p3bullets = font.render("Bullets: %s" %(varglob.players[2][4]), 1, varglob.DeepBlue)
			p3bullets = font.render("   : %s" %(varglob.players[2][4]), 1, varglob.DeepBlue)
			p3bulletspos = p3bullets.get_rect()

			p3bulletspos[1] = varglob.fenetre.get_rect()[2]-p3bulletspos[3]
			p3livespos[1] = varglob.fenetre.get_rect()[2]-p3bulletspos[3]-p3livespos[3]
			p3scorepos[1] = varglob.fenetre.get_rect()[2]-p3bulletspos[3]-p3livespos[3]-p3scorepos[3]
			p3namepos[1] = varglob.fenetre.get_rect()[2]-p3bulletspos[3]-p3livespos[3]-p3scorepos[3]-p3namepos[3] #both-hightext
			try: # thread may lock bilt
				varglob.fenetre.blit(p3bullets, p3bulletspos)
				varglob.fenetre.blit(g_bulletBlue, p3bulletspos)
				varglob.fenetre.blit(p3lives, p3livespos)
				varglob.fenetre.blit(g_livesBlue, p3livespos)
				varglob.fenetre.blit(p3score, p3scorepos)
				varglob.fenetre.blit(p3name, p3namepos)
			except:
				pass
		
		# exist if angle != "free"
		if (varglob.players[3][2]!="free"):# or True:
			p4name = font.render("P4: %s" %(varglob.players[3][1]), 1, varglob.DeepRed)
			p4namepos = p4name.get_rect()
			p4score = font.render("Score: %s" %(varglob.players[3][3]), 1, varglob.DeepRed)
			p4scorepos = p4score.get_rect()
			#p4lives = font.render("Balls: %s" %(varglob.players[3][5]), 1, varglob.DeepRed)
			p4lives = font.render("   : %s" %(varglob.players[3][5]), 1, varglob.DeepRed)
			p4livespos = p4lives.get_rect()
			#p4bullets = font.render("Bullets: %s" %(varglob.players[3][4]), 1, varglob.DeepRed)
			p4bullets = font.render("   : %s" %(varglob.players[3][4]), 1, varglob.DeepRed)
			p4bulletspos = p4bullets.get_rect()

			p4bulletspos[0] = varglob.fenetre.get_rect()[2]-p4bulletspos[2]
			p4bulletspos[1] = varglob.fenetre.get_rect()[2]-p4bulletspos[3]
			p4livespos[0] = varglob.fenetre.get_rect()[2]-p4livespos[2] #left-longtext
			p4livespos[1] = varglob.fenetre.get_rect()[2]-p4livespos[3]-p4bulletspos[3]
			p4scorepos[0] = varglob.fenetre.get_rect()[2]-p4scorepos[2] #left-longtext
			p4scorepos[1] = varglob.fenetre.get_rect()[3]-p4scorepos[3]-p4livespos[3]-p4bulletspos[3]
			p4namepos[0] = varglob.fenetre.get_rect()[2]-p4namepos[2] #left-longtext
			p4namepos[1] = varglob.fenetre.get_rect()[3]-p4namepos[3]-p4scorepos[3]-p4livespos[3]-p4bulletspos[3] #bot-hightext
			try: # thread may lock bilt
				varglob.fenetre.blit(p4bullets, p4bulletspos)
				varglob.fenetre.blit(g_bulletRed, p4bulletspos)
				varglob.fenetre.blit(p4lives, p4livespos)
				varglob.fenetre.blit(g_livesRed, p4livespos)
				varglob.fenetre.blit(p4score, p4scorepos)
				varglob.fenetre.blit(p4name, p4namepos)
			except:
				pass
		
		#Refresh
		pygame.display.flip()
		
		# end game when all players have not bullets nor balls
		endgame = True
		#for idx, player in enumerate(varglob.players): #
		if varglob.howplayers == 1: #in  one players, game finish with no ball nor bullet, or last level
			if (nbbricks == 0) and (varglob.levelNumber >= varglob.nb_levels):
				endgame = True
			else:
				for idx in xrange(0, 4):
					# exist if angle != "free"
					if (varglob.players[idx][2]!="free"):
						# player got bullets?
						if (varglob.players[idx][4]!=0):
							endgame = False
						# player got balls?
						if (varglob.players[idx][5]!=0):
							endgame = False
		
		if varglob.howplayers > 1: #in multiplayers, always have ball, game finish with level (only one level played)
			if nbbricks != 0:
				endgame = False
			a="""
			for idx in xrange(0, 4):
				# exist if angle != "free"
				if (is_serveur) and (varglob.players[idx][2]!="free"): #player angle
					# player got bullets?
					if (varglob.players[idx][4]!=0):
						endgame = False

				if (not is_serveur) and (varglob.players[idx][1]!="free"): #player name
					# player got bullets?
					if (varglob.players[idx][4]!=0):
						endgame = False
			a="""
		
		if endgame and continuer:
			#if S_applaudissement:
			#	S_applaudissement.play()
			p1name, p2name, p3name, p4name = "free", "free", "free", "free"
			p1score, p2score, p3score, p4score = 0, 0, 0, 0
			if varglob.players[0][2] != "free":
				p1name = varglob.players[0][1]
				p1score = varglob.players[0][3]
			if varglob.players[1][2] != "free":
				p2name = varglob.players[1][1]
				p2score = varglob.players[1][3]
			if varglob.players[2][2] != "free":
				p3name = varglob.players[2][1]
				p3score = varglob.players[2][3]
			if varglob.players[3][2] != "free":
				p4name = varglob.players[3][1]
				p4score = varglob.players[2][3]
			
			#WARNING: hiscore only available from single player (limited ball quantity)
			#HS.hiscores = [["Classic480","Gino","0","URANUS"], ["Classic480Fast","Delf","765","LUNA"]]
			if varglob.howplayers == 1: #update hiscores
				newhiscorelevelpack = True
				newhiscoreplayer = False
				for idx, checkscore in enumerate(HS.hiscores):
					if checkscore[0] == ParLevelPack:
						newhiscorelevelpack = False
						if p1score > eval(checkscore[2]):
							newhiscoreplayer = True
							HS.hiscores[idx][1] = varglob.players[0][1] #p1name
							HS.hiscores[idx][2] = str(p1score)
							HS.hiscores[idx][3] = varglob.levelName
				if newhiscorelevelpack:
					subscore = [ParLevelPack, varglob.players[0][1], str(p1score), varglob.levelName]
					HS.hiscores.append(subscore)
					newhiscoreplayer = True
				if newhiscoreplayer:
					HS.save_hiscores(HS.hiscores)
			
			hiscorename = "None"
			hiscore = "0"
			hiscorelevel = "None"
			for checkscore in HS.hiscores:
				if checkscore[0] == ParLevelPack:
					hiscorename = checkscore[1]
					hiscore = checkscore[2]
					hiscorelevel = checkscore[3]					

			msg_endgame = \
"""
      --- GAME END ---   

P1:%s : %s
P2:%s : %s
P3:%s : %s
P4:%s : %s

LevelPack: %s
HiScore: %s from: %s
in level: %s

 (SPACE OR ENTER TO RESUME)
""" \
			%(p1name, p1score, p2name, p2score, p3name, p3score, p4name, p4score, ParLevelPack, hiscore, hiscorename, hiscorelevel)

			msg_endgame = Reader(msg_endgame, pos=((varglob.fenetre_size[0]-300)/2,(varglob.fenetre_size[1]-250)/2), width=300, fontsize=16, height=250, bg=(200,200,200), fgcolor=(20,20,20))
			msg_endgame.show()
			
			# return to game
			while endgame:
				for event in pygame.event.get():    # waitting for events
					if (event.type == KEYDOWN):
						if (event.key == K_SPACE or event.key == K_RETURN):
							endgame = False
							
							#stop balls and missils for all players
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
								#th_E.sendMsg("T:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0))
								th_E.sendMsg("T:%s:%s:%s:%s:%s:%s:%s\n" %(idx, idx+1, 0, 0, 0, 0, varglob.players[idx][2]))

							#designer.level_blit(varglob.levelNumber)

							for idx in range(0, 4):
								varglob.players[idx][3] = 0 # score
								varglob.players[idx][4] = ParBulletQty
								varglob.players[idx][5] = ParLives
								if is_serveur:
									if varglob.players[idx][2] != "free":
										th_E.sendMsg("S%s:%s\n" %(idx, varglob.players[idx][3]))

			# exit endgame adding bullets
			for idx in xrange(0, 4):
				# Set amount balls
				varglob.players[idx][5] = ParLives
				if is_serveur:
					if varglob.players[idx][2] != "free":
						th_E.sendMsg("S%s:%s\n" %(idx, varglob.players[idx][3]))

			if is_serveur:
				designer.level_blit(varglob.levelNumber)
				# impose level to clients
				th_E.sendMsg("!L\n" )
				time.sleep(0.3)
			else:
				th_E.sendMsg("?L\n" )
				time.sleep(0.3)
	
############################################
	print ("shutting down PyBreak360...")
	music_stop()
	#FIXME: somes objects/Thread remain
	#th_E.sendMsg("FIN\n")
	#stop com balls and bullets
	#if is_serveur: #only if we was server.
	print ("stop balls and bullets communication...")
	for idx, ball in enumerate(varglob.balls):
		varglob.balls[idx][0].setth_E(0)
	for idx, bullet in enumerate(varglob.bullets):
		varglob.bullets[idx][0].setth_E(0)
	
	#Stop all threads th_E, th_R, serveur1 and th_serverClient's(x4)
	#priority for reception?
	try:
		th_E.sendMsg("FIN\n")	
		print ("th_E.sendMsg('D%s')\n" %(varglob.playerno))
		time.sleep(0.1) # secure to be done
	except:
		pass

	try:
		#th_E.stop()
		#print ("th_E.stop\n")
		time.sleep(0.1) # secure to be done
	except:
		pass

	try:
		th_R.stop()
		print ("th_R.stop\n")
		time.sleep(0.1) # secure to be done
	except:
		pass

	try:
		serveur1.stop()
		print ("serveur1.stop\n")
		time.sleep(0.1) # secure to be done
	except:
		pass

	try:
		# try a connexion for relaese thread
		connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connexion.connect((IPaddressLocal, IPport))
	except:
		pass
	
	#delete objects
	try:
		print ("del th_E")
		del th_E
	except:
		pass		
	try:
		print ("del th_R")
		del th_R
	except:
		pass
	try:
		print ("del serveur1")
		del serveur1
	except:
		pass		
	try:
		print ("del fenetre")
		varglob.fenetre.destroy()
		del varglob.fenetre
	except:
		pass

	print ("program end")
	time.sleep(0.2)
	pygame.quit()
	time.sleep(0.2)
	sys.exit()


if __name__ == '__main__':
	main()
