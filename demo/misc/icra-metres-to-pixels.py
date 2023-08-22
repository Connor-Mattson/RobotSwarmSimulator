import numpy as np

def coord_to_bl(coord):
    centimeters = coord * 0.1 * 100
    return centimeters / 15.0    # Assuming 15 cm body length for agents (Flockbots + ICRA)


if __name__ == "__main__":
    data = np.loadtxt('../configs/flockbots-icra/position_data/seed5.csv', delimiter=',')
    for line in data:
        line[1] = coord_to_bl(line[1])
        line[2] = coord_to_bl(line[2])
        line[3] = line[3] - np.radians(90)
    print(data)

    """
    Verify that all transformations are within the specified bounding box
    """
    bounding_box = [[30, 63.3], [36.7, 70.7]]
    for line in data:
        if line[1] < bounding_box[0][0] or line[1] > bounding_box[1][0]:
            raise Exception(f"Error on X Coord for translated point: {line}")
        if line[2] < bounding_box[0][1] or line[2] > bounding_box[1][1]:
            raise Exception(f"Error on Y Coord for translated point: {line}")
    print("All Tests Pass!")

    """
    Output Translation
    """
    np.savetxt("../configs/flockbots-icra/position_data/s5.csv", data, delimiter=",", fmt="%10.5f")