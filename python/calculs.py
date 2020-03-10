# coding: utf8

import numpy as np
import objects as obj
print(">> Main .py file...")

# Hangar
hangar_x = 1.25
hangar_y = 1.25
hangar_z = 1
# Mobile
mobile_x = .25
mobile_y = .25
mobile_z = .3
# Trajectoire
var_trajectoire = np.random.rand(10, 6)


# 1. DISCRETISATION

def calcul_pas_adapte(trajectoire, pas_maximal):
    """
    Donne le nombre de pas à effectuer pour chaque dimension pour une étape
    dans la trajectoire.

    Pour calculer le pas adapté, on calcule le nombre de pas minimal que l'on
    devra faire pour aller de la source à la destination (la dimension dont le
    pas est le plus petit dicte le nombre de pas).

    :param trajectoire: Trajectoire souhaitée
    :param pas_maximal: vecteur de taille 6 des pas maximaux

    :type trajectoire: np.array
    :type pas_maximal: np.array de taille 6

    :return: Vecteur de taille 9 des pas pour chaque intervalle
    :rtype: np.array
    """
    pass


def discretisation_trajectoire(trajectoire, pas_maximal):
    """
    Discrétise la trajectoire souhaitée en divisant les parties trop grandes en
    pas de longueurs constantes par morceaux plus petits que pas_maximal.
    Renvoie 2 listes :
    1. la liste des points par lesquels il faut passer, inutile pour les
    moteurs mais utile pour tracer les courbes de trajectoire ;
    2. la liste des déplacements infinitésimaux qu'il faut pour passer d'un
    point à un autre. Chacun de ces déplacements infintésimaux est un np.arra
    de 6 dimensions, 3 en position et 3 angulaires.

    :param trajectoire: Trajectoire souhaitée
    :param pas_maximal: vecteur de taille 6 des pas maximaux

    :type trajectoire: np.array
    :type pas_maximal: np.array de taille 6

    :return: Couple d'arrays
    :rtype: (np.array, np.array)

    USING: - calcul_pas_adapte
    """
    pass


# 2. LONGUEUR DES CABLES

def pos_to_cable_length(position):
    """
    cf calcul_longueurs_cables

    Renvoie les longueurs des 8 câbles correspondant à la position du mobile
    dans le hangar.
    Les câbles étant croisés dans le hangar, on introduit en (a) une liste de
    changements d'indices.

    :param pos_coins_mobile: liste des positions des 8 coins du mobile, chaque
    position étant un np.array de taille 3 (x, y, z) dans l'ordre de la
    numérotation donnée sur le schéma.
    :param pos_coins_hangar: liste des positions des 8 coins du hangar, chaque
    position étant un np.array de taille 3 (x, y, z) dans l'ordre de la
    numérotation donnée sur le schéma.

    #########################
    ##### Quel schéma ? #####
    #########################

    :type pos_coins_mobile: np.array
    :type pos_coins_hangar: np.array

    :return: vecteur des longueurs des 8 câbles
    :rtype: np.array de taille 8
    """
    pass


def get_cable_var(mobile, trajectoire_disc, dimensions):
    """
    cf commande_longieurs_cables

    Convertit la trajectoire discrétisée (liste des déplacements infinitésimaux
    qu'il faut réaliser pour parcourir la trajectoire souhaitée) en la liste
    des modifications infinitésimales des longueurs des câbles et la liste des
    longueurs des cordes.

    Pour cela, on doit garder en mémoire (dans des variables locales) la
    position actuelle du module (6 valeurs), ainsi que les longueurs actuelles
    des cordes.

    Pour chaque déplacement infinitésimal dans cette boucle on devra :
    1. Mettre à jour la position mémorisée du mobile (selon les 6 dimensions) ;
    2. Reconstruire les coins du mobile (en prenant en compte l'orientation
    avec reconstruction_coins) ;
    3. Calculer les nouvelles longueurs des cordes ;
    4. En déduire les variations des longueurs des cordes par rapport à celles
    de l'état précédent ;
    5. Mettre à jour les longueurs des cordes.


    :param traj_disc: trajectoire discrétisée dans la première partie du code,
    chaque point de la trajectoire est un np.array de taille 6.
    :param dimensions_mobile: np.array de taille 3 (longueur, largeur, hauteur)
    représentant les dimensions physiques du mobile.
    :param dimensions_hangar: np.array de taille 3 (longueur, largeur, hauteur)
    représentant les dimensions physiques du hangar.

    :type traj_disc: np.array de taille 6
    :type dimensions_mobile: np.array de taille 3
    :type dimensions_hangar: np.array de taille 3

    :return: liste des variations des longueurs des cordes, chaque élément de
    la liste étant un np.array de dimension 8 dont le ième élément est la
    variation de longueur de la ième corde ; liste des longeurs des cordes pour
    chaque itération.
    :rtype: (np.array, np.array)

    USING: - pos_to_cable_length
    """
    pass


if __name__ == '__main__':

    # Trajectoire
    trajectoire = var_trajectoire

    # Hangar
    dimensions_hangar = np.array([hangar_x, hangar_y, hangar_z])
    print("Dimensions du hangar : %s" % dimensions_hangar)
    hangar = obj.Hangar(dimensions_hangar)

    # Mobile
    dimensions_mobile = np.array([mobile_x, mobile_y, mobile_z])
    print("Dimensions du mobile : %s" % dimensions_mobile)
    mobile = obj.Mobile(dimensions_mobile)

    # Main
