import pygame as py
from fonctions import *


py.init()
py.joystick.init()

try: controller = py.Joystick(0)
except py.error: controller = None

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
joueur = Joueur((100,100))

zone = "hub"
souszone = 1
objetsDict = preparationZone(zone, souszone)

running = True
clock = py.time.Clock()
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE: menuPause(screen)
            
                
    keys = py.key.get_pressed()
    

    # BOUCLE MAIN #

    joueur.move(keys,controller)
    collisions(objetsDict, joueur)
    
    joueur.setPorteCooldown(max(0,joueur.getPorteCooldown()-1))
    if (keys[py.K_e] or controllerState(controller,"interaction")) and joueur.getPorteCooldown() == 0:         # TéléPortation
        objetsDict , zone , souszone = telePorte(objetsDict,zone,souszone,joueur)
                

    if joueur.getRect().x + joueur.getRect().width > SCREEN_WIDTH  or  joueur.getRect().x < 0: 
        objetsDict , souszone = switchSousZone(zone,souszone,joueur,objetsDict)

    if joueur.getRect().y > 720 and SCREEN_WIDTH > joueur.getRect().x > 0:
        joueur.setXY(objetsDict["spawn"][0].x, objetsDict["spawn"][0].y)

    background(screen,zone)
    affichageZone(objetsDict, screen)
    py.draw.rect(screen,"red",joueur.getRect())

    py.display.flip()
    clock.tick(60)
    


py.quit()