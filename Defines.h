
#ifndef __DEFINES_H__
#define __DEFINES_H__

const int SCREEN_WIDTH = 800; //pixels wide
const int SCREEN_HEIGHT = 600; //pixels high
const int COLOR_DEPTH = 16; //number of bits to store colors
#define TRANSPARENT_COLOR RGB(254,0,254) //transparent color

const int MOUSE_SCALE = 1;



enum GamePhaseType { LOGO_PHASE, TITLE_PHASE, MENU_PHASE, PLAYING_PHASE, GAMEOVER_PHASE, HELP_PHASE, ENEMY_PHASE };

#endif
