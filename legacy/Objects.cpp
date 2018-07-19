//objects.cpp

//Copyright Ian Parberry, 1999
//Last updated October 10, 2000

#include "objects.h"
#include "timer.h" //game timer
#include "csprite.h" //for clipped sprite class
#include "sound.h"
#include "view.h"



extern CClippedSprite *g_pSprite[]; //sprites
extern CTimer Timer; //game timer
extern int g_nScreenWidth,g_nScreenHeight;
extern CSoundManager* SoundManager; //sound manager

extern CViewPoint Viewpoint; //player viewpoint
extern int CurrentLevel;

CObject::CObject(){ //constructor
  m_nX=m_nY=m_nXspeed=m_nYspeed=0;
  m_pSprite=NULL;
  m_nLastXMoveTime=m_nLastYMoveTime=0;
  m_nCurrentFrame=m_nFrameCount=m_nLastFrameTime=0;
  m_bForwardAnimation=TRUE;
  m_nFrameInterval=30;
  m_nNotDead = FALSE;
 
}

void CObject::draw(LPDIRECTDRAWSURFACE surface){ //draw
  //draw the current frame
  m_pSprite->draw(m_nCurrentFrame,m_nX,m_nY,surface);
  //figure out which frame is next
  int t=m_nFrameInterval/(1+abs(m_nXspeed)); //frame interval
  if(m_nFrameCount>1&&Timer.elapsed(m_nLastFrameTime,t)){
 	  ++m_nCurrentFrame;
	  m_nCurrentFrame %= m_nFrameCount;
  }
 
}

CObject::CObject(ObjectType object,int x,int y,
                     int xspeed,int yspeed){

m_nLastXMoveTime=m_nLastYMoveTime=Timer.time(); //time
  m_nX=x; m_nY=y; //location
  m_nXspeed=xspeed; m_nYspeed=yspeed; //speed
  m_pSprite=g_pSprite[object]; //sprite
  m_nFrameCount=m_pSprite->frame_count();//frame count
  m_nType = object;
  m_nNotDead = 1;		//hit points left, can be int or BOOL 	
  m_nHitPoints = 1;
  m_nShotPower = 200;	//amount of damage it does when it hits
  m_bIntelligent = FALSE;
  m_bIsShot = FALSE;
  m_bIsBoss = FALSE;
  
  //customize properties of each object type
  switch(object){
    case STARFIRE_OBJECT:
		
      m_nMinXSpeed=-4; m_nMaxXSpeed=4;
      m_nMinYSpeed=-5; m_nMaxYSpeed=3;
	  m_nNotDead = m_nHitPoints = 16;
	  m_nFrameInterval = 70;
      m_nShotPower = 10;
  
	  break;

	case GUNSHIP_OBJECT:
		m_nMinXSpeed=-2; m_nMaxXSpeed=2;
		m_nMinYSpeed=-2;	m_nMaxYSpeed=3;
		m_nNotDead = m_nHitPoints = 6;
		m_nFrameInterval = 70;
		break;
	
	case DRONE_OBJECT:
	    m_nMinXSpeed=-3; m_nMaxXSpeed=3;
		m_nMinYSpeed=1;	m_nMaxYSpeed=4;
		m_nNotDead = m_nHitPoints = 4;
		m_nFrameInterval = 100000;
		break;

	case DART_OBJECT:

		m_nMinXSpeed=-2; m_nMaxXSpeed=2;
		m_nMinYSpeed=2;	m_nMaxYSpeed=m_nYspeed = 9;
		m_nNotDead = m_nHitPoints = 4;
		m_nFrameInterval = 70;
		break;

	case BOSS_OBJECT:
		m_nMinXSpeed=-2; m_nMaxXSpeed=2;
		m_nMinYSpeed=-2;	m_nMaxYSpeed=3;
		m_nYspeed= 2;
		m_nNotDead = m_nHitPoints = 100 + 20* CurrentLevel;
		m_nFrameInterval = 700000;
		m_nShotPower = 2000;
		m_bIsBoss = TRUE;
		break;
	
	case BONUS_OBJECT:
	case X_OBJECT:

	case POWER_OBJECT:
	
		m_nShotPower = 0;
		m_nMinYSpeed=0;	m_nMaxYSpeed=2;
		m_nNotDead = FALSE;
		m_nHitPoints = 1;
		break;

	case SHIELD_OBJECT:

		m_nShotPower = -20;
		m_nMinYSpeed=0;	m_nMaxYSpeed=2;
		m_nNotDead = FALSE;
		m_nHitPoints = 1;

		break;


	case EXPLOSION_OBJECT:
      
	
		m_nNotDead = m_nHitPoints = 5;
		m_nFrameInterval = 70;
		break;

	case ENEMY_BLASTER_OBJECT:
	case BLASTER_OBJECT:
		
		m_bIsShot = TRUE;
		m_nNotDead = FALSE;
		m_nShotPower = 2;
		m_nMinYSpeed = -20; m_nMaxYSpeed = 4;
		break;

	case BULLET_OBJECT:
	
		m_bIsShot = TRUE;
		m_nNotDead = FALSE;
		m_nShotPower = 1;
		m_nMinXSpeed = -3; m_nMaxXSpeed = 3;
	
			m_nMinYSpeed = -1; m_nMaxYSpeed = 3;
		break;
  }
}
void CObject::changedirection(int xdelta,int ydelta){
  //change speed
  //horizontal
  m_nXspeed=xdelta;
  if(m_nXspeed<m_nMinXSpeed)m_nXspeed=m_nMinXSpeed;
  if(m_nXspeed>m_nMaxXSpeed)m_nXspeed=m_nMaxXSpeed;
  //vertical
  m_nYspeed=ydelta;
  if(m_nYspeed<m_nMinYSpeed)m_nYspeed=m_nMinYSpeed;
  if(m_nYspeed>m_nMaxYSpeed)m_nYspeed=m_nMaxYSpeed;
}
void CObject::accelerate(int xdelta,int ydelta){
  //change speed
  //horizontal
  m_nXspeed+=xdelta;
  if(m_nXspeed<m_nMinXSpeed)m_nXspeed=m_nMinXSpeed;
  if(m_nXspeed>m_nMaxXSpeed)m_nXspeed=m_nMaxXSpeed;
  //vertical
  m_nYspeed+=ydelta;
  if(m_nYspeed<m_nMinYSpeed)m_nYspeed=m_nMinYSpeed;
  if(m_nYspeed>m_nMaxYSpeed)m_nYspeed=m_nMaxYSpeed;
}
 int CObject::getY(){

	return m_nY;
}

 ObjectType CObject::getType(){

    return m_nType;
}

 void CObject::move(){  //move object
  const int XSCALE=8; //to scale back horizontal motion
  const int YSCALE=16; //to scale back vertical motion

  int xdelta,ydelta; //change in position
  int time=Timer.time(); //current time
  //horizontal motion
  int tfactor=time-m_nLastXMoveTime; //time since last move
  xdelta=(m_nXspeed*tfactor)/XSCALE; //x distance moved
  m_nX+=xdelta; //x motion
  if(m_nX<-MARGIN){
	  if(m_nType == BULLET_OBJECT) m_nNotDead = FALSE;
	  
	  m_nX=g_nScreenWidth+MARGIN; //wrap left
  }
  if(m_nX>g_nScreenWidth+MARGIN){
	  if(m_nType == BULLET_OBJECT) m_nNotDead = FALSE;
	 
	  m_nX=-MARGIN; //wrap right
  }
  if(xdelta||m_nXspeed==0) //record time of move
    m_nLastXMoveTime=time;
  //vertical motion
  tfactor=time-m_nLastYMoveTime; //time since last move
  ydelta=(m_nYspeed*tfactor)/YSCALE; //y distance moved
  m_nY+=ydelta; //y motion
  if(m_nY<-MARGIN){//m_nY=g_nScreenHeight+MARGIN; //wrap top
	if(m_nType == ENEMY_BLASTER_OBJECT  || m_nType == BLASTER_OBJECT || m_nType == BULLET_OBJECT)
        m_nNotDead = FALSE;
	m_nY = -MARGIN;
  }
  if(m_nY>g_nScreenHeight+MARGIN){
	  if(m_nType == ENEMY_BLASTER_OBJECT  || m_nType == BLASTER_OBJECT || m_nType == BULLET_OBJECT)
        m_nNotDead = FALSE;
   // m_nY=g_nScreenHeight+MARGIN; //wrap bottom
   m_nY = -MARGIN;
  }
  if(ydelta||m_nYspeed==0) //record time of move
    m_nLastYMoveTime=time;
}

void CObject::kill(){

 m_nNotDead = FALSE;

}

void CObject::reduce(int amt){

	if(m_nNotDead<=amt) m_nNotDead = 0;

	else m_nNotDead-=amt;

	if(m_nNotDead>m_nHitPoints) m_nNotDead = m_nHitPoints;
}
	

void CObject::revive(){

	m_nNotDead = m_nHitPoints;
}

int CObject::isDead(){

	if(m_nNotDead) return FALSE;
	return TRUE;
}



CStarfire::CStarfire(ObjectType object,int x,int y,
					 int xspeed,int yspeed) : CObject(object,x,y,xspeed,yspeed){

	timeCreated = Timer.time();
}

void CStarfire::move(){ //move object
  const int XSCALE=16; //to scale back horizontal motion
  const int YSCALE=8; //to scale back vertical motion
  const int MARGIN=10; //margin on outside of page
  int xdelta,ydelta; //change in position
  int time=Timer.time(); //current time
  //horizontal motion
  int tfactor=time-m_nLastXMoveTime; //time since last move
  xdelta=(m_nXspeed*tfactor)/XSCALE; //x distance moved
  m_nX+=xdelta; //x motion
  if(m_nX<-MARGIN)m_nX=-MARGIN; //no wrap left
  if(m_nX>g_nScreenWidth+MARGIN)m_nX=g_nScreenWidth+MARGIN; //no wrap right
  if(xdelta||m_nXspeed==0) //record time of move
    m_nLastXMoveTime=time;
  //vertical motion
  tfactor=time-m_nLastYMoveTime; //time since last move
  ydelta=(m_nYspeed*tfactor)/YSCALE; //y distance moved
  m_nY+=ydelta; //y motion
  if(m_nY<-MARGIN) {
	  

    m_nY=g_nScreenHeight+MARGIN;	 
	// m_nY=-MARGIN; //do not wrap bottom
  }
  if(m_nY>g_nScreenHeight+MARGIN){

    m_nY=g_nScreenHeight+MARGIN; //do not wrap 
  }
  if(ydelta||m_nYspeed==0) //record time of move
    m_nLastYMoveTime=time;
}

int CStarfire::isVulnerable(){

	if(Timer.time() - timeCreated < TIME_INVULNERABLE) return FALSE;
	
	return TRUE;

}

void CStarfire::resetClock(){

	timeCreated = Timer.time();
}

CExplosion::CExplosion() : CObject(){

}


CExplosion::CExplosion(int x, int y, int time) : CObject(EXPLOSION_OBJECT,x,y,0,0) {

	timeCreated = time;
	timeExpired = timeCreated + 4 * m_nFrameInterval;
		m_nCurrentFrame = 0;
}

void CExplosion::kill(){


	if(Timer.time() >= timeExpired){ 
		
		m_nNotDead = FALSE;
	
	}
}