import pygame as py
from fonctions import *


py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


joueur = Joueur((100,100))
blocs, portes = defgrille(1)

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
