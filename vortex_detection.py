import numpy as np
import matplotlib.pyplot as plt


def detect_vortex(X, Y, U, V):
    """Calculate and display the rotation of a simulated flow."""

    dx = X[0, 1] - X[0, 0]
    dy = Y[1, 0] - Y[0, 0]

    # Calculate the change in velocity
    dV_dx = np.gradient(V, dx, axis=1)
    dU_dy = np.gradient(U, dy, axis=0)

    # Curl of a 2D velocity field
    vorticity = dV_dx - dU_dy

    fig, ax = plt.subplots(figsize=(7, 5))

    image = ax.contourf(
        X,
        Y,
        vorticity,
        levels=30,
        cmap="coolwarm"
    )

    fig.colorbar(image, ax=ax, label="Vorticity (1/s)")

    ax.set_title("Simulated Vortex Detection")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    return fig, vorticity
