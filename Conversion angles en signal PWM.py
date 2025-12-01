# Ce code a été élaboré avec l'assistance de Gemini, une intelligence artificielle développée par Google

# Date de génération : 1 décembre 2025
# Outil : Gemini (Google) – https://gemini.google.com


#Bryan Onadja
def angle_to_duty(angle_deg):
    # --- CONFIGURATION ---
    # Paramètres physiques du servomoteur et du signal PWM
    pulse_min_us = 500    # Largeur d'impulsion pour 0° (en µs)
    pulse_max_us = 2500   # Largeur d'impulsion pour 180° (en µs)
    periode_us   = 20000  # Période du signal 50Hz (20ms = 20000µs)
    echelle_bit  = 65535  # Résolution 16-bit de MicroPython (0-65535)
    
    # --- CALCULS ---
    
    # 1. Conversion de l'angle (degrés) en durée d'impulsion (µs)
    # Formule linéaire : y = ax + b
    # On mappe la plage 0-180° vers la plage 500-2500µs
    ratio = angle_deg / 180
    pulse_width_us = pulse_min_us + (ratio * (pulse_max_us - pulse_min_us))

    # 2. Calcul du rapport cyclique (Duty Cycle)
    # C'est la fraction de temps où le signal est à l'état haut sur 20ms
    duty_cycle = pulse_width_us / periode_us

    # 3. Mise à l'échelle 16-bit
    # Conversion en entier pour le registre PWM
    duty_u16 = int(duty_cycle * echelle_bit)
    
    # --- SÉCURITÉ ---
    # Bornage pour protéger le mécanisme du servo.
    # On empêche le signal de sortir de la plage 500µs - 2500µs.
    
    seuil_bas = 1638  # Valeur brute pour 500µs
    seuil_haut = 8192 # Valeur brute pour 2500µs
    
    # Logique : on prend le MIN pour le plafond, et le MAX pour le plancher
    duty_u16 = max(seuil_bas, min(seuil_haut, duty_u16))
    
    return duty_u16

# --- ZONE DE TEST ---
# Test de la fonction avec des angles clés (0°, 90°, 180°) et un cas limite (200°)

angles_a_tester = [0, 45, 90, 135, 180, 200]

print("--- Résultats de la conversion PWM ---")

for angle in angles_a_tester:
    resultat = angle_to_duty(angle)
    # Affichage formaté
    print(f"Angle demandé : {angle:>3}°  ->  Signal PWM (u16) : {resultat}")
    
    # Petit message pour vérifier si la sécurité s'active
    if angle > 180 or angle < 0:
        print(f"   (Note : Valeur bornée par sécurité pour {angle}°)")