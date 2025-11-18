import sys
import types
import importlib
import math
import unittest
from machine import Pin, PWM

from groupe_projet_test_new import cinematique_inverse

# helper stubs pour remplacer le module 'machine' sous CPython
class StubPin:
    def __init__(self, n): self.n = n

class StubPWM:
    def __init__(self, pin):
        self.pin = pin
        self._freq = None
        self._last_duty = None
    def freq(self, f=None):
        self._freq = f
    def duty_u16(self, val):
        self._last_duty = int(val)

def reload_module_with(cinem_inv_func):
    # inject stubs BEFORE import/reload du module testé
    m = types.ModuleType("machine")
    m.Pin = StubPin
    m.PWM = StubPWM
    sys.modules["machine"] = m

    # fake groupe_projet_test avec la cinématique souhaitée
    g = types.ModuleType("groupe_projet_test")
    g.cinematique_inverse = cinem_inv_func
    sys.modules["groupe_projet_test"] = g

    # (re)charger le module testé
    if "def_envoyer_angles_compenses" in sys.modules:
        return importlib.reload(sys.modules["def_envoyer_angles_compenses"])
    return importlib.import_module("def_envoyer_angles_compenses")

from traducteur_servo import traduit as angle_to_duty

class TestDefEnvoyerAnglesCompenses(unittest.TestCase):
    def test_center_position_sends_90_deg(self):
        mod = reload_module_with(lambda x, y: (0.0, 0.0))
        servo_a, servo_b = mod.servo_epaule, mod.servo_coude

        a, b = mod.envoyer_angles(0, 0)
        self.assertAlmostEqual(a, 90.0)
        self.assertAlmostEqual(b, 90.0)
        self.assertEqual(servo_a._last_duty, angle_to_duty(90.0))
        self.assertEqual(servo_b._last_duty, angle_to_duty(90.0))

    def test_clamping_applied_when_angle_out_of_range(self):
        # alpha = -200 deg -> servo_alpha = 90 - (-200) = 290 -> clamp 180
        mod = reload_module_with(lambda x, y: (math.radians(-200.0), 0.0))
        servo_a, servo_b = mod.servo_epaule, mod.servo_coude

        a, b = mod.envoyer_angles(0, 0)
        self.assertEqual(a, 180.0)
        self.assertEqual(b, 90.0)
        self.assertEqual(servo_a._last_duty, angle_to_duty(180.0))
        self.assertEqual(servo_b._last_duty, angle_to_duty(90.0))

    def test_pwm_called_for_both_servos(self):
        mod = reload_module_with(lambda x, y: (math.radians(10.0), math.radians(20.0)))
        servo_a, servo_b = mod.servo_epaule, mod.servo_coude

        mod.envoyer_angles(1, 2)
        self.assertIsNotNone(servo_a._last_duty)
        self.assertIsNotNone(servo_b._last_duty)
        # valeurs cohérentes avec la conversion angle->duty
        self.assertEqual(servo_a._last_duty, angle_to_duty(mod.envoyer_angles(1,2)[0]))
        self.assertEqual(servo_b._last_duty, angle_to_duty(mod.envoyer_angles(1,2)[1]))

if __name__ == "__main__":
    unittest.main()
