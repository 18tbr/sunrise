# coding: utf8

import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import modules.utils as utils


# PARAMETERS

class Parameters(object):

    def __init__(self):
        """
        Parameters class constructor.
        """
        # Hangar
        self.hangar_x = 125     # cm
        self.hangar_y = 125
        self.hangar_z = 100
        self.dimensions_hangar = np.array([self.hangar_x,
                                           self.hangar_y,
                                           self.hangar_z])
        # Mobile
        self.mobile_x = 25      # cm
        self.mobile_y = 25
        self.mobile_z = 30
        self.dimensions_mobile = np.array([self.mobile_x,
                                           self.mobile_y,
                                           self.mobile_z])
        # maximal steps authorized
        self.max_step_x = 1     # cm
        self.max_step_y = 1
        self.max_step_z = 1
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
        self.units = ['cm', 'rad']


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
            print(f"{self.dim6d[dim]}: {self.dimensions_hangar[dim]:.3f} m")

    def display_mobile(self):
        """Display mobile parameters."""
        print("\nMobile:")
        for dim in range(3):
            print(f"{self.dim6d[dim]}: {self.dimensions_mobile[dim]:.3f} m")


# 3D OBJECTS

class Object3d(object):

    def __init__(self, name, parameters, *args, **kwargs):
        """
        Object3d class constructor.
        """
        super().__init__(*args, **kwargs)
        self._name = name
        self._position = np.array([0, 0, 0, 0, 0, 0])
        # self._dimensions = dimensions

    def __str__(self):
        """
        Prettily display an Object3d.
        """
        str_dim = f"| > Dimensions: {self.dimensions}\n"
        str_pos = f"| > Position: {self.position[0:3]}\n|             {self.position[3:6]}\n"
        str_vertices = "| > Vertices:\n"
        for vertex in self.vertices:
            str_vertices += '|   '
            str_vertices += str(vertex) + '\n'
        return f"\n| {self.name}:\n{str_dim}{str_pos}{str_vertices}"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, destination):
        """
        Move a mobile.
        """
        # change position
        self._position = destination
        # refresh the vertices
        self.vertices = utils.pos_to_vertices(self.position, self.dimensions)
        print(f"{self.name} has moved!")

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
        self.vertices = utils.pos_to_vertices(self.position, self.dimensions)

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
        self.vertices = utils.pos_to_vertices(self.position, self.dimensions)

    @property
    def dimensions(self):
        return self._dimensions


# TRAJECTORY

class Trajectory(object):

    def __init__(self, parameters, array, *args, **kwargs):
        """
        Trajectory class constructor.
        """
        super().__init__(*args, **kwargs)
        self.parameters = parameters
        # initial trajectory
        self.initial_traj = array
        # discretized trajectory
        self.discretized_traj_pos,\
        self.discretized_traj_var = self.get_discretized()
        # cables
        self.cable_length,\
        self.cable_var = self.get_cable()
        # motor rotations
        self.motor_rotation = self.get_rotation()

    def __str__(self):
        """
        Prettily display a trajectory
        """
        display = (
            f"Initial trajectory:\n{self.initial_traj}\n"
            f"Discretized trajectory:\n{self.discretized_traj_pos}\n"
            f"Cable lengths:\n{self.cable_length}\n"
            f"Cable var:\n{self.cable_var}\n"
            f"Motor rotations:\n{self.motor_rotation}\n"
        )
        return display

    def get_discretized(self):
        """
        Discretize a trajectory
        """
        return utils.discretize_traj(self.initial_traj, self.parameters.max_step)

    def get_cable(self):
        """
        Transform a discretized trajectory into the motor cable lengths
        """
        # return None, None
        return utils.disc_to_cable_length(self.discretized_traj_pos,
                                          self.parameters.dimensions_mobile,
                                          self.parameters.dimensions_hangar)

    def get_rotation(self):
        """
        Transform the motor cable lengths into the motor rotations
        """
        return None

    def animate(self, save):
        """
        Animate a trajectory
        """
        print("Animating...")

        def init():
            """
            Initialization function, background of each frame
            """
            trajectory.set_data([], [])
            trajectory.set_3d_properties([])

            # graph.set_data([], [])
            return trajectory, cable1, cable2, cable3, cable4, cable5, cable6, cable7, cable8

        def update_fig(i):
            """
            Animation function
            """
            trajectory.set_data(self.discretized_traj_pos[0:i+1, 0], self.discretized_traj_pos[0:i+1, 1])
            trajectory.set_3d_properties(self.discretized_traj_pos[0:i+1, 2])
            # print(self.cable_length[0:i+1, :])
            # print(self.cable_length[0:i+1])
            cable1.set_data(range(i+1), self.cable_length[0:i+1, 0])
            cable2.set_data(range(i+1), self.cable_length[0:i+1, 1])
            cable3.set_data(range(i+1), self.cable_length[0:i+1, 2])
            cable4.set_data(range(i+1), self.cable_length[0:i+1, 3])
            cable5.set_data(range(i+1), self.cable_length[0:i+1, 4])
            cable6.set_data(range(i+1), self.cable_length[0:i+1, 5])
            cable7.set_data(range(i+1), self.cable_length[0:i+1, 6])
            cable8.set_data(range(i+1), self.cable_length[0:i+1, 7])
            return trajectory, cable1, cable2, cable3, cable4, cable5, cable6, cable7, cable8

        # SETUP
        fig = plt.figure(figsize=(10,6))

        # TRAJECTORY
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        xlim_traj = self.parameters.dimensions_hangar[0]/2
        ylim_traj = self.parameters.dimensions_hangar[1]/2
        zlim_traj = self.parameters.dimensions_hangar[2]/2
        ax.set_xlim3d((-xlim_traj, xlim_traj))
        ax.set_ylim3d((-ylim_traj, ylim_traj))
        ax.set_zlim3d((-zlim_traj, zlim_traj))
        trajectory, = ax.plot([], [], [], marker='')
        # vector = ax.quiver([0], [0], [0], [0], [1], [1])

        # CABLES
        ax2 = fig.add_subplot(1, 2, 2)
        plt.xlim((0, 1.5*len(self.cable_length)))
        plt.ylim((0, 1.1*np.max(self.cable_length)))
        cable1, = ax2.plot([], [], label="1st cable")
        cable2, = ax2.plot([], [], label="2nd cable")
        cable3, = ax2.plot([], [], label="3rd cable")
        cable4, = ax2.plot([], [], label="4th cable")
        cable5, = ax2.plot([], [], label="5th cable")
        cable6, = ax2.plot([], [], label="6th cable")
        cable7, = ax2.plot([], [], label="7th cable")
        cable8, = ax2.plot([], [], label="8th cable")
        plt.legend()


        # SETUP
        plt.tight_layout()
        anim = animation.FuncAnimation(fig, update_fig,
                                       frames=len(self.discretized_traj_pos),
                                       interval=10,
                                       blit=True)
        # save and show
        if save:
            print("Saving gif...")
            anim.save('animation.gif', fps=30)
        plt.show()
