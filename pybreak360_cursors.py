#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import pygame

#################################################
def load_png(name):
	"""Charge une image et retourne un objet image"""
	fullname = os.path.join('images', name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha is None:
			image = image.convert()
		else:
			image = image.convert_alpha()

	except pygame.error, message:
		print "Impossible de charger l'image : ", fullname
		raise SystemExit, message

	return image, image.get_rect()

g_livesYellow, toto = load_png('livesyellow.png')
g_livesGreen, toto = load_png('livesgreen.png')
g_livesBlue, toto = load_png('livesblue.png')
g_livesRed, toto = load_png('livesred.png')

#cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
#pygame.mouse.set_cursor(*pygame.cursors.arrow)

#the hand cursor
_HAND_CURSOR = (
"     XX         ",
"    X..X        ",
"    X..X        ",
"    X..X        ",
"    X..XXXXX    ",
"    X..X..X.XX  ",
" XX X..X..X.X.X ",
"X..XX.........X ",
"X...X.........X ",
" X.....X.X.X..X ",
"  X....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    X.......X   ",
"     X....X.X   ",
"     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)
#pygame.mouse.set_cursor(*HAND_CURSOR)

#the hand cursor
_WAIT_CURSOR = (
" XXXXXXXXXXXXXX ",
"  XX........XX  ",
"   X........X   ",
"   X........X   ",
"   XXX....XXX   ",
"    XXXXXXXX    ",
"      XXXX      ",
"       XX       ",
"      X..X      ",
"    X......X    ",
"   X........X   ",
"   X........X   ",
"   X...X....X   ",
"   X...X....X   ",
"  XX..XXX...XX  ",
" XXXXXXXXXXXXXX ")
_HCURS, _HMASK = pygame.cursors.compile(_WAIT_CURSOR, ".", "X")
WAIT_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)
#pygame.mouse.set_cursor(*WAIT_CURSOR)

#pygame.mouse.set_cursor(*pygame.cursors.arrow)
#pygame.mouse.set_cursor(*pygame.cursors.diamond)
#pygame.mouse.set_cursor(*pygame.cursors.ball)

