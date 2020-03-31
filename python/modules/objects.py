# coding: utf8

import modules.utils as utils
import matplotlib.pyplot as plt


class Object3d(object):

    def __init__(self, name, dimensions, *args, **kwargs):
        """
        Object3d class constructor.
        """
        super().__init__(*args, **kwargs)
        self._name = name
        self._position = Coord6d([0, 0, 0, 0, 0, 0])
        self._dimensions = dimensions
        self.vertices = [Coord3d(vertex) for vertex in utils.pos_to_vertices(self.position, self.dimensions)]

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
    def dimensions(self):
        return self._dimensions

    @property
    def name(self):
        return self._name


class Mobile(Object3d):

    def __init__(self, dimensions, *args, **kwargs):
        """
        Mobile class constructor.
        """
        super().__init__("Mobile", dimensions, *args, **kwargs)


class Hangar(Object3d):

    def __init__(self, dimensions, *args, **kwargs):
        """
        Hangar class constructor.
        """
        super().__init__("Hangar", dimensions, *args, **kwargs)


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

    def __init__(self, array, max_step, *args, **kwargs):
        """
        Trajectory class constructor.
        """
        super().__init__(*args, **kwargs)
        self.name = "Initial"
        self.array = array
        self.max_step = max_step

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

    def dx(self, nb_steps, j):
        """Returns the infinitesimal distance along the x direction
        for the j-th interval of self."""
        return (self.array[j+1][0] - self.array[j][0]) / nb_steps[j]

    def dy(self, nb_steps, j):
        """Returns the infinitesimal distance along the y direction
        for the j-th interval of self."""
        return (self.array[j+1][1] - self.array[j][1]) / nb_steps[j]

    def dz(self, nb_steps, j):
        """Returns the infinitesimal distance along the z direction
        for the j-th interval of self."""
        return (self.array[j+1][2] - self.array[j][2]) / nb_steps[j]

    def da(self, nb_steps, j):
        """Returns the infinitesimal distance along the a direction
        for the j-th interval of self."""
        return (self.array[j+1][3] - self.array[j][3]) / nb_steps[j]

    def db(self, nb_steps, j):
        """Returns the infinitesimal distance along the b direction
        for the j-th interval of self."""
        return (self.array[j+1][4] - self.array[j][4]) / nb_steps[j]

    def dg(self, nb_steps, j):
        """Returns the infinitesimal distance along the g direction
        for the j-th interval of self."""
        return (self.array[j+1][5] - self.array[j][5]) / nb_steps[j]

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
