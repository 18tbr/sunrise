# coding: utf8
import numpy as np
import math

import modules.objects as obj

# Trajectoire
# array_trajectory = np.random.rand(10, 6)
array_trajectory = np.array([[0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0]])

if __name__ == "__main__":
    parameters = obj.Parameters()
    print(parameters)
    traj = obj.Trajectory(parameters, array_trajectory)
    print(traj)
    traj.discretize()
    print(traj)
    mobile = obj.Mobile(parameters)
    for emplacement in traj.array:
        mobile.position = emplacement
        print(mobile)
