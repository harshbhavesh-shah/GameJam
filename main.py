import pygame as py
from fonctions import *


py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
joueur = Joueur((100,100))

souszone = 1
biome = "foret"
objetsDict = preparationZone("hub", souszone)

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
        for porte in objetsDict["portes"]:
            if porte.getRect().colliderect(joueur.getRect()):
                destination_id = PORTES_CORRESPONDANCES[porte.getId()]
                zone , souszone , y , x = destination_id.split('-')[0] , int(destination_id.split('-')[1]) , int(destination_id.split('-')[2]) , int(destination_id.split('-')[3])
                objetsDict = preparationZone(zone,souszone)
                joueur.setXY(x*TILE_SIZE,y*TILE_SIZE)
                joueur.setPorteCooldown(PORTE_COOLDOWN)
                break
                
    if joueur.getRect().x + joueur.getRect().width > SCREEN_WIDTH  or  joueur.getRect().x < 0: 
        objetsDict , souszone = switchSousZone(souszone,joueur)

    if joueur.getRect().y > SCREEN_HEIGHT: 
        joueur.setXY(objetsDict["spawn"][0].x, objetsDict["spawn"][0].y)

    affichageZone(objetsDict, screen)
    py.draw.rect(screen,"red",joueur.getRect())

    py.display.flip()
    clock.tick(60)
    


py.quit()