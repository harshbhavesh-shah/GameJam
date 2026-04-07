import pygame as py
from constantes import *

class Joueur:
    def __init__(self,pos:tuple[int,int]):
        self.rect = py.Rect(pos,(TILE_SIZE,TILE_SIZE))

    def setX(self,x):
        self.rect.x = x

    def getX(self):
        return self.rect.x
    
    def setY(self,y):
        self.rect.y = y

    def getY(self):
        return self.rect.y
    
    def getXY(self):
        return (self.rect.x,self.rect.y)
    
    def getRect(self):
        return self.rect
    
    def move(self, keys):
        """
        Fonction qui gére les déplacement (sans gravité) du joueur
        """
        if keys[py.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[py.K_q]:
            self.rect.x -= PLAYER_SPEED
        if keys[py.K_z]:
            self.rect.y -= PLAYER_SPEED
        if keys[py.K_s]:
            self.rect.y += PLAYER_SPEED

class Bloc(py.Rect):
    pass

class Porte:
    def __init__(self,pos:tuple[int,int]):
        self.rect = py.Rect(pos,(TILE_SIZE,TILE_SIZE))
        self.id = id(self)