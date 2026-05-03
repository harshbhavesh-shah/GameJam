import pygame as py
import pygame_widgets as pw
from pygame_widgets.slider import Slider
from classes import *
from levels import *
from textures import *
import time

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



def collisions(objetsDict:dict[str,list[Bloc|BlocMouv]], j:Joueur):
    """
    Gère les collisions entre le Joueur (j) et l'envirronement (Blocs,Pics...). \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire des objets.
        \n- j : le Joueur.
    """
    joueur_rect = j.getRect()

    for bloc in objetsDict["blocs"]:
        if bloc.colliderect(joueur_rect): 
            collisionsBlocJoueur(joueur_rect,bloc,j)    
    
    for blocpic in objetsDict["piques"]:
        if blocpic.colliderect(joueur_rect):
            j.setXY(objetsDict["spawn"][0].x,objetsDict["spawn"][0].y)
            py.time.wait(150)   
            joueur_rect = j.getRect()   #   TODO  
    
    for ennemi in objetsDict["ennemis"]:
        if ennemi.getRect().colliderect(joueur_rect):
            j.setXY(objetsDict["spawn"][0].x,objetsDict["spawn"][0].y)
            py.time.wait(150)   
            joueur_rect = j.getRect()
 
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

        if j.getDashState()[0] >= DASH_TIMER: j.setDashState((0,"n",j.getDashState()[2])) 
    




def switchSousZone(zone:str,souszone:int,joueur:Joueur,objetsDict:dict):
    """
    Téléporte le joueur à la prochaine sous-zone s'il sors de l'écran.
    """
    level = f"{zone}-{souszone}"

    if joueur.getRect().x + joueur.getRect().width > SCREEN_WIDTH:
        for source, dest in TABLEAUX_CORRESPONDANCES.items():
            if source == level: 
                zone, souszone = dest.split('-')[0] , int(dest.split('-')[1])
                objetsDict = preparationZone(zone,souszone)
                joueur.setXY(objetsDict["spawn"][0].x,objetsDict["spawn"][0].y)
                return objetsDict , souszone
        joueur.setX(SCREEN_WIDTH-joueur.getRect().width)

    if joueur.getRect().x < 0:
        for source, dest in TABLEAUX_CORRESPONDANCES.items():
            if dest == level: 
                zone, souszone = source.split('-')[0] , int(source.split('-')[1])
                objetsDict = preparationZone(zone,souszone)
                joueur.setXY(objetsDict["end"][0].x,objetsDict["end"][0].y)
                return objetsDict , souszone
        joueur.setX(0)
        
    return objetsDict , souszone



def telePorte(objetsDict:dict[str,list[Bloc|BlocMouv|Porte]],zone,souszone,joueur:Joueur):
    for porte in objetsDict["portes"]:
            if porte.getRect().colliderect(joueur.getRect()):
                for source, dest in PORTES_CORRESPONDANCES.items():
                    if source == porte.getId(): destination_id = dest
                    if dest == porte.getId(): destination_id = source
                zone , souszone , y , x = destination_id.split('-')[0] , int(destination_id.split('-')[1]) , int(destination_id.split('-')[2]) , int(destination_id.split('-')[3])
                objetsDict = preparationZone(zone,souszone)
                joueur.setXY(x*TILE_SIZE,y*TILE_SIZE)
                joueur.setInteractionCooldown(INTERACTION_COOLDOWN)
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
        bordure_texte = py.draw.rect(screen,"black",py.Rect(50, SCREEN_HEIGHT - 200,  700, 150), border_radius=3)
        py.draw.rect(screen,"gray70",py.Rect(bordure_texte.left + 3, bordure_texte.top + 3, bordure_texte.width - 6, bordure_texte.height - 6), border_radius=3)
        bordure_nom = py.draw.rect(screen,"black",py.Rect(bordure_texte.left - 30, bordure_texte.top - 30, 100 , 50), border_radius=3)
        py.draw.rect(screen,"gray80",py.Rect(bordure_nom.left + 3, bordure_nom.top + 3, bordure_nom.width - 6, bordure_nom.height - 6), border_radius=3)

        affichageTexte(screen, pnj.getNom(), bordure_nom.center, 25, "black")
        affichageTexte(screen, pnj.getLine(index), bordure_texte.center, 50, "black")
        affichageTexte(screen, "Appuyez sur E", (bordure_texte.right - 45, bordure_texte.bottom - 15), 15, "black")
        py.display.flip()



def preparationZone(zone:str, souszone:int) -> dict[str,list[Bloc|BlocMouv|Porte|Ennemi]]:
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
    objetsDict = {"blocs":[], "portes":[], "piques":[], "blocmouvs":[], "spawn":[], "end":[], "ennemis":[], "pnjs": [], "decorations":[]}
    map_tile = tileMaps[zone]
    for i in range(len(map_tile[souszone])):
        for j in range(len(map_tile[souszone][i])):
            match map_tile[souszone][i][j]:
                    case "b": objetsDict["blocs"].append(Bloc((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)).setSprite(blocSprite(map_tile[souszone],i,j)))
                    case "p": objetsDict["portes"].append(Porte(((j-1)*TILE_SIZE,(i-1)*TILE_SIZE), f"{zone}-{souszone}-{i}-{j}"))
                    case "s": objetsDict["piques"].append(Pique((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
                    case "m": objetsDict["blocmouvs"].append(BlocMouv((j*TILE_SIZE,i*TILE_SIZE)))
                    case "S": objetsDict["spawn"].append(Spawn((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)))
                    case "E": objetsDict["end"].append(End((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)))
                    case "r": objetsDict["ennemis"].append(Ennemi((j*TILE_SIZE,i*TILE_SIZE),(4*TILE_SIZE,2*TILE_SIZE),5,0).setType("requin"))
                    case "l": objetsDict["decorations"].append(Decoration((j*TILE_SIZE,i*TILE_SIZE),(TILE_SIZE,2*TILE_SIZE)).setSprite(sprite_lianes[(i+j)%2]))
                    case "P": objetsDict["pnjs"].append(PNJ(((j*TILE_SIZE,i*TILE_SIZE), (TILE_SIZE,TILE_SIZE)),f"{zone}-{souszone}"))
    return objetsDict




def affichageZone(objetsDict:dict[str,list[Bloc|BlocMouv|Porte|Pique|Ennemi]], screen:py.Surface):
    """
    Affiche tous les objets du dictionnaire sur la surface screen. \n
    Prends en paramètres : 
        \n- objetsDict : dictionnaire associant chaque type d'objet à la liste des objets à ajouter.
        \n- screen : la surface (pygame) sur laquelle on affiche les objets
    """
    for bloc in objetsDict["blocs"]:
        screen.blit(bloc.getSprite().convert_alpha(),bloc.topleft)

    for porte in objetsDict["portes"]:
        screen.blit(sprite_porte[int(10*time.time())%len(sprite_porte)].convert_alpha(),porte.getRect().topleft)

    for pique in objetsDict["piques"]:
        screen.blit(sprite_pique.convert_alpha(),pique.topleft)

    for deco in objetsDict["decorations"]:
        screen.blit(deco.getSprite().convert_alpha(),deco.topleft)

    for bmouv in objetsDict["blocmouvs"]:
        py.draw.rect(screen, "blue", bmouv)
        bmouv.move()
    
    for ennemi in objetsDict["ennemis"]:
        match ennemi.getType():
            case "requin" : screen.blit(sprite_requin[int(10*time.time())%len(sprite_requin)].convert_alpha(),ennemi.getRect().topleft)
        ennemi.move()

    for pnj in objetsDict["pnjs"]:
        py.draw.rect(screen, "green", pnj.getRect())




### TEXTURES ###

def background(ecran:py.Surface,zone):
    match zone:
        case "foret": ecran.blits(((bg_foret_1,(0,0)),(bg_foret_2,(0,0)),(bg_foret_3,(0,0))))
        case _ : ecran.fill("darkblue")


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



### OPTIONS / MENUS ###

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



        bt_appliquer = py.draw.rect(screen,"green",py.Rect(fond_param.right - 180, fond_param.bottom - 80, 150, 50))
        affichageTexte(screen,"Appliquer",bt_appliquer.center)

        bt_defaut = py.draw.rect(screen,"green",py.Rect(fond_param.right - 480, fond_param.bottom - 80, 270, 50))
        affichageTexte(screen,"Remmettre par défaut",bt_defaut.center)

        if py.mouse.get_just_pressed()[0]:
            if bt_appliquer.collidepoint(py.mouse.get_pos()) :
                newSettingsDict = {"volume":slider_vol.getValue()}
                parametres.updateData(newSettingsDict)
                inParam = False
            if bt_defaut.collidepoint(py.mouse.get_pos()) :
                defaultSettings = parametres.default()
                slider_vol.setValue(defaultSettings["volume"])



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


def remplissageRect(contour:py.Rect,bordure:int=3):
    """Renvoie la partie interne d'un rect de telle sorte que le rect donné en paramètre fasse office de countour au rect renvoyé, avec un épaisseur de taille ''bordure''"""
    return py.Rect(contour.left + bordure, contour.top + bordure, contour.width - 2*bordure, contour.height - 2*bordure)