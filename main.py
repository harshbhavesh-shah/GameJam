import pygame as py
from constantes import *
from classes import *

py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


joueur = Joueur((100,100))


running = True
clock = py.time.Clock()

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    
    screen.fill("cyan")

    # BOUCLE MAIN #
    
    py.draw.rect(screen,"red",py.Rect(joueur.getXY(),(100,100)))



    py.display.flip()
    clock.tick(60)

py.quit()
