# coding: utf8

from utils import rotation, pos_to_sommets
import decorators as dec
import matplotlib.pyplot as plt
print(">> Loading module: 'objects'...")


class Objet3d:

    def __init__(self, name, dimensions):
        """
        Initialize an Objet3d.
        """
        self._name = name
        self._position = Coord6d([0,0,0,0,0,0])
        self._dimensions = dimensions
        self.sommets = pos_to_sommets(self._position, self._dimensions)

    def __str__(self):
        """
        Prettily display an Objet3d.
        """
        str_dim = "| > Dimensions: {}\n".format(self.dimensions)
        str_pos = "| > Position: {}\n|             {}\n".format(
                  self.position.spatial, self.position.angular)
        str_sommets = "| > Sommets:\n"
        for sommet in self.sommets:
            str_sommets += '|   '
            str_sommets += str(sommet) + '\n'
        return "\n| {}:\n{}{}{}".format(self.name, str_dim, str_pos, str_sommets)

    @property
    def position(self):
        return self._position

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def name(self):
        return self._name


class Mobile(Objet3d):

    def __init__(self, name, dimensions):
        """
        Initialize a mobile.
        """
        Objet3d.__init__(self, name, dimensions)

    def move(self, destination):
        """
        Move a mobile.
        """
        # change position
        self.position.move(destination)
        # refresh the sommets
        self.sommets = pos_to_sommets(self.position, self.dimensions)


class Hangar(Objet3d):

    def __init__(self, name, dimensions):
        """
        Initialize a hangar.
        """
        Objet3d.__init__(self, name, dimensions)


class Coord6d:

    def __init__(self, coord=[0,0,0,0,0,0]):
        """
        Initialize a Coord6d object.
        """
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



class Coord3d:

    def __init__(self, coord=[0,0,0]):
        """
        Initialize a Coord3d object.
        """
        x, y, z = coord
        self.x = x
        self.y = y
        self.z = z
        self.spatial = [x, y, z]

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


class Trajectoire:

    def __init__(self, name, array):
        """
        Class constructor.
        """
        self._name = name  # Accessible uniquement en lecture
        self.array = array
        pass

    @property
    def name(self):
        """
        Accéder en lecture à name
        """
        return self._name

    def __str__(self):
        """
        Prettily display a trajectory
        """
        return "Trajectoire :\n" + str(self.array)

    def dx(self, nb_steps, j):
        return (self.array[j+1][0] - self.array[j][0]) / nb_steps[j]

    def dy(self, nb_steps, j):
        return (self.array[j+1][1] - self.array[j][1]) / nb_steps[j]

    def dz(self, nb_steps, j):
        return (self.array[j+1][2] - self.array[j][2]) / nb_steps[j]

    def da(self, nb_steps, j):
        return (self.array[j+1][3] - self.array[j][3]) / nb_steps[j]

    def db(self, nb_steps, j):
        return (self.array[j+1][4] - self.array[j][4]) / nb_steps[j]

    def dg(self, nb_steps, j):
        return (self.array[j+1][5] - self.array[j][5]) / nb_steps[j]

    def plot(self):
        """
        Plot a trajectory
        """
        fig = plt.figure('Trajectoire {0}'.format(self.name))
        fig.suptitle('Trajectoire {0}'.format(self.name))
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
