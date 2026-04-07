import pygame as py
from constantes import *

class Joueur:
    def __init__(self,pos:tuple[int,int]):
        self.x = pos[0]
        self.y = pos[1]

    def setX(self,x):
        self.x = x

    def getX(self):
        return self.x
    
    def setY(self,y):
        self.y = y

    def getY(self):
        return self.y
    
    def getXY(self):
        return (self.x,self.y)
    
    def move(self, keys):
        if keys[py.K_d]:
            self.x += PLAYER_SPEED
        elif keys[py.K_q]:
            self.x -= PLAYER_SPEED
        elif keys[py.K_z]:
            self.y += PLAYER_SPEED
        elif keys[py.K_s]:
            self.y -= PLAYER_SPEED