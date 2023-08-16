import pandas
import seaborn as sns
import matplotlib.pyplot as plt

CMAES_DATA_PATH = "../../out/Homogeneous-Sweep-16/CMAES/genomes.csv"
if __name__ == "__main__":
    df = pandas.read_csv(CMAES_DATA_PATH)

    # df = pandas.concat([data_1])
    df = df.rename(columns={"Goal_Agents": "P_g"})
    # df = df.loc[df["P_g"] > 0.7]

    # sns.kdeplot(data=df, x="turning_rate", y="levy_scaler", fill=True)
    # sns.scatterplot(data=df, x="forward_rate", y="turning_rate", hue="P_g", size="P_g")
    # sns.scatterplot(data=df, x="turning_rate", y="P_g", hue="P_g")
    sns.pairplot(data=df, hue="P_g", vars=["forward_rate_0", "turning_rate_0", "forward_rate_1", "turning_rate_1"])

    # plt.title("Goal Finding CMAES for Random Levy Agents")
    # plt.xlim(150, 1000)
    # plt.ylim(0, 1.6)
    plt.show()
    print("Done!")
