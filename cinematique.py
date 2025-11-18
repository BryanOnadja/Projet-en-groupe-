import unittest
import math

# Fonction à tester
L1 = 100.0  # mm
L2 = 100.0  # mm
BASE_X = 50.0  # mm

def cinematique_inverse(x, y):
    dx = x + BASE_X
    dy = y
    r = math.sqrt(dx*dx + dy*dy)
    
    if r > L1 + L2 or r < abs(L1 - L2):
        raise ValueError(f"Position ({x}, {y}) hors d'atteinte (r={r:.1f} mm)")
    
    cos_gamma = (L1**2 + r**2 - L2**2) / (2 * L1 * r)
    cos_gamma = max(min(cos_gamma, 1.0), -1.0)
    gamma = math.acos(cos_gamma)
    
    theta = math.atan2(dy, dx)
    alpha = theta - gamma
    beta = math.pi - math.acos((L1**2 + L2**2 - r**2) / (2 * L1 * L2))
    
    return alpha, beta

# Tests unitaires
class TestCinematiqueInverse(unittest.TestCase):

    def test_position_centrale(self):
        alpha, beta = cinematique_inverse(50, 0)
        self.assertAlmostEqual(alpha + beta, 0.0, places=5)

    def test_position_maximale(self):
        x = 150  # L1 + L2 - BASE_X = 150
        y = 0
        alpha, beta = cinematique_inverse(x, y)
        self.assertIsInstance(alpha, float)
        self.assertIsInstance(beta, float)

    def test_position_minimale(self):
        x = -50  # L1 - L2 - BASE_X = -50
        y = 0
        alpha, beta = cinematique_inverse(x, y)
        self.assertIsInstance(alpha, float)
        self.assertIsInstance(beta, float)

    def test_position_hors_portee(self):
        with self.assertRaises(ValueError):
            cinematique_inverse(200, 0)  # Trop loin

    def test_position_negative(self):
        alpha, beta = cinematique_inverse(-30, -30)
        self.assertIsInstance(alpha, float)
        self.assertIsInstance(beta, float)

if __name__ == '__main__':
    unittest.main()