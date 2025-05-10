from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np
import rupho as rp
import pylab as pl
import pyvista as pv

def generate_multifractal_field(size, alpha=1.8, C1=0.1, H=0.5):
    nx, ny = size
    kx = np.fft.fftfreq(nx).reshape(-1, 1)
    ky = np.fft.fftfreq(ny).reshape(1, -1)
    k = np.sqrt(kx**2 + ky**2)
    k[0, 0] = 1e-10

    phi = np.random.uniform(0, 2 * np.pi, (nx, ny))
    noise = np.exp(1j * phi)
    amplitude = k ** (-(H + 1))
    spectrum = noise * amplitude
    field = np.fft.ifft2(spectrum).real
    field -= field.min()
    field /= field.max()
    field = np.exp(-C1 * field ** alpha)

    return field

def compute_shading(elevation, light_vector):
    dx, dy = np.gradient(elevation)
    normal = np.dstack((-dx, -dy, np.ones_like(elevation)))
    norm = np.linalg.norm(normal, axis=2)
    normal /= norm[..., np.newaxis]

    light_vector = np.array(light_vector)
    light_vector = light_vector / np.linalg.norm(light_vector)

    shading = np.clip(np.tensordot(normal, light_vector, axes=([2], [0])), 0, 1)
    return shading

# Parameters
size = (512, 512)
alpha = 1.8
C1 = 0.1
H = 0.5
light_vector = [1, 1, 1]  # Incident light direction

# Generate terrain
terrain = generate_multifractal_field(size, alpha, C1, H)
shading = compute_shading(terrain, light_vector)

# Visualization
fig, ax = plt.subplots()
ax.imshow(shading, cmap='gray', origin='lower')
ax.set_title('Shaded Relief of Multifractal Terrain')
ax.axis('off')
plt.tight_layout()
plt.show()


def generate_multifractal_field(size, alpha=1.8, C1=0.1, H=0.5):
    nx, ny = size
    kx = np.fft.fftfreq(nx).reshape(-1, 1)
    ky = np.fft.fftfreq(ny).reshape(1, -1)
    k = np.sqrt(kx**2 + ky**2)
    k[0, 0] = 1e-10

    phi = np.random.uniform(0, 2 * np.pi, (nx, ny))
    noise = np.exp(1j * phi)
    amplitude = k ** (-(H + 1))
    spectrum = noise * amplitude
    field = np.fft.ifft2(spectrum).real
    field -= field.min()
    field /= field.max()
    field = np.exp(-C1 * field ** alpha)

    return field

# Parameters
size = (256, 256)
alpha = 1.8
C1 = 0.1
H = 0.5

terrain = generate_multifractal_field(size, alpha, C1, H)
shading = compute_shading(terrain, light_vector)

# Create grid
nx, ny = size
x = np.linspace(0, 1, nx)
y = np.linspace(0, 1, ny)
x, y = np.meshgrid(x, y)
z = terrain

# Create structured grid
grid = pv.StructuredGrid(x, y, z)
plotter = pv.Plotter()
plotter.add_mesh(grid, scalars=shading, cmap='gray', lighting=False)
plotter.show()