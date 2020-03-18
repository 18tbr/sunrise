# coding: utf8

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import objects as obj
print(">> Loading module: 'utils'...")


# PARTIE 1 : DISCRETISATION DE LA TRAJECTOIRE #

def init_sommets(dimensions):
    lx, ly, lz = dimensions
    return np.array([[lx/2, -ly/2, -lz/2],
                     [lx/2, -ly/2, lz/2],
                     [lx/2, ly/2, -lz/2],
                     [lx/2, ly/2, lz/2],
                     [-lx/2, ly/2, -lz/2],
                     [-lx/2, ly/2, lz/2],
                     [-lx/2, -ly/2, -lz/2],
                     [-lx/2, -ly/2, lz/2]])


def pos_to_sommets(position, dimensions):
    sommets = init_sommets(dimensions)
    for sommet in range(8):
        sommets[sommet] = np.dot(rotation(position.angular), sommets[sommet])\
                          + position.spatial
    sommets = [obj.Coord3d(sommet) for sommet in sommets]
    # print(sommets[0])
    return sommets


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


# def plot_trajectoire(trajectoire, what):
#     fig = plt.figure("Trajectoire")
#     fig.suptitle('Trajectoire ' + what)
#     # 3d graph
#     ax = fig.add_subplot(111, projection='3d')
#     xdata = trajectoire[:, 0]
#     ydata = trajectoire[:, 1]
#     zdata = trajectoire[:, 2]
#     ax.plot3D(xdata, ydata, zdata)
#     ax.scatter3D(xdata, ydata, zdata)
#     ax.set_xlabel('x')
#     ax.set_ylabel('y')
#     ax.set_zlabel('z')
#     # Table
#     # To do
#     fig.savefig('pics/trajectoire_{0}.png'.format(what))
#     plt.show()
