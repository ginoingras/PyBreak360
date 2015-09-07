#!/usr/bin/env python
# -*- coding: utf8 -*-

import os

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
#file_path.replace(' ', '\\ ')
#file_path = file_path.dict['unicode']
#file_path = os.path.join("sounds", file_path)
print file_path
pygame.mixer.music.load(file_path)
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
