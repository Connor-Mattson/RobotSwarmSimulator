import numpy as np

def coord_to_bl(coord):
    centimeters = coord * 0.1 * 100
    return centimeters / 15.0    # Assuming 15 cm body length for agents (Flockbots + ICRA)


if __name__ == "__main__":
    data = np.zeros((100, 4))
    for i, line in enumerate(data):
        line[0] = i
        line[1] = 50.0
        line[2] = 0.5 + i
        line[3] = 0.0

    np.savetxt("../configs/flockbots-icra/test_agent_line.csv", data, delimiter=",", fmt="%10.5f")