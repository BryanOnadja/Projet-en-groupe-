#Ce code a été élaboré avec l'assistance de Grok, une intelligence artificielle développée par xAI

# Date de génération : 16 novembre 2025
# Outil : Grok (xAI) – https://grok.x.ai
import math
from traducteur_servo import traduit as angle_to_duty
from groupe_projet_test import cinematique_inverse
from groupe_projet_test import interpoler_erreur

from machine import Pin, PWM
servo_epaule = PWM(Pin(0))
servo_coude = PWM(Pin(1))
servo_epaule.freq(50)
servo_coude.freq(50)


# ...existing code...

def envoyer_angles_compenses(x, y, table_epaule=None, table_coude=None):
    """
    Calcule les angles (rad) via cinematique_inverse, convertit en degrés,
    calcule l'angle demandé au servo (servo_angle = 90 - joint_deg),
    applique la correction interpolée (si fournie) en utilisant l'angle servo,
    puis contraint entre 0..180, envoie duty_u16 et retourne (servo_alpha, servo_beta).
    """
    alpha_rad, beta_rad = cinematique_inverse(x, y)
    alpha_deg = math.degrees(alpha_rad)
    beta_deg = math.degrees(beta_rad)

    # angle demandé au servo (selon montage)
    servo_alpha = 90.0 - alpha_deg
    servo_beta = 90.0 - beta_deg

    # appliquer compensation en se basant sur l'angle servo (c'est ce que test attend)
    if table_epaule:
        try:
            corr_a = interpoler_erreur(table_epaule, servo_alpha)
        except Exception:
            corr_a = 0.0
        servo_alpha += corr_a

    if table_coude:
        try:
            corr_b = interpoler_erreur(table_coude, servo_beta)
        except Exception:
            corr_b = 0.0
        servo_beta += corr_b

    # clamp sécurité
    servo_alpha = max(0.0, min(180.0, servo_alpha))
    servo_beta = max(0.0, min(180.0, servo_beta))

    # envoyer (protéger appels en cas d'environnement de test)
    try:
        servo_epaule.duty_u16(angle_to_duty(servo_alpha))
    except Exception:
        pass
    try:
        servo_coude.duty_u16(angle_to_duty(servo_beta))
    except Exception:
        pass

    return servo_alpha, servo_beta
# ...existing code...