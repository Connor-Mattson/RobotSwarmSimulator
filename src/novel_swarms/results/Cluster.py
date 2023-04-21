import numpy
import numpy as np
import pygame
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering
from sklearn_extra.cluster import KMedoids

from ..novelty.NoveltyArchive import NoveltyArchive
from .ClusterPoint import ClusterPoint
from ..config.ResultsConfig import ResultsConfig


class Cluster:
    WORLD_PADDING = 15
    GUI_WIDTH = 700
    GUI_HEIGHT = 500
    MEDOID_RADIUS = 7
    COLORS = [
        (46, 134, 193),  # BLUE
        (231, 76, 60),  # RED
        (155, 89, 182),  # PURPLE
        (241, 196, 15),  # YELLOW
        (243, 156, 18),  # ORANGE
        (211, 84, 0),  # DARKER ORANGE
        (64, 224, 208),  # CYAN
        (125, 206, 160),  # MINT
        (34, 153, 84),  # GREEN
        (133, 146, 158),  # GREY
    ]

    def __init__(self, config: ResultsConfig, world_metadata=None):

        archive = config.archive
        if archive is None or not issubclass(type(archive), NoveltyArchive):
            raise Exception("Object of type NoveltyArchive must be provided to the Cluster Class")
        self.archive = archive
        self.reduced = np.array([])
        self.point_population = []
        self.center_population = []
        self.cluster_indices = []
        self.cluster_medoids = []
        self.medoid_genomes = []
        self.world_config = config.world
        self.world_metadata = world_metadata
        self.results_config = config

        self.initTSNE()
        self.clustering()
        self.pointMapping()

    def initTSNE(self):
        """
        Run dimensionality reduction on all elements of the Novelty Archive
        """
        print("Starting TSNE!")
        self.reduced = TSNE(
            n_components=2,
            learning_rate="auto",
            init="pca",
            perplexity=self.results_config.perplexity,
            early_exaggeration=self.results_config.early_exaggeration
        ).fit_transform(self.archive.archive)
        print("TSNE Finished!")

    def clustering(self):
        print("Starting k-Medoids Clustering")
        MEDOIDS = False
        if MEDOIDS:
            kmedoids = KMedoids(n_clusters=self.results_config.k, random_state=0).fit(self.reduced)
            self.cluster_indices = kmedoids.labels_
            self.cluster_medoids = kmedoids.cluster_centers_
            self.medoid_genomes = [[] for _ in self.cluster_medoids]
            for i, medoid in enumerate(self.cluster_medoids):
                index = numpy.where(self.reduced == medoid)[0][0]
                if index > -1:
                    self.medoid_genomes[i] = self.archive.genotypes[index]
        else:
            kmedoids = AgglomerativeClustering(n_clusters=self.results_config.k).fit(self.reduced)
            self.cluster_indices = kmedoids.labels_

        print("k-Medoids Finished!")

    def pointMapping(self):
        min_x = min(self.reduced[:, 0])
        min_y = min(self.reduced[:, 1])
        max_x = max(self.reduced[:, 0])
        max_y = max(self.reduced[:, 1])

        for i, point in enumerate(self.reduced):
            color = self.COLORS[self.cluster_indices[i] % (len(self.COLORS) - 1)]
            cluster_point = self.pointFromReductionToDisplaySpace(point, min_x, max_x, min_y, max_y, color,
                                                                  self.archive.genotypes[i])
            self.point_population.append(cluster_point)

        for i in range(len(self.cluster_medoids)):
            cluster_point = self.pointFromReductionToDisplaySpace(self.cluster_medoids[i], min_x, max_x, min_y, max_y,
                                                                  None, None)
            self.cluster_medoids[i] = [cluster_point.x, cluster_point.y]

    def displayGUI(self):
        pygame.init()
        pygame.display.set_caption("Clustered Swarm Novelty")
        screen = pygame.display.set_mode((self.GUI_WIDTH, self.GUI_HEIGHT))
        self.runDisplayLoop(screen)

    def clickInGUI(self, click):
        click_point = np.array(click)
        for i, medoid in enumerate(self.cluster_medoids):
            medoid_point = np.array(medoid)
            dist = np.linalg.norm(click_point - medoid_point)
            if dist < self.MEDOID_RADIUS:
                controller = self.medoid_genomes[i]
                from ..world.simulate import main
                print(f"Display Controller (Medoid): {controller}")

                metadata = self.sync_metadata_with_controller(controller)
                self.world_config.agentConfig.controller = controller
                self.world_config.set_attributes(metadata)

                main(world_config=self.world_config)
                return

        for i, point in enumerate(self.point_population):
            poi = np.array([point.x, point.y])
            dist = np.linalg.norm(click_point - poi)
            if dist < self.MEDOID_RADIUS:
                controller = self.archive.genotypes[i]
                from ..world.simulate import main
                print(f"Display Controller: {controller}")

                metadata = self.sync_metadata_with_controller(controller)
                self.world_config.agentConfig.controller = controller
                self.world_config.set_attributes(metadata)

                main(world_config=self.world_config)
                return

    def runDisplayLoop(self, screen):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.clickInGUI(pos)

            screen.fill((0, 0, 0))
            for cluster_point in self.point_population:
                cluster_point.draw(screen)

            for cluster_center in self.cluster_medoids:
                pygame.draw.circle(screen, (255, 255, 255), (int(cluster_center[0]), int(cluster_center[1])),
                                   self.MEDOID_RADIUS, width=0)

            pygame.display.flip()

    def pointFromReductionToDisplaySpace(self, point, min_x, max_x, min_y, max_y, color, genome):
        x = np.interp(point[0], (min_x, max_x), (self.WORLD_PADDING, self.GUI_WIDTH - self.WORLD_PADDING))
        y = np.interp(point[1], (min_y, max_y), (self.WORLD_PADDING, self.GUI_HEIGHT - self.WORLD_PADDING))
        return ClusterPoint(x=x, y=y, color=color, genome=genome)

    def sync_metadata_with_controller(self, controller):
        new_dict = {}
        if not self.world_metadata:
            return {}
        for key in self.world_metadata:
            new_dict[key] = controller[self.world_metadata[key]]
        return new_dict
