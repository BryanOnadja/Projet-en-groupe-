#Ce code a été élaboré avec l'assistance de Grok, une intelligence artificielle développée par xAI

# Date de génération : 16 novembre 2025
# Outil : Grok (xAI) – https://grok.x.ai
import math
from traducteur_servo import traduit as angle_to_duty
from groupe_projet_test import cinematique_inverse


from machine import Pin, PWM
servo_epaule = PWM(Pin(0))
servo_coude = PWM(Pin(1))
servo_epaule.freq(50)
servo_coude.freq(50)

# === ENVOI ANGLES ===
def envoyer_angles(x, y):
    alpha_rad, beta_rad = cinematique_inverse(x, y)
    alpha_deg = math.degrees(alpha_rad)
    beta_deg = math.degrees(beta_rad)
    
    # Conversion montage mécanique (inversion typique)
    servo_alpha = 90 - alpha_deg
    servo_beta = 90 - beta_deg
    
    # Sécurité
    servo_alpha = max(0, min(180, servo_alpha))
    servo_beta = max(0, min(180, servo_beta))
    
    # Envoi PWM
    servo_epaule.duty_u16(angle_to_duty(servo_alpha))
    servo_coude.duty_u16(angle_to_duty(servo_beta))
    
    return servo_alpha, servo_beta
