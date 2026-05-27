import pygame as py
from constantes import *
from manette import controllerState
import json
import os

class Joueur:
    def __init__(self,pos:tuple[int,int]):
        self.rect = py.Rect(pos,(TILE_SIZE,TILE_SIZE))
        self.fallState = True
        self.jumpTimer = MAX_JUMP_TIMER
        self.fallSpeed = MAX_FALL_SPEED
        self.coyoteTimer = 0
        self.dashState = (DASH_TIMER,"n",DASH_COOLDOWN)
        self.InteractionCooldown = 0
        self.hp = 100

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

    def setInteractionCooldown(self,val):
        self.InteractionCooldown = val
    
    def getInteractionCooldown(self):
        return self.InteractionCooldown

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
            case "hg": self.rect.y  -= DASH_SPEED//1.41 ; self.rect.x  -= DASH_SPEED//1.41
            case "hd": self.rect.y  -= DASH_SPEED//1.41 ; self.rect.x  += DASH_SPEED//1.41
            case "n": return
        self.setDashState((self.getDashState()[0] +1,self.getDashState()[1],self.getDashState()[2]))
    

    def move(self, keys,joystick, zone:str):
        """
        Fonction qui gére les déplacement (avec gravité) du joueur
        """
        # DÉPLACEMENTS DE BASE
        if (keys[py.K_d] or keys[py.K_RIGHT] or controllerState(joystick,"droite")):
            if zone == "mer": self.rect.x += PLAYER_SPEED_IN_WATER
            else : self.rect.x += PLAYER_SPEED
        if (keys[py.K_q] or keys[py.K_LEFT] or controllerState(joystick,"gauche")):
            if zone == "mer": self.rect.x -= PLAYER_SPEED_IN_WATER
            else : self.rect.x -= PLAYER_SPEED
        if keys[py.K_SPACE] or controllerState(joystick,"saut"):
            if not self.getFallState():
                self.setFallState(False)
                self.setFallSpeed(0)
                if zone == "mer": self.rect.y -= (JUMP_SPEED_IN_WATER - self.getJumpTimer()//4)
                else : self.rect.y -= (JUMP_SPEED - self.getJumpTimer()//2)
                self.jumpTimer += 1
                if self.jumpTimer >= MAX_JUMP_TIMER: self.setFallState(True)

        # GRAVITÉ

        elif self.jumpTimer > 0: self.setFallState(True) 
        
        if self.getDashState()[0] < DASH_TIMER and self.getDashState()[1] != "n": self.setFallState(False) # Si en dash : stop gravité

        if self.getFallState() : 
            self.fallSpeed += 1
            if zone == "mer": self.rect.y += min(MAX_FALL_SPEED_IN_WATER,self.getFallSpeed())
            else : self.rect.y += min(MAX_FALL_SPEED,self.getFallSpeed())

        # DASH

        self.setDashState((self.getDashState()[0],self.getDashState()[1],max(self.getDashState()[2]-1,0))) # Cooldown Dash

        if (keys[py.K_LSHIFT] or controllerState(joystick,"dash")) and self.getDashState()[0] < DASH_TIMER and self.getDashState()[2] == 0: # Seulement initialiser si le dash n'a pas commencé
            if self.getDashState()[1] == "n" and  ((keys[py.K_d] or keys[py.K_RIGHT] or controllerState(joystick,"droite")) and (keys[py.K_z] or keys[py.K_UP] or controllerState(joystick,"haut"))):  
                self.setFallSpeed(0)    # HAUT DROITE
                self.setDashState((0,"hd",DASH_COOLDOWN))
            elif self.getDashState()[1] == "n" and  ((keys[py.K_q] or keys[py.K_LEFT] or controllerState(joystick,"gauche")) and (keys[py.K_z] or keys[py.K_UP] or controllerState(joystick,"haut"))):  
                self.setFallSpeed(0)    # HAUT GAUCHE
                self.setDashState((0,"hg",DASH_COOLDOWN))
            elif self.getDashState()[1] == "n" and  (keys[py.K_d] or keys[py.K_RIGHT] or controllerState(joystick,"droite")):  
                self.setFallSpeed(0)    # DROITE
                self.setDashState((0,"d",DASH_COOLDOWN))
            elif self.getDashState()[1] == "n" and  (keys[py.K_q] or keys[py.K_LEFT] or controllerState(joystick,"gauche")):
                self.setFallSpeed(0)    # GAUCHE
                self.setDashState((0,"g",DASH_COOLDOWN))
            elif self.getDashState()[1] == "n" and  (keys[py.K_z] or keys[py.K_UP] or controllerState(joystick,"haut")):
                self.setFallSpeed(0)    # HAUT
                self.setDashState((0,"h",DASH_COOLDOWN))
        
        if self.getDashState()[0] < DASH_TIMER and self.getDashState()[1] != "n":
            self.dash()


    # HP (pour la ville)
    def getHp(self):
        return self.hp
    
    def setHp(self,hp):
        self.hp = hp

        



class Tile(py.Rect):
    def setSprite(self,sprite):
        self.sprite = sprite
        return self
    
    def getSprite(self) -> py.Surface:
        return self.sprite


class Bloc(Tile):
    pass

class Spawn(Tile):
    pass

class End(Tile):
    pass


class Porte(Tile):
    def setId(self,id):
        self.id = id
        return self
    
    def getId(self):
        return self.id


class Pique(Tile):
    pass


class BlocMouv(Tile):
    def setMouvement(self,mouvement:str):
        self.mouvement = mouvement.replace("a","a"*(TILE_SIZE//self.speed))
        self.orientation = mouvement[0]
        self.indexMouvement = 0
        return self
    
    def getMouvement(self):
        return self.mouvement
    
    def setSpeed(self,val:int):
        self.speed = val
        return self
    
    def getSpeed(self):
        return self.speed
    
    def getOrientation(self):
        return self.orientation
    
    def move(self):
        match self.getMouvement()[self.indexMouvement]:
            case "n" : self.orientation = "n"
            case "e" : self.orientation = "e"
            case "s" : self.orientation = "s"
            case "o" : self.orientation = "o"
            case "a" :
                match self.orientation:
                    case "n" : self.y -= self.speed
                    case "e" : self.x += self.speed
                    case "s" : self.y += self.speed
                    case "o" : self.x -= self.speed
        self.indexMouvement = (self.indexMouvement + 1) % len(self.getMouvement())
    
    
    
    
class Decoration(Tile):
    pass


class Ennemi(BlocMouv):
    def setType(self,type:str):
        self.type = type
        return self
    
    def getType(self):
        return self.type


class PNJ(Tile):
    def init_file(self,file:str):
        self.file = f"assets/textes/{file}.txt"
        self.texte = []
        self.nom = ""
        self.load(self.file)
        return self

    def load(self,file:str=None):
        if file is None:
            file = self.file
        if not os.path.exists(file):
            self.texte = ["Texte par défaut"]
            self.nom = "John Doe"
        else : 
            with open(file, "r") as f:
                tab = f.readlines()
                self.texte = tab[1:]
                self.nom = tab[0]
    
    def getLine(self,n):
        return self.texte[n]
    
    def getTexte(self):
        return self.texte
    
    def getRect(self):
        return self.rect

    def getNom(self):
        return self.nom
    

class BlocTombant(BlocMouv):
    def activeDelay(self):
        self.actif = True
        
    def init(self):
        self.actif = False
        self.compteur = 0
        return self
    
    def getCompteur(self):
        return self.compteur
    
    def incrCompteur(self):
        self.compteur += 1

    def getActif(self):
        return self.actif
    
    def saveState(self):
        self.savedState = [self.x,self.y,self.width,self.height,self.getSpeed(),self.getMouvement()]
        return self
    
    def loadSavedState(self):
        self.x = self.savedState[0]
        self.y = self.savedState[1]
        self.width = self.savedState[2]
        self.height = self.savedState[3]
        self.setSpeed(self.savedState[4])
        self.setMouvement(self.savedState[5])
        self.init()
        self.saveState()
        return self
    
    def setLabel(self,label:str):
        self.label = label

    def getLabel(self):
        return self.label
    

class Levier(Tile):    
    def setEstActif(self,etat:bool=True):
        self.estActif = etat
        return self

    def getEstActif(self):
        return self.estActif

    def setActifSprite(self,sprite):
        self.actifSprite = sprite
        return self

    def getActifSprite(self):
        return self.actifSprite


class BossSoleil(Ennemi):
    def setDeactif(self):
        self.actif = False

    def setActif(self):
        self.actif = True

    def init(self):
        self.actif = True
        self.compteur = 0
        return self
    
    def getCompteur(self):
        return self.compteur
    
    def incrCompteur(self):
        self.compteur += 1

    def getActif(self):
        return self.actif
    
    



class Settings:
    def __init__(self,file:str="settings.json"):
        self.file = file
        self.data = self.load()
    
    def load(self):
        if not os.path.exists(self.file):
            return self.default()
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def default(self):
        return {
            "volume": 50,
        }
    
    def getData(self):
        return self.data
    
    def updateData(self,dataDict:dict):
        self.data = dataDict
        self.save()