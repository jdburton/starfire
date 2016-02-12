//main.cpp


//system includes
#include <windows.h>
#include <windowsx.h>
#include <ddraw.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <string>
#include <vector>

using namespace std;

//system defines
#define WIN32_LEAN_AND_MEAN

//custom includes
#include "defines.h" //global definitions
#include "bmp2.h" //bmp file reader, unpalettized
#include "timer.h" //game timer
#include "csprite.h" //for clipped sprite class
#include "objects.h" //for object class
#include "objman.h"
#include "sound.h"
#include "view.h"
#include "directmidi.h"
#include "musiclist.h"
#include "InputSystem.h"

//globals


const double PI = atan(1)*4;

BOOL ActiveApp; //is this application active?

LPDIRECTDRAW lpDirectDrawObject=NULL; //direct draw object
LPDIRECTDRAWSURFACE lpPrimary=NULL; //primary surface
LPDIRECTDRAWSURFACE lpSecondary=NULL; //back buffer
LPDIRECTDRAWSURFACE lpBackground=NULL; //background image

CTimer Timer; //game timer

HWND g_hwnd; //window handle

DWORD g_dwTransparentColor; //transparent color as a DWORD
int g_nColorDepth=COLOR_DEPTH; //color depth in bits
int g_nScreenWidth=SCREEN_WIDTH; //screen width
int g_nScreenHeight=SCREEN_HEIGHT; //screen height

CBmpFileReader2 background; //background image
CBmpFileReader2 g_cSpriteImages; //sprite images

vector<string> song_list;

CObjectManager theObjects(128);

CRandom Random; //random number generator

CViewPoint Viewpoint; //player viewpoint

CClippedSprite *g_pSprite[NUM_SPRITES]; //sprites
CSoundManager* SoundManager; //sound manager
CDirectMidi MidiPlayer;

int framerate_timer=0; //timer for updating frame rate display
int framecount=0; //number of frames in this interval (so far)
int last_framecount=0; //number of frames in last full interval

BOOL exploding = FALSE;

GamePhaseType GamePhase;
BOOL endphase = FALSE;

int PhaseTime = 0;
int CurrentLevel = 0;

//helper functions
BOOL InitDirectDraw(HWND hwnd);
HWND CreateDefaultWindow(char* name,HINSTANCE hInstance);
BOOL InitSurfaces(HWND); //in ddsetup.cpp

CInputSystem  g_input;	//direct input system
int     g_mouseX        = SCREEN_WIDTH / 2;
int     g_mouseY        = SCREEN_HEIGHT / 2;

bool mouse_mode = true;

void PutText(const char* text,LPDIRECTDRAWSURFACE surface);

/***************** Load all images from sprite file ****************/

BOOL LoadStarfireSprite(){ //load starfire image
    BOOL result = TRUE;
	result = result && g_pSprite[STARFIRE_OBJECT]->load(&g_cSpriteImages,0,1,1);
	result = result && g_pSprite[STARFIRE_OBJECT]->load(&g_cSpriteImages,1,74,1);
	result = result && g_pSprite[STARFIRE_OBJECT]->load(&g_cSpriteImages,2,147,1);

	return result;
} //LoadStarfireSprite


BOOL LoadEnemySprites(){ //load starfire image
    BOOL result = TRUE;
	//Gunship
	result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,0,1,75);
	result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,1,76,75);
	result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,2,150,75);
	result = result && g_pSprite[GUNSHIP_OBJECT]->load(&g_cSpriteImages,3,226,75);
	
	//Drone

	//All Enemies must have the same number of frames, even though it might be the same drawing!
	
	result = result && g_pSprite[DRONE_OBJECT]->load(&g_cSpriteImages,0,1,236);
	result = result && g_pSprite[DRONE_OBJECT]->load(&g_cSpriteImages,1,1,236);
	result = result && g_pSprite[DRONE_OBJECT]->load(&g_cSpriteImages,2,1,236);
	result = result && g_pSprite[DRONE_OBJECT]->load(&g_cSpriteImages,3,1,236);

	//========= Dart =======//
	result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,0,1,306);
	result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,1,147,306);
	result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,2,74,306);
	result = result && g_pSprite[DART_OBJECT]->load(&g_cSpriteImages,3,220,306);

	//********** Boss *********
	result = result && g_pSprite[BOSS_OBJECT]->load(&g_cSpriteImages,0,293,236);
    result = result && g_pSprite[BOSS_OBJECT]->load(&g_cSpriteImages,1,293,236);
    result = result && g_pSprite[BOSS_OBJECT]->load(&g_cSpriteImages,2,293,236);
    result = result && g_pSprite[BOSS_OBJECT]->load(&g_cSpriteImages,3,293,236);

	return result;
} //LoadStarfireSprite




BOOL LoadBullet(){

 BOOL result = TRUE;
	result = result && g_pSprite[BULLET_OBJECT]->load(&g_cSpriteImages,0,220,1);

	return result;
}

BOOL LoadBlaster(){

	BOOL result = TRUE;
	result = result && g_pSprite[BLASTER_OBJECT]->load(&g_cSpriteImages,0,220,11);
	result = result && g_pSprite[ENEMY_BLASTER_OBJECT]->load(&g_cSpriteImages,0,220,33);
	
	return result;
}



BOOL LoadExplosions(){

	BOOL result = TRUE;
	result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,0,1,136);
	result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,1,101,136);
	result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,2,301,136);
	result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,3,201,136);
	result = result && g_pSprite[EXPLOSION_OBJECT]->load(&g_cSpriteImages,4,401,136);
	return result;
}

BOOL LoadPowerUps(){

		BOOL result = TRUE;
	result = result && g_pSprite[SHIELD_OBJECT]->load(&g_cSpriteImages,0,231,1);
	result = result && g_pSprite[POWER_OBJECT]->load(&g_cSpriteImages,0,231,30);
	result = result && g_pSprite[BONUS_OBJECT]->load(&g_cSpriteImages,0,290,1);
	result = result && g_pSprite[X_OBJECT]->load(&g_cSpriteImages,0,290,30);
	
	return result;
}




/*************************************************************************************/
void LoadMusic(){

	song_list.push_back(string("./music/intro.mid"));
	song_list.push_back(string("./music/boss.mid"));
	song_list.push_back(string("./music/boss.mid"));
	song_list.push_back(string("./music/highscore.mid"));

}


void LoadSounds(int level=1){ //load sounds for level
  const int copies=4; //copies of repeatable sounds
  switch(level){
    case 0: //intro sounds
      SoundManager->load("./sounds/typewriter.wav");
      SoundManager->load("./sounds/monkey.wav");
      break;
    case 1: //game engine sounds
	  SoundManager->load("./sounds/engine.wav");
      SoundManager->load("./sounds/blaster.wav",copies);
      SoundManager->load("./sounds/explosion.wav",copies);
      SoundManager->load("./sounds/hitshield.wav",copies);
	  SoundManager->load("./sounds/dying.wav");
	  SoundManager->load("./sounds/ehitshield.wav",copies);
	  SoundManager->load("./sounds/laser.wav",copies);
	  SoundManager->load("./sounds/flyby.wav");
	  SoundManager->load("./sounds/begin0.wav");
      SoundManager->load("./sounds/begin1.wav");
      SoundManager->load("./sounds/begin2.wav");
      SoundManager->load("./sounds/gameover.wav");
      SoundManager->load("./sounds/gameover1.wav");
      
      
	  break;
  }
}

/***********************************************************************************/


BOOL GetBackground(){ //get background from file reader

  return background.draw(lpBackground); //draw to bgrnd surface
} //GetBackground

void CreateSprites(){ //create the sprites
	g_pSprite[BULLET_OBJECT] = new CClippedSprite(1,9,9);
	g_pSprite[BLASTER_OBJECT] = new CClippedSprite(1,9,20);
	g_pSprite[STARFIRE_OBJECT]=new CClippedSprite(3,72,73); //73
	g_pSprite[GUNSHIP_OBJECT]= new CClippedSprite(4,73,58);
	g_pSprite[EXPLOSION_OBJECT] = new CClippedSprite(5,99,99);
	g_pSprite[ENEMY_BLASTER_OBJECT] = new CClippedSprite(1,9,20);
	g_pSprite[POWER_OBJECT] = new CClippedSprite(1,57,27);
	g_pSprite[SHIELD_OBJECT] = new CClippedSprite(1,57,27);
	g_pSprite[DRONE_OBJECT] = new CClippedSprite(4,79,68);
	g_pSprite[DART_OBJECT] = new CClippedSprite(4,71,68);
	g_pSprite[BONUS_OBJECT] = new CClippedSprite(1,57,27);
	g_pSprite[X_OBJECT] = new CClippedSprite(1,57,27);
	g_pSprite[BOSS_OBJECT] = new CClippedSprite(4,182,169);
	

}//CreateSprites

BOOL GetImages(){ //get images from file readers
  //background
  if(!GetBackground())return FALSE; 
  //sprites
  CreateSprites(); //create before getting images
  if(!LoadStarfireSprite())return FALSE;
  if(!LoadEnemySprites())return FALSE;
  if(!LoadExplosions())return FALSE;
  if(!LoadBullet())return FALSE;
  if(!LoadBlaster())return FALSE;
  if(!LoadPowerUps())return FALSE;
  return TRUE;
} //GetImages

BOOL LoadSpriteFile(){ //load sprite file to file reader
  return g_cSpriteImages.load("./images/newsprites.bmp");
} //LoadSpriteFile

BOOL LoadBackgroundFile(){ //load background to file reader
  //if(g_bGlassHouse)
    return background.load("./images/starfield800.bmp"); //photograph
} //LoadBackgroundFile

BOOL LoadImageFiles(){ //loadi mage files to file readers
  if(!LoadBackgroundFile())return FALSE;
  if(!LoadSpriteFile())return FALSE;

  return TRUE;
} //LoadImageFiles

BOOL InitImages(){ //initialize all images for first time
  if(!LoadImageFiles())return FALSE;
  if(!GetImages())return FALSE;
  return TRUE;
} //InitImages

void CreateObjects(){
srand(time(NULL));
 theObjects.create(STARFIRE_OBJECT,SCREEN_WIDTH/2,SCREEN_HEIGHT,0,-1); //put fighter at bottom of screen
 

 for(int i = 0; i < NUM_BLASTERS; i++)
 theObjects.create(BLASTER_OBJECT,0,0,0,0);
 


 for(int j = 0; j < NUM_EBLASTERS; j++)
 theObjects.create(ENEMY_BLASTER_OBJECT,0,0,0,0);

 for(int k = 0; k < NUM_BULLETS; k++)
 theObjects.create(BULLET_OBJECT,0,0,0,0); 
  

 theObjects.create(POWER_OBJECT,SCREEN_WIDTH/2,0,0,1);
 theObjects.create(SHIELD_OBJECT,SCREEN_WIDTH/2,0,0,1);
 theObjects.create(BONUS_OBJECT,SCREEN_WIDTH/2,0,0,1);
 theObjects.create(X_OBJECT,SCREEN_WIDTH/2,0,0,1);

 theObjects.create(DART_OBJECT,400,0,0,2);
 theObjects.create(DART_OBJECT,256,0,0,1);		//and enemies at top
 theObjects.create(DART_OBJECT,600,0,0,2);

 theObjects.initExplosions();

} //CreateObjects



BOOL RestoreSurfaces(){ //restore all surfaces
  BOOL result=TRUE;
  if(FAILED(lpPrimary->Restore()))return FALSE;
  if(FAILED(lpSecondary->Restore()))return FALSE;
  if(SUCCEEDED(lpSecondary->Restore())) //if secondary restored
    result=result&&background.draw(lpSecondary); //redraw image
  else return FALSE;
  if(g_pSprite[STARFIRE_OBJECT]->Restore()) //if starfire restored
    result=result&&LoadStarfireSprite(); //redraw image
  else return FALSE;  
  if(g_pSprite[GUNSHIP_OBJECT]->Restore()) //if enemies restored
    result=result&&LoadEnemySprites(); //redraw image
  else return FALSE;
  if(g_pSprite[EXPLOSION_OBJECT]->Restore()) //if enemies restored
    result=result&&LoadExplosions(); //redraw image
  else return FALSE;
  if(g_pSprite[BULLET_OBJECT]->Restore()) //if  restored
    result=result&&LoadExplosions(); //redraw image
  else return FALSE;
  if(g_pSprite[DRONE_OBJECT]->Restore()) //if  restored
    result=result&&LoadExplosions(); //redraw image
  else return FALSE;
  if(g_pSprite[BLASTER_OBJECT]->Restore()) //if restored
    result=result&&LoadExplosions(); //redraw image
  else return FALSE;
  if(g_pSprite[ENEMY_BLASTER_OBJECT]->Restore()) //if restored
    result=result&&LoadExplosions(); //redraw image
  else return FALSE;
  if(g_pSprite[POWER_OBJECT]->Restore()) //if restored
    result=result&&LoadExplosions(); //redraw image
  else return FALSE;
  if(g_pSprite[SHIELD_OBJECT]->Restore()) //if restored
    result=result&&LoadExplosions(); //redraw image
  if(g_pSprite[BONUS_OBJECT]->Restore()) //if restored
    result=result&&LoadExplosions(); //redraw image
  else return FALSE;
  
  return result;
} //RestoreSurfaces

BOOL PageFlip(){ //return TRUE if page flip succeeds
  if(lpPrimary->Flip(NULL,DDFLIP_WAIT)==DDERR_SURFACELOST)
    return RestoreSurfaces();
  return TRUE;
} //PageFlip

BOOL ComposeFrame(){ //compose a frame of animation
  //draw background


  static int next_powerup = Timer.time()+Random.number(3000,12000);
  static int frame = 1;
  RECT rect; //drawing rectangle
  rect.left=0; rect.right=g_nScreenWidth; 
  rect.top=0; rect.bottom=g_nScreenHeight; 
  lpSecondary->Blt(&rect,lpBackground,&rect,DDBLT_WAIT,NULL);
  //move objects


  Viewpoint.draw_background(lpBackground,lpSecondary,8);
  
  int collision = theObjects.collisiondetection();
  
  
  theObjects.animate(lpSecondary);	//animate the current frame
  theObjects.refresh(collision);	//refresh the objects

  


if(Timer.time()>=next_powerup){
	theObjects.powerup();
    next_powerup += Random.number(10000,30000);	//next power up in 10 - 30 sec
	
}

  //frame rate
  framecount++; //count frame
  if(Timer.elapsed(framerate_timer,500)){

   theObjects.set_current(STARFIRE_INDEX);
	  theObjects.changedirection(0,0);
    last_framecount=framecount; framecount=0;
  }
 
  return PageFlip(); //flip video memory surfaces
 // return TRUE;
} //ComposeFrame


void display_screen(char * filename){

	CBmpFileReader2 image;
	image.load(filename);
	image.draw(lpSecondary);
	PageFlip();
}

void change_phase(GamePhaseType new_phase){

	GamePhase = new_phase;
	PhaseTime = Timer.time();
	endphase = FALSE;
	static int first = 1;

	switch(GamePhase){

	case LOGO_PHASE:
			LoadSounds(0);
			display_screen("./images/logo.bmp");
			SoundManager->play(TITLE_SOUND);
			SoundManager->play(LOGO_SOUND);
			break;

	case TITLE_PHASE:
		
			SoundManager->stop(); //silence previous phase
        	MidiPlayer.Load(song_list[INTRO_MUSIC].c_str());
			MidiPlayer.Play();
			display_screen("./images/title.bmp"); 
			break;
			
	case HELP_PHASE:
			SoundManager->stop();
			display_screen("./images/help.bmp"); break;

	case ENEMY_PHASE:
			display_screen("./images/enemies.bmp"); break;

	case MENU_PHASE:

			SoundManager->stop(); //silence previous phase
        
			if(!first){
				MidiPlayer.Stop();
				MidiPlayer.Load(song_list[INTRO_MUSIC].c_str());
				MidiPlayer.Play();
			}
			
			display_screen("./images/menu.bmp"); break;

	case PLAYING_PHASE:

			
	        SoundManager->stop(); //silence previous phase
            SoundManager->clear(); //clear out old sounds
			LoadSounds(1);

			if(first){
		    CreateObjects(); //create new objects
			first = 0;

			}
				SoundManager->play(BEGIN0_SOUND+Random.number(0,2));
			
				MidiPlayer.Stop();
				MidiPlayer.Load(song_list[THEME_MUSIC].c_str());
				MidiPlayer.Play();
			
		//	SoundManager->play(ENGINE_SOUND,LOOP_SOUND);
			break;
	case GAMEOVER_PHASE:

			MidiPlayer.Stop();
			
						
			display_screen("./images/game_over.bmp");
			Sleep(2000);
			SoundManager->stop(); //silence previous phase
			SoundManager->play(GAMEOVER1_SOUND);
			 break;

	}
}

void Redraw(){ //redraw in response to surface loss
  switch(GamePhase){
    case LOGO_PHASE:
      display_screen("./images/logo.bmp");
      break;
    case TITLE_PHASE:
      display_screen("./images/title.bmp");
      break;
    case HELP_PHASE:
      display_screen("./images/help.bmp");
      break;
    case ENEMY_PHASE:
      display_screen("./images/enemies.bmp");
      break;
   
	case MENU_PHASE:
      display_screen("./images/menu.bmp"); //display main menu
      break;
    case GAMEOVER_PHASE:
      display_screen("./images/game_over.bmp"); //display main menu
      break;
    
	case PLAYING_PHASE:
      //do nothing, next frame of animation will catch it
      break;
  }
}

void ProcessInput()
{
  static bool leftButtonDown = false;
  static bool rightButtonDown = false;
  static bool first = true;
 
  
  

  // rotate through mouse cursors on mouseclicks or wheel movement
  if (g_input.ButtonDown(0)){
    leftButtonDown = true;

	if(theObjects.lives_remaining >= 0) theObjects.fire(Timer.time());
  }
  if (g_input.ButtonDown(1)){
	if(theObjects.lives_remaining >= 0) theObjects.fire(Timer.time());
    rightButtonDown = true;
  }



  // update the mouse position
  int dx, dy;
  g_input.GetMouseMovement(dx, dy);

  int scale = (dx < 0)? 2:4;	//going up is faster than going down
  theObjects.changedirection(dx * 3,dy/scale);

} // end ProcessInput()

void ProcessFrame(){ //process a frame of animation
  const int LOGO_DISPLAY_TIME=5500; //duration of logo
  const int TITLE_DISPLAY_TIME=20000; //duration of title
  static int not_first = 0;
  static int last_time = Timer.time();
  
  //check for lost surfaces, eg alt+tab
  if(lpPrimary->IsLost()){
    RestoreSurfaces(); Redraw();
  }
  


  switch(GamePhase){ //what phase are we in?
    case LOGO_PHASE: //displaying logo screen
      Sleep(100); //surrender time to other processes
      if(endphase||Timer.elapsed(PhaseTime,LOGO_DISPLAY_TIME))
        change_phase(TITLE_PHASE); //go to title screen
      break;
    case TITLE_PHASE: //displaying title screen
      Sleep(100); //surrender time to other processes
      if(endphase||Timer.elapsed(PhaseTime,TITLE_DISPLAY_TIME))
        change_phase(MENU_PHASE); //go to menu
      break;
	case HELP_PHASE: if(endphase)
					  change_phase(ENEMY_PHASE); //go to menu
    case ENEMY_PHASE: if(endphase)
					  change_phase(MENU_PHASE); //go to menu
      
    case MENU_PHASE: //main menu
	
      Sleep(100); //surrender time to other processes
      if(endphase){
		  if(not_first){
		   CurrentLevel = 0;
		  theObjects.reset(0);
		  }
		  else{
			   not_first = 1;

		  }

		  change_phase(PLAYING_PHASE); //play game
	  }
      break;
    case PLAYING_PHASE: //game engine
	  
		if(Timer.elapsed(last_time,35)){
			if(mouse_mode){
			g_input.Update();	//update the input
			ProcessInput();	//process it
			}
			last_time = Timer.time();
		}

	  ComposeFrame(); //compose a frame in back surface
	  //PutText(temp.c_str(),lpPrimary);
      if(endphase) 
        change_phase(MENU_PHASE); 
	  if(theObjects.lives_remaining < 0){

		  change_phase(GAMEOVER_PHASE);
	  }
	  if(theObjects.won()) {
		 //change_phase(MENU_PHASE);
		  theObjects.reset(++CurrentLevel);
	  }
	  
	  
	  
      break;
	case GAMEOVER_PHASE:
		Sleep(100);
		if(endphase){
			change_phase(MENU_PHASE);
		}
		break;
	default: break;
  }
} //ProcessFrame





void ReleaseSurfaces(){
  if(lpSecondary!=NULL) //if secondary surface exists
    lpSecondary->Release(); //release secondary surface
  if(lpPrimary!=NULL) //if primary surface exists
    lpPrimary->Release(); //release primary surface
  if(lpBackground!=NULL) //if background exists
    lpBackground->Release(); //release background
  for(int i=0; i<NUM_SPRITES; i++){ //for each sprite
    if(g_pSprite[i]) //if sprite exists
      g_pSprite[i]->Release(); //release sprite
    delete g_pSprite[i]; //delete sprite
    }
}


void PutText(const char* text,LPDIRECTDRAWSURFACE surface){
  HDC hdc;
  if(SUCCEEDED(surface->GetDC(&hdc))){
    RECT rect;
    rect.left=10; rect.right=g_nScreenWidth-10; 
    rect.top= 10; rect.bottom=g_nScreenHeight; 
    DrawText(hdc,text,-1,&rect,0);
    surface->ReleaseDC(hdc);
  }
}


void ShutDownDirectDraw(){
  if(lpDirectDrawObject!=NULL){ //if DD object exists
    ReleaseSurfaces();
    lpDirectDrawObject->Release(); //release DD object
  }
}

BOOL game_keyboard_handler(WPARAM keystroke){ //keyboard handler
  BOOL result=FALSE; 
  switch(keystroke){
    theObjects.set_current(STARFIRE_INDEX);
  
  
    case VK_SPACE: if(theObjects.lives_remaining >= 0) theObjects.fire(Timer.time());/* theObjects.fire(Timer.time())*/; break;
    case VK_ESCAPE:	endphase=TRUE; break; //exit game
    case VK_UP: theObjects.changedirection(0,-2); break;
    case VK_DOWN: theObjects.changedirection(0,1); break;
    case VK_LEFT: theObjects.changedirection(-3,0); break;
    case VK_RIGHT: theObjects.changedirection(3,0); break;
	case 'Z': mouse_mode = !mouse_mode; break;
	
 
    default: break;
  }
  return result;
} //keyboard_handler

void intro_keyboard_handler(WPARAM keystroke){
  endphase=TRUE; //any key ends the phase
} //intro_keyboard_handler

BOOL menu_keyboard_handler(WPARAM keystroke){
  BOOL result=FALSE;
  switch(keystroke){
    case VK_ESCAPE:
    case 'Q': //exit game
      result=TRUE;
      break;
    case 'N': //play new game
      endphase=TRUE;
      break;
	case 'H': change_phase(HELP_PHASE);
    case 'Z': mouse_mode = !mouse_mode; break;
	
 
	default: break; //do nothing
  }
  return result;
} //menu_keyboard_handler

BOOL keyboard_handler(WPARAM keystroke){ //keyboard handler
  BOOL result=FALSE; //TRUE if we are to exit game
  switch(GamePhase){ //select handler for phase
    case LOGO_PHASE:
    case TITLE_PHASE:
	case GAMEOVER_PHASE:
	case HELP_PHASE:
	case ENEMY_PHASE:
      intro_keyboard_handler(keystroke);
      break;
    case MENU_PHASE:
      result=menu_keyboard_handler(keystroke);
      break;
    case PLAYING_PHASE:
      game_keyboard_handler(keystroke);
      break;
  }
  return result;
} //keyboard_handler

//message handler (window procedure)
long CALLBACK WindowProc(HWND hwnd,UINT message,
                         WPARAM wParam,LPARAM lParam){
  switch(message){
    case WM_ACTIVATE: 
		  if (!HIWORD(wParam))
      {
        // program was restored or maximized
        ActiveApp = wParam;
        g_input.AcquireAll();
      }
      else
      {
        // program was minimized
        g_input.UnacquireAll();
      }

      break;
    case WM_CREATE: break;
    case WM_KEYDOWN: //keyboard hit
      if(keyboard_handler(wParam))DestroyWindow(hwnd);
      break;
    case WM_DESTROY: //end of game
      ShutDownDirectDraw(); //shut down DirectDraw
	  g_input.Shutdown(); //shut down DirectInput
      ShowCursor(TRUE); //show the mouse cursor
      PostQuitMessage(0); //and exit
      delete SoundManager; //reclaim sound manager memory

      break;
    default: //default window procedure
      return DefWindowProc(hwnd,message,wParam,lParam);
  } //switch(message)
  return 0L;
} //WindowProc

int WINAPI WinMain(HINSTANCE hInstance,HINSTANCE hPrevInstance,
LPSTR lpCmdLine,int nCmdShow){
  MSG msg; //current message
  HWND hwnd; //handle to fullscreen window
  hwnd=CreateDefaultWindow("Demo 4a",hInstance);
  if(!hwnd){  return FALSE;}
  g_hwnd=hwnd;
  //set up window
  ShowWindow(hwnd,nCmdShow); UpdateWindow(hwnd);
  SetFocus(hwnd); //allow input from keyboard
  ShowCursor(FALSE); //hide the cursor
  g_input.Initialize(g_hwnd, hInstance, true, IS_USEMOUSE);	//initialize mouse with dinput
  //init graphics  
  for(int i=0; i<NUM_SPRITES; i++) //null out sprites
    g_pSprite[i]=NULL;
  BOOL OK=InitDirectDraw(hwnd);//initialize DirectDraw
  if(OK)OK=InitImages(); //load images from disk
  if(!OK){ //bail out if initialization failed
    DestroyWindow(hwnd); return FALSE;
  }
  //start game timer
  Timer.start();
 SoundManager=new CSoundManager(hwnd);
 LoadMusic();
 change_phase(LOGO_PHASE);
  //message loop
  while(TRUE)
    if(PeekMessage(&msg,NULL,0,0,PM_NOREMOVE)){
      if(!GetMessage(&msg,NULL,0,0))return msg.wParam;
      TranslateMessage(&msg); DispatchMessage(&msg);
    }
    else if(ActiveApp)ProcessFrame(); else WaitMessage();
} //WinMain
