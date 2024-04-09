import pandas as pd
import argparse
import os

def pixel_per_s_to_meters_per_s(data):
    """
    Convert the normalized Pixels/s forward rate to m/s
    """
    data["forward_rate_0"] *= 0.1 * 15 * 0.01
    data["forward_rate_1"] *= 0.1 * 15 * 0.01
    return data

def negate_fitness(data):
    """
    Negate Fitness (CMA-ES is a minimizer so revert back to a maximizing problem)
    i.e. in terms of minimization, the best fitness is -(max(Circliness)) = -1,
    the fitness column is negative Circliness, so we are simply changing it back to Circliness
    """
    data["fitness"] *= -1
    return data

def sort_best(data):
    return data.sort_values(by="Circliness", ascending=False)

def aggregate_fitness_to_vector(data):
    res = [[None, 0, repr([])]]
    for i in range(100):
        time = data.loc[data["gen"] == i].head(1)["time"].item()
        epoch = i + 1
        fitness = list(data.loc[data["gen"] == i]["Circliness"])
        l = [time, epoch, repr(fitness)]
        res.append(l)
    return pd.DataFrame(res, columns=["time", "epoch", "fitness"])

def csv_to_dataframe(path):
    return pd.read_csv(path)

def convert_to_tsv(data, file_name="results.tsv"):
    data.to_csv(file_name, sep="\t", index=False)

def convert_to_csv(data, file_name="results.csv"):
    data.to_csv(file_name, index=False)

if __name__ == "__main__":
    """
    Example usage (from directory root)
    `python -m demo.results.post_process_optim_data --name "EXPERIMENT_NAME_HERE" --tsv`
    
    Outputs 2 files to the experiment directory (name arg)
    - EXPER_NAME_best: The 10 best solutions found throughout evolution
    - EXPER_NAME_raw: Fitness distribution for each epoch of G.A.
    
    The console will also print a command telling you how to see the best solution.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, help="Name of the experiment", default=None)
    parser.add_argument("--tsv", action="store_true", help="Whether to store a TSV (Default: CSV)")
    args = parser.parse_args()

    RESULTS_ROOT = "demo/results/out"
    parent_dir = os.path.join(RESULTS_ROOT, args.name)
    SUFFIX_CMAES = "CMAES/genomes.csv"
    genome_file = os.path.join(parent_dir, SUFFIX_CMAES)

    if not os.path.exists(parent_dir):
        raise Exception(f"Could not find experiment at {parent_dir}. Is the directory path correct?")
    if not os.path.exists(genome_file):
        raise Exception(f"Error: could not find CMAES results at the specified location. Was an experiment successfully run here?")

    data = csv_to_dataframe(genome_file)

    # Post-process the data so that it makes the m/s units and maximum fitness = 1
    translate_data = negate_fitness(pixel_per_s_to_meters_per_s(data))

    # Output the raw data
    if args.tsv:
        aggregated_fitness = aggregate_fitness_to_vector(translate_data)
        convert_to_tsv(aggregated_fitness, os.path.join(parent_dir, args.name.lower() + "_raw.tsv"))
    else:
        convert_to_csv(translate_data, os.path.join(parent_dir, args.name.lower() + "_raw.tsv"))

    # Sort the data by decreasing fitness
    sorted_data = sort_best(translate_data)

    # Output the best controllers
    if args.tsv:
        convert_to_tsv(sorted_data.head(10), os.path.join(parent_dir, args.name.lower() + "_best.tsv"))
    else:
        convert_to_csv(sorted_data.head(10), os.path.join(parent_dir, args.name.lower() + "_best.csv"))

    print(f"Two files saved to... {parent_dir}")

    # Create a README with executables for the best genomes
    best = sorted_data.head(1)
    print(f"Best fitness: {best['Circliness'].item()}")
    print(f"python -m demo.evolution.optim_milling.sim_results --v0 {best['forward_rate_0'].item()} --w0 {best['turning_rate_0'].item()} --v1 {best['forward_rate_1'].item()} --w1 {best['turning_rate_1'].item()} --n 10 --t 1000")