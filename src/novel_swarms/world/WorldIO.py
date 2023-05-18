import time
import json

class WorldIO:
    @staticmethod
    def save_world(world, file_name=None):
        world_dict = world.as_config_dict()
        j_string = json.dumps(world_dict)
        if file_name is None:
            file_name = f"world_{int(time.time())}.json"
        with open(file_name, "w") as f:
            f.write(j_string)
        print(f"World data saved to {file_name}.")

    @staticmethod
    def load_world(file_name):
        pass
