import rupho
import numpy as np

# Generate synthetic data
np.random.seed(42)  # For reproducibility
run = int(1e1)
n = (int(1e4), 10)

incidence = np.random.uniform(0, 90, size=n)  # Incidence angles in degrees
emergence = np.random.uniform(0, 90, size=n)  # Emergence angles in degrees
azimuth = np.random.uniform(0, 360, size=n)   # Azimuth angles in degrees
phase = np.random.uniform(0, 180, size=n)     # Phase angles in degrees

micro_struct = (0.3, 0.3, 0.5, 0, 0.5, 0.5)
scene_geometry = (incidence, emergence, azimuth, phase)

print(rupho.reflectance(*micro_struct, *scene_geometry))
