import pygame as py
from classes import *
from levels import *
from textures import *

def keybinds(keys):
    """
    Fonction qui gére tous les racourcis clavier (Esc,Tab...)
    """
    if keys[py.K_ESCAPE]:
        py.quit()
    if keys[py.K_TAB]:
        pass                                                  #Pour ouvrir l'inventaire




def collisions(objetsDict:dict[str,list[Bloc|BlocMouv]], j:Joueur):
    """
    Gère les collisions entre le Joueur (j) et l'envirronement (Blocs,Pics...). \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire des objets.
        \n- j : le Joueur.
    """
    joueur_rect = j.getRect()
    
    if j.rect.x + j.rect.width >= SCREEN_WIDTH : j.rect.x = SCREEN_WIDTH - j.rect.width
    if j.rect.x <= 0 : j.rect.x = 0

    for bloc in objetsDict["blocs"]:
        if bloc.colliderect(joueur_rect): 
            # Calcul de l'overlap
            overlap_left = joueur_rect.right - bloc.left      # bloc à droite du joueur
            overlap_right = bloc.right - joueur_rect.left     # bloc à gauche du joueur
            overlap_top = joueur_rect.bottom - bloc.top       # bloc en haut du joueur
            overlap_bottom = bloc.bottom - joueur_rect.top    # bloc en bas du joueur
            
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
            
            if min_overlap == overlap_top:  # Collision par le haut
                j.setY(bloc.top - joueur_rect.height)
                j.setFallState(False) # Reset du saut
                j.setJumpTimer(0)
                j.setFallSpeed(0)
            elif min_overlap == overlap_bottom:  # Collision par le bas
                j.setY(bloc.bottom)
                j.setFallState(True)
            elif min_overlap == overlap_left:  # Collision par la gauche
                j.setX(bloc.left - joueur_rect.width)
            elif min_overlap == overlap_right:  # Collision par la droite
                j.setX(bloc.right)
            
            j.setDashState((DASH_TIMER,"n",j.getDashState()[2]))
            joueur_rect = j.getRect()  # Mise à jour
    
    
    for blocpic in objetsDict["blocpics"]:
        if blocpic.colliderect(joueur_rect):
            py.time.wait(500)            
            joueur_rect = j.getRect()  # Mise à jour      

    if not any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in objetsDict["blocs"]) and j.getJumpTimer() == 0: # Si il n'y a rien sous le joueur -> chute
        if j.getCoyoteTimer() < COYOTE_JUMP_TIME:
            j.setCoyoteTimer(j.getCoyoteTimer()+1)
        else:
            j.setCoyoteTimer(0)
            j.setFallState(True) 

    if any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in objetsDict["blocs"]) and j.getDashState()[0] >= DASH_TIMER:   # Reset dash
        j.setDashState((0,"n",j.getDashState()[2]))  
    
    for blocmouv in objetsDict["blocmouvs"]:
        if blocmouv.getRect().colliderect(joueur_rect):
            # Calcul de l'overlap
            overlap_left = joueur_rect.right - blocmouv.getRect().left      # bloc à droite du joueur
            overlap_right = blocmouv.getRect().right - joueur_rect.left     # bloc à gauche du joueur
            overlap_top = joueur_rect.bottom - blocmouv.getRect().top       # bloc en haut du joueur
            overlap_bottom = blocmouv.getRect().bottom - joueur_rect.top    # bloc en bas du joueur
            
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
            
            if min_overlap == overlap_top:  # Collision par le haut
                j.setY(blocmouv.getRect().top - joueur_rect.height)
                j.setFallState(False) # Reset du saut
                j.setJumpTimer(0)
                j.setFallSpeed(0)
            elif min_overlap == overlap_bottom:  # Collision par le bas
                j.setY(blocmouv.getRect().bottom)
                j.setFallState(True)
            elif min_overlap == overlap_left:  # Collision par la gauche
                j.setX(blocmouv.getRect().left - joueur_rect.width)
            elif min_overlap == overlap_right:  # Collision par la droite
                j.setX(blocmouv.getRect().right)
            joueur_rect = j.getRect()  # Mise à jour 

    if not any(blocmouv.getRect().colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for blocmouv in objetsDict["blocmouvs"]) and j.getJumpTimer() == 0: # Si il n'y a rien sous le joueur -> chute
        if j.getCoyoteTimer() < COYOTE_JUMP_TIME:
            j.setCoyoteTimer(j.getCoyoteTimer()+1)
        else:
            j.setCoyoteTimer(0)
            j.setFallState(True)




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
    objetsDict = {"blocs":[], "portes":[], "blocpics":[], "blocmouvs":[]}
    map_tile = tileMaps[zone]
    for i in range(len(map_tile[souszone])):
        for j in range(len(map_tile[souszone][i])):
            match map_tile[souszone][i][j]:
                    case 1: objetsDict["blocs"].append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                    case 2: objetsDict["portes"].append(Porte(((j-1)*TILE_SIZE,(i-1)*TILE_SIZE), f"{zone}-{souszone}-{i}-{j}"))
                    case 3: objetsDict["blocpics"].append(BlocPic((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                    case 4: objetsDict["blocmouvs"].append(BlocMouv((j*TILE_SIZE,i*TILE_SIZE)))
    return objetsDict




def affichageZone(objetsDict:dict[str,list[Bloc|BlocMouv|Porte]], screen:py.Surface):
    """
    Affiche tous les objets du dictionnaire sur la surface screen. \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire associant chaque type d'objet à la liste des objets à ajouter.
        \n- screen : la surface (pygame) sur laquelle on affiche les objets
    """
    for objet in objetsDict["blocs"]:
        py.draw.rect(screen,"brown",objet)
    for objet in objetsDict["portes"]:
        py.draw.rect(screen,"green",objet)
    for objet in objetsDict["blocpics"]:
        py.draw.rect(screen,"pink",objet)
    for objet in objetsDict["blocmouvs"]:
        py.draw.rect(screen, "blue", objet)
        objet.move()




### TEXTURES ###

def background(ecran:py.Surface,zone):
    match zone:
        case "foret": ecran.blits(((bg_foret_1,(0,0)),(bg_foret_2,(0,0)),(bg_foret_3,(0,0))))
