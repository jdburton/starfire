//ai.h: header file for intelligent object class

//Copyright Ian Parberry, 1999
//Last updated October 25, 1999

#ifndef __AI__
#define __AI__

enum StateType{CRUISING_STATE,AVOIDING_STATE};

#include "objects.h"
#include "random.h"

class CIntelligentObject: public CObject{ //abstract class for all intelligent objects
  protected:
    StateType m_eState; //state
    int m_nDesiredHeight; //desired altitude
    int m_nHeightTime; //time between height changes
    int m_nHeightDelayTime; //time to next height change
    int m_nSpeedVariationTime; //last time speed varied
    int m_nSpeedVariationDuration; //time to next speed vrn
    int m_nLastAiTime; //last time AI was used
    int m_nAiDelayTime; //time until AI next used
    int m_nDistance; //distance to plane
    int m_nVerticalDistance; //vertical distance from plane
    int m_nHorizontalDistance; //hor. distance from plane
    int m_nLastFired;

  
  public:
    CIntelligentObject(ObjectType object,int x,int y,
      int xspeed,int yspeed); //constructor
    virtual void move(); //move depending on time and speed
    void plane(int x,int y,int d); //relationship w/plane
	virtual void ai() = 0; //artificial intelligence
    
	friend class CObjectManager;
};


//individual classes of enemies:  Each ai() function is different

class CGunship : public CIntelligentObject {



public:

	CGunship(int x, int y);
	void ai();
};

class CDrone : public CIntelligentObject {



public:

	CDrone(int x, int y);
	void ai();
};


class CDart : public CIntelligentObject {

private:

	int passed;			//has it passed the starfire

public:

	CDart(int x, int y);
	void ai();
};

class CBoss : public CIntelligentObject {

public:

	CBoss(int x, int y);
	void ai();

};



#endif
