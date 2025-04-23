import rupho
import numpy as np
import functions as fn
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

# Time the Python function
start_time = time.time()
python_result = fn.reflectance_photometry_HG2(
    *micro_struct, incidence, emergence, azimuth)
python_duration = time.time() - start_time
print(f"Python function execution time: {python_duration:.4f} seconds")

# Optionally print the results to verify correctness (this step can be omitted if just timing)
# print(rust_result)
# print(python_result)
