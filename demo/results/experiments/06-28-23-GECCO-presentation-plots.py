import matplotlib.pyplot as plt

def plot_results_single():
    X = [i for i in range(0, 5)]
    SINGLE_SENSOR_RESULTS = [3.2, 4.9, 5.8, 5.4, 6.0]
    TITLE = "Single-Sensor Behavior Discovery Yields"
    X_AXIS = "Behavior Discovery Approach"
    Y_AXIS = "Average no. Distinct Behaviors Returned"
    X_TICKS = ["Random Sampling", "Random Sampling + Filtering", "Hand-Crafted Behavior Metrics", "Hand-Crafted + Filter", "HIL Latent Embedding"]

    plt.bar(X, SINGLE_SENSOR_RESULTS, color=[(0.7, 0.7, 0.7)] * 4 + [(1.0, 0.0, 0.0)])
    plt.xticks(X, X_TICKS, rotation=30, ha="right")
    plt.title(TITLE)
    # plt.xlabel(X_AXIS)
    plt.ylabel(Y_AXIS)
    plt.tight_layout()
    plt.show()

def plot_results_double():
    X = [i for i in range(0, 5)]
    SINGLE_SENSOR_RESULTS = [4.4, 4.8, 5.1, 5.3, 6.1]
    TITLE = "Two-Sensor Behavior Discovery Yields"
    X_AXIS = "Behavior Discovery Approach"
    Y_AXIS = "Average no. Distinct Behaviors Returned"
    X_TICKS = ["Random Sampling", "Random Sampling + Filtering", "Hand-Crafted Behavior Metrics", "Hand-Crafted + Filter", "HIL Latent Embedding"]

    plt.bar(X, SINGLE_SENSOR_RESULTS, color=[(0.7, 0.7, 0.7)] * 4 + [(1.0, 0.0, 0.0)])
    plt.xticks(X, X_TICKS, rotation=30, ha="right")
    plt.title(TITLE)
    # plt.xlabel(X_AXIS)
    plt.ylabel(Y_AXIS)
    plt.tight_layout()
    plt.show()

def plot_discrete_space_size():
    X = [i / 2 for i in range(0, 2)]
    SIZES = [3.77e12, 194_481]
    LABELS = ["Two-Sensor", "Single-Sensor"]

    TITLE = "Controller Space Size"
    X_LABEL = "Size of Discrete Controller Space (Log Scale)"
    Y_LABEL = "Capability Model"

    COLORS = [(0.8, 0.8, 0.8), (0.6, 0.6, 0.6)]

    plt.barh(X, SIZES, 0.4, color=COLORS, log=True)
    plt.yticks(X, LABELS)
    plt.title(TITLE)
    plt.xlabel(X_LABEL)
    # plt.ylabel(Y_LABEL)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_discrete_space_size()

