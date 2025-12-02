# Ce code a été élaboré avec l'assistance de Gemini, une intelligence artificielle développée par Google

# Date de génération : 30 novembre 2025
# Outil : Gemini (Google) – https://gemini.google.com
#Ayméric, Bryan, Mbappé, Koami

import time
import machine
import math

# ---------- CONFIGURATION PHYSIQUE ----------
L1 = 155.0  # Longueur épaule-coude (mm)
L2 = 155.0  # Longueur coude-stylo (mm)

# Dimensions papier
PAPER_WIDTH = 8.5 * 25.4  # 215.9mm
PAPER_HEIGHT = 11 * 25.4   # 279.4mm

# Zone de travail sécurisée
X_MIN = 0
X_MAX = PAPER_WIDTH
Y_MIN = 0  
Y_MAX = PAPER_HEIGHT

# Position de la base du bras
BASE_X = -50
BASE_Y = 140  # Mis à jour à 140 pour correspondre à votre nouvelle cinématique

# ---------- CONFIGURATION MATÉRIEL ----------
# Servomoteurs
pen_servo = machine.PWM(machine.Pin(2))
elbow_servo = machine.PWM(machine.Pin(1)) 
shoulder_servo = machine.PWM(machine.Pin(0))

# Fréquence PWM pour servos (50Hz standard)
pen_servo.freq(50)
elbow_servo.freq(50)
shoulder_servo.freq(50)

# Potentiomètres et bouton
left_knob = machine.ADC(machine.Pin(27))  # Contrôle X
right_knob = machine.ADC(machine.Pin(26))  # Contrôle Y
pen_button = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)

# ---------- VARIABLES GLOBALES ----------
pen_state = False
last_button_state = 0
last_debounce = 0
DEBUG = True

# ---------- FONCTIONS DE BASE ----------

#Bryan
def button_checker():
    """Gestion du bouton stylo avec anti-rebond"""
    global pen_state, last_button_state, last_debounce
    
    current_button_state = pen_button.value()
    now = time.ticks_ms()
    
    # Détection front montant avec anti-rebond
    if current_button_state == 1 and last_button_state == 0:
        if time.ticks_diff(now, last_debounce) > 200:
            pen_state = not pen_state
            last_debounce = now
            print(f"Bouton pressé - Stylo: {'BAISSÉ' if pen_state else 'LEVÉ'}")
    
    last_button_state = current_button_state
    return pen_state

def pen_placement(state):
    """Contrôle position du stylo"""
    if state:  # stylo baissé - dessin
        duty_cycle_pen = 3000
    else:      # stylo levé - déplacement
        duty_cycle_pen = 2300
    
    # Sécurité PWM
    duty_cycle_pen = max(1639, min(8192, duty_cycle_pen))
    pen_servo.duty_u16(duty_cycle_pen)
    
    return duty_cycle_pen

#Mbappe
def lire_position_xy():
    """Lecture des potentiomètres et conversion en coordonnées"""
    # Lecture ADC (0-65535)
    val_x = left_knob.read_u16()
    val_y = right_knob.read_u16()
    
    # Conversion vers zone de travail
    x = X_MIN + (val_x / 65535) * (X_MAX - X_MIN)
    y = Y_MIN + (val_y / 65535) * (Y_MAX - Y_MIN)
    
    return round(x, 1), round(y, 1)


#Koami
def cinematique_inverse(xB, yB):
    """
    Nouvelle cinématique inverse basée sur Al-Kashi.
    Utilise BASE_X et BASE_Y comme point d'ancrage A.
    """
    # Point d'ancrage A (épaule) récupéré des variables globales
    xA, yA = BASE_X, BASE_Y
    
    # --- CALCULS ---
    
    # 1. Calcul de la distance D (hypoténuse AB)
    dx = xB - xA
    dy = yB - yA
    D = math.sqrt(dx**2 + dy**2)

    # Sécurité : est-ce que le point est accessible ?
    if D > (L1 + L2):
        # On lève une erreur pour que le 'try/except' du main() l'attrape
        raise ValueError(f"Erreur : Le point ({xB}, {yB}) est trop loin !")
    
    # Sécurité 2 : Distance minimale
    if D < abs(L1 - L2):
         raise ValueError(f"Erreur : Le point ({xB}, {yB}) est trop proche !")

    # 2. Calcul des angles internes avec Al-Kashi (Loi des cosinus)
    
    # Angle 'phi' (angle interne à l'épaule entre le bras L1 et la ligne AB)
    # Formule : L2² = L1² + D² - 2*L1*D*cos(phi)
    num_phi = L1**2 + D**2 - L2**2
    den_phi = 2 * L1 * D
    phi = math.acos(num_phi / den_phi)

    # Angle 'gamma' (angle interne au coude, entre L1 et L2)
    # Formule : D² = L1² + L2² - 2*L1*L2*cos(gamma)
    num_gamma = L1**2 + L2**2 - D**2
    den_gamma = 2 * L1 * L2
    gamma = math.acos(num_gamma / den_gamma)

    # 3. Calcul de l'angle global de la ligne AB par rapport à la verticale
    theta_vert = math.atan2(dx, -dy)

    # 4. Calcul des angles finaux
    # Alpha : angle de l'épaule par rapport à la verticale
    alpha_rad = theta_vert - phi
    
    # Beta : angle du coude (extérieur)
    # Ici on veut l'angle de flexion
    beta_rad =  math.pi - gamma 

    # --- CONVERSION EN DEGRÉS ---
    alpha_deg = math.degrees(alpha_rad) + 48
    beta_deg = 143 - math.degrees(beta_rad)
    

    if DEBUG:
         # On affiche de temps en temps pour debug
         # print(f"Pos: ({xB}, {yB}) -> Alpha={alpha_deg:.1f}, Beta={beta_deg:.1f}")
         pass

    return alpha_deg, beta_deg

#Bryan 
def angle_to_duty(angle_deg):
    """Conversion angle en signal PWM pour servos"""
    # 500-2500µs pulse width pour 0-180°
    pulse_width_us = 500 + (angle_deg / 180) * 2000
    duty_cycle = pulse_width_us / 20000  # 20ms period
    duty_u16 = int(duty_cycle * 65535)
    
    # Limites de sécurité
    duty_u16 = max(1638, min(8192, duty_u16))  # ~500-2500µs
    
    return duty_u16

# ---------- INITIALISATION ET TESTS ----------

#Ayméric
def test_servos():
    """Test de calibration des servos"""
    print("TEST SERVOS - Position milieu...")
    
    # Position milieu (90°)
    duty_mid = angle_to_duty(90)
    
    shoulder_servo.duty_u16(duty_mid)
    elbow_servo.duty_u16(duty_mid)
    pen_placement(False)  # Stylo levé
    
    time.sleep(0.02)
    print("Test servos terminé")

def test_cinematique():
    """Test de la cinématique inverse"""
    print("TEST CINÉMATIQUE INVERSE")
    
    points_test = [
        (50, 50),    # Coin inférieur gauche
        (100, 100),  # Diagonale
        (150, 150),  # Centre
        (200, 200),  # Coin supérieur droit
    ]
    
    for x, y in points_test:
        try:
            alpha, beta = cinematique_inverse(x, y)
            print(f"  ({x}, {y}) -> S={alpha:.1f}°, E={beta:.1f}°")
        except ValueError as e:
            print(f"  ({x}, {y}) -> {e}")


#Bryan
def test_potentiometres():
    """Test direct des potentiomètres"""
    print("TEST POTENTIOMÈTRES - Tournez les boutons...")
    
    for i in range(10):
        val_x = left_knob.read_u16()
        val_y = right_knob.read_u16()
        x, y = lire_position_xy()
        print(f"Pot X: {val_x:5d}, Pot Y: {val_y:5d} -> Position: ({x:5.1f}, {y:5.1f})")
        time.sleep(0.02)

# ---------- PROGRAMME PRINCIPAL ----------

#Ayméric, Bryan, Mbappé, Koami

def main():
    global pen_state, last_button_state
    
    print("=== DÉMARRAGE BRAS ROBOTIQUE (Logiciel V2 - Al-Kashi) ===")
    print("Contrôles:")
    print("  - Potentiomètre GAUCHE: position X")
    print("  - Potentiomètre DROIT: position Y") 
    print("  - Bouton: lever/baisser le stylo")
    print("  - CTRL+C pour arrêter")
    
    # Tests initiaux
    test_servos()
    test_cinematique()
    test_potentiometres()
    
    # Initialisation
    pen_placement(pen_state)
    
    print("\n=== SYSTÈME PRÊT ===")
    print(f"Zone de travail: {PAPER_WIDTH}x{PAPER_HEIGHT}mm")
    print("Utilisez les potentiomètres pour contrôler le bras!")

    # Boucle principale
    while True:
        try:
            # 1. Gestion bouton stylo
            pen_state = button_checker()
            pen_placement(pen_state)
            
            # 2. Lecture position désirée
            x, y = lire_position_xy()
            
            # 3. Calcul cinématique inverse et commande servos
            try:
                shoulder_angle, elbow_angle = cinematique_inverse(x, y)
                
                duty_shoulder = angle_to_duty(shoulder_angle)
                duty_elbow = angle_to_duty(elbow_angle)
                
                shoulder_servo.duty_u16(duty_shoulder)
                elbow_servo.duty_u16(duty_elbow)
                
            except ValueError:
                # Position inaccessible - on ignore silencieusement
                pass
            
            time.sleep(0.05)  # 20Hz
            
        except KeyboardInterrupt:
            print("\n=== ARRÊT DU SYSTÈME ===")
            # Remettre les servos en position sécurité
            duty_mid = angle_to_duty(90)
            shoulder_servo.duty_u16(duty_mid)
            elbow_servo.duty_u16(duty_mid)
            pen_placement(False)
            break
            
        except Exception as e:
            print(f"ERREUR: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()