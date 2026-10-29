import matplotlib.pyplot as plt


def show_insect_eye(X, Y, U, V):
    """Display a simulated insect-eye sensing array."""

    fig, ax = plt.subplots(figsize=(7, 6))

    ax.quiver(
        X,
        Y,
        U,
        V,
        color="blue",
        angles="xy"
    )

    ax.set_title("Insect-Eye Optical Flow Array")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)

    return fig
