import pygame as py

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

class Bloc(py.Rect):
    pass