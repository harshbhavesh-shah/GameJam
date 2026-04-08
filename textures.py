import pygame as py
from constantes import *

### BACKGROUND ###

bg_foret_1 = py.image.load("./assets/textures/foret/background/bg1.png")
bg_foret_2 = py.image.load("./assets/textures/foret/background/bg2.png")
bg_foret_3 = py.image.load("./assets/textures/foret/background/bg3.png")

bg_foret_1 = py.transform.scale(bg_foret_1,(SCREEN_WIDTH,SCREEN_HEIGHT))
bg_foret_2 = py.transform.scale(bg_foret_2,(SCREEN_WIDTH,SCREEN_HEIGHT))
bg_foret_3 = py.transform.scale(bg_foret_3,(SCREEN_WIDTH,SCREEN_HEIGHT))


### OBJETS ###

sprite_porte = py.image.load("./assets/textures/autre/porte.png")
sprite_pique = py.image.load("./assets/textures/autre/pique.png")
sprite_bloc = py.image.load("./assets/textures/autre/briqueTextureBloc.png")

sprite_porte = py.transform.scale(sprite_porte,(2*TILE_SIZE,2*TILE_SIZE))
sprite_pique = py.transform.scale(sprite_pique,(TILE_SIZE,TILE_SIZE))
sprite_bloc = py.transform.scale(sprite_bloc,(TILE_SIZE,TILE_SIZE))
