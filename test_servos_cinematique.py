# Ce code a été élaboré avec l'assistance de Gemini, une intelligence artificielle développée par Google

# Date de génération : 30 novembre 2025
# Outil : Gemini (Google) – https://gemini.google.com

#Aymeric Sin-Yan-Too
def test_servos():
    """Test de calibration des servos"""
    print("TEST SERVOS - Position milieu...")
    
    # Position milieu (90°)
    duty_mid = angle_to_duty(90)
    
    shoulder_servo.duty_u16(duty_mid)
    elbow_servo.duty_u16(duty_mid)
    pen_placement(False)  # Stylo levé
    
    time.sleep(2)
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
