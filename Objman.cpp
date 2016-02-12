//objman.cpp: object manager class
//Copyright James Burton

#include "objman.h"
#include "Timer.h"
#include "sound.h"
#include "view.h" //for viewpoint class

#include <stdio.h>	//for sprintf


extern CRandom Random;
extern CViewPoint Viewpoint; //player viewpoint
extern CTimer Timer;
extern void PutText(const char* text,LPDIRECTDRAWSURFACE surface);
extern CSoundManager* SoundManager; //sound manager
extern int CurrentLevel;

CObjectManager::CObjectManager(int max){ //constructor
  
  m_nMaxCount=max;
  m_nCount=0; 
  m_nCurrentObject=0; 
  total_score = 0; 
  lives_remaining = 4;
  m_nPowerLevel = 1;
  first = TRUE;		//so you don't accidentally delete the last item

  int i;

  num_enemies = 0;
  total_enemies = ENEMY_TOTAL;
  time_last_enemy = 0;
  enemy_delay = 5000;
  m_nGameMode = NORMAL_MODE;
  m_pObjectList=new CObject*[max]; //object list

  for(i=0; i<m_nMaxCount; i++) //create objects
    m_pObjectList[i]=new CObject;

  m_pExplosionBuffer = new CExplosion*[max];	//buffer for explosions
  
  
  for(i = 0; i < m_nMaxCount/4; i++){


		m_pExplosionBuffer[i] =  new CExplosion;
	}
	

}
//================================================================
CObjectManager::~CObjectManager(){ //destructor
	for(int i=0; i<m_nMaxCount; i++){ //for each object
    delete m_pObjectList[i]; //delete it
	
	}
	for(int j = 0; j < m_nMaxCount/4; j++){
		delete m_pExplosionBuffer[i];
	}
	
	delete[] m_pExplosionBuffer;
  delete[]m_pObjectList; //delete object list
}

//==================================================================
void CObjectManager::initExplosions(){
	for(int j = 0; j < m_nMaxCount/4; j++){
		m_pExplosionBuffer[j] =  new CExplosion(0,0,0);

	}

}

//===========================================================

int CObjectManager::create(ObjectType object,int x,int y,
                           int xspeed,int yspeed){
  if(m_nCount<m_nMaxCount){ //if room, create object
	
	  switch(object){
		case GUNSHIP_OBJECT:
		
		  time_last_enemy = Timer.time();
		  total_enemies--;
		  num_enemies++;
		  m_pObjectList[m_nCount] = new CGunship(x,y);
	      break;
		
		case DRONE_OBJECT:
			time_last_enemy = Timer.time();
			total_enemies--;
			num_enemies++;
		  
			m_pObjectList[m_nCount] = new CDrone(x,y);
			break;
	      
		case DART_OBJECT:
			time_last_enemy = Timer.time();
			total_enemies--;
			num_enemies++;
		  
		  	m_pObjectList[m_nCount] = new CDart(x,y);
			break;

		case STARFIRE_OBJECT:
		    m_pObjectList[m_nCount] = new CStarfire(object,x,y,xspeed,yspeed); break;
	
		case BOSS_OBJECT:
			m_pObjectList[m_nCount] = new CBoss(x,y); break;

		default:
		      m_pObjectList[m_nCount] = 
      new CObject(object,x,y,xspeed,yspeed); break;
	  }
    return m_nCount++; //return index into object list
  }
  else return -1; //no room
}

//===================================================================================
void CObjectManager::explode(int x, int y){

	for(int i = 0; i < m_nMaxCount / 4; i++)
		if(m_pExplosionBuffer[i]->isDead()){
			m_pExplosionBuffer[i]->m_nX = x;
			m_pExplosionBuffer[i]->m_nY = y;
			m_pExplosionBuffer[i]->revive();
			m_pExplosionBuffer[i]->timeCreated = Timer.time();
			m_pExplosionBuffer[i]->timeExpired = Timer.time() + 4 * m_pExplosionBuffer[i]->m_nFrameInterval;
			m_pExplosionBuffer[i]->m_nCurrentFrame = 0;
			SoundManager->play(BOOM_SOUND);
			break;
		}


}
//==================================================================================

void CObjectManager::animate(LPDIRECTDRAWSURFACE surface){
  //move objects
	int dist;
	int i;
	for(i=0; i<m_nCount; i++){

		if(m_pObjectList[i]->m_bIntelligent){ //if intelligent
			if(!m_pObjectList[i]->isDead()){
		
			dist = static_cast<int>(distance(m_pObjectList[i],m_pObjectList[m_nCurrentObject]));
        //tell object about plane current position


			((CIntelligentObject*)m_pObjectList[i])->plane(
			m_pObjectList[m_nCurrentObject]->m_nX,
			m_pObjectList[m_nCurrentObject]->m_nY,
			dist);
    
			avoid();

			m_pObjectList[i]->move();

				if(/*abs(m_pObjectList[m_nCurrentObject]->m_nX-m_pObjectList[i]->m_nX) < 100 && */m_pObjectList[i]->getType() == GUNSHIP_OBJECT) 
					blaster_attack(Timer.time(),i,m_nCurrentObject);
			
				else if(bullet_attack(Timer.time(),i,m_nCurrentObject))
				
				if(m_pObjectList[i]->getType() == BOSS_OBJECT)
				boss_attack(Timer.time(),i,m_nCurrentObject);

			}//if not dead
	
		}//if intelligent
		else{
			m_pObjectList[i]->move();

		}
	}
  

  for(i=0; i<m_nCount; i++){
  
	  if(!m_pObjectList[i]->isDead()){
  
		  m_pObjectList[i]->draw(surface);
	  }
  }
  for(i = 0; i < m_nMaxCount /4; i++){
	  if(!m_pExplosionBuffer[i]->isDead())
		  m_pExplosionBuffer[i]->draw(surface);
  }

  char buffer[128];
	sprintf(buffer,"Lives %d   Shields %d%%\nLevel %d    Score %d\n",lives_remaining,((m_pObjectList[STARFIRE_INDEX]->m_nNotDead*100)/(m_pObjectList[STARFIRE_INDEX]->m_nHitPoints)),CurrentLevel+1,total_score);
  
	PutText(buffer,surface);
  
}

//===============================================================

void CObjectManager::accelerate(int xdelta,int ydelta){ 
  //change speed of current object
  m_pObjectList[m_nCurrentObject]->
    accelerate(xdelta,ydelta);
}

//================================================================

void CObjectManager::changedirection(int xdelta,int ydelta){ 
  //change speed of current object
  m_pObjectList[m_nCurrentObject]->
    changedirection(xdelta,ydelta);
}

//==================================================================

int CObjectManager::collisiondetection(){

    int result = FALSE;

	
	int i = STARFIRE_INDEX;  
	int j;



	if(static_cast<CStarfire*>(m_pObjectList[i])->isVulnerable()){


	for(j = EBLASTER_INDEX; j < m_nCount; j++){

		//if you hit something or something hit you
		if(!m_pObjectList[i]->isDead() && !m_pObjectList[j]->isDead()){	//if objects aren't dead

			if(distance(m_pObjectList[i],m_pObjectList[j]) < 40 + 40 * m_pObjectList[j]->m_bIsBoss){
				//each objects do damage to each other
				m_pObjectList[i]->reduce(m_pObjectList[j]->m_nShotPower);	
				m_pObjectList[j]->reduce(m_pObjectList[i]->m_nShotPower);
				

				ObjectType tempOT = m_pObjectList[j]->getType();

				//check to see if it's a bonus object

				//note:  SHIELD_OBJECTS have no special property.  They just do negative damage when hit.

				if(tempOT == POWER_OBJECT){
					if(m_nPowerLevel<3)
						m_nPowerLevel++;
				}

				else if(tempOT == BONUS_OBJECT)
					addtoscore(tempOT);

				else if(tempOT == X_OBJECT){

					//this kills all enemies on screen, except bosses.

					for(int k = ENEMY_INDEX; k < m_nCount; k++){

						if(!m_pObjectList[k]->isDead()){
						
							m_pObjectList[k]->reduce(10);
						
							if(m_pObjectList[k]->isDead()){			
									//if you killed it, it will blow up!
								m_nCurrentObject = k;
								addtoscore(m_pObjectList[k]->getType());
		
								explode(m_pObjectList[k]->m_nX,m_pObjectList[k]->m_nY);
								num_enemies--;
							}//end if you killed it
						}//end if it wasn't already dead

					}//next k
	

					return 1;
				}//end X_OBJECT
					
					
				else if(m_pObjectList[i]->isDead() && m_pObjectList[j]->isDead()){
					//if you hit an enemy and killed it.
					m_nPowerLevel = 1;
					lives_remaining--;
					
					if(m_pObjectList[j]->m_bIntelligent){				//if you collided with an enemy
						m_nCurrentObject = j;
						addtoscore(tempOT);
						num_enemies--;
					}
			
					    explode(m_pObjectList[i]->m_nX,m_pObjectList[i]->m_nY);
					if(lives_remaining >= 0)
						SoundManager->play(DYING_SOUND);
					else
						SoundManager->play(GAMEOVER_SOUND);
						
					result++;
	

				}//end if dead

				else if(m_pObjectList[i]->isDead()){
					//if you just got killed (usually for collisions with bosses)
					m_nPowerLevel = 1;
					lives_remaining--;
					
					explode(m_pObjectList[i]->m_nX,m_pObjectList[i]->m_nY);
					if(lives_remaining >= 0)
					SoundManager->play(DYING_SOUND);
					else
						SoundManager->play(GAMEOVER_SOUND);
						
				}
				else if(tempOT != SHIELD_OBJECT){
					SoundManager->play(HIT_SOUND); //object hitting ground
				}

			}//end if distance
		}//end if
	}//next j
	}//end if vulnerable

// see if your blasters hit anything

	for(i = 1; i < EBLASTER_INDEX; i++){		//for all blasters i
	
		for(j = ENEMY_INDEX; j < m_nCount; j++){  //for all enemies j
			if((!m_pObjectList[i]->isDead() && !m_pObjectList[j]->isDead())){ //if neither is dead
		
			if(distance(m_pObjectList[i],m_pObjectList[j]) < 40 +40 * m_pObjectList[j]->m_bIsBoss){
				//do damage to each other
				m_pObjectList[i]->reduce(m_pObjectList[j]->m_nShotPower);	
				m_pObjectList[j]->reduce(m_pObjectList[i]->m_nShotPower);
				
				if(m_pObjectList[i]->isDead() && m_pObjectList[j]->isDead()){
					//if your blaster took it out
					//if(m_pObjectList[j]->m_bIntelligent){				//if you collided with an enemy
						//if it was an enemy
						m_nCurrentObject = j;
						addtoscore(m_pObjectList[j]->getType());
						explode(m_pObjectList[j]->m_nX,m_pObjectList[j]->m_nY);
						num_enemies--;
					//}
					result++;


				}//end if dead
				else{
					SoundManager->play(EHIT_SOUND); //object hitting ground
				}

			}//end if distance
		  }//end if not dead


		}//next j
	}//next i

	return result;
}

//==================================================================================

void CObjectManager::avoid(){

	//try to keep enemy ships from hitting each other

	int i;
	int j;
	
	CIntelligentObject* E0;
	CIntelligentObject* E1;

	for(i = ENEMY_INDEX; i < m_nCount; i++){
		for(j = i+1; j < m_nCount; j++){

			E0 = dynamic_cast<CIntelligentObject*>(m_pObjectList[i]);
			E1 = dynamic_cast<CIntelligentObject*>(m_pObjectList[j]);

			if(E0 && E1){
			if(distance(m_pObjectList[i],m_pObjectList[j])<(50 + 40 * m_pObjectList[j]->m_bIsBoss) && !E0->isDead() && !E1->isDead()){
				if(m_pObjectList[i]->m_nX <= m_pObjectList[j]->m_nX){
					m_pObjectList[i]->m_nXspeed = m_pObjectList[i]->m_nMinXSpeed;
					m_pObjectList[j]->m_nXspeed = m_pObjectList[j]->m_nMaxXSpeed;
				}
				else{
					m_pObjectList[i]->m_nXspeed = m_pObjectList[i]->m_nMaxXSpeed;
					m_pObjectList[j]->m_nXspeed = m_pObjectList[j]->m_nMinXSpeed;
				}
				E0->m_nLastAiTime = Timer.time();
				E0->m_nAiDelayTime=300+Random.number(0,300);
      
				E1->m_nLastAiTime = Timer.time();
				E1->m_nAiDelayTime=300+Random.number(0,300);
      
			}
			}
		}
	}

}

//===========================================================================================

void CObjectManager::refresh(int times){


	if(lives_remaining >= 0){

		if(m_pObjectList[STARFIRE_INDEX]->isDead()){
	
			m_pObjectList[STARFIRE_INDEX]->m_nY = SCREEN_HEIGHT;
			m_pObjectList[STARFIRE_INDEX]->m_nX = SCREEN_WIDTH/2;
			m_pObjectList[STARFIRE_INDEX]->revive();
			static_cast<CStarfire*>(m_pObjectList[STARFIRE_INDEX])->resetClock();
		}
	}
	
	
		//****** put enemies back at top ******

	switch(m_nGameMode){	
		
	case NORMAL_MODE:

		if(total_enemies > 0){
			
			for(int i = ENEMY_INDEX; i < m_nCount; i++){
				
				ObjectType temp = m_pObjectList[i]->getType();  //You will need to know the ObjectType after you delete the object,
																//so you'd better get it now!

				

				if(m_pObjectList[i]->isDead() && Timer.elapsed(time_last_enemy,enemy_delay)){
						temp = static_cast<ObjectType>(Random.number(0,2));
					switch(temp){

						case GUNSHIP_OBJECT:
							time_last_enemy = Timer.time();
							total_enemies--;
							num_enemies++;
							m_pObjectList[i] = new CGunship(Random.number(100, SCREEN_WIDTH-100),0); break;
						case DRONE_OBJECT:
							
							time_last_enemy = Timer.time();
							total_enemies--;
							num_enemies++;
							m_pObjectList[i] = new CDrone(Random.number(100, SCREEN_WIDTH-100),0); break;
						
						case DART_OBJECT:
						    time_last_enemy = Timer.time();
						    total_enemies--;
							num_enemies++;
							m_pObjectList[i] = new CDart(Random.number(100, SCREEN_WIDTH-100),0); break;
						
					}
	    		enemy_delay = 1000 + Random.number(0,3000) - (250 * CurrentLevel);
				
				}//end if dead
				else if(Timer.elapsed(time_last_enemy,enemy_delay)){
				
						create(static_cast<ObjectType>(Random.number(0,2)),Random.number(100, SCREEN_WIDTH-100),0,0,3);
    			enemy_delay = 1000 + Random.number(0,3000) - (250 * CurrentLevel);

				}//end else if 
			}//next i
		}//end if total enemies
		
		else{

			m_nGameMode = BOSS_MODE;
			
			if(!create(BOSS_OBJECT,SCREEN_WIDTH/2,0,0,2)){
				m_pObjectList[m_nCount] = new CBoss(SCREEN_WIDTH/2,0);
			}

		}

		
//	case BOSS_MODE:
				
	}//end switch
				for(int j = 0; j < m_nMaxCount/4; j++)
					m_pExplosionBuffer[j]->kill();		//attempt to kill explosions
						

}

//=====================================================================================

void CObjectManager::fire(int time){


	static int lastfire = 0;

	if(time-lastfire< 350) return;
	SoundManager->play(BLASTER_SOUND);

	//fire center blaster
	if(m_nPowerLevel != 2){

		for(int i = 0; i < NUM_BLASTERS; i++){



	
			if(m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->isDead()){
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->m_nX = m_pObjectList[STARFIRE_INDEX]->m_nX;
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->m_nY = m_pObjectList[STARFIRE_INDEX]->m_nY-65;
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->changedirection(0,-4);
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->revive();
				
				break;
			}//end if
		}//next i
	}//end if


	int side = 0;

	//fire side blasters
	for(int j = 0; j < 2*(m_nPowerLevel/2); j++){
		for(int i = 0; i < NUM_BLASTERS; i++){

			if(m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->isDead()){
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->m_nX = m_pObjectList[STARFIRE_INDEX]->m_nX+(static_cast<int>(pow(-1,(side%2)))*31);
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->m_nY = m_pObjectList[STARFIRE_INDEX]->m_nY-40;
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->changedirection(0,-4);
				m_pObjectList[BLASTER_INDEX+(i % NUM_BLASTERS)]->revive();
				side++;     
				break;
			}//end if
		}//next i
	}//next j

	lastfire = time;

	

}

//==============================================================================================

void CObjectManager::boss_attack(int time, int enemy, int starfire){

	int i;


	CIntelligentObject * Enemy = dynamic_cast<CIntelligentObject*>(m_pObjectList[enemy]);

	if(Enemy){

	
	SoundManager->play(ELASER_SOUND);
	
	static int side = 0;
	for(int j = 0; j < 2; j++){
		for(i = 0; i < NUM_EBLASTERS; i++){


	
			if(m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->isDead()){
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->m_nX = m_pObjectList[enemy]->m_nX+(static_cast<int>(pow(-1,side))*35);
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->m_nY = m_pObjectList[enemy]->m_nY+30;
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->changedirection(0,6);
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->revive();
				side++;
				break;
			}//end if
		}//next i
	}//next j

    
//	Enemy->m_nLastFired = time;

	}//if enemy	

}

//=======================================================================================

void CObjectManager::blaster_attack(int time, int enemy, int starfire){

	int i;


	CIntelligentObject * Enemy = dynamic_cast<CIntelligentObject*>(m_pObjectList[enemy]);

	if(Enemy){

	if(time-Enemy->m_nLastFired < Random.number(1000,2000)) return;
	SoundManager->play(ELASER_SOUND);
	
	static int side = 0;
	for(int j = 0; j < 2; j++){
		for(i = 0; i < NUM_EBLASTERS; i++){


	
			if(m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->isDead()){
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->m_nX = m_pObjectList[enemy]->m_nX+(static_cast<int>(pow(-1,side))*27);
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->m_nY = m_pObjectList[enemy]->m_nY+35;
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->changedirection(0,6);
				m_pObjectList[EBLASTER_INDEX+(i % NUM_EBLASTERS)]->revive();
				side++;
				break;
			}//end if
		}//next i
	}//next j

	Enemy->m_nLastFired = time;

	}//if enemy	

}

//=========================================================================================

int CObjectManager::bullet_attack(int time, int enemy, int starfire){

	int i;

	CIntelligentObject * Enemy = dynamic_cast<CIntelligentObject*>(m_pObjectList[enemy]);


	//if it is an enemy
	if(Enemy){

	if(time-Enemy->m_nLastFired < Random.number(1000,2000)) return 0;
		
	for(i = 0; i < NUM_BULLETS; i++){
		if(m_pObjectList[BULLET_INDEX+(i % NUM_BULLETS)]->isDead()){
			m_pObjectList[BULLET_INDEX+(i % NUM_BULLETS)]->m_nX = Enemy->m_nX;//+(-1*(side%2)*32);
			m_pObjectList[BULLET_INDEX+(i % NUM_BULLETS)]->m_nY = Enemy->m_nY+20;
			m_pObjectList[BULLET_INDEX+(i % NUM_BULLETS)]->changedirection(static_cast<int>(3*(m_pObjectList[STARFIRE_INDEX]->m_nX - Enemy->m_nX)/distance(Enemy,m_pObjectList[STARFIRE_INDEX])),static_cast<int>(4*(m_pObjectList[STARFIRE_INDEX]->m_nY - Enemy->m_nY)/distance(Enemy,m_pObjectList[STARFIRE_INDEX])));
			m_pObjectList[BULLET_INDEX+(i % NUM_BULLETS)]->revive();
			break;
		}
	}
	
	Enemy->m_nLastFired = time;

	}

	return 1;

}

//===========================================================================================

double CObjectManager::distance(CObject * const first, CObject * const second){

   //Compensate for Starfire Sprite being off center// 
	
   if(first->getType()==STARFIRE_OBJECT) 
      return sqrt(static_cast<double>((first->m_nX-second->m_nX)*(first->m_nX-second->m_nX) + ((first->getY()-25)-second->getY())*((first->getY()-25)-second->getY())));

 
   return sqrt(static_cast<double>((first->m_nX-second->m_nX)*(first->m_nX-second->m_nX) + (first->getY()-second->getY())*(first->getY()-second->getY())));

}

//==============================================================================================

void CObjectManager::set_current(int index){
  //set current object
  if(index>=0&&index<m_nCount)m_nCurrentObject=index;
}

//=================================================================================================

int CObjectManager::speed(){ 
  //return magnitude of current object speed
  return abs(m_pObjectList[m_nCurrentObject]->m_nYspeed);

}

//======================================================================================

void CObjectManager::addtoscore(enum ObjectType object){

	static int mult = 1;

	switch(object){

	case GUNSHIP_OBJECT:

			total_score+=200;			// 400

	case DRONE_OBJECT:

			total_score += 100;			// 200		

	case DART_OBJECT:

			total_score += 100; break;

	case BOSS_OBJECT:
			
			explode(m_pObjectList[m_nCurrentObject]->m_nX+50,m_pObjectList[m_nCurrentObject]->m_nY+50);
			explode(m_pObjectList[m_nCurrentObject]->m_nX-50,m_pObjectList[m_nCurrentObject]->m_nY+50);
			explode(m_pObjectList[m_nCurrentObject]->m_nX+50,m_pObjectList[m_nCurrentObject]->m_nY-50);
			explode(m_pObjectList[m_nCurrentObject]->m_nX-50,m_pObjectList[m_nCurrentObject]->m_nY-50);
			
			total_score += 2000; break;

	case BONUS_OBJECT:

			total_score += (100 * Random.number(5,20)); break;

	default: break;
	
	}

	//check to see if you get another life (lives are at 10k + 10k(mult^2) points)
	if(total_score >= 10000 + 10000*mult*mult){
		lives_remaining++;
		mult++;
	}
	m_nCurrentObject = 0;
}

//=======================================================================================

void CObjectManager::powerup(){

	int i = Random.number(0,3);

	switch (i){

	case 0:
		if(m_pObjectList[SHIELD_INDEX]->isDead()){
			m_pObjectList[SHIELD_INDEX]->revive(); 
			m_pObjectList[SHIELD_INDEX]->accelerate(0,1);
			m_pObjectList[SHIELD_INDEX]->m_nX = SCREEN_WIDTH/2;
			m_pObjectList[SHIELD_INDEX]->m_nY = 0;
		}
		break;

	case 1:
		if(m_pObjectList[POWER_INDEX]->isDead()){
			m_pObjectList[POWER_INDEX]->revive(); 
			m_pObjectList[POWER_INDEX]->accelerate(0,1);
			m_pObjectList[POWER_INDEX]->m_nX = SCREEN_WIDTH/2;
			m_pObjectList[POWER_INDEX]->m_nY = 0; 
		}
		break;
	
	case 2:
		if(m_pObjectList[BONUS_INDEX]->isDead()){
			m_pObjectList[BONUS_INDEX]->revive(); 
			m_pObjectList[BONUS_INDEX]->accelerate(0,1);
			m_pObjectList[BONUS_INDEX]->m_nX = SCREEN_WIDTH/2;
			m_pObjectList[BONUS_INDEX]->m_nY = 0; 
		}
		break;
	case 3:
		//X objects do not appear during BOSS_MODE
		if(m_pObjectList[X_INDEX]->isDead() && m_nGameMode != BOSS_MODE){
			m_pObjectList[X_INDEX]->revive(); 
			m_pObjectList[X_INDEX]->accelerate(0,1);
			m_pObjectList[X_INDEX]->m_nX = SCREEN_WIDTH/2;
			m_pObjectList[X_INDEX]->m_nY = 0; 
		}
		break;
	}
}

//============================================================================================

int CObjectManager::won(){




	if(m_nGameMode == BOSS_MODE){		//if it's BOSS_MODE
	
		for(int i = ENEMY_INDEX; i < m_nCount; i++){

			if(!m_pObjectList[i]->isDead()) return 0;	//and all the enemies are dead
		}
		return 1;	//you won the level
	}

	return 0;


}

//================================================================================================

void CObjectManager::reset(int level){

	if(level == 0){

		//reset lives and total score
		lives_remaining = 4;
		total_score = 0;
		m_pObjectList[0]->revive();
		m_pObjectList[0]->m_nX = SCREEN_WIDTH/2;
	    m_pObjectList[0]->m_nY = SCREEN_HEIGHT;
		static_cast<CStarfire*>(m_pObjectList[STARFIRE_INDEX])->resetClock();
		
	
		//kill all the old bullets
		for(int i = 1; i < ENEMY_INDEX; i++)
			m_pObjectList[i]->kill();
	}

	//a good message of encouragement
	SoundManager->stop();
	SoundManager->play(BEGIN0_SOUND+Random.number(0,2));

	//the program can't see any of the old enemies now
	m_nCount = ENEMY_INDEX;

	//set total number of enemies
	total_enemies = ENEMY_TOTAL + 10 * level;
	num_enemies = 0;

	//restore the shields
	m_pObjectList[0]->m_nNotDead = m_pObjectList[0]->m_nHitPoints;

	//start off the level with some darts headed straight for you!
	for(int i  = 0; i < 3 + level; i++)
		create(DART_OBJECT,Random.number(100, SCREEN_WIDTH-100),0,0,7);

	//start the delay

	enemy_delay = 1000 + Random.number(0,3000);

	//set game mode back to normal
	m_nGameMode = NORMAL_MODE;

	
}
