# coding: utf8
import numpy as np
import math

import modules.objects as obj

# Trajectory
# array_trajectory = 10 * np.random.rand(10, 6)
array_trajectory = np.array(
    [
        [0, 0, 0, 0, 0, 0],
        [0, 10, 10, 0, 0, 0],
        [10, 10, 10, 0, 0, 0],
        [10, 10, 0, 0, 0, 0],
        [10, 0, 20, 0, 0, 0],
    ],
    dtype=float,
)

if __name__ == "__main__":
    parameters = obj.Parameters()
    # print(parameters)
    traj = obj.Trajectory(parameters, array_trajectory)
    # print(traj)

    # mobile = obj.Mobile(parameters)
    # for emplacement in traj.discretized_traj_pos:
    #     mobile.position = emplacement
    #     print(mobile)

    traj.animate(save=True)
