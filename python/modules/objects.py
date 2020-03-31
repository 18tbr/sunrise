# coding: utf8

import modules.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import math


class Parameters(object):

    def __init__(self):
        """
        Parameters class constructor.
        """
        # Hangar
        self.hangar_x = 1.25
        self.hangar_y = 1.25
        self.hangar_z = 1
        self.dimensions_hangar = np.array([self.hangar_x,
                                           self.hangar_y,
                                           self.hangar_z])
        # Mobile
        self.mobile_x = .25
        self.mobile_y = .25
        self.mobile_z = .3
        self.dimensions_mobile = np.array([self.mobile_x,
                                           self.mobile_y,
                                           self.mobile_z])
        # maximal steps authorized
        self.max_step_x = .1
        self.max_step_y = .1
        self.max_step_z = .1
        self.max_step_alpha = math.radians(10)
        self.max_step_beta = math.radians(10)
        self.max_step_gamma = math.radians(10)
        # array
        self.max_step = np.array([self.max_step_x, self.max_step_y,
                                  self.max_step_z, self.max_step_alpha,
                                  self.max_step_beta, self.max_step_gamma])
        # display
        self.display = False
        self.dim6d = ['x', 'y', 'z', 'alpha', 'beta', 'gamma']
        self.typedim = ['translation', 'rotation']
        self.units = ['m', 'rad']


    def __str__(self):
        """
        Display the parameters.
        """
        self.display_step()
        self.display_hangar()
        self.display_mobile()
        return ""


    def display_step(self):
        """Display step parameters."""
        print("\nSteps:")
        for dim in range(6):
            print("{}-{} step: {:.3f} {}".format(self.dim6d[dim],
                                                 self.typedim[dim//3],
                                                 self.max_step[dim],
                                                 self.units[dim//3]))

    def display_hangar(self):
        """Display hangar parameters."""
        print("\nHangar:")
        for dim in range(3):
            print("{}: {:.3f} m".format(self.dim6d[dim],
                                        self.dimensions_hangar[dim]))

    def display_mobile(self):
        """Display mobile parameters."""
        print("\nMobile:")
        for dim in range(3):
            print("{}: {:.3f} m".format(self.dim6d[dim],
                                        self.dimensions_mobile[dim]))


class Object3d(object):

    def __init__(self, name, parameters, *args, **kwargs):
        """
        Object3d class constructor.
        """
        super().__init__(*args, **kwargs)
        self._name = name
        self._position = Coord6d([0, 0, 0, 0, 0, 0])
        # self._dimensions = dimensions

    def __str__(self):
        """
        Prettily display an Object3d.
        """
        str_dim = "| > Dimensions: {}\n".format(self.dimensions)
        str_pos = "| > Position: {}\n|             {}\n".format(
                  self.position.spatial, self.position.angular)
        str_vertices = "| > Vertices:\n"
        for vertex in self.vertices:
            str_vertices += '|   '
            str_vertices += str(vertex) + '\n'
        return "\n| {}:\n{}{}{}".format(self.name, str_dim, str_pos, str_vertices)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, destination):
        """
        Move a mobile.
        """
        # change position
        self.position.move(destination)
        # refresh the vertices
        self.vertices = [Coord3d(vertex) for vertex in utils.pos_to_vertices(self.position, self.dimensions)]
        print('{} has moved!'.format(self.name))


    @property
    def name(self):
        return self._name


class Mobile(Object3d):

    def __init__(self, parameters, *args, **kwargs):
        """
        Mobile class constructor.
        """
        super().__init__("Mobile", parameters, *args, **kwargs)
        self._dimensions = parameters.dimensions_mobile
        self.vertices = [Coord3d(vertex) for vertex in utils.pos_to_vertices(self.position, self.dimensions)]

    @property
    def dimensions(self):
        return self._dimensions


class Hangar(Object3d):

    def __init__(self, parameters, *args, **kwargs):
        """
        Hangar class constructor.
        """
        super().__init__("Hangar", parameters, *args, **kwargs)
        self._dimensions = parameters.dimensions_hangar
        self.vertices = [Coord3d(vertex) for vertex in utils.pos_to_vertices(self.position, self.dimensions)]

    @property
    def dimensions(self):
        return self._dimensions


class Coord3d(object):

    def __init__(self, coord=[0, 0, 0], *args, **kwargs):
        """
        Coord3d class constructor.
        """
        super().__init__(*args, **kwargs)
        x, y, z = coord
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """
        Prettily display a Coord3d object.
        """
        return "({0:.3f}, {1:.3f}, {2:.3f})".format(self.x, self.y, self.z)

    def move(self, destination):
        """
        Change the coordinates.
        """
        self.__init__(destination)


class Coord6d(object):

    def __init__(self, coord=[0, 0, 0, 0, 0, 0], *args, **kwargs):
        """
        Coord6d class constructor.
        """
        super().__init__(*args, **kwargs)
        x, y, z, alpha, beta, gamma = coord
        self.x = x
        self.y = y
        self.z = z
        self.spatial = [x, y, z]
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.angular = [alpha, beta, gamma]

    def __str__(self):
        """
        Prettily display a Coord6d object.
        """
        return "({0:.3f}, {1:.3f}, {2:.3f}, {0:.3f}, {1:.3f}, {2:.3f})".format(
                self.x, self.y, self.z, self.alpha, self.beta, self.gamma)

    def move(self, destination):
        """
        Change the coordinates.
        """
        self.__init__(destination)

    # def change_spatial(self, spatial):
    #     """
    #     Change the spatial coordinates.
    #     """
    #     self.spatial = spatial
    #     self.x, self.y, self.z = spatial

    # def change_angular(self, angular):
    #     """
    #     Change the angular coordinates.
    #     """
    #     self.angular = angular
    #     self.alpha, self.beta, self.gamme = angular


class Trajectory(object):

    def __init__(self, parameters, array, *args, **kwargs):
        """
        Trajectory class constructor.
        """
        super().__init__(*args, **kwargs)
        self.name = "Initial"
        self.array = array
        self.max_step = parameters.max_step

    def __str__(self):
        """
        Prettily display a trajectory.
        """
        return "{} trajectory :\n".format(self.name) + str(self.array)

    def discretize(self):
        """
        Disctretize a trajectory
        """
        assert self.name == "Initial"
        self.array = utils.discretize_traj(self.array, self.max_step)[0]
        self.name = "Discretized"

    # def dx(self, nb_steps, j):
    #     """Returns the infinitesimal distance along the x direction
    #     for the j-th interval of self."""
    #     return (self.array[j+1][0] - self.array[j][0]) / nb_steps[j]

    # def dy(self, nb_steps, j):
    #     """Returns the infinitesimal distance along the y direction
    #     for the j-th interval of self."""
    #     return (self.array[j+1][1] - self.array[j][1]) / nb_steps[j]

    # def dz(self, nb_steps, j):
    #     """Returns the infinitesimal distance along the z direction
    #     for the j-th interval of self."""
    #     return (self.array[j+1][2] - self.array[j][2]) / nb_steps[j]

    # def da(self, nb_steps, j):
    #     """Returns the infinitesimal distance along the a direction
    #     for the j-th interval of self."""
    #     return (self.array[j+1][3] - self.array[j][3]) / nb_steps[j]

    # def db(self, nb_steps, j):
    #     """Returns the infinitesimal distance along the b direction
    #     for the j-th interval of self."""
    #     return (self.array[j+1][4] - self.array[j][4]) / nb_steps[j]

    # def dg(self, nb_steps, j):
    #     """Returns the infinitesimal distance along the g direction
    #     for the j-th interval of self."""
    #     return (self.array[j+1][5] - self.array[j][5]) / nb_steps[j]

    def plot(self):
        """
        Plot a trajectory.
        """
        fig = plt.figure('{0} trajectory'.format(self.name))
        fig.suptitle('{0} trajectory'.format(self.name))
        # 3d graph
        ax = fig.add_subplot(111, projection='3d')
        xdata = self.array[:, 0]
        ydata = self.array[:, 1]
        zdata = self.array[:, 2]
        ax.plot3D(xdata, ydata, zdata)
        ax.scatter3D(xdata, ydata, zdata)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        # Table
        # To do
        # fig.savefig('pics/trajectoire_{0}.png'.format(self.name))
        plt.show()
