import numpy as np


def generate_flow(grid_size=20, vortex_strength=5.0):
    """Generate a simulated airflow velocity field."""

    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)

    X, Y = np.meshgrid(x, y)

    # Position of the simulated vortex
    vortex_x = 0.5
    vortex_y = 0.0

    dx = X - vortex_x
    dy = Y - vortex_y

    distance_squared = dx**2 + dy**2 + 0.15

    # Simulated rotational airflow
    U = -vortex_strength * dy / distance_squared
    V = vortex_strength * dx / distance_squared

    return X, Y, U, V
