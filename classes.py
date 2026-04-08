import pygame as py
from constantes import *

class Joueur:
    def __init__(self,pos:tuple[int,int]):
        self.rect = py.Rect(pos,(TILE_SIZE,TILE_SIZE))
        self.fallState = True
        self.jumpTimer = MAX_JUMP_TIMER
        self.fallSpeed = MAX_FALL_SPEED
        self.coyoteTimer = 0

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
    
    def setJumpTimer(self,val:int):
        self.jumpTimer = val

    def getJumpTimer(self):
        return self.jumpTimer
    
    def setFallState(self,state:bool):
        self.fallState = state

    def getFallState(self) -> bool :
        return self.fallState
    
    def setFallSpeed(self,val:int):
        self.fallSpeed = val

    def getFallSpeed(self):
        return self.fallSpeed
    
    def getCoyoteTimer(self):
        return self.coyoteTimer
    
    def setCoyoteTimer(self,val):
        self.coyoteTimer = val
    
    def move(self, keys):
        """
        Fonction qui gére les déplacement (avec gravité) du joueur
        """
        if keys[py.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[py.K_q]:
            self.rect.x -= PLAYER_SPEED
        if keys[py.K_SPACE]:
            if not self.getFallState():
                self.setFallState(False)
                self.setFallSpeed(0)
                self.rect.y -= (JUMP_SPEED - self.getJumpTimer())
                self.jumpTimer += 1
                if self.jumpTimer >= MAX_JUMP_TIMER: self.setFallState(True)

        elif self.jumpTimer > 0: self.setFallState(True)

        if self.getFallState() : 
            self.fallSpeed += 1
            self.rect.y += min(MAX_FALL_SPEED,self.getFallSpeed())


class Bloc(py.Rect):
    pass

class Porte:
    def __init__(self,pos:tuple[int,int]):
        self.rect = py.Rect(pos,(TILE_SIZE,TILE_SIZE))
        self.id = id(self)

    def getRect(self):
        return self.rect

class BlocPic(py.Rect):
    pass

class BlocMouv:
    def __init__(self, pos:tuple[int,int], x=0, y=5):
        self.rect = py.Rect(pos,(TILE_SIZE, TILE_SIZE))
        self.distxParc, self.distyParc = x*TILE_SIZE, y*TILE_SIZE
        self.distxAParc, self.distyAParc = 0, 0
        self.directionAbs, self.directionOrd = "droite", "haut"

    def move(self):
        if self.distxParc != 0:
            if self.directionAbs == "droite":
                self.rect.x += 2
                self.distxAParc += 2
                if self.distxAParc == self.distxParc:
                    self.directionAbs = "gauche"
            elif self.directionAbs == "gauche":
                self.rect.x -= 2
                self.distxAParc -= 2
                if self.distxAParc == 0:
                    self.directionAbs = "droite"
        if self.distyParc != 0:
            if self.directionOrd == "haut":
                self.rect.y += 2
                self.distyAParc += 2
                if self.distyAParc == self.distyParc:
                    self.directionOrd = "bas"
            elif self.directionOrd == "bas":
                self.rect.y -= 2
                self.distyAParc -= 2
                if self.distyAParc == 0:
                    self.directionOrd = "haut"