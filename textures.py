import pygame as py
from constantes import *

### BACKGROUND ###

bg_foret = py.image.load("./assets/textures/foret/background/bg_vert.png")
bg_foret = py.transform.scale(bg_foret,(SCREEN_WIDTH,SCREEN_HEIGHT))

bg_mer = py.image.load("./assets/textures/mer/background.png")
bg_mer = py.transform.scale(bg_mer,(SCREEN_WIDTH,SCREEN_HEIGHT))

bg_ville = py.image.load("./assets/textures/ville/background.png")
bg_ville = py.transform.scale(bg_ville,(SCREEN_WIDTH,SCREEN_HEIGHT))

### PERSO PRINCIPAL ###

sprites_perso_hub = {
    "idle" :py.image.load("./assets/textures/autre/personnage/hub/pose_attente.png"),
    "saut" : py.image.load("./assets/textures/autre/personnage/hub/saut.png"),
    "base" : py.image.load("./assets/textures/autre/personnage/hub/regard_face.png"),
    "marche" : [s[0] for s in py.image.load_animation("./assets/textures/autre/personnage/hub/marche.gif")]
}

sprites_perso_mer = {
    "idle" :py.image.load("./assets/textures/autre/personnage/mer/pose_attente.png"),
    "saut" : py.image.load("./assets/textures/autre/personnage/mer/saut.png"),
    "base" : py.image.load("./assets/textures/autre/personnage/mer/regard_face.png"),
    "marche" : [s[0] for s in py.image.load_animation("./assets/textures/autre/personnage/mer/marche.gif")]
}

sprites_perso_foret = {
    "idle" :py.image.load("./assets/textures/autre/personnage/foret/pose_attente.png"),
    "saut" : py.image.load("./assets/textures/autre/personnage/foret/saut.png"),
    "base" : py.image.load("./assets/textures/autre/personnage/foret/regard_face.png"),
    "marche" : [s[0] for s in py.image.load_animation("./assets/textures/autre/personnage/foret/marche.gif")]
}

sprites_perso_colline = {
    "idle" :py.image.load("./assets/textures/autre/personnage/colline/pose_attente.png"),
    "saut" : py.image.load("./assets/textures/autre/personnage/colline/saut.png"),
    "base" : py.image.load("./assets/textures/autre/personnage/colline/regard_face.png"),
    "marche" : [s[0] for s in py.image.load_animation("./assets/textures/autre/personnage/colline/marche.gif")]
}

### OBJETS ###

sprite_porte = py.image.load_animation("./assets/textures/autre/porte.gif")

sprite_pique = py.image.load("./assets/textures/autre/pique.png")

sprite_panneau_metal = py.image.load("./assets/textures/autre/panneau_metal.png")
sprite_pnj = py.image.load("./assets/textures/autre/pnjs/pnj1.png")

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

tileset_invis = py.image.load("./assets/textures/ville/bloc2Tileset.png")
invis_tiles = {
   "base" : tileset_invis.subsurface(py.Rect(20,0,20,20)),
    "sol" : tileset_invis.subsurface(py.Rect(20,40,20,20)),
    "tout_angle_haut" : py.transform.rotate(tileset_invis.subsurface(py.Rect(20,20,20,20)), 270.0),
    "plafond" : py.transform.rotate(tileset_invis.subsurface(py.Rect(20,40,20,20)),180),
    "tout_angle_bas" : py.transform.rotate(tileset_invis.subsurface(py.Rect(20,20,20,20)), 90.0),
    "droite" : tileset_invis.subsurface(py.Rect(0,20,20,20)),
    "angle_exte_droite" : tileset_invis.subsurface(py.Rect(0,0,20,20)),
    "angle_inte_droite" : tileset_invis.subsurface(py.Rect(0,40,20,20)),
    "angle_exte_droite_inver" : py.transform.flip(tileset_invis.subsurface(py.Rect(0,0,20,20)),0,1),
    "angle_inte_droite_inver" : py.transform.flip(tileset_invis.subsurface(py.Rect(0,40,20,20)),0,1),
    "tout_angle_droite" : py.transform.flip(tileset_invis.subsurface(py.Rect(20,20,20,20)),1,0),
    "gauche" : py.transform.flip(tileset_invis.subsurface(py.Rect(0,20,20,20)),1,0),
    "angle_exte_gauche" : py.transform.flip(tileset_invis.subsurface(py.Rect(0,0,20,20)),1,0),
    "angle_inte_gauche" : py.transform.flip(tileset_invis.subsurface(py.Rect(0,40,20,20)),1,0),
    "angle_exte_gauche_inver" : py.transform.flip(tileset_invis.subsurface(py.Rect(0,0,20,20)),1,1),
    "angle_inte_gauche_inver" : py.transform.flip(tileset_invis.subsurface(py.Rect(0,40,20,20)),1,1),
    "tout_angle_gauche" : tileset_invis.subsurface(py.Rect(20,20,20,20))
}

tileset_BM_colline = py.image.load("./assets/textures/colline/blocMouv.png")
colline_BM_tiles = {
    "base" : tileset_BM_colline.subsurface(py.Rect(20,0,20,20)),
    "sol" : tileset_BM_colline.subsurface(py.Rect(20,40,20,20)),
    "tout_angle_haut" : py.transform.rotate(tileset_BM_colline.subsurface(py.Rect(20,20,20,20)), 270.0),
    "plafond" : py.transform.rotate(tileset_BM_colline.subsurface(py.Rect(20,40,20,20)),180),
    "tout_angle_bas" : py.transform.rotate(tileset_BM_colline.subsurface(py.Rect(20,20,20,20)), 90.0),
    "droite" : tileset_BM_colline.subsurface(py.Rect(0,20,20,20)),
    "angle_exte_droite" : tileset_BM_colline.subsurface(py.Rect(0,0,20,20)),
    "angle_inte_droite" : tileset_BM_colline.subsurface(py.Rect(0,40,20,20)),
    "angle_exte_droite_inver" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(0,0,20,20)),0,1),
    "angle_inte_droite_inver" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(0,40,20,20)),0,1),
    "tout_angle_droite" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(20,20,20,20)),1,0),
    "gauche" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(0,20,20,20)),1,0),
    "angle_exte_gauche" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(0,0,20,20)),1,0),
    "angle_inte_gauche" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(0,40,20,20)),1,0),
    "angle_exte_gauche_inver" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(0,0,20,20)),1,1),
    "angle_inte_gauche_inver" : py.transform.flip(tileset_BM_colline.subsurface(py.Rect(0,40,20,20)),1,1),
    "tout_angle_gauche" : tileset_BM_colline.subsurface(py.Rect(20,20,20,20))
}   
sprite_BT_ville = py.image.load("./assets/textures/ville/blocTombant.png")

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
sprite_nuage = py.image.load("./assets/textures/ville/nuage.png")


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
    "hub-1" : sprite_pnj,
    "hub-4" : sprite_panneau_metal,
    "mer-1" : sprite_panneau_metal
}