import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            absorption_distance = float(row['Absorption Distance']) if row['Absorption Distance'] else None
            row['Absorption Distance'] = absorption_distance
            data.append(row)
    return data

def calculate_statistics(data):
    escape_percentages = {}
    bump_counts = {}
    absorption_distances = {}
    absorbed_photons_count = {}
    
    for row in data:
        a = float(row['Absorption Coefficient (a)'])
        s = float(row['Scattering Coefficient (s)'])
        absorbed = row['Absorbed'] == 'True'
        bump_count = int(row['Bump Count'])
        absorption_distance = float(row['Absorption Distance']) if row['Absorption Distance'] else None

        if (a, s) not in escape_percentages:
            escape_percentages[(a, s)] = [0, 0]  # [total_photons, escaped_photons]
            bump_counts[(a, s)] = [0, 0]  # [total_photons, total_bumps]
            absorption_distances[(a, s)] = 0
            absorbed_photons_count[(a, s)] = 0

        escape_percentages[(a, s)][0] += 1
        escape_percentages[(a, s)][1] += int(not absorbed)

        bump_counts[(a, s)][0] += 1
        bump_counts[(a, s)][1] += bump_count
        
        if absorbed:
            absorbed_photons_count[(a, s)] += 1
            if absorption_distance:
                absorption_distances[(a, s)] += absorption_distance

    for key in escape_percentages:
        escape_percentages[key] = escape_percentages[key][1] / escape_percentages[key][0] * 100

    for key in bump_counts:
        bump_counts[key] = bump_counts[key][1] / bump_counts[key][0]

    for key in absorption_distances:
        if absorbed_photons_count[key] != 0:
            absorption_distances[key] /= absorbed_photons_count[key]

    return escape_percentages, bump_counts, absorption_distances

def plot_data(data, xlabel, ylabel, zlabel, title):
    x = np.unique([key[0] for key in data])
    y = np.unique([key[1] for key in data])
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    for i in range(len(x)):
        for j in range(len(y)):
            Z[j, i] = data[(X[j, i], Y[j, i])]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(title)

    plt.show()

# Read data from CSV
data = read_csv('photon_data_with_position.csv')

# Calculate statistics
escape_percentages, bump_counts, absorption_distances = calculate_statistics(data)

# Plot escape percentage over absorption coefficient
plot_data(escape_percentages, 'Absorption Coefficient (a)', 'Scattering Coefficient (s)', 'Escape Percentage (%)', 'Escape Percentage over Absorption Coefficient')

# Plot average bump count over absorption coefficient
plot_data(bump_counts, 'Absorption Coefficient (a)', 'Scattering Coefficient (s)', 'Average Bump Count', 'Average Bump Count over Absorption Coefficient')

# Plot average absorption distance over absorption coefficient
plot_data(absorption_distances, 'Absorption Coefficient (a)', 'Scattering Coefficient (s)', 'Average Absorption Distance', 'Average Absorption Distance over Absorption Coefficient')
