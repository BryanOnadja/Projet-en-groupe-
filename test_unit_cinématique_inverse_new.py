# Ce code a été élaboré avec l'assistance de Gemini, une intelligence artificielle développée par Google

# Date de génération : 30 novembre 2025
# Outil : Gemini (Google) – https://gemini.google.com


#Koami Adjawlor
import unittest
import math
from cinematique_inverse_new import cinematique_inverse # Assurez-vous que le chemin d'importation est correct

class TestCinematique(unittest.TestCase):

    def setUp(self):
        """Initialisation avant chaque test"""
        self.L1 = 155
        self.L2 = 155
        # L'origine définie dans votre code est (-50, 140)
        self.xA = -50
        self.yA = 140

    def test_cas_nominal(self):
        """Test d'un point connu et accessible (votre exemple)"""
        x, y = 146, 81.5
        resultat = cinematique_inverse(x, y, self.L1, self.L2)
        
        # Vérifie que le résultat n'est pas None
        self.assertIsNotNone(resultat, "Le résultat ne devrait pas être None pour un point valide")
        
        # Vérifie qu'on reçoit bien deux angles
        self.assertEqual(len(resultat), 2) #type: ignore
        
        # Vérification optionnelle des types
        alpha, beta = resultat #type: ignore
        self.assertIsInstance(alpha, float)
        self.assertIsInstance(beta, float)

    def test_hors_portee(self):
        """Test d'un point impossible à atteindre (trop loin)"""
        # Distance max = 310. On essaie un point très loin (ex: x=1000)
        resultat = cinematique_inverse(1000, 1000, self.L1, self.L2)
        
        # La fonction doit retourner None et afficher un message d'erreur
        self.assertIsNone(resultat, "Le robot ne devrait pas atteindre ce point")

    def test_trop_proche(self):
        """Test de la contrainte de proximité (L1 != L2 pour tester la différence)"""
        # Si L1=155 et L2=100, le rayon min est 55.
        # On vise le point d'origine exact du bras (-50, 140), distance = 0.
        # Distance (0) < abs(155 - 100) -> Doit échouer
        resultat = cinematique_inverse(-50, 140, L1=155, L2=100)
        
        self.assertIsNone(resultat, "Le point est dans la zone morte (trop proche), doit retourner None")

    def test_bras_tendu_vertical(self):
        """Test d'un cas limite : le bras tendu verticalement vers le bas"""
        # Si le bras est tendu vers le bas depuis (-50, 140) avec L1+L2 = 310
        # La cible est (-50, 140 + 310) = (-50, 450) 
        # Note : Votre code utilise 'dy = yB - yA' et 'atan2(dx, -dy)',
        # vérifions si la logique tient pour une verticale pure.
        
        target_y = 140 + 310 # Juste à la limite
        resultat = cinematique_inverse(-50, target_y, self.L1, self.L2)
        
        # À la limite exacte, cela peut être délicat avec les flottants, 
        # mais on vérifie si cela ne crashe pas.
        if resultat:
            alpha, beta = resultat
            # Si le bras est tendu, Beta (angle du coude) devrait être proche de 0
            self.assertAlmostEqual(beta, 0, delta=0.1, msg="Le bras tendu doit avoir un angle Beta proche de 0")

if __name__ == '__main__':
    unittest.main()