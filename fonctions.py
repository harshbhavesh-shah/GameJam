import pygame as py

def keybinds(keys):
    """
    Fonction qui gére toutes les racourcis clavier
    """
    if keys[py.K_ESCAPE]:
        py.quit()
    if keys[py.K_TAB]:
        pass    #Pour ouvrir l'inventaire