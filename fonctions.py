import pygame as py
import pygame_widgets as pw
from pygame_widgets.slider import Slider
from pygame_widgets.progressbar import ProgressBar
from classes import *
from levels import *
from textures import *
from random import *
import time
import copy

def keybinds(screen,keys):
    """
    Fonction qui gére tous les racourcis clavier (Esc,Tab...)
    """
    if keys[py.K_ESCAPE]:
        menuPause(screen)


### FONCTIONNEMENT DU JEU ###

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



def collisions(objetsDict:dict[str,list[Bloc|BlocMouv]], j:Joueur, zone_souszone:tuple):
    """
    Gère les collisions entre le Joueur (j) et l'envirronement (Blocs,Pics...). \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire des objets.
        \n- j : le Joueur.
    """
    joueur_rect = j.getRect()

    for bloc in objetsDict["blocs"] + objetsDict["blocmouvs"] + objetsDict["bloctombants"]:
        if bloc.colliderect(joueur_rect): 
            collisionsBlocJoueur(joueur_rect,bloc,j)
            if isinstance(bloc,BlocTombant): 
                for blocT in objetsDict["bloctombants"]:
                    if blocT.getLabel() == bloc.getLabel() : blocT.activeDelay()


    for blocpic in objetsDict["piques"]:
        if blocpic.colliderect(joueur_rect):
            py.time.wait(150)   
            objetsDict.update(dead(zone_souszone[0], zone_souszone[1], j, objetsDict))
    
    for ennemi in objetsDict["ennemis"]:
        if ennemi.colliderect(joueur_rect):
            py.time.wait(150)   
            objetsDict.update(dead(zone_souszone[0], zone_souszone[1], j, objetsDict))

    # Coyote et dash
    if (not any(bloc.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for bloc in objetsDict["blocs"]) 
        or not any(blocmouv.colliderect(py.Rect(joueur_rect.topleft,(joueur_rect.width,joueur_rect.height+1))) for blocmouv in objetsDict["blocmouvs"])) and j.getJumpTimer() == 0: # Si il n'y a rien sous le joueur -> chute
        if j.getCoyoteTimer() < COYOTE_JUMP_TIME:
            j.setCoyoteTimer(j.getCoyoteTimer()+1)
        else:
            j.setCoyoteTimer(0)
            j.setFallState(True)

        if j.getDashState()[0] >= DASH_TIMER: j.setDashState((0,"n",j.getDashState()[2])) 
    




def switchSousZone(zone:str,souszone:int,joueur:Joueur,objetsDict:dict):
    """
    Téléporte le joueur à la prochaine sous-zone s'il sors de l'écran.
    """
    level = f"{zone}-{souszone}"

    if joueur.getRect().x + joueur.getRect().width > SCREEN_WIDTH:
        if souszone+1 in tileMaps[zone].keys():
            objetsDict = preparationZone(zone,souszone+1)
            joueur.setXY(objetsDict["spawn"][0].x,objetsDict["spawn"][0].y)
            return objetsDict , souszone+1
        joueur.setX(SCREEN_WIDTH-joueur.getRect().width)

    if joueur.getRect().x < 0:
        if souszone-1 in tileMaps[zone].keys():
            objetsDict = preparationZone(zone,souszone-1)
            joueur.setXY(objetsDict["end"][0].x,objetsDict["end"][0].y)
            return objetsDict , souszone-1
        joueur.setX(0)
        
    return objetsDict , souszone



def telePorte(objetsDict:dict[str,list[Bloc|BlocMouv|Porte]],zone,souszone,joueur:Joueur):
    for porte in objetsDict["portes"]:
            if porte.colliderect(joueur.getRect()):
                if joueur.getInteractionCooldown() > 0:
                    break
                destination_id = PORTES_CORRESPONDANCES.get(porte.getId())
                zone , souszone , y , x = destination_id.split('-')[0] , int(destination_id.split('-')[1]) , int(destination_id.split('-')[2]) , int(destination_id.split('-')[3])
                objetsDict = preparationZone(zone,souszone)
                joueur.setXY(x*TILE_SIZE,y*TILE_SIZE)
                joueur.setInteractionCooldown(INTERACTION_COOLDOWN)
                joueur.setDir('n') 
                musique(zone)
                break
    return objetsDict , zone , souszone


def discussion(screen:py.Surface,pnj:PNJ,joueur:Joueur):
    index = 0
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:  # KEYDOWN = appui unique, pas maintenu
                    menuPause(screen)
                if event.key == py.K_e:
                    index += 1
        
        if index == len(pnj.getTexte()) :
            joueur.setInteractionCooldown(INTERACTION_COOLDOWN)
            break
        
        # Bordure et remplissage
        bordure_texte = py.draw.rect(screen,"black",py.Rect(50, SCREEN_HEIGHT - 200, TEXT_BOX_WIDTH, 150), border_radius=3)
        py.draw.rect(screen,"gray70",remplissageRect(bordure_texte,3), border_radius=3)
        bordure_nom = py.draw.rect(screen,"black",py.Rect(bordure_texte.left - 30, bordure_texte.top - 30, NAME_BOX_WIDTH , 50), border_radius=3)
        py.draw.rect(screen,"gray80",remplissageRect(bordure_nom,3), border_radius=3)

        affichageTexte(screen, pnj.getNom(), bordure_nom.center, 25, "black")
        affichageTexteWrap(screen, pnj.getLine(index), bordure_texte, py.font.SysFont("Arial",50), 50, "black")
        affichageTexte(screen, "Appuyez sur E", (bordure_texte.right - 45, bordure_texte.bottom - 15), 15, "black")
        py.display.flip()



def preparationZone(zone:str, souszone:int) -> dict[str,list[Bloc|BlocMouv|Porte|Pique|Ennemi|PNJ|Levier|BlocTombant]]:
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
    objetsDict = {"blocs":[], "portes":[], "piques":[], "blocmouvs":[], "spawn":[], "end":[], "ennemis":[], "pnjs": [], "decorations":[], "leviers":[] , "bloctombants":[], "bosssoleil":None}
    map_tile = tileMaps[zone]
    for i in range(len(map_tile[souszone])):
        for j in range(len(map_tile[souszone][i])):
            match map_tile[souszone][i][j]:
                case "b": objetsDict["blocs"].append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).setSprite(blocSprite(zone,souszone,i,j,1)))
                case "B": objetsDict["blocs"].append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).setSprite(blocSprite(zone,souszone,i,j,2)))
                case "p": objetsDict["portes"].append(Porte((((j-1)*TILE_SIZE,(i-1)*TILE_SIZE),(4*TILE_SIZE,2*TILE_SIZE))).setId(f"{zone}-{souszone}-{i}-{j}").setSprite(sprite_porte))
                case "s": objetsDict["piques"].append(Pique((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).setSprite(sprite_pique))
                case "m": objetsDict["blocmouvs"].append(BlocMouv((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).setSprite(blocSprite(zone,souszone,i,j,3)))
                case "S": objetsDict["spawn"].append(Spawn((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)))
                case "E": objetsDict["end"].append(End((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)))
                case "P": 
                    try : objetsDict["pnjs"].append(PNJ((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)).setSprite(SPRITES_PNJS[f"{zone}-{souszone}"]).init_file(f"{zone}-{souszone}"))
                    except : objetsDict["pnjs"].append(PNJ((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)).setSprite(None).init_file(f"{zone}-{souszone}"))

                case "e": 
                    match zone:
                        case "mer" : objetsDict["ennemis"].append(Ennemi((j*TILE_SIZE,i*TILE_SIZE),(3*TILE_SIZE,TILE_SIZE+1)).setSpeed(1).setMouvement("oaaaaaaaaaaeaaaaaaaaaa").setType("requin"))
                        case _ : pass

                case "d": 
                    match zone:
                        case "mer" : objetsDict["decorations"].append(Decoration((j*TILE_SIZE,(i-1)*TILE_SIZE),(TILE_SIZE,2*TILE_SIZE)).setSprite(sprite_algues))
                        case "ville" : objetsDict["decorations"].append(Decoration((j*TILE_SIZE,(i-1)*TILE_SIZE),(TILE_SIZE,2*TILE_SIZE)).setSprite(sprite_nuage))
                        case _ : objetsDict["decorations"].append(Decoration((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,2*TILE_SIZE)).setSprite(sprite_lianes[(i+j)%2]))
                
                case "l": 
                    match zone:
                        case "foret" : objetsDict["leviers"].append(Levier(((j-1)*TILE_SIZE,i*TILE_SIZE), (2*TILE_SIZE,TILE_SIZE)).setSprite(sprite_branche_en_feu).setEstActif(False).setActifSprite(sprite_branche_eteint))
                        case "mer" : objetsDict["leviers"].append(Levier(((j-1)*TILE_SIZE,i*TILE_SIZE), (2*TILE_SIZE,TILE_SIZE)).setSprite(sprite_tortue_plastique).setEstActif(False).setActifSprite(sprite_tortue_sauvee))
                        case _ : pass 

                case "T": 
                    match zone:
                        case "ville" : objetsDict["bloctombants"].append(BlocTombant((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).init().setSpeed(BTOMBANT_SPEED).setMouvement("saaaaaaaaaaa").setSprite(sprite_BT_ville).saveState())
                        case _ : objetsDict["bloctombants"].append(BlocTombant((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).init().setSpeed(BTOMBANT_SPEED).setMouvement("saaaaaaaaaaa").saveState())

                case "F": objetsDict["bosssoleil"] = BossSoleil((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).init()

                case "M1": objetsDict["decorations"].append(Decoration(((j-4)*TILE_SIZE,(i-11)*TILE_SIZE),(6*TILE_SIZE,12*TILE_SIZE)).setSprite(sprite_maison1))
                case "M2": objetsDict["decorations"].append(Decoration(((j-4)*TILE_SIZE,(i-14)*TILE_SIZE),(6*TILE_SIZE,15*TILE_SIZE)).setSprite(sprite_maison2))


    groupe_blocmouvs(objetsDict["blocmouvs"],zone,souszone)
    groupe_blocmouvs(objetsDict["bloctombants"],zone,souszone)
    return objetsDict






def affichageZone(objetsDict:dict[str,list[Bloc|BlocMouv|Porte|Pique|Ennemi|PNJ|Levier|BlocTombant|BossSoleil]], screen:py.Surface, zone):
    """
    Affiche tous les objets du dictionnaire sur la surface screen. \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire associant chaque type d'objet à la liste des objets à ajouter.
        \n- screen : la surface (pygame) sur laquelle on affiche les objets
    """
    for bloc in objetsDict["blocs"]:
        screen.blit(bloc.getSprite().convert_alpha(),bloc.topleft)

    for porte in objetsDict["portes"]:
        screen.blit(porte.getSprite()[int(10*time.time())%len(porte.getSprite())].convert_alpha(),porte.topleft)

    for pique in objetsDict["piques"]:
        screen.blit(pique.getSprite().convert_alpha(),pique.topleft)

    for deco in objetsDict["decorations"]:
        match zone:
            case "mer" : screen.blit(deco.getSprite()[(deco.left//TILE_SIZE + int(5*time.time())) %len(deco.getSprite())], deco.topleft)
            case _ : screen.blit(deco.getSprite().convert_alpha(),deco.topleft) 

    for bmouv in objetsDict["blocmouvs"]:
        match zone:
            case "mer" : # 0: tl, 1: tr, 2: bl, 3: br
                sprite_index = ((bmouv.default_pos[1] // TILE_SIZE) % 2 * 2 + (bmouv.default_pos[0] // TILE_SIZE) % 2) * 2 + int(10 * time.time()) %2 # Magie noire
                screen.blit(sprite_poissons_blocmouvs[sprite_index].convert_alpha(),bmouv.topleft)
            case _ : 
                screen.blit(bmouv.getSprite(),bmouv.topleft)
        bmouv.move()
    
    for ennemi in objetsDict["ennemis"]:
        match ennemi.getType():
            case "requin" : 
                if ennemi.getOrientation() == "e": screen.blit(py.transform.flip(sprite_requin[int(10*time.time())%len(sprite_requin)].convert_alpha(),1,0),(ennemi.left-(0.5*TILE_SIZE),ennemi.top-(0.5*TILE_SIZE)))
                else : screen.blit(sprite_requin[int(10*time.time())%len(sprite_requin)].convert_alpha(),(ennemi.left-(0.5*TILE_SIZE),ennemi.top-(0.5*TILE_SIZE))) # Fix hitbox ^
        ennemi.move()
    
    if objetsDict["bosssoleil"] is not None:
        screen.blit(sprite_boss_sun[int(10*time.time())%len(sprite_boss_sun)].convert_alpha(),objetsDict["bosssoleil"].topleft)

    for pnj in objetsDict["pnjs"]:
        if pnj.getSprite() is not None:
            sprite = pnj.getSprite()
            x = pnj.x
            y = pnj.bottom - sprite.get_height()  # aligne le bas du sprite avec le bas de la hitbox
            screen.blit(sprite, (x, y))
        else:
            py.draw.rect(screen, "green", pnj)

    for levier in objetsDict["leviers"]:
        screen.blit(levier.getSprite(),levier)

    for btombant in objetsDict["bloctombants"]:
        try: screen.blit(btombant.getSprite(),btombant)
        except: py.draw.rect(screen, "orange", btombant)

        if btombant.getActif(): btombant.incrCompteur()
        if btombant.getCompteur() >= BTOMBANT_DELAY:
            btombant.move()
        if btombant.getCompteur() >= BTOMBANT_RESPAWN_TIMER:
            btombant.loadSavedState()


def degatsEnvironnementauxColline(j:Joueur,objets:dict):
    """
    Dans la zone ville, inflige des dégats si à découvert:\n
    Crée un rect au dessus du joueur allant jusqu'en haut de l'écran 
    et inflige des dégats si il ne détecte aucune collision (soigne sinon)
    """

    blocDetectionRect = py.Rect(j.getRect().centerx-10, j.getY()-SCREEN_HEIGHT, 20, SCREEN_HEIGHT)
    
    isColliding = False
    for typeObjet in objets.keys():
        if objets[typeObjet] is None: continue
        for objet in objets[typeObjet]:

            objetCopie = copy.copy(objet)

            if isinstance(objet,(PNJ,Porte)):
                continue
            if blocDetectionRect.colliderect(objetCopie):    # Dérivés de py.rect
                isColliding = True
                
    if not isColliding:
        j.setHp(j.getHp()-VILLE_DPS)
    
    else:
        j.setHp(min(100,j.getHp()+VILLE_HEAL))


def dead(zone, souszone, joueur:Joueur, objetsDict:dict):    #Permet de recharger entièrement la page si le joueur meurt
    objetsDict = preparationZone(zone, souszone)
    joueur.setFallSpeed(0)
    joueur.setXY(objetsDict["spawn"][0].right-joueur.getRect().width, objetsDict["spawn"][0].bottom-joueur.getRect().height)
    return objetsDict




def groupe_blocmouvs(liste:list[BlocMouv],zone,souszone):
    if not liste:
        return

    blocs_par_position = {(bloc.x, bloc.y): bloc for bloc in liste}
    vus = []

    for bloc in liste:
        position = (bloc.x, bloc.y)
        if position in vus:
            continue

        groupe = []
        pile = [position]

        while pile:
            x, y = pile.pop()
            if (x, y) in vus or (x, y) not in blocs_par_position:
                continue

            vus.append((x, y))
            groupe.append(blocs_par_position[(x, y)])

            for voisin in ((x - TILE_SIZE, y), (x + TILE_SIZE, y), (x, y - TILE_SIZE), (x, y + TILE_SIZE)):
                if voisin not in vus and voisin in blocs_par_position:
                    pile.append(voisin)


        if isinstance(bloc,BlocTombant):
            for bloc_du_groupe in groupe:
                bloc_du_groupe.setLabel(f"{zone}-{souszone}-{bloc.y//TILE_SIZE}-{bloc.x//TILE_SIZE}")

        elif isinstance(bloc,BlocMouv):
            mouvement = None
            speed = None

            for bloc_du_groupe in groupe:
                if MOUVEMENTS_BLOCMOUVS[f"{zone}-{souszone}-{bloc_du_groupe.y//TILE_SIZE}-{bloc_du_groupe.x//TILE_SIZE}"]:
                    mouvement = MOUVEMENTS_BLOCMOUVS[f"{zone}-{souszone}-{bloc_du_groupe.y//TILE_SIZE}-{bloc_du_groupe.x//TILE_SIZE}"][0]
                    speed =  MOUVEMENTS_BLOCMOUVS[f"{zone}-{souszone}-{bloc_du_groupe.y//TILE_SIZE}-{bloc_du_groupe.x//TILE_SIZE}"][1]
                    break

            for bloc_du_groupe in groupe:
                bloc_du_groupe.setSpeed(speed)
                bloc_du_groupe.setMouvement(mouvement)
        


def presenceSoleil(objetsDict:dict):
    if (all(elt.getEstActif() == True for elt in objetsDict["leviers"]) and (objetsDict["bosssoleil"] is not None)):
        objetsDict["bosssoleil"] = None
        return False
    return True

def actifFire(objetsDict:dict):
    if objetsDict["bosssoleil"] is not None:
        if presenceSoleil(objetsDict):
            if SPAWN_FIRE_TREE_COOLDOWN > objetsDict["bosssoleil"].getCompteur(): objetsDict["bosssoleil"].incrCompteur()
            else:
                if objetsDict.get("leviers"):
                    enFeu = []
                    for j in objetsDict["leviers"]:
                        if j.getEstActif() == True:
                            enFeu.append(j)
                    i = randint(0, len(enFeu) - 1)
                    lev = objetsDict["leviers"][i]
                    lev.setEstActif(False)
                    lev.setSprite(sprite_branche_en_feu)
                    objetsDict["leviers"][i].update(lev)
                objetsDict["bosssoleil"].resetCompteur()
    return objetsDict
    
### TEXTURES ###

def background(ecran:py.Surface,zone):
    match zone:
        #case "hub" : ecran.blit(bg_hub)  #background pas adapté...
        case "foret": ecran.blit(bg_foret)
        case "mer" : ecran.blit(bg_mer)
        case "ville" : ecran.blit(bg_ville)
        case "colline" : ecran.blit(bg_colline)
        case _ : ecran.fill("darkblue")


def blocSprite(zone,souszone,i,j,type):
    tileMap = tileMaps[zone][souszone]

    if type == 1:
        bloc = "b"
        match zone:
            case "hub" : sprites = base_tiles
            case "foret": sprites = jungle_tiles
            case "mer": sprites = mer_tiles
            case _ : sprites = base_tiles
    elif type == 2:
        bloc = "B"
        match zone:
            case "foret": sprites = dirt_tiles
            case "ville": sprites = invis_tiles
            case _ : sprites = base_tiles
    elif type == 3:
        bloc = "m"
        match zone:
            case "mer" : return sprite_nuage # placeholder
            case _ : sprites = colline_BM_tiles

    if tileMap[i-1][j] == bloc : # s'il y a un bloc au dessus
        if tileMap[i][j-1] == bloc : # s'il y'a un bloc à gauche
            if tileMap[i-1][j-1] == bloc: # s'il y'a un bloc en diagonale gauche
                if tileMap[i][(j+1)%len(tileMap[0])] == bloc: # s'il y'a un bloc à droite
                    if tileMap[i-1][(j+1)%len(tileMap[0])] == bloc: #s'il y'a un bloc en diagonale droite
                        if tileMap[(i+1)%len(tileMap)][j] == bloc: # s'il y'a un bloc en dessus
                            if tileMap[(i+1)%len(tileMap)][(j+1)%len(tileMap[0])] != bloc : # s'il n'y'a pas de bloc en diagonale bas droite
                                return sprites["angle_inte_droite_inver"]
                            if tileMap[(i+1)%len(tileMap)][j-1] != bloc : # s'il n'y'a pas de bloc en diagonale bas gauche
                                return sprites["angle_inte_gauche_inver"]
                            return sprites["base"] # s'il y'a des blocs tout autour du bloc
                        else: return sprites["plafond"] # s'il n'y'a pas de bloc en dessus
                    else: return sprites["angle_inte_droite"]
                else: # s'il y'a pas de bloc à droite
                    if tileMap[(i+1)%len(tileMap)][j] == bloc: return sprites["droite"] # s'il y'a un bloc en dessus
                    else: return sprites["angle_exte_droite_inver"]
            else: return sprites["angle_inte_gauche"] # s'il n'y a pas de bloc en diagonale gauche
        else: 
            if tileMap[i][(j+1)%len(tileMap[0])] == bloc: #s'il y'a un bloc à droite
                if tileMap[(i+1)%len(tileMap)][j] == bloc: # s'il y'a un bloc en dessus
                    return sprites["gauche"]
                else:
                    return sprites["angle_exte_gauche_inver"]
            else:
                return sprites["tout_angle_bas"]
    else:
        if tileMap[i][(j+1)%len(tileMap[0])] == bloc: # s'il y'a un bloc à droite
            if tileMap[i][j-1] == bloc : #s'il y'a un bloc a gauche
                return sprites["sol"]
            else:
                if tileMap[(i+1)%len(tileMap)][j] == bloc: #s'il y'a un bloc en dessous
                    return sprites["angle_exte_gauche"]
                else:
                    return sprites["tout_angle_gauche"]
        else:
            if tileMap[i][j-1] == bloc : #s'il y'a un bloc a gauche
                return sprites["angle_exte_droite"] 
            else:
                return sprites["tout_angle_haut"]
        


def anim_perso(j:Joueur,zone:str):
    match zone:
        case "mer" : sprites_perso = sprites_perso_mer
        case "foret" : sprites_perso = sprites_perso_foret
        case "colline" : sprites_perso = sprites_perso_colline
        case _ : sprites_perso = sprites_perso_hub

    if j.getDir() == 'n' : return sprites_perso["base"]       # Spawn
    
    elif j.getJumpTimer() != 0 :                      # Saut
        if j.getDir() == 'd' : return sprites_perso["saut"]     # droite
        else : return py.transform.flip(sprites_perso["saut"] ,1,0)    # gauche
    
    elif j.isWalking:   # Marche
        if j.getDir() == 'd' : return sprites_perso["marche"][int(10*time.time()) % len(sprites_perso["marche"])]     # droite
        else : return py.transform.flip(sprites_perso["marche"][int(10*time.time()) % len(sprites_perso["marche"])],1,0)    # gauche

    elif j.getDir() == 'd' : return sprites_perso["idle"]
    else : return py.transform.flip(sprites_perso["idle"],1,0)


### OPTIONS / MENUS ###

def musique(zone:str):
    match zone:
        case "foret" : py.mixer_music.load("./assets/sons/music_foret.mp3")
        case "mer" : py.mixer_music.load("./assets/sons/music_mer.mp3")
        case "ville" : py.mixer_music.load("./assets/sons/music_ville.mp3")
        case "colline" : py.mixer_music.load("./assets/sons/music_colline.mp3")
        case _ : py.mixer_music.load("./assets/sons/music_hub.mp3")
    py.mixer_music.play(-1)

def menuPause(screen:py.Surface,parametres:Settings):
    """
    Affichage du menu pause et gestion de ses fonctionnalités
    """
    pause = True
    while pause:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:  # KEYDOWN = appui unique, pas maintenu
                    pause = False

        fond_pause = py.draw.rect(screen,"black",py.Rect(SCREEN_WIDTH//2-150,150,300,SCREEN_HEIGHT-300), border_radius=3)
        py.draw.rect(screen,"gray",remplissageRect(fond_pause), border_radius=3)
        affichageTexte(screen,"PAUSE",(fond_pause.centerx,fond_pause.top + 40),50)


        bt_continuer = py.draw.rect(screen,"green",py.Rect(fond_pause.centerx-130,fond_pause.top+100,260,50))
        bt_parametres = py.draw.rect(screen,"green",py.Rect(fond_pause.centerx-130,fond_pause.top+200,260,50))
        bt_quitter = py.draw.rect(screen,"green",py.Rect(fond_pause.centerx-130,fond_pause.top+300,260,50))
        affichageTexte(screen,"Continuer",bt_continuer.center)
        affichageTexte(screen,"Paramètres",bt_parametres.center)
        affichageTexte(screen,"Quitter",bt_quitter.center)

        if py.mouse.get_just_pressed()[0]:
            if bt_continuer.collidepoint(py.mouse.get_pos()): pause = False
            if bt_parametres.collidepoint(py.mouse.get_pos()): menuParametres(screen,parametres) ; pause = False
            if bt_quitter.collidepoint(py.mouse.get_pos()): py.quit()

        py.display.flip()





def menuParametres(screen:py.Surface,parametres:Settings):
    """
    Affichage du menu pause et gestion de ses fonctionnalités. Change le fichier ``settings.json`` en fonction.
    """

    slider_vol = Slider(screen, SCREEN_WIDTH//2 - 170, 200, 350, 10, max=100)
    slider_vol.setValue(parametres.getData()["volume"])

    slider_SFX = Slider(screen, SCREEN_WIDTH//2 - 170, 300, 350, 10, max=100)
    slider_SFX.setValue(parametres.getData()["volumeSFX"])

    inParam = True
    while inParam:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                py.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:  # KEYDOWN = appui unique, pas maintenu
                    inParam = False

        fond_param = py.draw.rect(screen,"black",py.Rect(SCREEN_WIDTH//2-300,100,600,SCREEN_HEIGHT-200), border_radius=3)
        py.draw.rect(screen, "gray", remplissageRect(fond_param), border_radius=3)
        affichageTexte(screen, "PARAMETRES", (fond_param.centerx, fond_param.top + 40), 50)



        affichageTexte(screen, "Volume", (fond_param.left + 50, fond_param.top + 100), 30)
        affichageTexte(screen, str(slider_vol.getValue()), (fond_param.right - 50, fond_param.top + 100), 30)
        py.mixer_music.set_volume(slider_vol.getValue()/100)

        affichageTexte(screen, "SFX", (fond_param.left + 50, fond_param.top + 200), 30)
        affichageTexte(screen, str(slider_SFX.getValue()), (fond_param.right - 50, fond_param.top + 200), 30)



        bt_appliquer = py.draw.rect(screen,"green",py.Rect(fond_param.right - 180, fond_param.bottom - 80, 150, 50))
        affichageTexte(screen,"Appliquer",bt_appliquer.center)

        bt_defaut = py.draw.rect(screen,"green",py.Rect(fond_param.right - 480, fond_param.bottom - 80, 270, 50))
        affichageTexte(screen,"Remmettre par défaut",bt_defaut.center)

        if py.mouse.get_just_pressed()[0]:
            if bt_appliquer.collidepoint(py.mouse.get_pos()) :
                newSettingsDict = {"volume":slider_vol.getValue(),"volumeSFX":slider_SFX.getValue()}
                parametres.updateData(newSettingsDict)
                inParam = False
            if bt_defaut.collidepoint(py.mouse.get_pos()) :
                defaultSettings = parametres.default()
                slider_vol.setValue(defaultSettings["volume"])
                slider_SFX.setValue(defaultSettings["volumeSFX"])



        pw.update(events)
        py.display.flip()




def affichageTexte(screen:py.Surface, 
                   texte:str, 
                   pos:tuple[int,int]=(0,0), 
                   taille:int=30,
                   couleur:tuple[int,int,int]=(0,0,0), 
                   police:str="Arial"):
    """
    Écris un texte sur la surface ``screen``, à la position ``pos``, de taille ``taille``, de couleur ``couleur`` avec la police ``police``.\n
    ``pos`` est le CENTRE du texte.
    """
    surface_texte = py.font.SysFont(police, taille).render(texte,None,couleur)
    screen.blit(surface_texte , (pos[0] - surface_texte.get_width()//2, pos[1] - surface_texte.get_height()//2))


def affichageTexteWrap(screen:py.Surface, 
                   texte:str, 
                   rect:py.Rect,
                   police,
                   taille:int=30,
                   couleur:tuple[int,int,int]=(0,0,0)):
    """
    Écris un texte sur une surface avec une police et une couleur donnée.\n
    Il faut également donner le rect dans lequel est écrit le texte pour le retour a la ligne.\n
    SOURCE : https://www.pygame.org/wiki/TextWrap
    """

    rect = py.Rect(rect.left + TEXT_BOX_MARGIN, rect.top + 2 * TEXT_BOX_MARGIN, rect.width - TEXT_BOX_MARGIN , rect.height - TEXT_BOX_MARGIN)
    y = rect.top
    lineSpacing = -2

    while texte:
        i = 1

        while police.size(texte[:i])[0] < rect.width and i < len(texte):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(texte): 
            i = texte.rfind(" ", 0, i) + 1

        image = police.render(texte[:i], 1, couleur)
        screen.blit(image, (rect.left, y))
        y += taille + lineSpacing

        # remove the text we just blitted
        texte = texte[i:]



def remplissageRect(contour:py.Rect,bordure:int=3):
    """Renvoie la partie interne d'un rect de telle sorte que le rect donné en paramètre fasse office de countour au rect renvoyé, avec un épaisseur de taille ''bordure''"""
    return py.Rect(contour.left + bordure, contour.top + bordure, contour.width - 2*bordure, contour.height - 2*bordure)