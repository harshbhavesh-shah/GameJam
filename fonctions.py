import pygame as py
from classes import *
from levels import *
from textures import *
import time

def keybinds(keys):
    """
    Fonction qui gére tous les racourcis clavier (Esc,Tab...)
    """
    if keys[py.K_ESCAPE]:
        py.quit()
    if keys[py.K_TAB]:
        pass                                                  #Pour ouvrir l'inventaire



def collisionsBlocJoueur(j_rect:py.Rect,b_rect:py.Rect,j:Joueur):
    """
    Collisions entre bloc et joueur, a part pour visibilité.\n 
    Prends en paramètres : 
        \n- j_rect : le rect du joueur AVANT pour éviter des bugs.
        \n- b_rect : le rect du bloc.
        \n- j : le Joueur."""
    # Calcul de l'overlap
    overlap_left = j_rect.right - b_rect.left      # bloc à droite du joueur
    overlap_right = b_rect.right - j_rect.left     # bloc à gauche du joueur
    overlap_top = j_rect.bottom - b_rect.top       # bloc en haut du joueur
    overlap_bottom = b_rect.bottom - j_rect.top    # bloc en bas du joueur
    
    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
    
    if min_overlap == overlap_top:  # Collision par le haut
        j.setY(b_rect.top - j_rect.height)
        j.setFallState(False) # Reset du saut
        j.setJumpTimer(0)
        j.setFallSpeed(0)
    elif min_overlap == overlap_bottom:  # Collision par le bas
        j.setY(b_rect.bottom)
        j.setFallState(True)
    elif min_overlap == overlap_left:  # Collision par la gauche
        j.setX(b_rect.left - j_rect.width)
    elif min_overlap == overlap_right:  # Collision par la droite
        j.setX(b_rect.right)
    j.setDashState((DASH_TIMER,"n",j.getDashState()[2]))
    joueur_rect = j.getRect()  # Mise à jour



def collisions(objetsDict:dict[str,list[Bloc|BlocMouv]], j:Joueur):
    """
    Gère les collisions entre le Joueur (j) et l'envirronement (Blocs,Pics...). \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire des objets.
        \n- j : le Joueur.
    """
    joueur_rect = j.getRect()
    
    if j.rect.x <= 0 : j.rect.x = 0

    for bloc in objetsDict["blocs"]:
        if bloc.colliderect(joueur_rect): 
            collisionsBlocJoueur(joueur_rect,bloc,j)
    
    for blocpic in objetsDict["piques"]:
        if blocpic.colliderect(joueur_rect):
            py.time.wait(500)            
            joueur_rect = j.getRect()  #  TODO   
 
    # Bloc mouv
    for blocmouv in objetsDict["blocmouvs"]:
        if blocmouv.getRect().colliderect(joueur_rect):
            collisionsBlocJoueur(joueur_rect,blocmouv.getRect(),j)

    # Coyote et dash
    if (not any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in objetsDict["blocs"]) 
        or not any(blocmouv.getRect().colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for blocmouv in objetsDict["blocmouvs"])) and j.getJumpTimer() == 0: # Si il n'y a rien sous le joueur -> chute
        if j.getCoyoteTimer() < COYOTE_JUMP_TIME:
            j.setCoyoteTimer(j.getCoyoteTimer()+1)
        else:
            j.setCoyoteTimer(0)
            j.setFallState(True)
    
    if any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in objetsDict["blocs"]) and j.getDashState()[0] >= DASH_TIMER:   # Reset dash
        j.setDashState((0,"n",j.getDashState()[2])) 




def preparationZone(zone:str, souszone:int) -> dict[str,list[Bloc|BlocMouv|Porte]]:
    """
    Renvoie un dictionnaire associant chaque type d'objet à la liste des objets à ajouter dans une sous-zone.
    Prends en paramètres :
        \n- zone : une chaine représenant la zone parmis tileMaps, qui repertorie des sous zones.
        \n- sous-zones : un entier représenant la sous-zone parmis zone.
    où tileMaps[zone][souszone] est le tilemap (list[list[int]]) de la sous-zone en question.

    La tile peut être de différents types :
        0 - Rien, de l'air
        1 - Bloc
        2 - Porte
        3 - Pics (tuent au toucher)
        4 - Blocmouv (Plateformes mouvantes)
      """
    objetsDict = {"blocs":[], "portes":[], "piques":[], "blocmouvs":[], "spawn":[]}
    map_tile = tileMaps[zone]
    for i in range(len(map_tile[souszone])):
        for j in range(len(map_tile[souszone][i])):
            match map_tile[souszone][i][j]:
                    case "b": objetsDict["blocs"].append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).setSprite(blocSprite(map_tile[souszone],i,j)))
                    case "p": objetsDict["portes"].append(Porte(((j-1)*TILE_SIZE,(i-1)*TILE_SIZE), f"{zone}-{souszone}-{i}-{j}"))
                    case "s": objetsDict["piques"].append(Pique((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                    case "m": objetsDict["blocmouvs"].append(BlocMouv((j*TILE_SIZE,i*TILE_SIZE)))
                    case "S": objetsDict["spawn"].append(Spawn((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)))
    return objetsDict




def affichageZone(objetsDict:dict[str,list[Bloc|BlocMouv|Porte|Pique]], screen:py.Surface):
    """
    Affiche tous les objets du dictionnaire sur la surface screen. \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire associant chaque type d'objet à la liste des objets à ajouter.
        \n- screen : la surface (pygame) sur laquelle on affiche les objets
    """
    for objet in objetsDict["blocs"]:
        screen.blit(objet.getSprite().convert_alpha(),objet.topleft)
    for objet in objetsDict["portes"]:
        screen.blit(sprite_porte[int(10*time.time())%len(sprite_porte)].convert_alpha(),objet.getRect().topleft)
    for objet in objetsDict["piques"]:
        screen.blit(sprite_pique.convert_alpha(),objet.topleft)
    for objet in objetsDict["blocmouvs"]:
        py.draw.rect(screen, "blue", objet)
        objet.move()




### TEXTURES ###

def background(ecran:py.Surface,zone):
    match zone:
        case "foret": ecran.blits(((bg_foret_1,(0,0)),(bg_foret_2,(0,0)),(bg_foret_3,(0,0))))


def blocSprite(tileMap,i,j):
    if tileMap[i-1][j] == "b" : # S'il y a un bloc au dessus
        if tileMap[i][j-1] != "b" : return sprite_brique_left # S'il y'a rien à gauche
        elif tileMap[i][(j+1)%len(tileMap[i])] != "b" : return sprite_brique_right # S'il y'a rien à droite
        else :  # S'il y'a un bloc à gauche ET à droite
            if tileMap[i-1][j-1] != "b" : return sprite_brique_topleft_corner  # S'il y'a rien au-dessus à gauche
            elif tileMap[i-1][(j+1)%len(tileMap[i])] != "b" : return sprite_brique_topright_corner # S'il y'a rien au-dessus à droite
            else: return sprite_brique
    else :  # S'il y'a rien au-dessus
        if tileMap[i][j-1] != "b" : return sprite_brique_topleft # S'il y'a rien à gauche
        elif tileMap[i][(j+1)%len(tileMap[i])] != "b" : return sprite_brique_topright # S'il y'a rien à droite
        else : return sprite_brique_top
