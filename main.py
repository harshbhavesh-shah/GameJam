import pygame as py
from fonctions import *


py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


joueur = Joueur((100,100))
blocs, portes, blocpics = preparationLevel(level1[1])

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
    collisions(blocs, blocpics, joueur)
    telePorte(portes, joueur, keys)
    
    affichageLevel(blocs, portes, blocpics, screen)
    py.draw.rect(screen,"red",joueur.getRect())
    



    py.display.flip()
    clock.tick(60)
    


py.quit()
