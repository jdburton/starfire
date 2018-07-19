//csprite.h
//header file for clipped sprite class

//Copyright Ian Parberry, 1999
//Last updated September 29, 1999

#include "bsprite.h"

#ifndef __csprite_h__
#define __csprite_h__

class CClippedSprite: public CBaseSprite{
  private:
    RECT m_rectSource; //bounding rectangle
  public:
    CClippedSprite(int frames,int w,int h); //constructor
    virtual void draw(int frame,int x,int y,
      LPDIRECTDRAWSURFACE destination); //draw sprite
};

#endif
