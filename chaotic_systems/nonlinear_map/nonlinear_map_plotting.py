import numpy as np
import matplotlib.pyplot as plt


# data processing
nonlinear_map_data = np.loadtxt(f"data/nonlinear_map_data.csv", delimiter = ",", skiprows = 1)
nonlinear_map_long_x_data = np.loadtxt(f"data/nonlinear_map_long_x_data.csv", delimiter = ",", skiprows = 1)
nonlinear_map_long_k_data = np.loadtxt(f"data/nonlinear_map_long_k_data.csv", delimiter = ",", skiprows = 1)

# data
mu_array = nonlinear_map_data[:,0]
x_n_array = nonlinear_map_data[:,1:]
n_array = np.array([i for i in range(len(x_n_array[0]))])

# long-term data
mu_long_array = nonlinear_map_long_x_data[:,0]
x_n_long_array = nonlinear_map_long_x_data[:,1:]
k_n_long_array = nonlinear_map_long_k_data[:,1:]
n_long_array = np.array([i for i in range(len(x_n_long_array[0]))])

print(x_n_long_array[5].shape, x_n_array[5].shape, n_long_array.shape, k_n_long_array[5].shape)

mu_i_plot_list = [0, 140, 150, 182, 190]
mu_long_i = [700]


# # plotting x_n
# fig, ax = plt.subplots(figsize=(6,3))
# ax.set_xlabel(r'iteration $n$') 
# ax.set_ylabel(r'value $x_n$')
# ax.grid()
# ax.grid(which='minor', color = '#999999', alpha = 0.2, linestyle = '-')
# ax.minorticks_on()

# for mu_i in mu_i_plot_list:     
#     ax.plot(n_array, x_n_array[mu_i], color = "xkcd:red pink", alpha = 0.5, linewidth = 2, label = f"µ={mu_array[mu_i]}")

# ax.legend()
# ax.legend(loc="upper left")

# plt.savefig('visualizations/nonlinear_map.pdf', facecolor = 'white', bbox_inches='tight')
# plt.show()


# plotting long-term x_n, k_n
fig, ax = plt.subplots(1, 2, figsize=(6,3))
ax[0].set_xlabel(r'iteration $n$') 
ax[0].set_ylabel(r'value $x_n$')
ax[0].grid()
ax[0].grid(which='minor', color = '#999999', alpha = 0.2, linestyle = '-')
ax[0].minorticks_on()

ax[0].plot(n_long_array, x_n_long_array[mu_long_i].T, color = "xkcd:red pink", alpha = 0.5, linewidth = 2, label = f"µ={mu_long_array[mu_long_i]}")
# ax[0].plot([1, 2, 3], [1, 2, 3], color = "xkcd:red pink", alpha = 0.5, linewidth = 2, label = f"µ={mu_long_array[mu_long_i]}")

ax[0].legend()
ax[0].legend(loc="upper left")


ax[1].set_xlabel(r'frequency $\omega$') 
# ax[1].set_ylabel(r'value $k_n$')
ax[1].grid()
ax[1].grid(which='minor', color = '#999999', alpha = 0.2, linestyle = '-')
ax[1].minorticks_on()

ax[1].plot(n_long_array[1:], k_n_long_array[mu_long_i].T[1:], color = "blue", alpha = 0.5, linewidth = 2, label = f"µ={mu_long_array[mu_long_i]}")

ax[1].legend()
ax[1].legend(loc="upper left")

plt.savefig('visualizations/nonlinear_map_long_xk.pdf', facecolor = 'white', bbox_inches='tight')
plt.show()