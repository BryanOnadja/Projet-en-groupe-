import time

# Import des modules faits par le groupe
from servo_control import setup_servos, move_servos     # Paul-Henri / Koami
from inputs import setup_inputs, read_potentiometers    # Bryan
from pen_module import pen_up, pen_down                 # Bryan
from angle_converter import convert_to_angles           # Aymeric


def init_hardware():
    """
    Initialise les servos + entrées et place le stylo en sécurité.
    Retourne (servos, inputs) pour être utilisés dans la boucle principale.
    """
    servos = setup_servos()          # fourni par Paul-Henri
    inputs = setup_inputs()          # fourni par Koami
    pen_up(servos)                   # stylo levé au démarrage
    return servos, inputs


def loop_main():
    """
    Boucle principale :
    - lit les potentiomètres
    - convertit en angles
    - bouge les servos
    - gère le stylo via bouton
    """

    servos, inputs = init_hardware()

    while True:
        # Lecture des deux potentiomètres ADC
        adc_shoulder, adc_elbow = read_potentiometers(inputs)

        # Conversion ADC → angles
        angle_shoulder, angle_elbow = convert_to_angles(adc_shoulder, adc_elbow)

        # Mouvement des servos
        move_servos(servos, angle_shoulder, angle_elbow)

        # Gestion du stylo via bouton
        if inputs.button.value():    # ou read_pen_button(inputs)
            pen_down(servos)
        else:
            pen_up(servos)

        time.sleep(0.02)


def main():
    print("Le programme commence maintenant...")

    # On lance la boucle principale
    loop_main()

if __name__ == "__main__":
    main()