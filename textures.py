import pygame as py
from constantes import *

### BACKGROUND ###

bg_foret = py.image.load("./assets/textures/foret/background/bg_vert.png")
bg_foret = py.transform.scale(bg_foret,(SCREEN_WIDTH,SCREEN_HEIGHT))

bg_mer = py.image.load("./assets/textures/mer/background.png")
bg_mer = py.transform.scale(bg_mer,(SCREEN_WIDTH,SCREEN_HEIGHT))

### PERSO PRINCIPAL ###

sprite_idle = py.image.load("./assets/textures/autre/personnage/pose_attente.png")
sprite_saut = py.image.load("./assets/textures/autre/personnage/saut.png")
sprite_base = py.image.load("./assets/textures/autre/personnage/regard_face.png")
sprite_marche = py.image.load_animation("./assets/textures/autre/personnage/marche.gif")
sprite_marche = [s[0] for s in sprite_marche]

### OBJETS ###

sprite_porte = py.image.load_animation("./assets/textures/autre/porte.gif")

sprite_pique = py.image.load("./assets/textures/autre/pique.png")

sprite_panneau_metal = py.image.load("./assets/textures/autre/panneau_metal.png")

sprite_tortue_plastique = py.image.load("./assets/textures/mer/tortuePlastique1.png")
sprite_tortue_sauvee = py.image.load("./assets/textures/mer/tortuePlastique2.png")

sprite_poissons_tl = py.image.load_animation("./assets/textures/mer/poissons_tl.gif")
sprite_poissons_tr = py.image.load_animation("./assets/textures/mer/poissons_tr.gif")
sprite_poissons_bl = py.image.load_animation("./assets/textures/mer/poissons_bl.gif")
sprite_poissons_br = py.image.load_animation("./assets/textures/mer/poissons_br.gif")
sprite_branche_eteint = py.image.load("./assets/textures/foret/spriteBrancheNoFeu.png")
sprite_branche_en_feu = py.image.load("./assets/textures/foret/spriteBrancheFeu.png")
sprite_poissons_blocmouvs = py.image.load_animation("./assets/textures/mer/poissons.gif")

# BLOCS #
tileset_base = py.image.load("./assets/textures/autre/blocBaseTileset.png")
base_tiles = {
    "base" : tileset_base.subsurface(py.Rect(20,0,20,20)),
    "sol" : tileset_base.subsurface(py.Rect(20,40,20,20)),
    "tout_angle_haut" : tileset_base.subsurface(py.Rect(20,40,20,20)),
    "plafond" : tileset_base.subsurface(py.Rect(20,0,20,20)),
    "tout_angle_bas" : tileset_base.subsurface(py.Rect(20,0,20,20)),
    "droite" : tileset_base.subsurface(py.Rect(0,20,20,20)),
    "angle_exte_droite" : tileset_base.subsurface(py.Rect(0,0,20,20)),
    "angle_inte_droite" : tileset_base.subsurface(py.Rect(0,40,20,20)),
    "angle_exte_droite_inver" : tileset_base.subsurface(py.Rect(0,20,20,20)),
    "angle_inte_droite_inver" : tileset_base.subsurface(py.Rect(20,0,20,20)),
    "tout_angle_droite" : tileset_base.subsurface(py.Rect(0,0,20,20)),
    "gauche" : py.transform.flip(tileset_base.subsurface(py.Rect(0,20,20,20)),1,0),
    "angle_exte_gauche" : py.transform.flip(tileset_base.subsurface(py.Rect(0,0,20,20)),1,0),
    "angle_inte_gauche" : py.transform.flip(tileset_base.subsurface(py.Rect(0,40,20,20)),1,0),
    "angle_exte_gauche_inver" : py.transform.flip(tileset_base.subsurface(py.Rect(0,20,20,20)),1,0),
    "angle_inte_gauche_inver" : tileset_base.subsurface(py.Rect(20,0,20,20)),
    "tout_angle_gauche" : py.transform.flip(tileset_base.subsurface(py.Rect(0,0,20,20)),1,0)
}

tileset_jungle = py.image.load("./assets/textures/foret/jungleBlocTileset.png")
jungle_tiles = {
    "base" : tileset_jungle.subsurface(py.Rect(20,0,20,20)),
    "sol" : tileset_jungle.subsurface(py.Rect(20,40,20,20)),
    "tout_angle_haut" : py.transform.rotate(tileset_jungle.subsurface(py.Rect(20,20,20,20)), 270.0),
    "plafond" : py.transform.rotate(tileset_jungle.subsurface(py.Rect(20,40,20,20)),180),
    "tout_angle_bas" : py.transform.rotate(tileset_jungle.subsurface(py.Rect(20,20,20,20)), 90.0),
    "droite" : tileset_jungle.subsurface(py.Rect(0,20,20,20)),
    "angle_exte_droite" : tileset_jungle.subsurface(py.Rect(0,0,20,20)),
    "angle_inte_droite" : tileset_jungle.subsurface(py.Rect(0,40,20,20)),
    "angle_exte_droite_inver" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,0,20,20)),0,1),
    "angle_inte_droite_inver" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,40,20,20)),0,1),
    "tout_angle_droite" : py.transform.flip(tileset_jungle.subsurface(py.Rect(20,20,20,20)),1,0),
    "gauche" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,20,20,20)),1,0),
    "angle_exte_gauche" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,0,20,20)),1,0),
    "angle_inte_gauche" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,40,20,20)),1,0),
    "angle_exte_gauche_inver" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,0,20,20)),1,1),
    "angle_inte_gauche_inver" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,40,20,20)),1,1),
    "tout_angle_gauche" : tileset_jungle.subsurface(py.Rect(20,20,20,20))
}   

tileset_dirt = py.image.load("./assets/textures/foret/blocTileset.png")
dirt_tiles = {
    "base" : tileset_dirt.subsurface(py.Rect(20,0,20,20)),
    "sol" : tileset_dirt.subsurface(py.Rect(20,40,20,20)),
    "tout_angle_haut" : py.transform.rotate(tileset_dirt.subsurface(py.Rect(20,20,20,20)), 270.0),
    "plafond" : py.transform.rotate(tileset_dirt.subsurface(py.Rect(20,40,20,20)),180),
    "tout_angle_bas" : py.transform.rotate(tileset_dirt.subsurface(py.Rect(20,20,20,20)), 90.0),
    "droite" : tileset_dirt.subsurface(py.Rect(0,20,20,20)),
    "angle_exte_droite" : tileset_dirt.subsurface(py.Rect(0,0,20,20)),
    "angle_inte_droite" : tileset_dirt.subsurface(py.Rect(0,40,20,20)),
    "angle_exte_droite_inver" : py.transform.flip(tileset_dirt.subsurface(py.Rect(0,0,20,20)),0,1),
    "angle_inte_droite_inver" : py.transform.flip(tileset_jungle.subsurface(py.Rect(0,40,20,20)),0,1),
    "tout_angle_droite" : py.transform.flip(tileset_dirt.subsurface(py.Rect(20,20,20,20)),1,0),
    "gauche" : py.transform.flip(tileset_dirt.subsurface(py.Rect(0,20,20,20)),1,0),
    "angle_exte_gauche" : py.transform.flip(tileset_dirt.subsurface(py.Rect(0,0,20,20)),1,0),
    "angle_inte_gauche" : py.transform.flip(tileset_dirt.subsurface(py.Rect(0,40,20,20)),1,0),
    "angle_exte_gauche_inver" : py.transform.flip(tileset_dirt.subsurface(py.Rect(0,0,20,20)),1,1),
    "angle_inte_gauche_inver" : py.transform.flip(tileset_dirt.subsurface(py.Rect(0,40,20,20)),1,1),
    "tout_angle_gauche" : tileset_dirt.subsurface(py.Rect(20,20,20,20))
}


tileset_mer = py.image.load("./assets/textures/mer/blocTileset.png")
mer_tiles = {
    "base" : tileset_mer.subsurface(py.Rect(20,0,20,20)),
    "sol" : tileset_mer.subsurface(py.Rect(20,40,20,20)),
    "tout_angle_haut" : py.transform.rotate(tileset_mer.subsurface(py.Rect(20,20,20,20)), 270.0),
    "plafond" : py.transform.rotate(tileset_mer.subsurface(py.Rect(20,40,20,20)),180),
    "tout_angle_bas" : py.transform.rotate(tileset_mer.subsurface(py.Rect(20,20,20,20)), 90.0),
    "droite" : tileset_mer.subsurface(py.Rect(0,20,20,20)),
    "angle_exte_droite" : tileset_mer.subsurface(py.Rect(0,0,20,20)),
    "angle_inte_droite" : tileset_mer.subsurface(py.Rect(0,40,20,20)),
    "angle_exte_droite_inver" : py.transform.flip(tileset_mer.subsurface(py.Rect(0,0,20,20)),0,1),
    "angle_inte_droite_inver" : py.transform.flip(tileset_mer.subsurface(py.Rect(0,40,20,20)),0,1),
    "tout_angle_droite" : py.transform.flip(tileset_mer.subsurface(py.Rect(20,20,20,20)),1,0),
    "gauche" : py.transform.flip(tileset_mer.subsurface(py.Rect(0,20,20,20)),1,0),
    "angle_exte_gauche" : py.transform.flip(tileset_mer.subsurface(py.Rect(0,0,20,20)),1,0),
    "angle_inte_gauche" : py.transform.flip(tileset_mer.subsurface(py.Rect(0,40,20,20)),1,0),
    "angle_exte_gauche_inver" : py.transform.flip(tileset_mer.subsurface(py.Rect(0,0,20,20)),1,1),
    "angle_inte_gauche_inver" : py.transform.flip(tileset_mer.subsurface(py.Rect(0,40,20,20)),1,1),
    "tout_angle_gauche" : tileset_mer.subsurface(py.Rect(20,20,20,20))
}

### ENNEMIS ### 

sprite_requin = py.image.load_animation("./assets/textures/mer/requin.gif")

### BOSS ###

sprite_boss_sun = py.image.load_animation("./assets/textures/foret/boss_soleil.gif")

### DÉCORATIONS ###

sprite_lianes = py.image.load_animation("./assets/textures/autre/lianes.gif")
sprite_brouillard = py.image.load("./assets/textures/ville/brouillard.png")
sprite_algues = py.image.load_animation("./assets/textures/mer/algues.gif")
sprite_maison1 = py.image.load("./assets/textures/ville/maison1.png")
sprite_maison2 = py.image.load("./assets/textures/ville/maison2.png")


##### MISE A ECHELLE #####

sprite_porte = [py.transform.scale(s[0],(2*TILE_SIZE,2*TILE_SIZE)) for s in sprite_porte]
sprite_pique = py.transform.scale(sprite_pique,(TILE_SIZE,TILE_SIZE))
sprite_requin = [py.transform.scale(s[0],(4*TILE_SIZE,2*TILE_SIZE)) for s in sprite_requin]
sprite_lianes = [py.transform.scale(s[0],(TILE_SIZE,2*TILE_SIZE)) for s in sprite_lianes]
sprite_poissons_blocmouvs = [py.transform.scale(s[0],(TILE_SIZE,TILE_SIZE)) for s in sprite_poissons_tl + sprite_poissons_tr + sprite_poissons_bl + sprite_poissons_br]

sprite_boss_sun = [py.transform.scale(s[0],(8*TILE_SIZE,8*TILE_SIZE)) for s in sprite_boss_sun]

sprite_algues = [py.transform.scale(s[0],(TILE_SIZE,2*TILE_SIZE)) for s in sprite_algues]
sprite_tortue_plastique = py.transform.scale(sprite_tortue_plastique,(2*TILE_SIZE,TILE_SIZE))
sprite_tortue_sauvee = py.transform.scale(sprite_tortue_sauvee,(2*TILE_SIZE,TILE_SIZE))
sprite_branche_eteint = py.transform.scale(sprite_branche_eteint, (2*TILE_SIZE, TILE_SIZE))
sprite_branche_en_feu = py.transform.scale(sprite_branche_en_feu, (2*TILE_SIZE, TILE_SIZE))
    

#### DICTIONNAIRES D'ACCES ####

SPRITES_PNJS = {
    "mer-1" : sprite_panneau_metal
}