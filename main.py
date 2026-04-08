import pygame as py
from fonctions import *


py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
joueur = Joueur((100,100))
objetsDict = preparationZone(niveaux, 1, 1)

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
    collisions(objetsDict, joueur)
    
    if keys[py.K_e] and any(porte.getRect().colliderect(joueur.getRect()) for porte in objetsDict["portes"]):
        objetsDict = preparationZone(niveaux, 1, 2)
        joueur.setXY(80,560)
    affichageZone(objetsDict, screen)
    py.draw.rect(screen,"red",joueur.getRect())
    



    py.display.flip()
    clock.tick(120)
    


py.quit()
