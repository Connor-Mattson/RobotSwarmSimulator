import os
import numpy as np
from PIL import Image
import matplotlib
import cv2

class ExternalSimulationArchive:
    def __init__(self, base_path, depth):
        self.base_path = base_path
        self.depth = depth

    def traverse_or_null(self, path: list):
        str_path = self.base_path + "/" + "/".join(path)
        if not os.path.exists(str_path):
            return None
        return str_path

    def retrieve_if_exists(self, path, with_image=False):
        p = self.traverse_or_null(path)
        if p is None:
            return None, None
        behavior_file = os.path.join(p, "test.csv")
        behavior = np.loadtxt(behavior_file, delimiter=",", dtype=float)
        if with_image:
            image = np.array(Image.open(os.path.join(p, "behavior.png")).convert('L'))
            if image:
                return behavior, image
        return behavior, None

    def save(self, path, behavior, image=None, size=(50,50)):
        str_path = self.base_path + "/" + "/".join(path)
        os.makedirs(str_path, exist_ok=False)
        behavior_file = os.path.join(str_path, "test.csv")
        np.savetxt(behavior_file, behavior, delimiter=",")
        if image:
            frame = image.astype(np.uint8)
            save_image = cv2.resize(frame, dsize=size, interpolation=cv2.INTER_AREA)
            matplotlib.image.imsave(os.path.join(path, "behavior.png"), save_image, cmap='gray')

