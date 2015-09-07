#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, pygame

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.set_num_channels(4)
pygame.mixer.init()

#################################################
def sound_play(song, volume=50):
	"""play a sound Freq, Vol"""

	sound = False
	#if ParMusicYN:
	if True:
		#path = os.path.join("sounds", song + ".ogg")
		path = os.path.join("sounds", song)
		sound = pygame.mixer.Sound(path)  #load sound
		#sound.play()
		sound.set_volume(volume)

	return sound
	#for sound effects: 
	#Sound.play(loops=0, maxtime=0, fade_ms=0): return Channel
	#jump.play() # play the jump sound effect once

#Loading sounds

#S_coeurbattements = sound_play("coeurbattements3.ogg")
#S_cornebrume = sound_play("cornebrume2.ogg")
S_applaudissement = sound_play("Applaudissement3.ogg")
S_gong = sound_play("gong2.ogg")
#S_trompette = sound_play("beep5b.ogg")
S_HitBrick = sound_play("beep5b.ogg")
S_missil = sound_play("missil3.ogg")
S_bomb = sound_play("bomb2.ogg")
#S_beep9 = sound_play("beep9.ogg")
S_BallLose = sound_play("beep9.ogg")
#S_beep1 = sound_play("beep1.ogg")
S_glassbreak = sound_play("glassbreak.ogg")
