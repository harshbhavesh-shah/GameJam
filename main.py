import pygame as py
from fonctions import *

param = Settings("settings.json")
param.save()


py.init()
py.joystick.init()

try: controller = py.Joystick(0)
except py.error: controller = None

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
joueur = Joueur((200,300))

zone = "mer"
souszone = 3
objetsDict = preparationZone(zone, souszone)

py.mixer_music.load("./assets/sons/DDD.mp3")
py.mixer_music.play(-1)

hpBar = ProgressBar(screen, 10, 10, 200, 20, lambda: 1 - joueur.getHp()/100, completedColour=(250, 10, 10), incompletedColour=(165, 120, 120))

running = True
clock = py.time.Clock()
while running:
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE: menuPause(screen,param)
            
                
    keys = py.key.get_pressed()
    
    py.mixer_music.set_volume(param.getData()["volume"]/100)

    # BOUCLE MAIN #

    joueur.move(keys,controller,zone)
    collisions(objetsDict, joueur, (zone, souszone))


    if zone == 'colline':     # Dégats Ville
        hpBar.show()
        degatsEnvironnementauxColline(joueur,objetsDict)
        if joueur.getHp() <= 0:
            joueur.setXY(objetsDict["spawn"][0].x, objetsDict["spawn"][0].y)
            joueur.setHp(100)
    else:
        hpBar.hide()
        joueur.setHp(100)
    

    joueur.setInteractionCooldown(max(0,joueur.getInteractionCooldown()-1))
    if (keys[py.K_e] or controllerState(controller,"interaction")) and joueur.getInteractionCooldown() == 0:         # INTERACTIONS
        objetsDict , zone , souszone = telePorte(objetsDict,zone,souszone,joueur)
        for pnj in objetsDict["pnjs"]:
            if joueur.getRect().colliderect(pnj) :
                discussion(screen,pnj,joueur)
        for levier in objetsDict["leviers"]:
            if joueur.getRect().colliderect(levier) :
                levier.setEstActif(True)
                levier.setSprite(levier.getActifSprite())
                

    if (joueur.getRect().x + joueur.getRect().width > SCREEN_WIDTH  or  joueur.getRect().x < 0):
        if all(elt.getEstActif() for elt in objetsDict["leviers"]): 
            objetsDict , souszone = switchSousZone(zone,souszone,joueur,objetsDict)
        else: 
            joueur.setX(SCREEN_WIDTH-joueur.getRect().width)


    if joueur.getRect().y > 720 and SCREEN_WIDTH > joueur.getRect().x > 0:  # Tomber dans le vide
        objetsDict = dead(zone, souszone, joueur, objetsDict)



    background(screen,zone)
    affichageZone(objetsDict, screen, zone)
    py.draw.rect(screen,"red",joueur.getRect())

    if zone == "ville":   # brouillard
        screen.blit(sprite_brouillard)

    pw.update(events)
    py.display.flip()
    clock.tick(60)
    


py.quit()