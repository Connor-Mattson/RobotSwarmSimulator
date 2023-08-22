import subprocess
import argparse
import os

N_SET = [10, 20, 30]
T_SET = [3000, 5000]
N_SET_TEST_ONLY = [2, 5]
T_SET_TEST_ONLY = [100, 500]

ROOT = "demo/results/out"
POPULATION_SIZE = 25

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, help="A custom experiment name")
    parser.add_argument("--python-script", type=str, help="The parameter after python -m that you want to run, a script")
    parser.add_argument("--fixed-config", action="store_true", help="Use the predefined init")
    parser.add_argument("--processes", type=int, default=1, help="Number of running concurrent processes")
    parser.add_argument("--n", type=int, default=-1, help="Number of Agents to Sweep over")
    parser.add_argument("--iters", type=int, default=100, help="Number of Evolutions to consider")
    parser.add_argument("--no-walls", action="store_true", help="Whether to include detectable walls")
    parser.add_argument("--sweep", action="store_true", help="Whether to sweep instead of search")
    parser.add_argument("--test", action="store_true", help="Whether to use a smaller test set for debugging")

    args = parser.parse_args()

    title = args.name if args.name is not None else "Sweeper"

    i = 1
    joined_path = os.path.join(ROOT, f"{title}-{i}")
    while os.path.exists(joined_path):
        joined_path = os.path.join(ROOT, f"{title}-{i}")
        i += 1
    os.mkdir(joined_path)

    experiment_folder = joined_path

    n_set = N_SET if not args.test else N_SET_TEST_ONLY
    t_set = T_SET if not args.test else T_SET_TEST_ONLY

    if args.n > 0:
        n_set = [args.n]

    def get_cmd(n, t):
        cmd = [
            "python", "-m", args.python_script, "--root", experiment_folder, "--t", str(t), "--n", str(n), "--processes",
            str(args.processes), "--iters", str(args.iters), "--pop-size", str(POPULATION_SIZE)
        ]
        if args.fixed_config:
            cmd.append("--fixed-config")
        if args.no_walls:
            cmd.append("--no-walls")
        if args.sweep:
            cmd.append("--sweep")
        return cmd

    for n in n_set:
        for t in t_set:
            sub_exp_name = f"n{n}-t{t}"
            sub_exp_name += "-test" if args.test else ""
            sub_exp_name += "-sweep" if args.sweep else ""
            sub_exp_name += "-fixed" if args.fixed_config else ""
            sub_exp_name += "-NoWalls" if args.no_walls else ""

            cmd = get_cmd(n, t)
            cmd.append("--name")
            cmd.append(sub_exp_name)

            print("========================================")
            print(f"Experiment Start")
            print(f"N: {n}, T: {t}")
            print(f"Output name: {sub_exp_name}")
            print("========================================")

            subprocess.call(cmd)

            print(f"Finished exp: {sub_exp_name}")


