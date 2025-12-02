## NDEDI MBAPPE 

"""
    NB : code  ecrit en partie( 45%) avec l'assistance d'une Intelligence
    Artificielle (IA) afin d'ameliorer sa structure, sa documentation et sa clarte
"""

def lire_position_xy():
    """
    Lit deux valeurs ADC (potentiomètres) et les convertit en coordonnées X-Y.
    Version securisée avec gestion d'erreurs via try/except.

    NOTE : Cette version inclut un try/except pour éviter les crashs
    si les entrées sont invalides ou si une opération échoue.
    """

    # Vérification de la lecture ADC
    try:
        val_x = left_knob.read_u16()

        val_y = right_knob.read_u16()

    except Exception as e:

        raise TypeError(f"Erreur : l'objet fourni ne possède pas read_u16() → {e}")

    #  Vérification de la plage X-Y

    if X_MIN >= X_MAX or Y_MIN >= Y_MAX:
        raise ValueError("Erreur : X_MIN doit être < X_MAX et Y_MIN < Y_MAX.")

    #  Conversion sécurisée
    
    try:
        x = X_MIN + (val_x / 65535) * (X_MAX - X_MIN)
        y = Y_MIN + (val_y / 65535) * (Y_MAX - Y_MIN)
    except Exception as e:
        raise RuntimeError(f"Erreur pendant la conversion en coordonnées : {e}")

    return round(x, 1), round(y, 1)


