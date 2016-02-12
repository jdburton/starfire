//view.h: header file for viewpoint manager
//Copyright Ian Parberry, 1999
//Last updated October 5, 1999

#ifndef __VIEWPOINT__
#define __VIEWPOINT__

#include <windows.h>
#include <windowsx.h>
#include <ddraw.h>

#include "defines.h"

const int WORLD_WIDTH = 1280; //width of the world

class CViewPoint{
  private:
    int m_nY; //x coordinate of viewpoint
    int m_nBgOffset; //offset of parallax scrolled background
    int m_nLastTimeBgDrawn; //last time background was drawn
  public:
    CViewPoint(); //constructor
    void set_position(int x); //set current viewpoint
    int screen(int x); //screen coords relative to viewpt
    void normalize(int &x); //normalize location x
    void draw_background(LPDIRECTDRAWSURFACE lpSource,
      LPDIRECTDRAWSURFACE lpDestination,int speed);
};

#endif
