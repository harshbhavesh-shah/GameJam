import pygame as py
from classes import *

def keybinds(keys):
    """
    Fonction qui gére toutes les racourcis clavier
    """
    if keys[py.K_ESCAPE]:
        py.quit()
    if keys[py.K_TAB]:
        pass    #Pour ouvrir l'inventaire

def collisions(blocs:list[Bloc],j:Joueur):
    for bloc in blocs:
        if bloc.colliderect(j.getRect()):

            if bloc.x > j.getX() :  # bloc à droite
                j.setX(bloc.x - j.getRect().width)
            if bloc.x < j.getX() :  # bloc à gauche
                j.setX(bloc.x + bloc.width)
            if bloc.y > j.getY() :  # bloc en bas
                j.setY(bloc.y - j.getRect().height)
            if bloc.y < j.getY() :  # bloc en haut
                j.setY(bloc.y + bloc.height)