from scipy.stats import gamma
import matplotlib.pyplot as plt

if __name__ == "__main__":
    samples = []

    for i in range(10000):
        l_sample = 501
        while l_sample > 500:
            l_sample = round(100 * (1 / (gamma.rvs(a=0.5, scale=2))))
        samples.append(l_sample)

    print(samples)
    plt.hist(samples, bins=80)
    plt.title(f"10000 Levy_Time Samples")
    plt.ylabel("No. Samples")
    plt.xlabel("100 * Levy(0, 1)")
    plt.show()
