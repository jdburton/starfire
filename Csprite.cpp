//csprite.cpp: clipped sprite class functions

//Copyright Ian Parberry, 1999
//Last updated September 29, 1999

#include "csprite.h"

CClippedSprite::CClippedSprite(int frames,int w,int h):
CBaseSprite(frames,w,h){ //constructor
  //set bounding rectangle for use with Blt()
  m_rectSource.left=0; m_rectSource.right=w; 
  m_rectSource.top=0; m_rectSource.bottom=h; 
}

void CClippedSprite::draw(int frame,int x,int y,
                          LPDIRECTDRAWSURFACE dest){ //draw
  //compute destination rectangle
  RECT rectDest; //destination rectangle
  //horizontal extent
  rectDest.left=x-m_nWidth/2;
  rectDest.right=rectDest.left+m_nWidth;
  //vertical extent
  rectDest.top=y-m_nHeight+1;
  rectDest.bottom=y+1;
  //blit it
  dest->Blt(&rectDest,m_lpDDImage[frame],&m_rectSource,
    DDBLT_KEYSRC|DDBLT_WAIT,NULL);
}

