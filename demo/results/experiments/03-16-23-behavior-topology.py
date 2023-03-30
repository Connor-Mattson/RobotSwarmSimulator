import matplotlib.pyplot as plt
import numpy as np
import random

if __name__ == "__main__":
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(projection='3d')

    # Create the mesh in polar coordinates and compute corresponding Z.
    r = np.linspace(0, 0.8, 10)
    p = np.linspace(0, 2*np.pi, 10)
    R, P = np.meshgrid(r, p)
    Z = (R * 0.9) + 0.6

    # Express the mesh in the cartesian system.
    X, Y = R*np.cos(P), R*np.sin(P)

    # Plot the surface.
    ax.plot_surface(X, Y, Z, color='grey', alpha=0.5)
    ax.scatter(0.2, 0.25, 0.8, c='red', marker='o', s=100, alpha=1.0, depthshade=0)
    # ax.scatter(0.0, 0.0, 1.2, c='green', marker='o', s=100, alpha=1.0, depthshade=0)
    ax.plot([0.2, 0.2], [0.25, 0.25], [0, 0.8], 'grey', linestyle="--")
    # ax.plot([0.0, 0.0], [0.0, 0.0], [0, 1.2], 'grey', linestyle="--")

    # ax.scatter3D(0.18, 0.25, 0.85, c='red', marker='x', s=15)
    # ax.scatter3D(0.18, 0.28, 0.9, c='red', marker='x', s=15)
    # ax.scatter3D(0.10, 0.28, 0.9, c='red', marker='x', s=15)
    # ax.scatter3D(0.10, 0.18, 0.95, c='red', marker='x', s=15)
    # ax.scatter3D(0.07, 0.15, 0.95, c='red', marker='x', s=15)
    # ax.scatter3D(0.05, 0.12, 0.98, c='red', marker='x', s=15)
    # ax.scatter3D(0.05, 0.08, 1.04, c='red', marker='x', s=15)
    # ax.scatter3D(0.03, 0.04, 1.12, c='red', marker='x', s=15)
    # ax.scatter3D(0.0, 0.02, 1.14, c='red', marker='x', s=15)

    # Tweak the limits and add latex math labels.
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-0.8, 0.8)
    ax.set_zlim(0, 1.5)

    # ax.set_xlabel(r'$C_1$')
    # ax.set_ylabel(r'$C_2$')
    # ax.set_zlabel(r'$C_3$')

    ax.set_zticks([])
    plt.xticks([])
    plt.yticks([])

    ax.autoscale_view('tight')

    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])

    plt.title("Controller Space")
    plt.show()