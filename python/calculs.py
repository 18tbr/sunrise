# coding: utf8

import numpy as np
import time
import math

import modules.objects as obj

print(">> Running calculs.py...")

# VARIABLES #

# Hangar
hangar_x = 1.25
hangar_y = 1.25
hangar_z = 1
dimensions_hangar = np.array([hangar_x, hangar_y, hangar_z])
# Mobile
mobile_x = .25
mobile_y = .25
mobile_z = .3
dimensions_mobile = np.array([mobile_x, mobile_y, mobile_z])

# Trajectoire
# array_trajectory = np.random.rand(10, 6)
array_trajectory = np.array([[0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0]])
# maximal steps authorized
max_step_x = 0.1
max_step_y = 0.1
max_step_z = 0.1
max_step_alpha = math.radians(10)
max_step_beta = math.radians(10)
max_step_gamma = math.radians(10)
# array
max_step = np.array([max_step_x, max_step_y, max_step_z,
                     max_step_alpha, max_step_beta, max_step_gamma])


# DISPLAY #
display = False
dim6d = ['x ', 'y ', 'z ', 'alpha', 'beta ', 'gamma']
typedim = ['translation', 'rotation']
units = ['m', 'rad']




def display_pas():
    for dim in range(6):
        print("Pas de %s %s : %.3f %s" % (typedim[dim//3],
                                          dim6d[dim],
                                          max_step[dim],
                                          units[dim//3]
                                          ))


# MAIN #

def main():
    # trajectory
    trajectory = obj.Trajectory("souhaitee", array_trajectory)
    traj_disc = obj.Trajectory("discretisee", discretize_traj(trajectory, max_step)[0])


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("\n*** End ***\n"
          "Start: {0}\n"
          "End: {1}\n"
          "Time Elapsed: {2:.2f}s".format(
            time.strftime("%Hh%Mm%Ss", time.localtime(start_time)),
            time.strftime("%Hh%Mm%Ss", time.localtime(end_time)),
            end_time - start_time))
