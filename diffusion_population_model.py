import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
L = 50    # Spatial domain length
N = 50    # Number of grid points
dx = L / N
dt = 0.05  # Time step
T = 10    # Total simulation time

# Diffusion coefficients
Du = 0.1
Dv = 0.05

# Growth, predation, and mortality rates
r = 0.6
K = 1.0
alpha = 0.02
beta = 0.01
delta = 0.1

# Initialize the grid
u = np.zeros((N, N))
v = np.zeros((N, N))

# Initial conditions
u[N//4:3*N//4, N//4:3*N//4] = 0.5
v[N//2:N//2+5, N//2:N//2+5] = 0.1

# Function to compute the Laplacian
def laplacian(Z):
    return (np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) + 
            np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) - 
            4 * Z) / dx**2

# Create a figure for the animation
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Set up the initial plots for prey and seagull populations
contour_u = ax[0].contourf(np.linspace(0, L, N), np.linspace(0, L, N), u, cmap='viridis')
ax[0].set_title('Prey Density')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
plt.colorbar(contour_u, ax=ax[0])

contour_v = ax[1].contourf(np.linspace(0, L, N), np.linspace(0, L, N), v, cmap='plasma')
ax[1].set_title('Seagull Density')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
plt.colorbar(contour_v, ax=ax[1])

# Function to update the frames
def update(frame):
    global u, v, contour_u, contour_v
    
    # Compute the new population densities
    u_new = u + dt * (Du * laplacian(u) + r * u * (1 - u / K) - alpha * u * v)
    v_new = v + dt * (Dv * laplacian(v) + beta * u * v - delta * v)
    
    u, v = u_new, v_new
    
    # Update the contour plots
    for c in contour_u.collections:
        c.remove()
    for c in contour_v.collections:
        c.remove()
    
    contour_u = ax[0].contourf(np.linspace(0, L, N), np.linspace(0, L, N), u, cmap='viridis')
    contour_v = ax[1].contourf(np.linspace(0, L, N), np.linspace(0, L, N), v, cmap='plasma')
    
    return contour_u.collections + contour_v.collections

# Create the animation
ani = FuncAnimation(fig, update, frames=range(int(T / dt)), blit=True)

# Save the animation as an MP4 file
ani.save('seagull_prey_interaction_contour_fixed1.mp4', writer='ffmpeg', fps=15)

# Display the animation
plt.show()

