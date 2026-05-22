SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SPEED = 9
TILE_SIZE = 40
JUMP_SPEED = 20
MAX_FALL_SPEED = 30
MAX_JUMP_TIMER = 20
COYOTE_JUMP_TIME = 7
DASH_TIMER = 5
DASH_COOLDOWN = 40
DASH_SPEED = 2*PLAYER_SPEED
INTERACTION_COOLDOWN = 10

# Environnement
MAX_FALL_SPEED_IN_WATER = 10
JUMP_SPEED_IN_WATER = 15
PLAYER_SPEED_IN_WATER = 6

VILLE_DPS = 1       # Dégats / Tick
VILLE_HEAL = 2      # Heal / Tick

BTOMBANT_SPEED = 3
BTOMBANT_DELAY = 20
BTOMBANT_RESPAWN_TIMER = 500

# Manette
CONTROLLER_DEADZONE = 0.2

# Zone - Sous-Zone - Ordonnées - Abcisses
PORTES_CORRESPONDANCES = {
    "hub-5-14-9" : "foret-1-16-2",
    "hub-5-4-9" : "mer-1-13-6",
    "hub-5-14-23" : "ville-1-16-2",
    "hub-5-4-23" : "colline-1-16-2"
}


TABLEAUX_CORRESPONDANCES = {
    "hub-1" : "hub-2",
    "hub-2" : "hub-3",
    "hub-3" : "hub-4",
    "hub-4" : "hub-5",
    "mer-1" : "mer-2"
}