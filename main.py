import pygame as py
from fonctions import *
from levels import *


py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


joueur = Joueur((100,100))
blocs = []
portes = []
map_tile = level1["map1"]
for i in range(len(map_tile)):
    for j in range(len(map_tile[i])):
        match map_tile[i][j]:
            case 1: blocs.append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
            case 2: portes.append(Porte((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))

running = True
clock = py.time.Clock()

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    keys = py.key.get_pressed()
    keybinds(keys)
    
    screen.fill("cyan")

    # BOUCLE MAIN #
    
    joueur.move(keys)
    collisions(blocs,joueur)
    py.draw.rect(screen,"red",joueur.getRect())
    for objet in blocs:
        py.draw.rect(screen,"brown",objet)
    for objet in portes:
        py.draw.rect(screen,"green",objet)
    



    py.display.flip()
    clock.tick(60)
    


py.quit()
