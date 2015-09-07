#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import pygame

pygame.init()
pygame.display.set_mode((480,480)) #otherwise unlable to pygame.image.load()

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
		aera = image.get_rect()

	except pygame.error, message:
		print ("ERROR: Fail to load image: %s" %(fullname))
		raise SystemExit, message

	return image, aera

#Loading lives sprites
print ("Loading lives sprites")
g_livesYellow, g_livesYellowRect = load_png('livesyellow.png')
g_livesGreen, g_livesGreenRect = load_png('livesgreen.png')
g_livesBlue, g_livesBlueRect = load_png('livesblue.png')
g_livesRed, g_livesRedRect = load_png('livesred.png')

#Loading bricks
print ("Loading bricks")
HexaNone, HexaNoneRect = load_png('H_NONE.PNG')
HexaNoneCenter = HexaNoneRect.center
HexaYellow, HexaYellowRect = load_png('H_YELLOW.PNG')
HexaYellowCenter = HexaYellowRect.center
HexaGreen, HexaGreenRect = load_png('H_GREEN.PNG')
HexaGreenCenter = HexaGreenRect.center
HexaBlue, HexaBlueRect = load_png('H_BLUE.PNG')
HexaBlueCenter = HexaBlueRect.center
HexaRed, HexaRedRect = load_png('H_RED.PNG')
HexaRedCenter = HexaRedRect.center
HexaBrown, HexaBrownRect = load_png('H_BROWN.PNG')
HexaBrownCenter = HexaBrownRect.center
HexaGrey, HexaGreyRect = load_png('H_GREY.PNG')
HexaGreyCenter = HexaGreyRect.center
HexaBlack, HexaBlackRect = load_png('H_BLACK.PNG')
HexaBlackCenter = HexaBlackRect.center

#Loading bricks Bonus
print ("Loading bricks Bonus")
HexaLive, HexaLiveRect = load_png('H_BALLS.PNG')
HexaLiveCenter = HexaLiveRect.center
HexaBullets, HexaBulletsRect = load_png('H_BULLETS.PNG')
HexaBulletsCenter = HexaBulletsRect.center
HexaSpeed, HexaSpeedRect = load_png('H_BALLSPEED.PNG')
HexaSpeedCenter = HexaSpeedRect.center
HexaGlue, HexaGlueRect = load_png('H_GLUE.PNG')
HexaGlueCenter = HexaGlueRect.center
HexaBomb, HexaBombRect = load_png('H_BOMB.PNG')
HexaBombCenter = HexaBombRect.center
#106
HexaWall, HexaWallRect = load_png('H_WALL.PNG')
HexaWallCenter = HexaWallRect.center
HexaRand, HexaRandRect = load_png('H_RANDOM.PNG')
HexaRandCenter = HexaRandRect.center
HexaInvert, HexaInvertRect = load_png('H_INVERT.PNG')
HexaInvertCenter = HexaInvertRect.center
HexaReduce, HexaReduceRect = load_png('H_REDUCE.PNG')
HexaReduceCenter = HexaReduceRect.center
HexaEnlarge, HexaEnlargeRect = load_png('H_ENLARGE.PNG')
HexaEnlargeCenter = HexaEnlargeRect.center
#107 - designer
HexaNuclear, HexaNuclearRect = load_png('H_NUCLEAR.PNG')
HexaNuclearCenter = HexaNuclearRect.center
HexaBigBall, HexaBigBallRect = load_png('H_BIGBALL.PNG')
HexaBigBallCenter = HexaBigBallRect.center
HexaEmpty, HexaEmptyRect = load_png('H_EMPTY.PNG')
HexaEmptyCenter = HexaEmptyRect.center
HexaEmpty2, HexaEmpty2Rect = load_png('H_EMPTY2.PNG')
HexaEmpty2Center = HexaEmpty2Rect.center

#Loading balls
print ("Loading balls")
g_ballnone, g_ballnoneRect = load_png('ballNone.png')
g_ball1yellow, g_ball1yellowRect = load_png('ball1yellow.png')
g_ball2green, g_ball2greenRect = load_png('ball2green.png')
g_ball3blue, g_ball3blueRect = load_png('ball3blue.png')
g_ball4red, g_ball4redRect = load_png('ball4red.png')
g_ball1yellowdark, g_ball1yellowdarkRect = load_png('ball1yellowdark.png')
g_ball2greendark, g_ball2greendarkRect = load_png('ball2greendark.png')
g_ball3bluedark, g_ball3bluedarkRect = load_png('ball3bluedark.png')
g_ball4reddark, g_ball4reddarkRect = load_png('ball4reddark.png')
g_ballnuclear, g_ballnuclearRect = load_png('ballnuclear.png')
g_bigballnuclear, g_bigballnuclearRect = load_png('bigballnuclear.png')


BckGndWall, BckGndWallRect = load_png('WALL.PNG')
BckGndWall2 = pygame.transform.scale(BckGndWall, (480, 480))

BricksColor = [HexaNone, HexaYellow, HexaGreen, HexaBlue, HexaRed, HexaBrown, HexaGrey, HexaBlack, None, None, \
HexaLive, HexaBullets, HexaSpeed, HexaGlue, HexaBomb, HexaWall, HexaRand, HexaInvert, HexaReduce, HexaEnlarge, HexaNuclear, HexaBigBall, HexaEmpty, HexaEmpty2]

BricksRect = [HexaNoneRect, HexaYellowRect, HexaGreenRect, HexaBlueRect, HexaRedRect, HexaBrownRect, HexaGreyRect, HexaBlackRect, None, None, \
HexaLiveRect, HexaBulletsRect, HexaSpeedRect, HexaGlueRect, HexaBombRect, HexaWallRect, HexaRandRect, HexaInvertRect, HexaReduceRect, HexaEnlargeRect, HexaNuclearRect, HexaBigBallRect, HexaEmptyRect, HexaEmpty2Rect]

BricksCenter = [HexaNoneCenter, HexaYellowCenter, HexaGreenCenter, HexaBlueCenter, HexaRedCenter, HexaBrownCenter, HexaGreyCenter, HexaBlackCenter, None, None, \
HexaLiveCenter, HexaBulletsCenter, HexaSpeedCenter, HexaGlueCenter, HexaBombCenter, HexaWallCenter, HexaRandCenter, HexaInvertCenter, HexaReduceCenter, HexaEnlargeCenter, HexaNuclearCenter, HexaBigBallCenter, HexaEmptyCenter, HexaEmpty2Center]

print ("Loading playerbats")
g_bat_none2, g_bat_none2Rect = load_png('bat_none2.png')
g_bat_none3short, g_bat_none3shortRect = load_png('bat_none3.png')
g_bat_none4long, g_bat_none4longRect = load_png('bat_none4.png')

g_bat_yellow2, g_bat_yellow2Rect = load_png('bat_yellow2.png')
g_bat_yellow2light, g_bat_yellow2lightRect = load_png('bat_yellow2light.png')
g_bat_yellow2dark, g_bat_yellow2darkRect = load_png('bat_yellow2dark.png')
g_bat_yellow3short, g_bat_yellow3shortRect = load_png('bat_yellow3.png')
g_bat_yellow3shortlight, g_bat_yellow3shortlightRect = load_png('bat_yellow3light.png')
g_bat_yellow3shortdark, g_bat_yellow3shortdarkRect = load_png('bat_yellow3dark.png')
g_bat_yellow4long, g_bat_yellow4longRect = load_png('bat_yellow4.png')
g_bat_yellow4longlight, g_bat_yellow4longlightRect = load_png('bat_yellow4light.png')
g_bat_yellow4longdark, g_bat_yellow4longdarkRect = load_png('bat_yellow4dark.png')

g_bat_green2, g_bat_green2Rect = load_png('bat_green2.png')
g_bat_green2light, g_bat_green2lightRect = load_png('bat_green2light.png')
g_bat_green2dark, g_bat_green2darkRect = load_png('bat_green2dark.png')
g_bat_green3short, g_bat_green3shortRect = load_png('bat_green3.png')
g_bat_green3shortlight, g_bat_green3shortlightRect = load_png('bat_green3light.png')
g_bat_green3shortdark, g_bat_green3shortdarkRect = load_png('bat_green3dark.png')
g_bat_green4long, g_bat_green4longRect = load_png('bat_green4.png')
g_bat_green4longlight, g_bat_green4longlightRect = load_png('bat_green4light.png')
g_bat_green4longdark, g_bat_green4longdarkRect = load_png('bat_green4dark.png')

g_bat_blue2, g_bat_blue2Rect = load_png('bat_blue2.png')
g_bat_blue2light, g_bat_blue2lightRect = load_png('bat_blue2light.png')
g_bat_blue2dark, g_bat_blue2darkRect = load_png('bat_blue2dark.png')
g_bat_blue3short, g_bat_blue3shortRect = load_png('bat_blue3.png')
g_bat_blue3shortlight, g_bat_blue3shortlightRect = load_png('bat_blue3light.png')
g_bat_blue3shortdark, g_bat_blue3shortdarkRect = load_png('bat_blue3dark.png')
g_bat_blue4long, g_bat_blue4longRect = load_png('bat_blue4.png')
g_bat_blue4longlight, g_bat_blue4longlightRect = load_png('bat_blue4light.png')
g_bat_blue4longdark, g_bat_blue4longdarkRect = load_png('bat_blue4dark.png')

g_bat_red2, g_bat_red2Rect = load_png('bat_red2.png')
g_bat_red2light, g_bat_red2lightRect = load_png('bat_red2light.png')
g_bat_red2dark, g_bat_red2darkRect = load_png('bat_red2dark.png')
g_bat_red3short, g_bat_red3shortRect = load_png('bat_red3.png')
g_bat_red3shortlight, g_bat_red3shortlightRect = load_png('bat_red3light.png')
g_bat_red3shortdark, g_bat_red3shortdarkRect = load_png('bat_red3dark.png')
g_bat_red4long, g_bat_red4longRect = load_png('bat_red4.png')
g_bat_red4longlight, g_bat_red4longlightRect = load_png('bat_red4light.png')
g_bat_red4longdark, g_bat_red4longdarkRect = load_png('bat_red4dark.png')

#Loading bullets
print ("Loading bullets")
g_bulletNone, g_bulletNoneRect = load_png('bulletNone.png')
g_bulletNoneCenter = g_bulletNoneRect.center
g_bulletYellow, g_bulletYellowRect = load_png('bulletYellow.png')
g_bulletYellowCenter = g_bulletYellowRect.center
g_bulletGreen, g_bulletGreenRect = load_png('bulletGreen.png')
g_bulletGreenCenter = g_bulletGreenRect.center
g_bulletBlue, g_bulletBlueRect = load_png('bulletBlue.png')
g_bulletBlueCenter = g_bulletBlueRect.center
g_bulletRed, g_bulletRedRect = load_png('bulletRed.png')
g_bulletRedCenter = g_bulletRedRect.center
