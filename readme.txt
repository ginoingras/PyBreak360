pybreak360, an arkanoid breakout multi player network game at 360!
------------------------------------------------------------------
press SPACE or ENTER for menu
-----------------------------
intermediates beta releases are Vx.y.1-9-a-z
stables releases are Vx.y.0
---------------------------

V1.0.7rc2
fix NuclearBall doesn't displayed over network multiplayer
modify BrickBombBonus to generate other BrickBombBonus in contact for explode too.

V1.0.7rc1
fix V1.0.6rc1 bug multiplayers reception message ball idx.
fix update ParBallSpeedSlow, ParBallSpeedFast, when change levelpack.
adjust blit level brick array, better centered.
add NuclearBall brick bonus, timed 10 Sec.
add BigBall brick bonus, timed 7 sec (ball sprite size x 2).
add level editor (FINALLY !!! very convinient to modify levels!). press D in game for level designer.
modify levelpacks Classic480 & 640 gameplay.
extract Brick class as pybreak360_bricks.py
clean code in progress...

V1.0.6rc1
add python module netifaces-0.10.4, get local ip from severals methods.
check all network available interfaces for server, allow user to set it manually, saved in pybreak360.cfg.
restart server when change local ip from menu F11 (Warning: may need to save and restart game).
enable game if no network found as localhost/127.0.0.1.
add international special keyboard map in pybreak360_kbd.py (edit to modify default), default keyboard parameter in pybreak360.cfg as [ParKeybi18n]
add wall brick bonus, timed 7 Sec.
add InvertCommand brick bonus, timed 5 Sec. Warning: not enabled if ParAllowMulti360 = False, nor with bootBat
add reduce/enlarge bat brick bonus, timed 10 Sec.
add timming 10 Sec speed brick bonus.
show random bricks as random brick sprites in level (have to shoot to set the random brick 0-6)
extract modules cursors, sounds, sprites, config_Parameters.

V1.0.5rc1
fix connect distant server and turn back reconnect local fail
fix when serveur disconnect, when serveur not found, or don't allow connexion
fix disconnect from server lock thread cause connexion locked...
fix glue bonus for porteurOrigin ball
fix send time lose penatily to clients
fix start and end game, display final score, check synchonus with multiplayers clients.
prior to display top level client's bat and ball.
agglomerate levels packs as Classic480, Classic480Fast & Classic640 done.
translate comments in code to be completly english, in progress.
hi-scores saved in pybreak360.hiscores. for single player only (cause limited ball quantity). shown end game for level, or press "H" to see High scores.

V1.0.4
add bot engine bat (one which act as player, low AI but enought, almost only following his ball, touch 'B' as Boot to start/stop).
add mode 360 degrees for all players (in pybreak360.cfg), send ParAllowMulti360 to clients, ball is catched prior to his owner.
modify menu keyboard input name & IP, as unicode.
design sprite ball and bullet instead of text quantity
change menu/F3 SCREEN SIZE (is levelParameter), for ALL PLAYERS 360 allow movement.
add ParKeybUnicode in pybreak360.cfg
add 1 seconds to relaunch ball, 3 seconds penality for multiplayers
agglomerate levels packs as Classic480, Classic480Fast, Classic640, in progress.

V1.0.3
add 4 new levels in ClassicText, change some others.
show level pack name in title screen.
change font brick score size, add constrast in brick show score and info's level.
add screen size in level parameter.
server send level with screen size, and own FPS to clients.
fix brick count fail in main loop changing from thread server -> client recive.
fix bug when player lose/get ball and have 0 ball
multiplayers allways have ball, game finish with no bricks nor bullets.
change name(F2) without need to exit game

V1.0.2
add sound when hit bomb, change sound (glassbreak) when bullet hit bat and score+/-10.
fix display end game windows freeze
fix synchro ball count when bat catch ball server -> client.
fix client porteur ball back when ball/bullet hit glue brick bonus

V1.0.1
fix shutdown Thread-locking-connection remain when game ended.
increase score of value brick, display +1+6 inside brick in color's player
fix bug lose ball around 0°

V1.0.0
initial release, alpha...
