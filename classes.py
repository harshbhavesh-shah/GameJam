import pygame as py
from constantes import *

class Joueur:
    def __init__(self,pos:tuple[int,int]):
        self.rect = py.Rect(pos,(TILE_SIZE,TILE_SIZE))
        self.fallState = True
        self.jumpTimer = MAX_JUMP_TIMER
        self.fallSpeed = MAX_FALL_SPEED
        self.coyoteTimer = 0
        self.dashState = (DASH_TIMER,"n",DASH_COOLDOWN)
        self.porteCooldown = 0

    # Coordonnées

    def setX(self,x):
        self.rect.x = x

    def getX(self):
        return self.rect.x
    
    def setY(self,y):
        self.rect.y = y

    def getY(self):
        return self.rect.y
    
    def setXY(self, x, y):
        self.rect.topleft = (x,y)
    
    def getXY(self):
        return (self.rect.x,self.rect.y)
    
    # Rect
    
    def setRect(self,rect:py.Rect):
        self.rect = rect

    def getRect(self):
        return self.rect
    
    # Saut / Chute

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
    
    # Coyote

    def setCoyoteTimer(self,val):
        self.coyoteTimer = val

    def getCoyoteTimer(self):
        return self.coyoteTimer

    # Porte Cooldown

    def setPorteCooldown(self,val):
        self.porteCooldown = val
    
    def getPorteCooldown(self):
        return self.porteCooldown

    # Dash

    def setDashState(self,state:tuple[int,str,int]):
        self.dashState = state

    def getDashState(self):
        return self.dashState
    
    
    def dash(self):
        """
        Effectue le dash en fonction de la direction est de la distance déjà parcourue
        """
        match self.getDashState()[1]:
            case "g": self.rect.x  -= DASH_SPEED
            case "d": self.rect.x  += DASH_SPEED
            case "h": self.rect.y  -= DASH_SPEED
            case "n": return
        self.setDashState((self.getDashState()[0] +1,self.getDashState()[1],self.getDashState()[2]))
    
    def move(self, keys):
        """
        Fonction qui gére les déplacement (avec gravité) du joueur
        """
        # DÉPLACEMENTS DE BASE
        if (keys[py.K_d] or keys[py.K_RIGHT])   and self.rect.x + self.rect.width < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if (keys[py.K_q] or keys[py.K_LEFT])   and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[py.K_SPACE]:
            if not self.getFallState():
                self.setFallState(False)
                self.setFallSpeed(0)
                self.rect.y -= (JUMP_SPEED - self.getJumpTimer())
                self.jumpTimer += 1
                if self.jumpTimer >= MAX_JUMP_TIMER: self.setFallState(True)

        # GRAVITÉ

        elif self.jumpTimer > 0: self.setFallState(True) 
        
        if self.getDashState()[0] < DASH_TIMER and self.getDashState()[1] != "n": self.setFallState(False) # Si en dash : stop gravité

        if self.getFallState() : 
            self.fallSpeed += 1
            self.rect.y += min(MAX_FALL_SPEED,self.getFallSpeed())

        # DASH

        self.setDashState((self.getDashState()[0],self.getDashState()[1],max(self.getDashState()[2]-1,0))) # Cooldown Dash

        if keys[py.K_LSHIFT] and self.getDashState()[0] < DASH_TIMER and self.getDashState()[2] == 0:
            if self.getDashState()[1] == "n" and  (keys[py.K_d] or keys[py.K_RIGHT]):  # Seulement initialiser si le dash n'a pas commencé
                self.setFallSpeed(0)
                self.setDashState((0,"d",DASH_COOLDOWN))
            elif self.getDashState()[1] == "n" and  (keys[py.K_q] or keys[py.K_LEFT]):
                self.setFallSpeed(0)
                self.setDashState((0,"g",DASH_COOLDOWN))
            elif self.getDashState()[1] == "n" and  (keys[py.K_z] or keys[py.K_UP]):
                self.setFallSpeed(0)
                self.setDashState((0,"h",DASH_COOLDOWN))
        
        if self.getDashState()[0] < DASH_TIMER and self.getDashState()[1] != "n":
            self.dash()

        



class Bloc(py.Rect):
    pass

class Porte:
    def __init__(self,pos:tuple[int,int], id: str):
        self.rect = py.Rect(pos,(2*TILE_SIZE,2*TILE_SIZE))
        self.id = id

    def getRect(self):
        return self.rect
    
    def getId(self):
        return self.id

class Pique(py.Rect):
    pass

class BlocMouv:
    def __init__(self, pos:tuple[int,int], x=0, y=5):
        self.rect = py.Rect(pos,(TILE_SIZE,TILE_SIZE))
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

    def getRect(self):
        return self.rect