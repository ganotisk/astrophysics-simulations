import numpy as np
import csv

class Photon:
    def __init__(self, position=(0.0,0.0,0.0), direction=None, bump_count=0, escaped=False, absorbed=False, absorption_distance=None):
        self.position = np.array(position)
        if direction is None:
            self.direction = self._random_direction()
        else:
            self.direction = np.array(direction)
        self.bump_count = bump_count
        self.escaped = escaped
        self.absorbed = absorbed
        self.absorption_distance = absorption_distance
    
    def _random_direction(self):
        direction = np.random.rand(3) - 0.5  # Random direction vector
        return direction / np.linalg.norm(direction)  # Normalize to unit vector
    
    def walk(self, l, epsilon, star_radius):
        step_length = np.random.exponential(scale=l)  # Random step length
        new_direction = self._random_direction()  # Random new direction

        step = step_length * new_direction.astype(float)  # Convert to float for compatibility

        self.position += step  # Update position
        self.bump_count += 1  # Increment bump count

        # Check if photon is absorbed
        if np.random.rand() < epsilon:
            self.absorbed = True
            self.absorption_distance = np.linalg.norm(self.position)  # Record absorption position
            return

        # Check if photon escaped
        if np.linalg.norm(self.position) > star_radius:
            self.escaped = True
            return

def simulate_photons(num_photons, star_radius, absorption_range, scattering_range):
    data = []

    for a in absorption_range:
        for s in scattering_range:
            l = 1 / (a + s)  # Mean free path
            epsilon = a * l
            for _ in range(num_photons):
                photon = Photon()
                while not (photon.escaped or photon.absorbed):
                    photon.walk(l, epsilon, star_radius)
                data.append([a, s, photon.bump_count, photon.absorbed, photon.escaped, photon.absorption_distance])

    return data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Absorption Coefficient (a)', 'Scattering Coefficient (s)', 'Bump Count', 'Absorbed', 'Escaped', 'Absorption Distance'])
        writer.writerows(data)

# Simulation parameters
num_photons = 100
star_radius = 10
absorption_range = np.linspace(0.1, 0.9, 100)
scattering_range = np.linspace(0.2, 2.0, 100)

# Simulate photons
output_data = simulate_photons(num_photons, star_radius, absorption_range, scattering_range)

# Save data to CSV
save_to_csv(output_data, 'photon_data_with_position.csv')
