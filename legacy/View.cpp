//view.cpp: viewpoint manager
//Copyright Ian Parberry, 1999
//Last updated October 5, 1999

#include "view.h"
#include "timer.h" //game timer

extern CTimer Timer; //game timer

CViewPoint::CViewPoint(){ //constructor
  m_nY=0; m_nBgOffset=0; m_nLastTimeBgDrawn=0;
}

void CViewPoint::set_position(int x){ //set current viewpoint
  normalize(x); m_nY=x;
}

int CViewPoint::screen(int x){ 
  //screen coords relative to viewpt
  int delta=x-m_nY;
  if(delta>WORLD_WIDTH/2)delta-=WORLD_WIDTH;
  if(delta<-WORLD_WIDTH/2)delta+=WORLD_WIDTH;
  return SCREEN_WIDTH/2+delta;
}

void CViewPoint::normalize(int &x){ //nomrmalize to world
  while(x<0)x+=WORLD_WIDTH;
  while(x>=WORLD_WIDTH)x-=WORLD_WIDTH;
}

void CViewPoint::draw_background(LPDIRECTDRAWSURFACE lpSource,
  LPDIRECTDRAWSURFACE lpDestination,int speed){
//draw scrolling background from surface lpSource to
//surface lpDestination
  //compute destination rectangle
  RECT rectDest; //destination rectangle
  rectDest.top=SCREEN_HEIGHT-m_nBgOffset; 
  rectDest.bottom=SCREEN_HEIGHT;
  rectDest.left=0; 
  rectDest.right=SCREEN_WIDTH; //vertical extent
  //compute source rectangle
  RECT rectSource; //source rectangle
  rectSource.top=0;
  rectSource.bottom=m_nBgOffset;
  rectSource.left=0; 
  rectSource.right=SCREEN_WIDTH;
  //draw left half of screen
  lpDestination->
    Blt(&rectDest,lpSource,&rectSource,DDBLT_WAIT,NULL);
  //compute destination rectangle
  rectDest.top=0;
  rectDest.bottom=SCREEN_HEIGHT-m_nBgOffset;
  rectDest.left=0; 
  rectDest.right=SCREEN_WIDTH;
  //compute source rectangle
  rectSource.top=m_nBgOffset; 
  rectSource.bottom=SCREEN_HEIGHT; 
  rectSource.left=0; 
  rectSource.right=SCREEN_WIDTH; 
  //draw right half of screen
  lpDestination->
    Blt(&rectDest,lpSource,&rectSource,DDBLT_WAIT,NULL); 
  //compute new offset
  int delta=(speed*(Timer.time()-m_nLastTimeBgDrawn))/50;
  if(delta){ //if nonzero
    m_nBgOffset-=delta; //initial offset
    if(m_nBgOffset>SCREEN_HEIGHT) //too positive
      m_nBgOffset=0;
    if(m_nBgOffset<0) //too negative
      m_nBgOffset=SCREEN_HEIGHT-1;
    m_nLastTimeBgDrawn=Timer.time(); //record time of move
  }
} //draw_background
