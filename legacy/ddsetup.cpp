//ddsetup.cpp: directDraw setup and release
//Copyright Ian Parberry, 1999
//Last updated October 10, 2000

//system includes
#include <windows.h>
#include <windowsx.h>
#include <ddraw.h>

//custom includes
#include "defines.h"

//globals
extern LPDIRECTDRAW lpDirectDrawObject; //direct draw object
extern LPDIRECTDRAWSURFACE lpPrimary; //primary surface
extern LPDIRECTDRAWSURFACE lpSecondary; //back buffer
extern LPDIRECTDRAWSURFACE lpBackground; //background image

extern DWORD g_dwTransparentColor;
extern HWND g_hwnd;
extern int g_nColorDepth;
extern int g_nScreenWidth,g_nScreenHeight;


//helper functions

DWORD color(COLORREF rgb,LPDIRECTDRAWSURFACE surface){
//return DWORD for rgb in surface's color mode
  DWORD dw=CLR_INVALID; //color in DWORD form
  COLORREF rgbT; //old color
  HDC hdc; //device context
  DDSURFACEDESC ddsd; //surface descriptor
  HRESULT hres; //result
  //use GDI SetPixel to color match for us
  if(rgb!=CLR_INVALID&&SUCCEEDED(surface->GetDC(&hdc))){
    rgbT=GetPixel(hdc,0,0); //save current pixel value
    SetPixel(hdc,0,0,rgb); //set our value
    surface->ReleaseDC(hdc); //release surface dc
  }
  //now lock the surface so we can read back the converted color
  ddsd.dwSize=sizeof(ddsd);
  while((hres=surface->Lock(NULL,&ddsd,0,NULL))
    ==DDERR_WASSTILLDRAWING); //keep trying
  if(SUCCEEDED(hres)){ //succeeded at last
    dw=*(DWORD *)ddsd.lpSurface; //get DWORD
    if(ddsd.ddpfPixelFormat.dwRGBBitCount!=32) //no mask
      dw&=(1<<ddsd.ddpfPixelFormat.dwRGBBitCount)-1; //mask
    surface->Unlock(NULL);
  }
  //now put the color that was there back.
  if(rgb!=CLR_INVALID&&SUCCEEDED(surface->GetDC(&hdc))){
    SetPixel(hdc,0,0,rgbT); //replace old value
    surface->ReleaseDC(hdc); //release surface dc
  }
  return dw;
}

BOOL InitSurfaces(HWND hwnd){
  //create the surfaces
  DDSURFACEDESC ddsd; //direct draw surface descriptor
  ddsd.dwSize=sizeof(ddsd);
  ddsd.dwFlags=DDSD_CAPS|DDSD_BACKBUFFERCOUNT;
  ddsd.ddsCaps.dwCaps=DDSCAPS_PRIMARYSURFACE|DDSCAPS_FLIP
    |DDSCAPS_COMPLEX;
  ddsd.dwBackBufferCount=1;
  if(FAILED(lpDirectDrawObject->
  CreateSurface(&ddsd,&lpPrimary,NULL)))
    return FALSE;
  //get pointer to the secondary surface
  DDSCAPS ddscaps;
  ddscaps.dwCaps=DDSCAPS_BACKBUFFER;
  if(FAILED(lpPrimary->
  GetAttachedSurface(&ddscaps,&lpSecondary)))
    return FALSE;
  //background surface
  ddsd.dwSize=sizeof(ddsd);
  ddsd.dwFlags=DDSD_CAPS|DDSD_HEIGHT|DDSD_WIDTH;
  ddsd.ddsCaps.dwCaps=DDSCAPS_OFFSCREENPLAIN;
  ddsd.dwHeight=g_nScreenHeight; ddsd.dwWidth=g_nScreenWidth;
  if(FAILED(lpDirectDrawObject->
  CreateSurface(&ddsd,&lpBackground,NULL)))
    return FALSE;
  //create direct draw clipper
  LPDIRECTDRAWCLIPPER lpClipper; //pointer to the clipper
  if(FAILED(lpDirectDrawObject-> //create the clipper
  CreateClipper(NULL,&lpClipper,NULL)))
    return FALSE;
  //set to clip to window boundaries
  if(FAILED(lpClipper->SetHWnd(NULL,hwnd)))
    return FALSE;
  //attach clipper to secondary surface
  if(FAILED(lpSecondary->SetClipper(lpClipper)))
    return FALSE;
  //transparent color 
  g_dwTransparentColor=color(TRANSPARENT_COLOR,lpPrimary);
  return TRUE;
}

BOOL InitDirectDraw(HWND hwnd){ //direct draw initialization
  //create and set up direct draw object
  if(FAILED(DirectDrawCreate(NULL,&lpDirectDrawObject,NULL)))
    return FALSE;
  //set cooperative level
  if(FAILED(lpDirectDrawObject->SetCooperativeLevel(hwnd,
  DDSCL_EXCLUSIVE|DDSCL_FULLSCREEN)))
    return FALSE;
  //change screen resolution
  if(FAILED(lpDirectDrawObject->
  SetDisplayMode(g_nScreenWidth,g_nScreenHeight,g_nColorDepth)))
    return FALSE;
  if(!InitSurfaces(g_hwnd))return FALSE;
  return TRUE;
} //InitDirectDraw2

long CALLBACK WindowProc(HWND hwnd,UINT message,
  WPARAM wParam,LPARAM lParam);

//windows system functions
HWND CreateDefaultWindow(char* name,HINSTANCE hInstance){
  WNDCLASS wc; //window registration info
  //register display window
  wc.style=CS_HREDRAW|CS_VREDRAW; //style
  wc.lpfnWndProc=WindowProc; //window message handler
  wc.cbClsExtra=wc.cbWndExtra=0;
  wc.hInstance=hInstance;
  wc.hIcon=LoadIcon(hInstance,IDI_APPLICATION);
  wc.hCursor=LoadCursor(NULL,IDC_ARROW);
  wc.hbrBackground=NULL;
  wc.lpszMenuName=NULL;
  wc.lpszClassName=name;
  RegisterClass(&wc);
  //create and set up fullscreen window
  return CreateWindowEx(WS_EX_TOPMOST,name,name,
    WS_POPUP,0,0,GetSystemMetrics(SM_CXSCREEN),
    GetSystemMetrics(SM_CYSCREEN),NULL,NULL,hInstance,NULL);
}
