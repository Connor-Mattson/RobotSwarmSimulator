import simulate
import pygame
from src.util.datasets.DiffDriveDataset import DiffDriveDataset
from src.util.datasets.GenomeDataSet import GenomeDataSet


def main():
    unknown_genomes = GenomeDataSet(file="../../data/unknown.csv")
    cyclic_genomes = DiffDriveDataset.CYCLIC_PURSUIT
    aggreg_genomes = DiffDriveDataset.AGGREGATION
    wall_follow_genomes = DiffDriveDataset.WALL_FOLLOWING
    dispersal_genomes = DiffDriveDataset.DISPERSAL
    milling_genomes = DiffDriveDataset.MILLING
    random_genomes = DiffDriveDataset.RANDOM

    key_mapping = {
        pygame.K_KP0: cyclic_genomes,
        pygame.K_0: cyclic_genomes,
        pygame.K_KP1: aggreg_genomes,
        pygame.K_1: aggreg_genomes,
        pygame.K_KP2: wall_follow_genomes,
        pygame.K_2: wall_follow_genomes,
        pygame.K_KP3: dispersal_genomes,
        pygame.K_3: dispersal_genomes,
        pygame.K_KP4: milling_genomes,
        pygame.K_4: milling_genomes,
        pygame.K_KP5: random_genomes,
        pygame.K_5: random_genomes,
    }

    for i, genome in enumerate(unknown_genomes.data):
        classified_pattern_keydown, time = simulate.main(controller=genome)

        if classified_pattern_keydown in key_mapping:
            key_mapping[classified_pattern_keydown].append(genome)
            print(f"{genome} assigned to {key_mapping[classified_pattern_keydown].name} (t={time})")

        elif classified_pattern_keydown == pygame.K_q:
            # Write out the unknown_set before quitting
            unknown_genomes.overwrite_data(unknown_genomes.data[i:])
            unknown_genomes.save()
            return

        else:
            continue

    unknown_genomes.overwrite_data([])
    unknown_genomes.save()

if __name__ == "__main__":
    main()
