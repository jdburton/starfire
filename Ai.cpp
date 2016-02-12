//ai.cpp: artificial intelligence



#include "ai.h"
#include "timer.h" //game timer
#include "random.h" //for random number generator
#include "view.h" //for viewpoint manager
#include <math.h>
#include "sound.h"

extern CTimer Timer;  //game timer
extern CRandom Random; //random number generator
extern CSoundManager * SoundManager;  //sound manager

const int CLOSE_DISTANCE=200; //close to plane
const int FAR_DISTANCE=300; //far from plane

//fall back at this vertical distance from plane
const int FALLBACK_DISTANCE=10; 

//horizontal distance considered to be behind plane
const int BEHIND_DISTANCE=-5; 

CIntelligentObject::CIntelligentObject(ObjectType object,
  int x,int y,int xspeed,int yspeed):
CObject(object,x,y,xspeed,yspeed){ //constructor
  m_bIntelligent=TRUE;
  m_nDesiredHeight=240; 
  m_nHeightTime=0;  m_nHeightDelayTime=0;
  m_nSpeedVariationTime=m_nSpeedVariationDuration=0;
  m_nDistance=m_nHorizontalDistance=m_nVerticalDistance=0;
  m_eState=CRUISING_STATE;
  m_nLastAiTime=0; m_nAiDelayTime=0;
  m_nLastFired = 0;
}

void CIntelligentObject::move(){ //move object
  CObject::move(); //move like a dumb object
  ai(); //act intelligently
}

void CIntelligentObject::plane(int x, int y,int d){ 
//compute relationship with plane
  //distances from plane
  m_nDistance=d;
  m_nVerticalDistance=m_nY-y;
  m_nHorizontalDistance=m_nX-x;

  if(m_nType == DART_OBJECT)
	  m_nDesiredHeight = x;
}

CGunship::CGunship(int x, int y) : CIntelligentObject(GUNSHIP_OBJECT,x,y,0,2){


}

void CGunship::ai(){

	if(!Timer.elapsed(m_nLastAiTime,m_nAiDelayTime)) return;

	//you have m_nDistance, m_nVerticalDistance, & m_nHorizontalDistance from plane()

	if(m_nVerticalDistance < 0) {		//if above the plane

		if(abs(m_nHorizontalDistance)<50){		//if too close

			m_nXspeed = (m_nHorizontalDistance < 0)? m_nMinXSpeed : m_nMaxXSpeed;  //get away asap!
		}
		else if(abs(m_nHorizontalDistance > 200)){  //if too far

			m_nXspeed = (m_nHorizontalDistance < 0)? m_nMaxXSpeed : m_nMinXSpeed;	//attack!
		}

		else{																		//if in between

			m_nXspeed = Random.number(m_nMinXSpeed,m_nMaxXSpeed);					//move randomly
		}

	}
		

		if(m_nY < 200)	m_nYspeed = Random.number(1,m_nMaxYSpeed);

		else{
			do{

				m_nYspeed = Random.number(m_nMinYSpeed,m_nMaxYSpeed);

			}while(m_nYspeed == 0);
		}
		m_nAiDelayTime = (m_nYspeed > 0)? 500 + Random.number(0,500) :  1000 + Random.number(0,1000);
}


CDrone::CDrone(int x, int y) : CIntelligentObject(DRONE_OBJECT,x,y,0,3){


}

void CDrone::ai(){

	if(!Timer.elapsed(m_nLastAiTime,m_nAiDelayTime)) return;

	//you have m_nDistance, m_nVerticalDistance, & m_nHorizontalDistance from plane()

	if(m_nVerticalDistance < 0) {		//if above the plane

		if(abs(m_nHorizontalDistance)<50){		//if too close

			m_nXspeed = (m_nHorizontalDistance < 0)? Random.number(-1,m_nMinXSpeed) : Random.number(1,m_nMaxXSpeed);  //get away asap!
		}
		else if(abs(m_nHorizontalDistance > 200)){  //if too far

			do{
			m_nXspeed = (m_nHorizontalDistance < 0)? m_nMaxXSpeed : m_nMinXSpeed;	//attack!
			}while(m_nXspeed == 0);
		}

		else{																		//if in between

			m_nXspeed = Random.number(m_nMinXSpeed,m_nMaxXSpeed);					//move randomly
		}

	}
		
			

				m_nYspeed = Random.number(m_nMinYSpeed,m_nMaxYSpeed);

		
		m_nAiDelayTime = 500 + Random.number(0,500) ;
}

CDart::CDart(int x, int y) : CIntelligentObject(DART_OBJECT,x,y,0,7){

	passed = 0; 

}

void CDart::ai(){

	

	if(!Timer.elapsed(m_nLastAiTime,m_nAiDelayTime)) return;
	

	if(m_nVerticalDistance < 0){
		m_nXspeed = (m_nHorizontalDistance < 0)? m_nMaxXSpeed : m_nMinXSpeed;
		passed = 0;
	}
	else{
		if(passed = 0){
			SoundManager->play(FLYBY_SOUND);
			passed = 1;
		}
		m_nXspeed = (m_nHorizontalDistance < 0)? -1 : 1;

	}

	m_nAiDelayTime = 500 + Random.number(0,1000);
}

CBoss::CBoss(int x, int y) : CIntelligentObject(BOSS_OBJECT,x,y,0,1){


	m_nAiDelayTime = 3500;
	m_nLastAiTime = Timer.time();
}

void CBoss::ai(){

	//if(!Timer.elapsed(m_nLastAiTime,m_nAiDelayTime)) return;

	if(abs(m_nHorizontalDistance) < 70 && m_nY < SCREEN_HEIGHT/2){ m_nYspeed = m_nMaxYSpeed; m_nXspeed = 0;}
		else{
	if(m_nX < 150) m_nXspeed = Random.number(1,m_nMaxXSpeed);
	if(m_nX > SCREEN_HEIGHT-150) m_nXspeed = Random.number(m_nMinXSpeed,-1);
	}
	if(m_nY < 50) m_nYspeed = Random.number(1,m_nMaxYSpeed);
	if(m_nY > SCREEN_HEIGHT-100){
		m_nYspeed = Random.number(m_nMinYSpeed,-1);
		do{
		m_nXspeed = Random.number(m_nMinXSpeed,m_nMaxXSpeed);		//make sure Xspeed is non zero;
		}while(m_nXspeed == 0);
	}

}