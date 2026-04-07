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
        pass    #Pour ouvrir l'inventaire

def collisions(blocs:list[Bloc],j:Joueur):
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
            elif min_overlap == overlap_bottom:  # Collision par le bas
                j.setY(bloc.bottom)
            elif min_overlap == overlap_left:  # Collision par la gauche
                j.setX(bloc.left - joueur_rect.width)
            elif min_overlap == overlap_right:  # Collision par la droite
                j.setX(bloc.right)
            
            joueur_rect = j.getRect()  # Mise à jour
            

def defgrille(lvl:int):
    blocs, portes = [], []
    map_tile = level1[lvl]
    for i in range(len(map_tile)):
        for j in range(len(map_tile[i])):
            match map_tile[i][j]:
                case 1: blocs.append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                case 2: portes.append(Porte((j*TILE_SIZE,i*TILE_SIZE)))
    return blocs, portes

def teleporte(portes:list[Porte], j:Joueur, keys):
    for porte in portes:
        if porte.colliderect(j.getRect()):
            if keys[py.K_e]:
                py.quit()
