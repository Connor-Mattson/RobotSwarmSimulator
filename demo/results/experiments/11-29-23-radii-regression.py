import os
os.environ['PATH'] += os.pathsep + '/home/connor/.juliaup/bin'

from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import LinearLocator
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib
from pylab import cm
from pysr import PySRRegressor

"""
Least Squares prediction of R = f(n, fov, omega_max, v)
"""
CROSS_SECTION_ONLY = True

def function_linear(X, a1, a2, a3, a4):
    args = [a1, a2, a3, a4]
    tot = 0
    for i in range(4):
        tot += X[i] * args[i]
    return tot

def function_quadratic(X, a1, a2, a3, a4, a5, a6, a7, a8):
    args = [a1, a2, a3, a4, a5, a6, a7, a8]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 2)]
        tot += (X[i] ** 2) * args[(i * 2) + 1]
    return tot

def function_3(X, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12):
    args = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 3)]
        tot += (X[i] ** 2) * args[(i * 3) + 1]
        tot += (X[i] ** 3) * args[(i * 3) + 2]
    tot += a0
    return tot

def function_linear_cs(X, bias, a1, a2):
    args = [a1, a2]
    tot = 0
    for i in range(2):
        tot += X[i] * args[i]
    return tot + bias

def function_quadratic_cs(X, a1, a2, a3, a4):
    args = [a1, a2, a3, a4]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 2)]
        tot += (X[i] ** 2) * args[(i * 2) + 1]
    return tot

def function_cubic_cs(X, bias, a1, a2, a3, a4, a5, a6):
    args = [a1, a2, a3, a4, a5, a6]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 3)]
        tot += (X[i] ** 2) * args[(i * 3) + 1]
        tot += (X[i] ** 3) * args[(i * 3) + 2]
    tot += bias
    return tot

def function_quartic_cs(X, bias, a1, a2, a3, a4, a5, a6, a7, a8):
    args = [a1, a2, a3, a4, a5, a6, a7, a8]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 3)]
        tot += (X[i] ** 2) * args[(i * 3) + 1]
        tot += (X[i] ** 3) * args[(i * 3) + 2]
        tot += (X[i] ** 4) * args[(i * 4) + 3]
    tot += bias
    return tot

def function_log_cs(X, bias, a1, a2, a3, a4, a5, a6, a7, a8):
    args = [a1, a2, a3, a4, a5, a6, a7, a8]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 4)]
        tot += (X[i] ** 2) * args[(i * 4) + 1]
        tot += np.sqrt(X[i]) * args[(i * 4) + 2]
        tot += np.log(X[i]) * args[(i * 4) + 3]
    tot += bias
    return tot

def function_expon_cs(X, bias, a1, a2, a3, a4, a5, a6, a7, a8):
    args = [a1, a2, a3, a4, a5, a6, a7, a8]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 4)]
        tot += (X[i] ** 2) * args[(i * 4) + 1]
        tot += np.exp(X[i]) * args[(i * 4) + 2]
        tot += np.sqrt(X[i]) * args[(i * 4) + 3]
    tot += bias
    return tot

def function_combined_root_cs(X, bias, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12):
    args = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]
    tot = 0
    for i in range(0, len(X)):
        tot += X[i] * args[(i * 5)]
        tot += ((X[i] + args[(i * 5) + 1]) ** 2) * args[(i * 5) + 2]
        tot += ((X[i] + args[(i * 5) + 3]) ** 3) * args[(i * 5) + 4]
        # tot += (X[i] ** 3) * args[(i * 3) + 2]

    tot += (np.sqrt(X[0] + X[1])) * a11
    tot += np.power(X[0] + X[1], a12)
    tot += bias
    return tot


def preprocess_data(df):
    df = df.loc[df["n"] <= 16]
    df_parsed = df.loc[df["fov"] <= (360 / df["n"])]
    df_parsed = df_parsed.loc[df_parsed["circliness"] > 0.95]
    if CROSS_SECTION_ONLY:
        df_parsed = df_parsed.loc[df_parsed["v"] == 1.0]
        df_parsed = df_parsed.loc[df_parsed["omega"] == 30.0]
    print(f"Reduced Datasize from {len(df)} to {len(df_parsed)}")

    y_truth = df_parsed["radius"].to_numpy() * 1.5  # Convert from px to cm
    X = df_parsed.loc[:, "n":"v"].to_numpy()
    X = np.swapaxes(X, 0, 1)
    # print(f"Reduced Datasize from {len(df)} to {len(X)}")
    return X, y_truth

def build_truth_dictionary(X, y_truth):
    t_dict = {}
    for i in range(len(X[0])):
        key = tuple(list(X[:, i]))
        t_dict[key] = y_truth[i]
    return t_dict

def plot_estimate(func, args, truth_dict):
    PLOT_ESTIMATE = True
    PLOT_TRUTH = False
    FILTER_MANIFOLD = True
    FILTER_CIRCLINESS = True
    N = range(4, 40)
    PHI = range(3, 90)
    V, OMEGA = 1.0, 30

    X, Y, Z = [], [], []
    for i in range(len(N)):
        for j in range(len(PHI)):
            if FILTER_MANIFOLD and PHI[j] > (360 / N[i]):
                continue
            X.append(N[i])
            Y.append(PHI[j])
            Z.append(func(row, *list(args)))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    if PLOT_ESTIMATE:
        p = ax.scatter(X, Y, Z, c=Z, marker='o', cmap=cm.plasma, label="Predicted")
    squared_error = []

    if PLOT_TRUTH:
        X_T, Y_T, Z_T = [], [], []
        for k in truth_dict:
            r = truth_dict[k]
            if CROSS_SECTION_ONLY:
                n, phi = k
            else:
                n, phi, w, v = k
                if w != OMEGA or v != V:
                    continue

            if CROSS_SECTION_ONLY:
                row = [n, phi]
            else:
                row = [n, phi, w, v]
            estim = func(row, *list(args))
            squared_error.append(abs(estim - r))

            X_T.append(n)
            Y_T.append(phi)
            Z_T.append(r)
        ax.scatter(X_T, Y_T, Z_T, c="red", marker="^", label="Truth")
        ax.set_zlim(0, max(max(Z), max(Z_T)))

    mae = sum(squared_error) / len(squared_error)
    mse = np.sum(np.square(squared_error)) / len(squared_error)
    print(f"Max Error: {max(squared_error)}")
    print(f"Prediction MAE: {mae}")
    print(f"Prediction MSE: {mse}")

    ax.set_xlabel("No. Agents (N)")
    ax.set_ylabel("Sensing Angle ($\phi$)")
    ax.set_zlabel("Predicted Radius (cm)")

    plt.title("Predicted Milling Radius")
    if PLOT_ESTIMATE:
        fig.colorbar(p)
    # Show the plot
    plt.show()

def plot_symbolic_model(model, model_index, truth_dict, filter_manifold=False, plot_estimate=True, plot_truth=True):
    N = range(4, 40)
    GAMMA = range(50, 200, 10)
    V, OMEGA = 1.0, 30

    X, Y, Z = [], [], []
    for i in range(len(N)):
        for j in range(len(GAMMA)):
            X.append(N[i])
            Y.append(GAMMA[j])
            if CROSS_SECTION_ONLY:
                row = [[N[i], GAMMA[j], 15, 30, OMEGA, V]]
            else:
                row = [[N[i], GAMMA[j], OMEGA, V]]
            Z.append(model.predict(row, model_index))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    if plot_estimate:
        p = ax.scatter(X, Y, Z, c=Z, marker='o', cmap=cm.plasma, label="Predicted")
    squared_error = []

    if plot_truth:
        X_T, Y_T, Z_T = [], [], []
        for k in truth_dict:
            r = truth_dict[k]
            if CROSS_SECTION_ONLY:
                n, phi = k
            else:
                n, phi, w, v = k
                if w != OMEGA or v != V:
                    continue

            row = [[n, phi, w, v]]
            estim = model.predict(row, model_index)
            squared_error.append(abs(estim - r))

            X_T.append(n)
            Y_T.append(phi)
            Z_T.append(r)
        ax.scatter(X_T, Y_T, Z_T, c="red", marker="^", label="Truth")
        ax.set_zlim(0, max(max(Z), max(Z_T)))
        mae = sum(squared_error) / len(squared_error)
        mse = np.sum(np.square(squared_error)) / len(squared_error)
        print(f"Max Error: {max(squared_error)}")
        print(f"Prediction MAE: {mae}")
        print(f"Prediction MSE: {mse}")

    ax.set_xlabel("No. Agents (N)")
    ax.set_ylabel("Gamma (cm)")
    ax.set_zlabel("Radius (cm)")

    plt.title(f"Measured Milling Radius" if not plot_estimate else f"Predicted Milling Radius" )
    if plot_estimate:
        fig.colorbar(p)
    # Show the plot
    plt.show()

def add_static_column_values(df):
    df.insert(2, "rho", np.ones(len(df)) * 15, False)
    df.insert(2, "gamma", np.ones(len(df)) * 150, False)
    print(df.head())
    return df

def optimize(df, func):
    X, y_truth = preprocess_data(df)
    params = curve_fit(func, X, y_truth, full_output=True, maxfev=2000)
    # print(y_truth)
    print(params)
    truth_dict = build_truth_dictionary(X, y_truth)
    plot_estimate(func, params[0], truth_dict)


def symbolic_regression(df):
    X, y_truth = preprocess_data(df)
    print(f"Training with {len(X[0])} observations")
    truth_dict = build_truth_dictionary(X, y_truth)
    # print(len(y_truth))
    model = PySRRegressor(
        niterations=250,
        population_size=250,
        binary_operators=[
            "*",
            "+",
            "-",
            "/"
        ],
        unary_operators=[
            "square",
            "cube",
            "inv(x) = 1/x",
            "neg",
            "cos",
            "sin",
            "pidiv(x) = 3.14159 / x",
            "pitimes(x) = 3.14159 * x",
            "tx(x) = 2 * x"
        ],
        extra_sympy_mappings={"inv": lambda x: 1 / x, "pitimes": lambda x: 3.14159 * x, "pidiv": lambda x: 3.14159 / x, "tx": lambda x: 2 * x},
        complexity_of_variables=1,
        # complexity_of_operators={
        #     "tx" : 2,
        # },
        complexity_of_constants=2,
        precision=64,
        maxsize=10
    )
    #
    model.fit(X.T, y_truth, variable_names=["n", "gam", "rho", "phi", "omega", "v"])
    print(model)
    eq = model.equations_
    print(eq.columns)
    selection = int(input("Select Index: "))
    print(eq.iloc[selection]["equation"])
    print("Latex: ", model.latex(selection))
    print("Table: ", model.latex_table(precision=3))
    plot_symbolic_model(model, selection, truth_dict=truth_dict, filter_manifold=True, plot_estimate=False)
    plot_symbolic_model(model, selection, truth_dict=truth_dict, filter_manifold=True, plot_truth=False)



if __name__ == "__main__":
    # RESULTS_FILE = "demo/results/out/r-convergence-8/sweep/genes.csv"
    # RESULTS_FILE = "demo/results/out/SM-Full-Run/sweep/genes.csv"
    RESULTS_FILE = "demo/results/out/r-manifold-mini/sweep/genes.csv"
    df = pd.read_csv(RESULTS_FILE)
    df = add_static_column_values(df)
    # optimize(df, function_combined_root_cs)
    symbolic_regression(df)

