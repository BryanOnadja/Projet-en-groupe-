## NDEDI MBAPPE 

"""
    NB : code  ecrit en partie( 45%) avec l'assistance d'une Intelligence
    Artificielle (IA) afin d'ameliorer sa structure, sa documentation et sa clarte
"""

def lire_position_xy():
    """
    Convertit les valeurs ADC des potentiometres en coordonnees X-Y.

    Parametres :
        left_knob  : objet ayant une methode read_u16(), pour la position X
        right_knob : objet ayant read_u16(), pour la position Y
        X_MIN, X_MAX : limites horizontales
        Y_MIN, Y_MAX : limites verticales

    Retour :
        tuple (x, y) arrondi a une decimale
    """

    val_x = left_knob.read_u16()

    val_y = right_knob.read_u16()

     # conversion vers la zone de travail

    x = X_MIN + (val_x / 65535) * (X_MAX - X_MIN)
    y = Y_MIN + (val_y / 65535) * (Y_MAX - Y_MIN)

    return round(x, 1), round(y, 1)

