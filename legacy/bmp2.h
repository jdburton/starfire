//bmp2.h: header file for the bmp file reader, high color
//Copyright Ian Parberry, 2000
//Last modified October 10, 2000

#include <windows.h>
#include <windowsx.h>
#include <ddraw.h>

#include "defines.h"

#ifndef __bmp2_h__
#define __bmp2_h__

class CBmpFileReader2{ //bmp file input class
protected:
  HBITMAP m_hBitmap; //bitmap
  int m_nFileWidth,m_nFileHeight; //file height and width
public:
  CBmpFileReader2(); //constructor
  ~CBmpFileReader2(); //destructor
  BOOL draw(LPDIRECTDRAWSURFACE surface); //draw image
  BOOL draw(LPDIRECTDRAWSURFACE surface,int w,int h,
    int x,int y); //draw image
  BOOL draw(LPDIRECTDRAWSURFACE surface,int w1,int h1,
    int w2,int h2,int x,int y); //draw image
  BOOL load(char *filename); //load from file
};

#endif
