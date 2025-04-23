import rupho
import numpy as np
import time

# Generate synthetic data
np.random.seed(42)  # For reproducibility
n = int(1e6)

incidence = np.random.uniform(1, 89, size=n)  # Incidence angles in degrees
emergence = np.random.uniform(1, 89, size=n)  # Emergence angles in degrees
azimuth = np.random.uniform(1, 359, size=n)   # Azimuth angles in degrees
phase = np.random.uniform(1, 179, size=n)     # Phase angles in degrees

micro_struct = (0.3, 0.3, 0.5, 0, 0.5, 0.5)
scene_geometry = (incidence, emergence, azimuth, phase)

# Time the Rust function
start_time = time.time()
rust_result = rupho.reflectance(*micro_struct, *scene_geometry)
rust_duration = time.time() - start_time
print(f"Rust function execution time: {rust_duration:.4f} seconds")
print(rust_result)
