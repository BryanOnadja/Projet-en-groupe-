# Ce code a été élaboré avec l'assistance de Gemini, une intelligence artificielle développée par Google

# Date de génération : 1 décembre 2025
# Outil : Gemini (Google) – https://gemini.google.com


#Bryan Onadja
import unittest
from Conversion_angles_en_signal_PWM import angle_to_duty 

class TestServoPWM(unittest.TestCase):

    def setUp(self):
        """Initialisation des constantes attendues"""
        self.MIN_DUTY = 1638  # Valeur pour 0° (500µs)
        self.MAX_DUTY = 8192  # Valeur limite haute (2500µs)
        self.MID_DUTY = 4915  # Valeur approx pour 90° (1500µs)

    def test_angles_nominaux(self):
        """Test des angles standards (0, 90, 180)"""
        
        # Test 0 degrés
        res_0 = angle_to_duty(0)
        self.assertAlmostEqual(res_0, self.MIN_DUTY, delta=1, msg="0° doit correspondre au duty cycle min")
        
        # Test 180 degrés
        res_180 = angle_to_duty(180)
        self.assertAlmostEqual(res_180, self.MAX_DUTY, delta=1, msg="180° doit correspondre au duty cycle max")

        # Test 90 degrés (Milieu)
        res_90 = angle_to_duty(90)
        self.assertAlmostEqual(res_90, self.MID_DUTY, delta=1, msg="90° doit être au milieu de la plage")

    def test_securite_bornes_hautes(self):
        """Test si la fonction bloque bien les valeurs > 180°"""
        # On demande 250 degrés (impossible physiquement)
        resultat = angle_to_duty(250)
        
        # La fonction doit retourner le plafond (8192)
        self.assertEqual(resultat, self.MAX_DUTY, "L'angle 250° doit être borné à 8192")

    def test_securite_bornes_basses(self):
        """Test si la fonction bloque bien les valeurs < 0°"""
        # On demande -45 degrés
        resultat = angle_to_duty(-45)
        
        # La fonction doit retourner le plancher (1638)
        self.assertEqual(resultat, self.MIN_DUTY, "L'angle négatif doit être borné à 1638")

    def test_type_retour(self):
        """Vérifie que la fonction retourne bien un Entier (int)"""
        resultat = angle_to_duty(45)
        self.assertIsInstance(resultat, int, "La fonction doit retourner un type 'int'")

if __name__ == '__main__':
    unittest.main()