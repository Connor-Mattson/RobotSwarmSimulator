import os

import numpy as np

from src.novel_swarms.world.initialization.FixedInit import FixedInitialization
from src.novel_swarms.world.simulate import main as sim
from .goal_search import get_world_generator as levy_world_sample
from .levy_milling_mix import get_world_generator as milling_and_levy_sample
from .homogeneous_search import get_world_generator as homogeneous_sample
from .two_species_mix import get_world_generator as two_species_sample

FILE_NAMES = [f"s{i}.csv" for i in range(1, 21)]
ROOT_SEED_FOLDER = "demo/configs/flockbots-icra/position_data"
FIXED_START_FILE = "demo/configs/flockbots-icra/init_translated.csv"

def FITNESS(world_set):
    total = 0
    for w in world_set:
        total -= w.behavior[0].out_average()[1]
    avg = total / len(world_set)
    return avg

###################################
# ONLY THING YOU SHOULD NEED TO CHANGE
T, N = 5000, 30

# CONTROLLER = [0.9976554047039169, -0.05913625023588143]
# CONTROLLER = [9.573899955413868, -0.24592161829306858, 9.17237427329869, 1.463405426779694]
CONTROLLER = [9.448152017350683, -0.3610072626695202, 9.922158135648829, 1.4762892056776575]
# CONTROLLER = [5.39607461574926, 0.6335149030384191, 7.004354721600954, -1.4579008025640738]
# CONTROLLER = [0.9274814380744913,0.8567118449150167,0.049730872369215806,3.793115357849018,-0.920251534200156,6.073268142516637,-0.1442217064794291]
# CONTROLLER = [0.00038655312299820655,0.9312229516936061,-1.324339339796072,8.251644256400727,-0.22228553376507976,9.59101653045968,1.4926548086430564]
FIXED_START = False
SHOW = True
NO_STOP = True
world_call = homogeneous_sample
###################################

if __name__ == "__main__":
    print(f"STARTING ({len(FILE_NAMES)} worlds), n={N}, t={T}")
    if FIXED_START:
        print(f"Simulating World...")
        get_world = world_call(horizon=T, n_agents=N, init=FixedInitialization(FIXED_START_FILE))
        sample_worlds = get_world(CONTROLLER, [-1, -1, -1, -1])
        if NO_STOP:
            sample_worlds[0].stop_at = None
        world = sim(sample_worlds[0], show_gui=SHOW, save_every_ith_frame=8, save_duration=T)
        fitness = -FITNESS([world])  # Negate becuase of minimum -> maximum conversion
        print("==============================")
        print(f"FIXED START, n={N}, t={T}")
        print(f"Controller: {CONTROLLER}")
        print(f"** FITNESS: {fitness} **")
        print("==============================")
    else:
        worlds = []
        individual_scores = []
        for i in range(len(FILE_NAMES)):
            print(f"Simulating... {FILE_NAMES[i]}")
            file = os.path.join(ROOT_SEED_FOLDER, FILE_NAMES[i])
            get_world = world_call(horizon=T, n_agents=N, init=FixedInitialization(file))
            sample_worlds = get_world(CONTROLLER, [-1, -1, -1, -1])
            if NO_STOP:
                sample_worlds[0].stop_at = None
            world = sim(sample_worlds[0], show_gui=SHOW, save_every_ith_frame=8, save_duration=T)
            worlds.append(world)

            self_score = -FITNESS([world])
            print(f"Done. Score: {self_score}")
            individual_scores.append(self_score)
        fitness = -FITNESS(worlds)  # Negate becuase of minimum -> maximum conversion
        print("==============================")
        print(f"GENERAL START ({len(FILE_NAMES)} worlds), n={N}, t={T}")
        print(f"Controller: {CONTROLLER}")
        print(individual_scores)
        print(f"Training Fitness: {np.mean(individual_scores[0:3])}")
        print(f"** AVG FITNESS: {fitness} **")
        print(f"StdDev: {np.std(individual_scores)}")
        print("==============================")
