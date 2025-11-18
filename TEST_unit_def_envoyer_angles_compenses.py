import unittest
from unittest.mock import Mock, patch, call
import math

from groupe_projet_test import envoyer_angles_compenses

class TestEnvoyerAnglesCompenses(unittest.TestCase):
    
    def setUp(self):
        """Initialisation avant chaque test"""
        # Mock des servos globaux
        self.mock_servo_epaule = Mock()
        self.mock_servo_coude = Mock()
        
        # Mock des fonctions dépendantes
        self.patcher_cinematique = patch('groupe_projet_test.cinematique_inverse')
        self.patcher_interpoler = patch('groupe_projet_test.interpoler_erreur')
        self.patcher_angle_to_duty = patch('groupe_projet_test.angle_to_duty')
        self.patcher_servo_epaule = patch('groupe_projet_test.servo_epaule', self.mock_servo_epaule)
        self.patcher_servo_coude = patch('groupe_projet_test.servo_coude', self.mock_servo_coude)
        
        self.mock_cinematique_inverse = self.patcher_cinematique.start()
        self.mock_interpoler_erreur = self.patcher_interpoler.start()
        self.mock_angle_to_duty = self.patcher_angle_to_duty.start()
        self.patcher_servo_epaule.start()
        self.patcher_servo_coude.start()
        
        # Configuration par défaut des mocks
        self.mock_angle_to_duty.side_effect = lambda angle: int(angle * 100)
        self.mock_interpoler_erreur.return_value = 0
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        patch.stopall()
    
    def test_conversion_basique_sans_compensation(self):
        """Test conversion de base sans tables de compensation"""
        self.mock_cinematique_inverse.return_value = (math.radians(30), math.radians(45))
        
        servo_alpha, servo_beta = envoyer_angles_compenses(100, 150)
        
        self.assertAlmostEqual(servo_alpha, 60, places=5)  
        self.assertAlmostEqual(servo_beta, 45, places=5)   # ✅
        self.mock_servo_epaule.duty_u16.assert_called_once_with(6000)
        self.mock_servo_coude.duty_u16.assert_called_once_with(4500)
    
    def test_avec_compensation_epaule(self):
        """Test avec table de compensation pour l'épaule"""
        self.mock_cinematique_inverse.return_value = (math.radians(40), math.radians(50))
        table_epaule = [(0, -2), (90, 3), (180, -1)]
        self.mock_interpoler_erreur.side_effect = [5, 0]
        
        servo_alpha, servo_beta = envoyer_angles_compenses(100, 150, table_epaule=table_epaule)
        
        self.assertAlmostEqual(servo_alpha, 55, places=5) 
        self.assertAlmostEqual(servo_beta, 40, places=5)  
        self.mock_interpoler_erreur.assert_any_call(table_epaule, 50)
    
    def test_avec_compensation_coude(self):
        """Test avec table de compensation pour le coude"""
        self.mock_cinematique_inverse.return_value = (math.radians(35), math.radians(60))
        table_coude = [(0, 1), (90, -2), (180, 0)]
        self.mock_interpoler_erreur.side_effect = [0, -3]
        
        servo_alpha, servo_beta = envoyer_angles_compenses(100, 150, table_coude=table_coude)
        
        self.assertAlmostEqual(servo_alpha, 55, places=5)  
        self.assertAlmostEqual(servo_beta, 27, places=5)   
        self.mock_interpoler_erreur.assert_any_call(table_coude, 30)
    
    def test_avec_compensations_completes(self):
        """Test avec les deux tables de compensation"""
        self.mock_cinematique_inverse.return_value = (math.radians(20), math.radians(70))
        table_epaule = [(0, -2), (90, 3)]
        table_coude = [(0, 1), (90, -2)]
        self.mock_interpoler_erreur.side_effect = [2, -4]
        
        servo_alpha, servo_beta = envoyer_angles_compenses(100, 150, table_epaule, table_coude)
        
        self.assertAlmostEqual(servo_alpha, 72, places=5)   
        self.assertAlmostEqual(servo_beta, 16, places=5)    
    
    def test_clamping_angle_minimum(self):
        """Test limitation à 0° minimum"""
        self.mock_cinematique_inverse.return_value = (math.radians(100), math.radians(110))
        self.mock_interpoler_erreur.return_value = -50
        
        servo_alpha, servo_beta = envoyer_angles_compenses(100, 150, [(0, 0)], [(0, 0)])
        
        self.assertEqual(servo_alpha, 0)
        self.assertEqual(servo_beta, 0)
    
    def test_clamping_angle_maximum(self):
        """Test limitation à 180° maximum"""
        self.mock_cinematique_inverse.return_value = (math.radians(-100), math.radians(-110))
        self.mock_interpoler_erreur.return_value = 50
        
        servo_alpha, servo_beta = envoyer_angles_compenses(100, 150, [(0, 0)], [(0, 0)])
        
        self.assertEqual(servo_alpha, 180)
        self.assertEqual(servo_beta, 180)
    
    def test_valeurs_retournees(self):
        """Test que les valeurs retournées correspondent aux angles après compensation et clamping"""
        self.mock_cinematique_inverse.return_value = (math.radians(25), math.radians(55))
        
        result = envoyer_angles_compenses(100, 150)
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], (int, float))
        self.assertIsInstance(result[1], (int, float))
    
    def test_appel_cinematique_inverse(self):
        """Test que cinematique_inverse est appelée avec les bons paramètres"""
        self.mock_cinematique_inverse.return_value = (0, 0)
        
        envoyer_angles_compenses(123.45, 678.90)
        
        self.mock_cinematique_inverse.assert_called_once_with(123.45, 678.90)
    
    def test_pas_dappel_interpolation_sans_tables(self):
        """Test qu'interpoler_erreur n'est pas appelé sans tables"""
        self.mock_cinematique_inverse.return_value = (math.radians(30), math.radians(45))
        
        envoyer_angles_compenses(100, 150)
        
        self.mock_interpoler_erreur.assert_not_called()
    
    def test_conversion_degres_correcte(self):
        """Test la conversion radians -> degrés"""
        alpha_rad = math.radians(45)
        beta_rad = math.radians(60)
        self.mock_cinematique_inverse.return_value = (alpha_rad, beta_rad)
        
        servo_alpha, servo_beta = envoyer_angles_compenses(100, 150)
        
        self.assertAlmostEqual(servo_alpha, 45, places=5)  # ✅
        self.assertAlmostEqual(servo_beta, 30, places=5)   # ✅


if __name__ == '__main__':
    unittest.main()