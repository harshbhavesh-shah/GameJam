import pygame as py
from constantes import *

py.init()

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

running = True
clock = py.time.Clock()

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    

    # BOUCLE MAIN #


    py.display.flip()
    clock.tick(60)

py.quit()
