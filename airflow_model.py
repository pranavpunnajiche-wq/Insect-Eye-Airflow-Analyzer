import numpy as np
import matplotlib.pyplot as plt


def show_airflow():
    """Draw illustrative airflow around an aerofoil."""

    x = np.linspace(-3, 3, 100)
    y = np.linspace(-2, 2, 70)

    X, Y = np.meshgrid(x, y)

    # Illustrative velocity field
    U = np.ones_like(X)
    V = (
        0.8 * np.exp(-((X - 0.2) ** 2) / 1.5)
        * np.exp(-(Y ** 2) / 0.2)
        * Y
    )

    # Aerofoil-like outline
    foil_x = np.linspace(-1.5, 1.5, 200)
    foil_y = 0.12 * np.sin(np.pi * foil_x / 3)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.streamplot(
        X,
        Y,
        U,
        V,
        density=1.2,
        color=np.hypot(U, V),
        cmap="viridis"
    )

    ax.fill_between(
        foil_x,
        foil_y - 0.04,
        foil_y + 0.04,
        color="black"
    )

    ax.set_title("Illustrative Airflow Around an Aerofoil")
    ax.set_xlabel("Horizontal Position")
    ax.set_ylabel("Vertical Position")

    return fig
