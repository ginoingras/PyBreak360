#!/usr/bin/env python
# -*- coding: utf8 -*-

"""#https://www.python.org/dev/peps/pep-0263/
# -*- coding: cp1252 -*-
# -*- coding: cp852 -*-
# -*- coding: cp437 -*-
# -*- coding: ascii -*-
# -*- coding: iso-8859-15 -*-
# -*- coding: utf8 -*-
# -*- coding: latin-1 -*-
"""

#from __future__ import unicode_literals
#from __future__ import unicode_literals

import os

from codecs import open

import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((408,408))
screen.fill((255,255,255))#remplissage en blanc
continuer=1
#pour utiliser la police broadway
font=pygame.font.SysFont("broadway", 24, bold=False, italic=False)
#dans un jeu, on veut par exemple récupérer le nom du joueur
nom="NOM :"
text=font.render(nom,1,(220,0,80))#crée un objet pour la chaine nom
screen.blit(text,(30,30))

pygame.init()
pygame.mixer.set_num_channels(3)
pygame.mixer.init()

file_path = "07-Boabdil, Bulerías.ogg"
print file_path
file_path = file_path.decode('utf8')
#print file_path
#file_path = file_path.encode('cp437')
#file_path = file_path.encode('utf8')
#print file_path
#file_path = os.path.join("", file_path)
#print file_path
#file_path = """%s""" %(file_path)
#print file_path
#file_path = file_path.replace(' ', '\\ ')
#print file_path

pygame.mixer.music.load(open(file_path))
pygame.mixer.music.play(1)
pygame.mixer.music.set_volume(0.5)

while continuer:

	for event in pygame.event.get():
		if event.type==QUIT:#pour quitter
			continuer=0
		elif event.type==KEYDOWN:
			carac= event.dict['unicode']
#récupère le caractère grâce à son unicode
#attention normalement le clavier de pygame est en qwerty, donc si on écrit
#(pygame.key.name(event.key) et que l'on a tapé a on a q et w donne z (et inv)
			nom =nom+ carac

			text=font.render(nom,1,(220,0,80))
			screen.blit(text,(30,30))
		else:
			continue
	pygame.display.flip()

pygame.quit()
