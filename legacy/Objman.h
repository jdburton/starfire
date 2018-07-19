//objman.h: header file for the object manager
//Copyright Ian Parberry, 1999
//Last updated September 29, 1999

#ifndef __OBJMAN__
#define __OBJMAN__

#include <windows.h>
#include <windowsx.h>
#include <ddraw.h>
#include <math.h>

#include "objects.h"
#include "ai.h"

const int STARFIRE_INDEX   = 0;
const int BLASTER_INDEX  = 1;
const int NUM_BLASTERS  = 15;
const int EBLASTER_INDEX = BLASTER_INDEX+NUM_BLASTERS;
const int NUM_EBLASTERS = 12;
const int NUM_BULLETS = 7;
const int BULLET_INDEX = EBLASTER_INDEX+NUM_EBLASTERS; 
const int POWER_INDEX = BULLET_INDEX+NUM_BULLETS;
const int SHIELD_INDEX = POWER_INDEX+1;
const int BONUS_INDEX = SHIELD_INDEX+1;
const int X_INDEX = BONUS_INDEX+1;
const int ENEMY_INDEX = X_INDEX+1;


const int ENEMY_TOTAL = 30;

const int DART_LEVEL = 1;
const int DRONE_LEVEL = 3;
const int GUNSHIP_LEVEL = 5;

enum GameMode{NORMAL_MODE = 0, BOSS_MODE};

class CObjectManager{
  private:
    CObject **m_pObjectList; //list of objects in game
 	CExplosion **m_pExplosionBuffer;
	int m_nPowerLevel;
	int m_nCount; //how many objects in list
    int m_nMaxCount; //maximum number of objects
    int m_nCurrentObject; //index of the current object
    int total_score;
	int first;		//so you don't accidentally delete the last item
	int num_enemies;		//number of enemies on screen
	int time_last_enemy;
	int enemy_delay;
	int total_enemies;		//total enemies in level
	GameMode m_nGameMode;

	void explode(int x, int y);
	void avoid(void);
	void blaster_attack(int time, int x, int y);
	int bullet_attack(int time, int x, int y);
	void boss_attack(int time, int x, int y);
	void addtoscore(ObjectType object);
    void accelerate(int xdelta,int ydelta=0); //change speed
	double distance(CObject * const first, CObject * const second);

  public:
	int lives_remaining;
	
    CObjectManager(int max); //constructor
    ~CObjectManager(); //destructor
    int create(ObjectType object,int x,int y,
      int xspeed,int yspeed); //create new object
	void refresh(int times);
	void initExplosions(void);
	void fire(int time);
	void powerup(void);
	void reset(int level);
	int won();

    //animate all objects
    void animate(LPDIRECTDRAWSURFACE surface);
    //the following functions operate on the current object
  
	void changedirection(int xdelta,int ydelta=0);
    void set_current(int index); //set current object
	BOOL collisiondetection();

    int speed(); //return magnitude of speed

};

#endif
