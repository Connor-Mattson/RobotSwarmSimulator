import matplotlib.pyplot as plt
import numpy as np

x_data = [i for i in range(0, 21)]
y_n10_t3000 = [(16.33 * i) / 60 for i in range(0, 21)]
y_n10_t5000 = [(30.33 * i) / 60 for i in range(0, 21)]

y_n20_t3000 = [(55.33 * i) / 60 for i in range(0, 21)]
y_n20_t5000 = [(94 * i) / 60 for i in range(0, 21)]

y_n30_t3000 = [(111 * i) / 60 for i in range(0, 21)]
y_n30_t5000 = [(191.33 * i) / 60 for i in range(0, 21)]


plt.plot(x_data, y_n10_t3000, label="10N_3000T")
plt.plot(x_data, y_n10_t5000, label="10N_5000T")
plt.plot(x_data, y_n20_t3000, label="20N_3000T")
plt.plot(x_data, y_n20_t5000, label="20N_5000T")
plt.plot(x_data, y_n30_t3000, label="30N_3000T")
plt.plot(x_data, y_n30_t5000, label="30N_5000T")

plt.legend()
plt.title("Evolution Time for Varying (N, T) (Extrapolation)")
plt.xlabel("Size of Training Data (no. Starting Seeds)")
plt.ylabel("Time (Hours)")
plt.xticks(np.arange(0, 21, 2))

plt.show()
