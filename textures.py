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

sprite_porte = py.image.load_animation("./assets/textures/autre/porte.gif")
sprite_pique = py.image.load("./assets/textures/autre/pique.png")

# BRIQUE #
sprite_brique = py.image.load("./assets/textures/autre/brique/brique.png")
sprite_brique_top = py.image.load("./assets/textures/autre/brique/brique_top.png")
sprite_brique_left = py.image.load("./assets/textures/autre/brique/brique_left.png")
sprite_brique_right = py.image.load("./assets/textures/autre/brique/brique_right.png")
sprite_brique_topleft = py.image.load("./assets/textures/autre/brique/brique_topleft.png")
sprite_brique_topright = py.image.load("./assets/textures/autre/brique/brique_topright.png")
sprite_brique_topleft_corner = py.image.load("./assets/textures/autre/brique/brique_topleft_corner.png")
sprite_brique_topright_corner = py.image.load("./assets/textures/autre/brique/brique_topright_corner.png")

### ENNEMIS ### 

sprite_requin = py.image.load_animation("./assets/textures/mer/requin.gif")

### DÉCORATIONS ###

sprite_lianes = py.image.load_animation("./assets/textures/autre/lianes.gif")


##### MISE A ECHELLE #####

sprite_porte = [py.transform.scale(s[0],(2*TILE_SIZE,2*TILE_SIZE)) for s in sprite_porte]
sprite_pique = py.transform.scale(sprite_pique,(TILE_SIZE,TILE_SIZE))
sprite_requin = [py.transform.scale(s[0],(4*TILE_SIZE,2*TILE_SIZE)) for s in sprite_requin]
sprite_lianes = [py.transform.scale(s[0],(TILE_SIZE,2*TILE_SIZE)) for s in sprite_lianes]

