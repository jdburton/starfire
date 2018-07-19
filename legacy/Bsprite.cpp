//bsprite.cpp: base sprite class functions

//Copyright Ian Parberry, 1999
//Last updated October 10, 2000

#include <string.h> //for memcpy
#include "defines.h"
#include "bsprite.h"

extern LPDIRECTDRAW lpDirectDrawObject; //direct draw object
extern DWORD g_dwTransparentColor;

CBaseSprite::CBaseSprite(int frames,int width,int height){
  //settings
  m_nWidth=width; m_nHeight=height; //width and height
  m_nFrameCount=frames; //assign number of frames
  //create space for sprite surface pointers
  m_lpDDImage=new LPDIRECTDRAWSURFACE[frames];
  for(int i=0; i<frames; i++)m_lpDDImage[i]=NULL;
  //create surfaces for sprite images
  CreateSurfaces();
}

CBaseSprite::~CBaseSprite(){ //destructor
  //deallocate memory allocated in constructor
  delete[]m_lpDDImage;
}

void CBaseSprite::CreateSurfaces(){ //create surfaces
  //set parameters of surface to be created
  DDSURFACEDESC ddsd; //direct draw surface descriptor
  ddsd.dwSize=sizeof(ddsd); //required field
  ddsd.dwFlags=DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH; //attributes
  ddsd.ddsCaps.dwCaps=DDSCAPS_OFFSCREENPLAIN; //offscreen
  ddsd.dwHeight=m_nHeight; //sprite height
  ddsd.dwWidth=m_nWidth; //sprite width
  //set the transparent color
  DDCOLORKEY ddck; //direct draw color descriptor
  ddck.dwColorSpaceLowValue=
    ddck.dwColorSpaceHighValue=g_dwTransparentColor;
  //create surfaces
  for(int i=0; i<m_nFrameCount; i++){ //for each frame
    //create surface
    if(FAILED(lpDirectDrawObject->
    CreateSurface(&ddsd,&(m_lpDDImage[i]),NULL)))
      m_lpDDImage[i]=NULL;
    //set the transparent color
    m_lpDDImage[i]->SetColorKey(DDCKEY_SRCBLT,&ddck);
  }
}

void CBaseSprite::Release(){ //release all sprite surfaces
  for(int i=0; i<m_nFrameCount; i++) //for each frame
    if(m_lpDDImage[i]!=NULL) //if it is really there
      m_lpDDImage[i]->Release(); //release it
}

BOOL CBaseSprite::load(CBmpFileReader2 *buffer,
                       int frame,int x,int y){
//grab sprite image from (x,y) in *buffer
//and store in m_lpDDImage[frame]
  return buffer->draw(m_lpDDImage[frame],
    m_nWidth,m_nHeight,x,y);
}

void CBaseSprite::draw(int frame,int x,int y,
                       LPDIRECTDRAWSURFACE dest){
  dest->BltFast(x-m_nWidth/2,y-m_nHeight,m_lpDDImage[frame],
    NULL,DDBLTFAST_SRCCOLORKEY|DDBLTFAST_WAIT);
}

BOOL CBaseSprite::Restore(){ //restore surfaces
  BOOL result=TRUE; //return TRUE if all surfaces restored OK
  for(int i=0; i<m_nFrameCount; i++) //for each frame
    if(m_lpDDImage[i]) //if it exists
      result=result&&
        SUCCEEDED(m_lpDDImage[i]->Restore()); //restore it
  return result;
}

//reader functions

int CBaseSprite::frame_count(){ //return number of frames
  return m_nFrameCount; 
}

int CBaseSprite::height(){ //return height
  return m_nHeight;
}

int CBaseSprite::width(){ //return width
  return m_nWidth;
}
