//objects.h: header file for CObject class

//Copyright Ian Parberry, 1999
//Last updated September 29, 1999

#ifndef __OBJECTS__
#define __OBJECTS__

#include "bsprite.h"


const int TIME_INVULNERABLE = 2500;

const int MARGIN=20; //margin on outside of page

//object types
enum ObjectType{GUNSHIP_OBJECT=0, DRONE_OBJECT, DART_OBJECT, BOSS_OBJECT, BULLET_OBJECT, ENEMY_BLASTER_OBJECT, BLASTER_OBJECT, EXPLOSION_OBJECT,STARFIRE_OBJECT, POWER_OBJECT, SHIELD_OBJECT, BONUS_OBJECT, X_OBJECT, NUM_SPRITES};
//note: NUM_SPRITES must be last

class CObject{ //class for a moving object
  protected:

	BOOL m_nNotDead;    
    int m_nLastXMoveTime; //last time moved horizontally
    int m_nLastYMoveTime; //last time moved vertically
    CBaseSprite *m_pSprite; //pointer to sprite
    int m_nMinXSpeed,m_nMaxXSpeed; //min, max horizontal speeds
    int m_nMinYSpeed,m_nMaxYSpeed; //min,max vertical speeds
    int m_nCurrentFrame; //frame to be displayed
    int m_nFrameCount; //number of frames in animation
    int m_nLastFrameTime; //last time the frame was changed
    int m_nFrameInterval; //interval between frames
    BOOL m_bForwardAnimation; //is animation going forwards?
	int m_bIsBoss;			//is this the Boss of the stage?

	ObjectType m_nType;
   
	BOOL m_bIsShot;		//whether or not it is a shot
	int m_nHitPoints;
	BOOL m_bIntelligent;
	int m_nShotPower;  //power of shots, 10000 for solid objects.
	int m_nXspeed,m_nYspeed; //current speed
	int m_nX,m_nY; //current location

  public:


    CObject(); //constructor
	CObject(ObjectType object,int x,int y,
      int xspeed,int yspeed); //create object 
	int getX(void);
	 int getY(void);
	 void fire(void);
	 virtual void kill(void);
	 void reduce(int amt);
	 void revive(void);
	 BOOL isDead(void);
	 ObjectType getType();
    void draw(LPDIRECTDRAWSURFACE surface); //draw
    
	void changedirection(int xdelta = 0, int ydelta = 0);
    void accelerate(int xdelta,int ydelta=0); //change speed
    virtual void move(); //make a move depending on time and speed

	friend class CObjectManager;

};

class CStarfire : public CObject {

private:
	int timeCreated;

public:
	CStarfire(ObjectType object,int x,int y,
      int xspeed,int yspeed); //create object



	virtual void move();
	BOOL isVulnerable();		//see if starfire is vulnerable
		void resetClock();			//reset time when starfire was created
};

class CExplosion : public CObject {

private:

	int timeCreated;
	int timeExpired;

	public:
		CExplosion();
		CExplosion(int x, int y, int time);
		void kill(void);

	friend class CObjectManager;
		

};

#endif
