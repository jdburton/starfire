//sndlist.h: list of sound definitions

//Copyright Ian Parberry, 1999
//Last updated November 2, 1999

#ifndef __SNDLIST__
#define __SNDLIST__

#define LOOP_SOUND TRUE

enum GameSoundType{ //sounds used in game engine
  
  ENGINE_SOUND = 0, //sound of engine
  BLASTER_SOUND, //sound of gun firing
  BOOM_SOUND, //sound of explosion
  HIT_SOUND, //sound of hit on shields
  DYING_SOUND,
  EHIT_SOUND, 
  ELASER_SOUND,
  FLYBY_SOUND,
  BEGIN0_SOUND,
  BEGIN1_SOUND,
  BEGIN2_SOUND,
  GAMEOVER_SOUND,
  GAMEOVER1_SOUND


};

enum IntroSoundType{ //sounds used during the intro
  TITLE_SOUND=0, //sound used during title screen
  LOGO_SOUND, //signature chord
};

#endif
