import numpy as np
import pickle

array = 10 * np.random.rand(10, 6)

np.save("traj.npy", array)
np.savetxt("traj.txt", array)
np.savetxt("traj.csv", array, delimiter=",")
array.tofile("traj.dat")
with open("traj", "wb") as target:
    pickle.dump(array, target)
