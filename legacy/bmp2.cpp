//bmp2.cpp: member functions for the bmp file reader, high color

//Copyright Ian Parberry, 2000
//Last updated October 10, 2000

#include "bmp2.h" //header file
#include "defines.h" //defines

extern int g_nScreenWidth,g_nScreenHeight;

//constructors and destructors

CBmpFileReader2::CBmpFileReader2(){ //constructor
  m_hBitmap=NULL; m_nFileWidth=m_nFileHeight=0;
}

CBmpFileReader2::~CBmpFileReader2(){ //destructor
  if(m_hBitmap)DeleteObject(m_hBitmap);
}

//member functions

BOOL CBmpFileReader2::draw(LPDIRECTDRAWSURFACE surface){ 
//draw whole image scaled from (0,0) to screen-sized surface
  return draw(surface,g_nScreenWidth,g_nScreenHeight,
    m_nFileWidth,m_nFileHeight,0,0);
}

BOOL CBmpFileReader2::draw(LPDIRECTDRAWSURFACE surface,
                           int w,int h,int x,int y){
//draw unscaled rectangle of this width and height from location
  return draw(surface,w,h,w,h,x,y);
}

BOOL CBmpFileReader2::draw(LPDIRECTDRAWSURFACE surface,
                    int w1,int h1,int w2,int h2,int x,int y){
//draw scaled from src to dest rectangle, from src origin
  HDC hDCSurface,hDCBitmap; //device contexts for surface, bitmap
  //get the device context for the DD surface
  surface->GetDC(&hDCSurface);
  //create compatible device context for bitmap
  hDCBitmap=CreateCompatibleDC(hDCSurface);
  SetMapMode(hDCBitmap,GetMapMode(hDCSurface));
  //attach the bitmap to the device context 
  SelectObject(hDCBitmap,m_hBitmap);
  SetStretchBltMode(hDCSurface,COLORONCOLOR);
  //blit to the DD surface
  StretchBlt(hDCSurface,0,0,w1,h1,hDCBitmap,x,y,w2,h2,SRCCOPY);
  //clean up and exit
  DeleteDC(hDCBitmap);
  surface->ReleaseDC(hDCSurface);
  return TRUE; //need to write error detection code here
}

BOOL CBmpFileReader2::load(char *filename){ //load from file
  //free up old bitmap, if any
  if(m_hBitmap){DeleteObject(m_hBitmap); m_hBitmap=NULL;};
  // load new image from a file
  m_hBitmap=(HBITMAP)LoadImage(NULL,filename,IMAGE_BITMAP,0,0,
    LR_LOADFROMFILE|LR_CREATEDIBSECTION);
if(m_hBitmap==NULL){   return FALSE;}
  //get bitmap width and height
  BITMAP bm; //bitmap info
  GetObject(m_hBitmap,sizeof(bm),&bm); //get info
  m_nFileWidth=bm.bmWidth; m_nFileHeight=bm.bmHeight;
  return TRUE;
}
