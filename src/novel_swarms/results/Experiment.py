import time
import os

class Experiment:
    def __init__(self, root=None, title=None):
        if title is None:
            title = f"e{int(time.time())}"

        joined_path = os.path.join(root, title)
        i = 1
        while os.path.exists(joined_path):
            joined_path = os.path.join(root, f"{title}-{i}")
            i += 1
        os.mkdir(joined_path)

        self.root_path = joined_path

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
