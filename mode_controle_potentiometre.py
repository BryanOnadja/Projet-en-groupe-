def mode_controle_potentiometre():
    """
    Mode de contrôle manuel avec les potentiomètres du Pico.

    - Les deux potentiomètres contrôlent la position X/Y de la pointe.
    - Un bouton permet d’alterner stylo levé / stylo baissé.
    - La fonction tourne en boucle jusqu’à un Ctrl+C (KeyboardInterrupt).
    """

    print("Mode contrôle par potentiomètres (Ctrl+C pour arrêter)")

    # Charge les tables de calibration des servos
    err_epaule, err_coude = configuration_calibration()

    # Bouton pour lever/abaisser le stylo (GPIO3, avec pull-up)
    bouton_stylo = Pin(3, Pin.IN, Pin.PULL_UP)

    dernier_toggle = 0.0      # dernier moment où on a changé l'état du stylo
    DEBOUNCE = 0.3            # délai minimum entre deux bascules (en secondes)

    # Position initiale du stylo
    controler_stylo(stylo_leve)

    try:
        while True:
            # Gestion du bouton de stylo (actif à 0)
            if not bouton_stylo.value():     # bouton appuyé
                maintenant = time.time()
                if maintenant - dernier_toggle > DEBOUNCE:
                    # on inverse l'état du stylo
                    controler_stylo(not stylo_leve)
                    dernier_toggle = maintenant
                    # petit délai pour éviter plusieurs lectures du même appui
                    time.sleep(0.05)

            # Lecture des potentiomètres et calcul X/Y
            x, y = lire_position(adc_x, adc_y)

            # Envoi aux servos avec calibration
            try:
                alpha, beta = envoyer_angles_compenses(x, y, err_epaule, err_coude)
                # Affichage sur une seule ligne
                print(
                    f"\rX={x:5.1f}  Y={y:5.1f}  |  Epaule={alpha:5.1f}°  Coude={beta:5.1f}°",
                    end=""
                )
            except ValueError as e:
                # Position hors d’atteinte : on affiche juste le message
                print(f"\r{e}", end="")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nArrêt du contrôle par potentiomètres.")
        # Remet les servos dans un état "neutre"
        servo_epaule.duty_u16(0)
        servo_coude.duty_u16(0)
        # Leve le stylo à l’arrêt
        controler_stylo(True)
