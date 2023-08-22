import pandas
import seaborn as sns
import matplotlib.pyplot as plt

CMAES_DATA_PATH = "../../out/Levy-Fixed-1/n20-t4000-fixed/CMAES/genomes.csv"
CMAES_DATA_PATH_1 = "../../out/Levy-Fixed-1/n20-t5000-fixed/CMAES/genomes.csv"
CMAES_DATA_PATH_2 = "../../out/Levy-Fixed-1/n20-t2000-fixed/CMAES/genomes.csv"
CMAES_DATA_PATH_3 = "../../out/Levy-Fixed-1/n30-t4000-fixed/CMAES/genomes.csv"
CMAES_DATA_PATH_4 = "../../out/Levy-Fixed-1/n30-t5000-fixed/CMAES/genomes.csv"
if __name__ == "__main__":
    df = pandas.read_csv(CMAES_DATA_PATH)
    df2 = pandas.read_csv(CMAES_DATA_PATH_1)
    df3 = pandas.read_csv(CMAES_DATA_PATH_2)
    df4 = pandas.read_csv(CMAES_DATA_PATH_1)
    df5 = pandas.read_csv(CMAES_DATA_PATH_2)

    df = pandas.concat([df, df2, df3, df4, df5])
    df = df.rename(columns={"Goal_Agents": "P_g"})
    # df = df.loc[df["P_g"] > 0.7]

    sns.kdeplot(data=df, x="turning_rate", y="forward_rate", fill=True)
    # sns.scatterplot(data=df, x="forward_rate", y="turning_rate", hue="P_g", size="P_g")
    # sns.scatterplot(data=df, x="turning_rate", y="P_g", hue="P_g")
    # sns.pairplot(data=df, hue="P_g", vars=["population_ratio", "forward_rate_levy", "turning_rate_levy", "forward_rate_0", "turning_rate_0", "forward_rate_1", "turning_rate_1"])

    plt.title("CMAES Levy Optima")

    # plt.title("Goal Finding CMAES for Random Levy Agents")
    # plt.xlim(150, 1000)
    # plt.ylim(0, 1.6)
    plt.show()
    print("Done!")
