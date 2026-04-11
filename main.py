import pygame as py
from fonctions import *


py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
joueur = Joueur((100,100))

zone = "hub"
souszone = 1
biome = "foret"
objetsDict = preparationZone(zone, souszone)

running = True
clock = py.time.Clock()
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    keys = py.key.get_pressed()
    keybinds(keys)
    
    background(screen,biome)

    # BOUCLE MAIN #

    joueur.move(keys)
    collisions(objetsDict, joueur)
    
    joueur.setPorteCooldown(max(0,joueur.getPorteCooldown()-1))
    if keys[py.K_e] and joueur.getPorteCooldown() == 0:         # TéléPortation
        objetsDict = telePorte(objetsDict,joueur)
                

    if joueur.getRect().x + joueur.getRect().width > SCREEN_WIDTH  or  joueur.getRect().x < 0: 
        objetsDict , souszone = switchSousZone(zone,souszone,joueur,objetsDict)

    if joueur.getRect().y > 720 and SCREEN_WIDTH > joueur.getRect().x > 0:
        joueur.setXY(objetsDict["spawn"][0].x, objetsDict["spawn"][0].y)

    affichageZone(objetsDict, screen)
    py.draw.rect(screen,"red",joueur.getRect())

    py.display.flip()
    clock.tick(60)
    


py.quit()