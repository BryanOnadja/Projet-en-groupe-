def normalize_adc(adc_value):
    """Convertit une valeur ADC brute en ratio 0.0 → 1.0."""
    if adc_value < 0:
        adc_value = 0
    if adc_value > 65535:
        adc_value = 65535
    return adc_value / 65535


def convert_to_angles(adc_shoulder, adc_elbow):
    """
    Transforme les valeurs ADC (0 → 65535) en angles pour les servos.
    Retourne (angle_epaule, angle_coude).
    """

    # À ajuster selon la calibration du bras mécanique
    SHOULDER_MIN = 25   # degrés
    SHOULDER_MAX = 150  # degrés

    ELBOW_MIN = 20      # degrés
    ELBOW_MAX = 160     # degrés

    r_shoulder = normalize_adc(adc_shoulder)
    r_elbow    = normalize_adc(adc_elbow)

    # Conversion en angles
    angle_shoulder = SHOULDER_MIN + r_shoulder * (SHOULDER_MAX - SHOULDER_MIN)
    angle_elbow    = ELBOW_MIN    + r_elbow    * (ELBOW_MAX    - ELBOW_MIN)

    return angle_shoulder, angle_elbow