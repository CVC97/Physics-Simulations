from manim import *


# visualization of three proteins (low, medium, and high number of H-H links)
A3_protein_folding_high_energy_data = np.loadtxt("data/protein_folding_high_energy.csv", delimiter = ",", skiprows = 1)
A3_protein_folding_medium_energy_data = np.loadtxt("data/protein_folding_medium_energy.csv", delimiter = ",", skiprows = 1)
A3_protein_folding_low_energy_data = np.loadtxt("data/protein_folding_low_energy.csv", delimiter = ",", skiprows = 1)

# data processing
high_m_array = A3_protein_folding_high_energy_data[:,0].astype(int)
high_n_array = A3_protein_folding_high_energy_data[:,1].astype(int)
high_status_array = A3_protein_folding_high_energy_data[:,2].astype(int)
high_energy = A3_protein_folding_high_energy_data[-1,3]
len_high = len(high_m_array)

medium_m_array = A3_protein_folding_medium_energy_data[:,0].astype(int)
medium_n_array = A3_protein_folding_medium_energy_data[:,1].astype(int)
medium_status_array = A3_protein_folding_medium_energy_data[:,2].astype(int)
medium_energy = A3_protein_folding_medium_energy_data[-1,3]
len_medium = len(medium_m_array)

low_m_array = A3_protein_folding_low_energy_data[:,0].astype(int)
low_n_array = A3_protein_folding_low_energy_data[:,1].astype(int)
low_status_array = A3_protein_folding_low_energy_data[:,2].astype(int)
low_energy = A3_protein_folding_low_energy_data[-1,3]
len_low = len(low_m_array)

mn_ticks = np.arange(0, 31, 5)

# hydrophobicity arrays
hydrophobicity_high_array = np.zeros((31, 31))
hydrophobicity_medium_array = np.zeros((31, 31))
hydrophobicity_low_array = np.zeros((31, 31))
# H-H linker lists
hh_high_x_list = []
hh_high_y_list = []
hh_medium_x_list = []
hh_medium_y_list = []
hh_low_x_list = []
hh_low_y_list = []
# place first monomers
if (high_status_array[0] == 1):
    hydrophobicity_high_array[15,15] = 1
if (medium_status_array[0] == 1):
    hydrophobicity_medium_array[15,15] = 1
if (low_status_array[0] == 1):
    hydrophobicity_low_array[15,15] = 1

# high:iterate through polymers
for i in range(1, len_high):
    m_prior = high_m_array[i-1]
    n_prior = high_n_array[i-1]
    m = high_m_array[i]
    n = high_n_array[i]
    delta_m = m_prior-m
    delta_n = n_prior-n
    state = high_status_array[i]
    if (state == 1):
        hydrophobicity_high_array[m,n] = 1
        # NORTH
        if (m != 0 and hydrophobicity_high_array[m-1,n] == 1 and delta_m != -1):
            hh_high_x_list.append(n)
            hh_high_y_list.append(m-0.5)
        # EAST
        if (n != 30 and hydrophobicity_high_array[m,n+1] == 1 and delta_n != 1):
            hh_high_x_list.append(n+0.5)
            hh_high_y_list.append(m)
        # SOUTH
        if (m != 30 and hydrophobicity_high_array[m+1,n] == 1 and delta_m != 1):
            hh_high_x_list.append(n)
            hh_high_y_list.append(m+0.5)
        # WEST
        if (n != 0 and hydrophobicity_high_array[m,n-1] == 1 and delta_n != -1):
            hh_high_x_list.append(n-0.5)
            hh_high_y_list.append(m)

for i in range(1, len_medium):
    m_prior = medium_m_array[i-1]
    n_prior = medium_n_array[i-1]
    m = medium_m_array[i]
    n = medium_n_array[i]
    delta_m = m_prior-m
    delta_n = n_prior-n
    state = medium_status_array[i]
    if (state == 1):
        hydrophobicity_medium_array[m,n] = 1
        # NORTH
        if (m != 0 and hydrophobicity_medium_array[m-1,n] == 1 and delta_m != -1):
            hh_medium_x_list.append(n)
            hh_medium_y_list.append(m-0.5)
        # EAST
        if (n != 30 and hydrophobicity_medium_array[m,n+1] == 1 and delta_n != 1):
            hh_medium_x_list.append(n+0.5)
            hh_medium_y_list.append(m)
        # SOUTH
        if (m != 30 and hydrophobicity_medium_array[m+1,n] == 1 and delta_m != 1):
            hh_medium_x_list.append(n)
            hh_medium_y_list.append(m+0.5)
        # WEST
        if (n != 0 and hydrophobicity_medium_array[m,n-1] == 1 and delta_n != -1):
            hh_medium_x_list.append(n-0.5)
            hh_medium_y_list.append(m)

for i in range(1, len_low):
    m_prior = low_m_array[i-1]
    n_prior = low_n_array[i-1]
    m = low_m_array[i]
    n = low_n_array[i]
    delta_m = m_prior-m
    delta_n = n_prior-n
    state = low_status_array[i]
    if (state == 1):
        hydrophobicity_low_array[m,n] = 1
        # NORTH
        if (m != 0 and hydrophobicity_low_array[m-1,n] == 1 and delta_m != -1):
            hh_low_x_list.append(n)
            hh_low_y_list.append(m-0.5)
        # EAST
        if (n != 30 and hydrophobicity_low_array[m,n+1] == 1 and delta_n != 1):
            hh_low_x_list.append(n+0.5)
            hh_low_y_list.append(m)
        # SOUTH
        if (m != 30 and hydrophobicity_low_array[m+1,n] == 1 and delta_m != 1):
            hh_low_x_list.append(n)
            hh_low_y_list.append(m+0.5)
        # WEST
        if (n != 0 and hydrophobicity_low_array[m,n-1] == 1 and delta_n != -1):
            hh_low_x_list.append(n-0.5)
            hh_low_y_list.append(m)