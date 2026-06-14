import pygame as py

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SPEED = 6
TILE_SIZE = 20
JUMP_SPEED = 10
MAX_FALL_SPEED = 30
MAX_JUMP_TIMER = 20
COYOTE_JUMP_TIME = 7
DASH_TIMER = 5
DASH_COOLDOWN = 1
DASH_SPEED = 2*PLAYER_SPEED
INTERACTION_COOLDOWN = 10


# Environnement
MAX_FALL_SPEED_IN_WATER = 10
JUMP_SPEED_IN_WATER = 8
PLAYER_SPEED_IN_WATER = 4

VILLE_DPS = 1       # Dégats / Tick
VILLE_HEAL = 2      # Heal / Tick

BTOMBANT_SPEED = 3
BTOMBANT_DELAY = 20
BTOMBANT_RESPAWN_TIMER = 500

SPAWN_FIRE_TREE_COOLDOWN = 600

# Manette
CONTROLLER_DEADZONE = 0.2

# Affichage
TEXT_BOX_WIDTH = SCREEN_WIDTH - 100
NAME_BOX_WIDTH = 150
TEXT_BOX_MARGIN = 7

# Zone - Sous-Zone - y - x
PORTES_CORRESPONDANCES = {
    "hub-5-30-15" : "foret-1-16-2",
    "hub-5-31-53" : "mer-1-22-17",
    "hub-5-9-14" : "ville-1-25-3",
    "hub-5-12-50" : "colline-1-25-3"
}


MOUVEMENTS_BLOCMOUVS = {
    "hub-5-22-23" : ("naaaasaaaa",1),
    "hub-5-15-25" : ("naaaasaaaa",1),
    "hub-5-18-32" : ("naaaasaaaa",1),
    "foret-2-15-39" : ("saanaa",1),
    "foret-3-23-6" : ("eaaaaaaaaaaoaaaaaaaaaa",1),
    "foret-4-14-2" : ("naaaasaaaa",1),
    "mer-3-26-31" : ("naaaaaaaasaaaaaaaa",1),
    "mer-5-24-15" :("naaaaaaaaaaasaaaaaaaaaaa",1),
    "mer-5-14-44" :("saaaaaaaaaanaaaaaaaaaaasa",1),
    "mer-6-10-20" : ("saaaaaaanaaaaaaa",1),
    "mer-6-10-40" : ("saaaaaaanaaaaaaa",1),
    "mer-6-26-30" : ("naaaaaaasaaaaaaa",1),
    "mer-8-26-19" : ("naaaaaaaaaaaaaaaasaaaaaaaaaaaaaaaa",1),
    "mer-8-26-41" : ("naaaaaaaaaaaaaaaasaaaaaaaaaaaaaaaa",1),
}