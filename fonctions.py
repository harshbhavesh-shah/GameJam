import pygame as py
from classes import *
from levels import *

def keybinds(keys):
    """
    Fonction qui gére toutes les racourcis clavier
    """
    if keys[py.K_ESCAPE]:
        py.quit()
    if keys[py.K_TAB]:
        pass                                                  #Pour ouvrir l'inventaire

def collisions(dictDonnees, j:Joueur):
    joueur_rect = j.getRect()
    
    for bloc in dictDonnees["blocs"]:
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
    
    
    for blocpic in dictDonnees["blocpics"]:
        if blocpic.colliderect(joueur_rect):
            py.time.wait(500)            
            joueur_rect = j.getRect()  # Mise à jour      

    if not any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in dictDonnees["blocs"]) and j.getJumpTimer() == 0: # Si il n'y a rien sous le joueur -> chute
        if j.getCoyoteTimer() < COYOTE_JUMP_TIME:
            j.setCoyoteTimer(j.getCoyoteTimer()+1)
        else:
            j.setCoyoteTimer(0)
            j.setFallState(True) 

    if any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in dictDonnees["blocs"]) and j.getDashState()[0] >= DASH_TIMER:   # Reset dash
        j.setDashState((0,"n",j.getDashState()[2]))  
    
    for blocmouv in dictDonnees["blocmouvs"]:
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
    if not any(blocmouv.getRect().colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for blocmouv in dictDonnees["blocmouvs"]) and j.getJumpTimer() == 0: # Si il n'y a rien sous le joueur -> chute
        if j.getCoyoteTimer() < COYOTE_JUMP_TIME:
            j.setCoyoteTimer(j.getCoyoteTimer()+1)
        else:
            j.setCoyoteTimer(0)
            j.setFallState(True)

def preparationLevel(zone:dict, level:int, souszone:int):
    dictDonnees = {"blocs":[], "portes":[], "blocpics":[], "blocmouvs":[]}
    map_tile = zone[level]
    for i in range(len(map_tile[souszone])):
        for j in range(len(map_tile[souszone][i])):
            match map_tile[souszone][i][j]:
                    case 1: dictDonnees["blocs"].append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                    case 2: dictDonnees["portes"].append(Porte(((j-1)*TILE_SIZE,(i-1)*TILE_SIZE), f"{zone}-{souszone}"))
                    case 3: dictDonnees["blocpics"].append(BlocPic((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                    case 4: dictDonnees["blocmouvs"].append(BlocMouv((j*TILE_SIZE,i*TILE_SIZE)))
    return dictDonnees

def affichageLevel(dictDonnees, screen):
    for objet in dictDonnees["blocs"]:
        py.draw.rect(screen,"brown",objet)
    for objet in dictDonnees["portes"]:
        py.draw.rect(screen,"green",objet)
    for objet in dictDonnees["blocpics"]:
        py.draw.rect(screen,"pink",objet)
    for  objet in dictDonnees["blocmouvs"]:
        py.draw.rect(screen, "blue", objet)
        objet.move()

def telePorte(souszone:int, level:int):
    return preparationLevel(niveaux, level, souszone)

