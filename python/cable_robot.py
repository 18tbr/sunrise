import numpy as np
import modules.objects as obj

def auto(array, temps, verbose=False):
    for i in range(np.shape(array)[0]):
        print(i, array[i], temps)
    parameters = obj.Parameters()
    traj = obj.Trajectory(parameters, array)

    if verbose:
        print(parameters)
        print(traj)

    # traj.animate(save=False)
    # return


def manual(vecteur, temps):
    print("manual")
    print(vecteur, temps)


def halt():
    print("Interrupting")
