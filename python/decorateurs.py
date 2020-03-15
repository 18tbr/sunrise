"""Pour gérer le temps, on importe le module time
On va utiliser surtout la fonction time() de ce module qui renvoie le nombre
de secondes écoulées depuis le premier janvier 1970 (habituellement).
On va s'en servir pour calculer le temps mis par notre fonction pour
s'exécuter"""

import time



def compute_time():
    """
    Contrôle le temps mis par une fonction pour s'exécuter.
    """

    def decorator(function):
        """Notre décorateur. C'est lui qui est appelé directement LORS
        DE LA DEFINITION de notre fonction (function)"""

        def modified_function(*unnamed, **named):
            """Fonction renvoyée par notre décorateur. Elle se charge
            de calculer le temps mis par la fonction à s'exécuter"""

            tps_avant = time.time()  # Avant d'exécuter la fonction
            res = function(*unnamed, **named)  # On exécute la fonction
            tps_apres = time.time()  # Après l'exécution de la fonction
            tps_execution = tps_apres - tps_avant
            print("La fonction {0} a mis {1} pour s'exécuter".format( \
                        function, tps_execution))
            return res
        return modified_function
    return decorator

def controler_types(*a_args, **a_kwargs):
    """On attend en paramètres du décorateur les types souhaités. On accepte
    une liste de paramètres indéterminés, étant donné que notre fonction
    définie pourra être appelée avec un nombre variable de paramètres et que
    chacun doit être contrôlé"""

    def decorateur(fonction_a_executer):
        """Notre décorateur. Il doit renvoyer fonction_modifiee"""
        def fonction_modifiee(*args, **kwargs):
            """Notre fonction modifiée. Elle se charge de contrôler
            les types qu'on lui passe en paramètres"""

            # La liste des paramètres attendus (a_args) doit être de même
            # Longueur que celle reçue (args)
            if len(a_args) != len(args):
                raise TypeError("le nombre d'arguments attendu n'est pas égal " \
                                "au nombre reçu")
            # On parcourt la liste des arguments reçus et non nommés
            for i, arg in enumerate(args):
                if a_args[i] is not type(args[i]):
                    raise TypeError("l'argument {0} n'est pas du type " \
                                    "{1}".format(i, a_args[i]))

            # On parcourt à présent la liste des paramètres reçus et nommés
            for cle in kwargs:
                if cle not in a_kwargs:
                    raise TypeError("l'argument {0} n'a aucun type " \
                                    "précisé".format(repr(cle)))
                if a_kwargs[cle] is not type(kwargs[cle]):
                    raise TypeError("l'argument {0} n'est pas de type" \
                                    "{1}".format(repr(cle), a_kwargs[cle]))
            return fonction_a_executer(*args, **kwargs)
        return fonction_modifiee
    return decorateur
