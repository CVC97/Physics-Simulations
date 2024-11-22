import numpy as np
import matplotlib.pyplot as plt


# data processing
nonlinear_map_data = np.loadtxt(f"data/nonlinear_map_data.csv", delimiter = ",", skiprows = 1)

mu_array = nonlinear_map_data[:,0]
x_n_array = nonlinear_map_data[:,1:]
n_array = np.array([i for i in range(len(x_n_array[0]))])

mu_i_plot_list = [0, 140, 150, 182, 190]
# print(mu_i_plot_list)


# plotting
fig, ax = plt.subplots(figsize=(6,3))
ax.set_xlabel(r'iteration $n$') 
ax.set_ylabel(r'value $x_n$')
ax.grid()
ax.grid(which='minor', color = '#999999', alpha = 0.2, linestyle = '-')
ax.minorticks_on()

for mu_i in mu_i_plot_list:     
    ax.plot(n_array, x_n_array[mu_i], color = "xkcd:red pink", alpha = 0.5, linewidth = 2, label = f"µ={mu_array[mu_i]}")

# ax.plot(n_array, x_n_array[10], color = "xkcd:red pink", alpha = 0.5, linewidth = 2, label = f"µ={mu_array[10]}")

ax.legend()
ax.legend(loc="upper left")

plt.savefig('visualizations/nonlinear_map.pdf', facecolor = 'white', bbox_inches='tight')
plt.show()