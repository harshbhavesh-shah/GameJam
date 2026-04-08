import pygame as py
from fonctions import *


py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
joueur = Joueur((100,100))
dictDonnees = preparationLevel(niveaux, 1, 1)
running = True
clock = py.time.Clock()
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    keys = py.key.get_pressed()
    keybinds(keys)
    
    background(screen,"foret")

    # BOUCLE MAIN #

    joueur.move(keys)
    collisions(dictDonnees, joueur)
    
    if keys[py.K_e] and any(porte.getRect().colliderect(joueur.getRect()) for porte in dictDonnees["portes"]):
        dictDonnees = preparationLevel(niveaux, 1, 2)
    affichageLevel(dictDonnees, screen)
    py.draw.rect(screen,"red",joueur.getRect())
    



    py.display.flip()
    clock.tick(60)
    


py.quit()
