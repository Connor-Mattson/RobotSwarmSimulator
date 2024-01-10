import time
import os
import yaml
import numpy as np
from pandas import DataFrame

class Experiment:
    def __init__(self, root=None, title=None):
        self.start_time = time.time()
        if title is None:
            title = f"e{int(self.start_time)}"

        joined_path = os.path.join(root, title)
        i = 1
        while os.path.exists(joined_path):
            joined_path = os.path.join(root, f"{title}-{i}")
            i += 1
        os.mkdir(joined_path)

        self.root_path = joined_path
        self.end_time = None

    def root(self):
        return self.root_path

    def add_sub(self, title):
        """
        Given a title, return the path to a new directory created under the experiment with name title
        """
        if title is None:
            raise Exception("The add_sub method requires a non-null title parameter")

        joined_path = os.path.join(self.root_path, title)
        os.mkdir(joined_path)
        return joined_path

    def write_metadata(self, data, file_name="metadata.yaml"):
        if not isinstance(data, dict):
            raise Exception("Metadata must be of type dict")

        data["start_time"] = self.start_time
        if not self.end_time:
            self.end_time = time.time()
        data["end_time"] = self.end_time
        data["duration"] = self.end_time - self.start_time
        with open(os.path.join(self.root_path, file_name), "w") as f:
            yaml.dump(data, f)

    def write_array(self, arr, file_name):
        if not arr or not file_name:
            raise Exception("Missing one or all required parameters for write_array")
        nparr = np.array(arr)
        np.savetxt(os.path.join(self.root_path, file_name), nparr)

    def write_data_frame(self, df, file_name):
        df.to_csv(os.path.join(self.root_path, file_name))