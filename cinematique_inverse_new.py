# Ce code a été élaboré avec l'assistance de Gemini, une intelligence artificielle développée par Google

# Date de génération : 30 novembre 2025
# Outil : Gemini (Google) – https://gemini.google.com


#Koami Adjawlor
import math

def cinematique_inverse(xB, yB, L1=155, L2=155):
    # --- CONFIGURATION ---
    # Point d'ancrage A (épaule)
    xA, yA = -50, 140
    
    # --- CALCULS ---
    
    # 1. Calcul de la distance D (hypoténuse AB)
    dx = xB - xA
    dy = yB - yA
    D = math.sqrt(dx**2 + dy**2)

    # Sécurité : est-ce que le point est accessible ?
    if D > (L1 + L2):
        print(f"Erreur : Le point ({xB}, {yB}) est trop loin !")
        return None
    
    # Sécurité 2 : Distance minimale (si le point est trop proche de l'épaule)
    if D < abs(L1 - L2):
         print(f"Erreur : Le point ({xB}, {yB}) est trop proche !")
         return None

    # 2. Calcul des angles internes avec Al-Kashi (Loi des cosinus)
    
    # Angle 'phi' (angle interne à l'épaule entre le bras L1 et la ligne AB)
    # Formule : L2² = L1² + D² - 2*L1*D*cos(phi)
    # Donc : cos(phi) = (L1² + D² - L2²) / (2*L1*D)
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
    # Si le bras est tout droit, l'angle interne (gamma) est 180°, donc Beta est 0°.
    # Ici on veut l'angle de flexion, donc :
    beta_rad = math.pi - gamma

    # --- CONVERSION EN DEGRÉS ---
    alpha_deg = math.degrees(alpha_rad)
    beta_deg = math.degrees(beta_rad)

    return alpha_deg, beta_deg

# --- ZONE DE TEST ---
# On re-teste le point validé ensemble pour être sûr
cible_x = 146
cible_y = 81.5

resultat = cinematique_inverse(cible_x, cible_y, L1=155, L2=155)

if resultat:
    alpha, beta = resultat
    print(f"Pour le point B({cible_x}, {cible_y}) avec L1=155, L2=155 :")
    print(f"Alpha = {alpha:.2f}°")
    print(f"Beta  = {beta:.2f}°")