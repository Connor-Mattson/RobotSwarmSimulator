import numpy as np
import pandas
import matplotlib.pyplot as plt

if __name__ == "__main__":
    COLUMNS = {
        "_": -1,
        "POP": 0,
        "SEED": 1,
        "TOTAL_STEPS": 2,
        'CONVEX_HULL': 3,
        "INVERSE_HULL": 4,
        "ELEMS_0D": 5,
        'ELEMS_1D': 6,
        "MAX_0D": 7,
        "MAX_1D": 8,
    }

    # Import Data
    cyclic_ds = pandas.read_csv("out/geometry-cyclic.csv")
    aggregation_ds = pandas.read_csv("out/geometry-aggregation.csv")
    dispersal_ds = pandas.read_csv("out/geometry-dispersal.csv")
    milling_ds = pandas.read_csv("out/geometry-milling.csv")
    wall_f_ds = pandas.read_csv("out/geometry-wall-following.csv")
    # random_ds = pandas.read_csv("out/geometry-random.csv")

    def convex_hull_ratio():
        plt.figure(figsize=(8, 4))
        total = 0
        x, y = cyclic_ds["CONVEX_HULL"], cyclic_ds["INVERSE_CONVEX_HULL"]
        y = np.divide(cyclic_ds["INVERSE_CONVEX_HULL"], cyclic_ds["CONVEX_HULL"])
        plt.scatter(x, y, c='orange', label="Cyclic Pursuit")
        total += len(x)

        x, y = aggregation_ds["CONVEX_HULL"], aggregation_ds["INVERSE_CONVEX_HULL"]
        y = np.divide(aggregation_ds["INVERSE_CONVEX_HULL"], aggregation_ds["CONVEX_HULL"])
        plt.scatter(x, y, c='blue', label="Aggregation")
        total += len(x)

        x, y = dispersal_ds["CONVEX_HULL"], dispersal_ds["INVERSE_CONVEX_HULL"]
        y = np.divide(dispersal_ds["INVERSE_CONVEX_HULL"], dispersal_ds["CONVEX_HULL"])
        plt.scatter(x, y, c='green', label="Dispersal")
        total += len(x)

        x, y = milling_ds["CONVEX_HULL"], milling_ds["INVERSE_CONVEX_HULL"]
        y = np.divide(milling_ds["INVERSE_CONVEX_HULL"], milling_ds["CONVEX_HULL"])
        plt.scatter(x, y, c='red', label="Milling")
        total += len(x)

        x, y = wall_f_ds["CONVEX_HULL"], wall_f_ds["INVERSE_CONVEX_HULL"]
        y = np.divide(wall_f_ds["INVERSE_CONVEX_HULL"], wall_f_ds["CONVEX_HULL"])
        plt.scatter(x, y, c='purple', label="Wall Following")
        total += len(x)

        plt.xlabel("Convex Hull Area")
        plt.ylabel("Hull:Frame Ratio")
        plt.title("Swarm Behavior Space")
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.show()
        print(f"TOTAL: {total}")

    def compare_keys(k1, k2, l1, l2):
        plt.figure(figsize=(8, 4))
        total = 0
        x, y = cyclic_ds[k1], cyclic_ds[k2]
        plt.scatter(x, y, c='orange', label="Cyclic Pursuit")
        total += len(x)

        x, y = aggregation_ds[k1], aggregation_ds[k2]
        plt.scatter(x, y, c='blue', label="Aggregation")
        total += len(x)

        x, y = dispersal_ds[k1], dispersal_ds[k2]
        plt.scatter(x, y, c='green', label="Dispersal")
        total += len(x)

        x, y = milling_ds[k1], milling_ds[k2]
        plt.scatter(x, y, c='red', label="Milling")
        total += len(x)

        x, y = wall_f_ds[k1], wall_f_ds[k2]
        plt.scatter(x, y, c='purple', label="Wall Following")
        total += len(x)

        plt.xlabel(l1)
        plt.ylabel(l2)
        plt.title("Swarm Behavior Space")
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.show()
        print(f"TOTAL: {total}")

    def persistence_3d():
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        total = 0

        DIVIDE_X_BY_Y = False
        X_FIELD, Y_FIELD, Z_FIELD = "CONVEX_HULL", "INVERSE_HULL", "MAX_1D"

        x, y, z = cyclic_ds[X_FIELD], cyclic_ds[Y_FIELD], cyclic_ds[Z_FIELD]
        y = np.divide(cyclic_ds[Y_FIELD], cyclic_ds[X_FIELD]) if DIVIDE_X_BY_Y else y
        ax.scatter(x, y, z, c='orange', label="Cyclic Pursuit")


        x, y, z = aggregation_ds[X_FIELD], aggregation_ds[Y_FIELD], aggregation_ds[Z_FIELD]
        y = np.divide(aggregation_ds[Y_FIELD], aggregation_ds[X_FIELD]) if DIVIDE_X_BY_Y else y
        ax.scatter(x, y, z, c='blue', label="Aggregation")

        x, y, z = dispersal_ds[X_FIELD], dispersal_ds[Y_FIELD], dispersal_ds[Z_FIELD]
        y = np.divide(dispersal_ds[Y_FIELD], dispersal_ds[X_FIELD]) if DIVIDE_X_BY_Y else y
        ax.scatter(x, y, z, c='green', label="Dispersal")

        x, y, z = milling_ds[X_FIELD], milling_ds[Y_FIELD], milling_ds[Z_FIELD]
        y = np.divide(milling_ds[Y_FIELD], milling_ds[X_FIELD]) if DIVIDE_X_BY_Y else y
        ax.scatter(x, y, z, c='red', label="Milling")

        x, y, z = wall_f_ds[X_FIELD], wall_f_ds[Y_FIELD], wall_f_ds[Z_FIELD]
        y = np.divide(wall_f_ds[Y_FIELD], wall_f_ds[X_FIELD]) if DIVIDE_X_BY_Y else y
        ax.scatter(x, y, z, c='purple', label="Wall Following")

        total_size = len(wall_f_ds) + len(milling_ds) + len(dispersal_ds) + len(aggregation_ds) + len(cyclic_ds)
        print(f"Total Controllers: {total_size}")

        plt.xlabel("Hull Area")
        plt.ylabel("Internal Frame Area")
        ax.set_zlabel("Max H1 Death Time")
        plt.title("Swarm Behavior Space")
        plt.legend()
        plt.show()


    k1, k2 = "ANGULAR_MOMENTUM", "GROUP_ROTATION"
    l1, l2 = "Angular Momentum", "Group Rotation"
    fig, axs = plt.subplots(2, 2)
    plt.figure(figsize=(8, 4))
    total = 0

    ax = axs[0][0]
    x, y = cyclic_ds[k1], cyclic_ds[k2]
    ax.scatter(x, y, c='orange', label="Cyclic Pursuit")
    total += len(x)

    x, y = aggregation_ds[k1], aggregation_ds[k2]
    ax.scatter(x, y, c='blue', label="Aggregation")
    total += len(x)

    x, y = dispersal_ds[k1], dispersal_ds[k2]
    ax.scatter(x, y, c='green', label="Dispersal")
    total += len(x)

    x, y = milling_ds[k1], milling_ds[k2]
    ax.scatter(x, y, c='red', label="Milling")
    total += len(x)

    x, y = wall_f_ds[k1], wall_f_ds[k2]
    ax.scatter(x, y, c='purple', label="Wall Following")
    total += len(x)

    ax.set_xlabel(l1)
    ax.set_ylabel(l2)


    k1, k2 = "SCATTER", "GROUP_ROTATION"
    l1, l2 = "Scatter", "Group Rotation"
    ax = axs[0][1]
    x, y = cyclic_ds[k1], cyclic_ds[k2]
    ax.scatter(x, y, c='orange', label="Cyclic Pursuit")
    total += len(x)

    x, y = aggregation_ds[k1], aggregation_ds[k2]
    ax.scatter(x, y, c='blue', label="Aggregation")
    total += len(x)

    x, y = dispersal_ds[k1], dispersal_ds[k2]
    ax.scatter(x, y, c='green', label="Dispersal")
    total += len(x)

    x, y = milling_ds[k1], milling_ds[k2]
    ax.scatter(x, y, c='red', label="Milling")
    total += len(x)

    x, y = wall_f_ds[k1], wall_f_ds[k2]
    ax.scatter(x, y, c='purple', label="Wall Following")
    total += len(x)

    ax.set_xlabel(l1)
    ax.set_ylabel(l2)

    k1, k2 = "AVERAGE_SPEED", "RADIAL_VARIANCE"
    l1, l2 = "Average Speed", "Radial Variance"
    ax = axs[1][0]
    x, y = cyclic_ds[k1], cyclic_ds[k2]
    ax.scatter(x, y, c='orange', label="Cyclic Pursuit")
    total += len(x)

    x, y = aggregation_ds[k1], aggregation_ds[k2]
    ax.scatter(x, y, c='blue', label="Aggregation")
    total += len(x)

    x, y = dispersal_ds[k1], dispersal_ds[k2]
    ax.scatter(x, y, c='green', label="Dispersal")
    total += len(x)

    x, y = milling_ds[k1], milling_ds[k2]
    ax.scatter(x, y, c='red', label="Milling")
    total += len(x)

    x, y = wall_f_ds[k1], wall_f_ds[k2]
    ax.scatter(x, y, c='purple', label="Wall Following")
    total += len(x)

    ax.set_xlabel(l1)
    ax.set_ylabel(l2)

    k1, k2 = "ANGULAR_MOMENTUM", "RADIAL_VARIANCE"
    l1, l2 = "Angular Momentum", "Radial Variance"
    ax = axs[1][1]
    x, y = cyclic_ds[k1], cyclic_ds[k2]
    ax.scatter(x, y, c='orange', label="Cyclic Pursuit")
    total += len(x)

    x, y = aggregation_ds[k1], aggregation_ds[k2]
    ax.scatter(x, y, c='blue', label="Aggregation")
    total += len(x)

    x, y = dispersal_ds[k1], dispersal_ds[k2]
    ax.scatter(x, y, c='green', label="Dispersal")
    total += len(x)

    x, y = milling_ds[k1], milling_ds[k2]
    ax.scatter(x, y, c='red', label="Milling")
    total += len(x)

    x, y = wall_f_ds[k1], wall_f_ds[k2]
    ax.scatter(x, y, c='purple', label="Wall Following")
    total += len(x)

    ax.set_xlabel(l1)
    ax.set_ylabel(l2)

    # fig.legend(loc='lower right')
    fig.tight_layout()
    plt.show()