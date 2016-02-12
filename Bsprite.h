//bsprite.h
//header file for base sprite class

//Copyright Ian Parberry, 1999
//Last updated October 10, 2000

#include <windows.h>
#include <windowsx.h>
#include <ddraw.h>
#include "bmp2.h"

#ifndef __BSPRITE__
#define __BSPRITE__

class CBaseSprite{ //simplest sprite
  protected:
    LPDIRECTDRAWSURFACE *m_lpDDImage; //sprite image
    int m_nFrameCount; //how many frames used in sprite
    int m_nWidth,m_nHeight; //dimensions of sprite images
    void CreateSurfaces(); //create surfaces
  public:
    CBaseSprite(int frames,int w,int h); //constructor
    ~CBaseSprite(); //destructor
    BOOL load(CBmpFileReader2 *image,int frame,
      int x,int y); //load sprite image
    virtual void draw(int frame,int x,int y,
      LPDIRECTDRAWSURFACE destination); //draw sprite
    void Release(); //release direct draw surfaces
    BOOL Restore(); //restore surfaces
    int frame_count(); //return number of frames
    int height(); //return height
    int width(); //return width
};

#endif
