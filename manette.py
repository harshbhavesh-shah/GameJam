from constantes import *

def controllerState(joystick,type:str) -> bool:
    """
    Renvoie True si le bouton coorespondant au type d'action est préssé (ou joystick dans la bonne direction)
    """
    if joystick is None : return False
    match type:
        case "gauche": return joystick.get_axis(0) < -CONTROLLER_DEADZONE or joystick.get_button(13)
        case "droite": return joystick.get_axis(0) > CONTROLLER_DEADZONE or joystick.get_button(14)
        case "haut": return joystick.get_axis(1) < -CONTROLLER_DEADZONE or joystick.get_button(11)
        case "saut": return joystick.get_button(0)          # X
        case "dash": return joystick.get_button(2)          # Carré
        case "interaction": return joystick.get_button(3)   # Triangle