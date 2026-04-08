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

def collisions(blocs:list[Bloc], blocpics:list[BlocPic], j:Joueur):
    joueur_rect = j.getRect()
    
    for bloc in blocs:
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
            
            joueur_rect = j.getRect()  # Mise à jour
    
    
    for blocpic in blocpics:
        if blocpic.colliderect(joueur_rect):
            py.time.wait(500)            
        
    if not any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in blocs) and j.getJumpTimer() == 0: # Si il n'y a rien sous le joueur -> chute
        if j.getCoyoteTimer() < COYOTE_JUMP_TIME:
            j.setCoyoteTimer(j.getCoyoteTimer()+1)
        else:
            j.setCoyoteTimer(0)
            j.setFallState(True)  
            

def preparationLevel(lvl:int):
    blocs, portes, blocpics = [], [], []
    map_tile = lvl
    for i in range(len(map_tile)):
        for j in range(len(map_tile[i])):
            match map_tile[i][j]:
                case 1: blocs.append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                case 2: portes.append(Porte((j*TILE_SIZE,i*TILE_SIZE)))
                case 3: blocpics.append(BlocPic((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
    return blocs, portes, blocpics

def affichageLevel(blocs, portes, blocpics, screen):
    for objet in blocs:
        py.draw.rect(screen,"brown",objet)
    for objet in portes:
        py.draw.rect(screen,"green",objet)
    for objet in blocpics:
        py.draw.rect(screen,"pink",objet)

def telePorte(portes:list[Porte], j:Joueur, keys):
    for porte in portes:
        if porte.getRect().right - j.getRect().right <= 0 and porte.getRect().right - j.getRect().right >= -TILE_SIZE:
            if keys[py.K_e]:
                py.quit()
        if porte.getRect().top - j.getRect().top <= 0 and porte.getRect().top - j.getRect().top >= -TILE_SIZE:
            if keys[py.K_e]:
                py.quit()
        if porte.getRect().left - j.getRect().left <= 0 and porte.getRect().left - j.getRect().left >= -TILE_SIZE:
            if keys[py.K_e]:
                py.quit()
