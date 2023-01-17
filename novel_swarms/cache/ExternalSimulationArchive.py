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
        str_path_list = [str(i) for i in path]
        str_path = self.base_path + "/" + "/".join(str_path_list)
        if not os.path.exists(str_path):
            return None
        return str_path

    def retrieve_if_exists(self, path, with_image=False):
        p = self.traverse_or_null(path)
        if p is None:
            return None, None
        behavior_file = os.path.join(p, "behavior.csv")
        behavior = np.loadtxt(behavior_file, delimiter=",", dtype=float)
        if with_image:
            image = np.array(Image.open(os.path.join(p, "behavior.png")).convert('L'))
            if image is not None:
                return behavior, image
        return behavior, None

    def save_if_empty(self, path, behavior, image=None, size=(50,50)):
        p = self.traverse_or_null(path)
        if p is not None:
            return False
        str_path_list = [str(i) for i in path]
        str_path = self.base_path + "/" + "/".join(str_path_list)
        os.makedirs(str_path, exist_ok=False)
        behavior_file = os.path.join(str_path, "behavior.csv")
        np.savetxt(behavior_file, behavior, delimiter=",")
        if image is not None:
            frame = image.astype(np.uint8)
            save_image = cv2.resize(frame, dsize=size, interpolation=cv2.INTER_AREA)
            matplotlib.image.imsave(os.path.join(str_path, "behavior.png"), save_image, cmap='gray')
        return True
