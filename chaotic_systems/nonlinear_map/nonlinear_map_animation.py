from manim import *


# data processing
nonlinear_map_data = np.loadtxt(f"data/nonlinear_map_data.csv", delimiter = ",", skiprows = 1)

mu_array = nonlinear_map_data[:,0]
x_n_array = nonlinear_map_data[:,1:]
x_n_long_array = nonlinear_map_data[:,10:]
n_array = np.array([i for i in range(len(x_n_array[0]))])