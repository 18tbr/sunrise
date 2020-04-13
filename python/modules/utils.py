# coding: utf8

import numpy as np
import math


# PART 1 : TRAJECTORY DISCRETIZATION #

def init_vertices(dimensions):
    lx, ly, lz = dimensions
    return np.array([[lx/2, -ly/2, -lz/2],
                     [lx/2, -ly/2, lz/2],
                     [lx/2, ly/2, -lz/2],
                     [lx/2, ly/2, lz/2],
                     [-lx/2, ly/2, -lz/2],
                     [-lx/2, ly/2, lz/2],
                     [-lx/2, -ly/2, -lz/2],
                     [-lx/2, -ly/2, lz/2]])


def pos_to_vertices(position, dimensions):
    vertices = init_vertices(dimensions)
    for vertex in range(8):
        vertices[vertex] = np.dot(rotation(position[3:6]), vertices[vertex])\
                          + position[0:3]
    # vertices = [obj.Coord3d(vertex) for vertex in vertices]
    return vertices


def rotation(angular_vect):
    rho = angular_vect[0]
    theta = angular_vect[1]
    phi = angular_vect[2]

    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rho), np.sin(rho)],
                   [0, -np.sin(rho), np.cos(rho)]])

    Ry = np.array([[np.cos(theta), 0, -np.sin(theta)],
                   [0, 1, 0],
                   [np.sin(theta), 0, np.cos(theta)]])

    Rz = np.array([[np.cos(phi), np.sin(phi), 0],
                   [-np.sin(phi), np.cos(phi), 0],
                   [0, 0, 1]])

    return np.dot(np.dot(Rx, Ry), Rz)


def calcul_nb_steps(array, max_step):
    """
    For each interval of the trajectory, gives the number of steps into which
    we are going to discretize it.

    If j is the inverval we consider, we compute the number of steps we have to
    do for each dimension in j, and we take the maximum of these numbers. The
    biggest number of steps (i.e. the lowest step) is then conserved.

    :param trajectory: trajectory we want the mobile to follow
    :param max_step: maximal step for each dimension

    :type array: np.array
    :type max_step: np.array (size 6)

    :return: number of steps into which each interval is discretized
    :rtype: list [ , , ...]
    """

    def calcul_nb_steps_interval(array, j):
        """
        Gives the number of steps to do for one interval j.
        At first, we compute the number of steps needed for each dimension
        (x, y, z, alpha, beta, gamma); then we take the maximum of these values
        and we round it to the next integer.
        """
        nb_steps_dim = []
        for dim in range(6):
            nb_steps_dim.append(abs(array[j+1][dim] -
                                    array[j][dim]) / max_step[dim])
        return math.ceil(max(nb_steps_dim))

    nb_interval = len(array) - 1
    nb_steps = []
    for j in range(nb_interval):
        nb_steps.append(calcul_nb_steps_interval(array, j))

    assert len(array) - 1 == len(nb_steps)
    return nb_steps


def discretize_traj(array, max_step):
    """
    Discretize the trajectory by cutting intervals into constant valued steps,
    of value inferior to max_step.
    Return 2 lists:
    1. the list of the points in space (6D) we have to go through. It is
    useless for the motors but it will be useful to plot the trajectory;
    2. the list of the infinitesimal moves we need to do to go from a point to
    another.

    :param array: array attribute of the trajectory we want the mobile to
    follow
    :param max_step: maximal step for each dimension

    :type array: np.array
    :type max_step: np.array (size 6)

    :return: points we have to go through; infinitesimal moves
    :rtype: (list, list)
    """
    nb_steps = calcul_nb_steps(array, max_step)
    nb_interval = len(array) - 1

    traj_disc = []
    var_disc = []
    for j in range(nb_interval):
        # for each interval between 2 points of the trajectory
        nb_steps_j = nb_steps[j]
        dx = (array[j+1][0] - array[j][0]) / nb_steps_j
        dy = (array[j+1][1] - array[j][1]) / nb_steps_j
        dz = (array[j+1][2] - array[j][2]) / nb_steps_j
        da = (array[j+1][3] - array[j][3]) / nb_steps_j
        db = (array[j+1][4] - array[j][4]) / nb_steps_j
        dg = (array[j+1][5] - array[j][5]) / nb_steps_j

        for i in range(0, nb_steps[j]):
            # for each step
            x = array[j][0] + i * dx
            y = array[j][1] + i * dy
            z = array[j][2] + i * dz
            a = array[j][3] + i * da
            b = array[j][4] + i * db
            g = array[j][5] + i * dg

            traj_disc.append([x, y, z, a, b, g])
            var_disc.append([dx, dy, dz, da, db, dg])

    print("Trajectory is discretized")
    return np.array(traj_disc), np.array(var_disc)


# PART 2: CABLE LENGTHS #

def pos_to_cable_length(position, dimensions_mobile, dimensions_hangar):
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

    :type pos_coins_mobile: np.array
    :type pos_coins_hangar: np.array

    :return: vecteur des longueurs des 8 câbles
    :rtype: np.array de taille 8
    """
    cable_length = np.zeros(8)
    # cable are crossed
    chg_num = [6, 7, 4, 5, 2, 3, 0, 1]
    vertices_mobile = pos_to_vertices(position, dimensions_mobile)
    vertices_hangar = pos_to_vertices([0, 0, 0, 0, 0, 0], dimensions_hangar)
    # for each cable
    for cable in range(8):
        # get vector of the cable
        cable_vector = vertices_mobile[chg_num[cable]] - vertices_hangar[cable]
        # get norm of vector
        cable_length[cable] = np.linalg.norm(cable_vector)
    return cable_length


def disc_to_cable_lengths(discretized_traj, dimensions_mobile, dimensions_hangar):
    """
    cf commande_longueurs_cables

    Convertit la trajectory discrétisée (liste des déplacements infinitésimaux
    qu'il faut réaliser pour parcourir la trajectory souhaitée) en la liste
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


    :param traj_disc: trajectory discrétisée dans la première partie du code,
    chaque point de la trajectory est un np.array de taille 6.
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

    # 1. get cable lengths (applying np.vectorize to pos_to_cable_length)
    mapping = lambda array: pos_to_cable_length(array, dimensions_mobile, dimensions_hangar)
    cable_length = np.vectorize(mapping, signature='(m)->(n)')(discretized_traj)

    # 2. get cable variations from cable lengths (using np.diff)
    cable_var = np.diff(cable_length, axis=0)

    print("Cable lengths computed")
    return np.array(cable_length), np.array(cable_var)


def len_to_rotations(cable_var, drum_motor_diameter):
    """
    docstring to do
    first variations, then rotation
    """

    nb_interval = len(cable_var)
    # 1. get rotation variations (simple product)
    motor_var = 2 * cable_var / drum_motor_diameter

    # 2. get rotations from variations (using np.cumsum)
    motor_rotation = np.zeros((len(cable_var) + 1, 8))
    motor_rotation[1:] = np.cumsum(motor_var, axis=0, dtype=float)

    print("Motor rotations computed")
    return np.array(motor_rotation), motor_var

