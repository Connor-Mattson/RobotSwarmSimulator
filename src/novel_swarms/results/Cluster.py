import numpy as np
import math
import pygame
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering, SpectralClustering, DBSCAN
from sklearn_extra.cluster import KMedoids

from ..novelty.NoveltyArchive import NoveltyArchive
from ..results.ClusterPoint import ClusterPoint
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
    
    def __init__(self, config: ResultsConfig, world_metadata=None, dim_reduction=True, heterogeneous=False):

        archive = config.archive
        if archive is None or not issubclass(type(archive), NoveltyArchive):
            raise Exception("Object of type NoveltyArchive must be provided to the Cluster Class")
        self.archive = archive
        self.reduced = np.array([])
        self.point_population = []
        self.center_population = []
        self.cluster_indices = []
        self.cluster_medoids = []
        self.medoid_indices = []
        self.medoid_genomes = []
        self.world_config = config.world
        self.world_metadata = world_metadata
        self.results_config = config
        self.dim_reduction = dim_reduction  # Whether to perform dimensionality reduction before clustering
        self.heterogeneous = heterogeneous

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
        print("Starting Clustering")
        implementation = self.results_config.clustering_type
        dataset = None
        if self.dim_reduction:
            dataset = self.reduced
        else:
            dataset = self.archive.archive

        if implementation == "k-medoids":
            kmedoids = KMedoids(n_clusters=self.results_config.k, random_state=1, method="pam").fit(dataset)
            print(kmedoids.labels_)
            self.cluster_indices = kmedoids.labels_
            self.cluster_medoids = kmedoids.cluster_centers_
        elif implementation == "hierarchical":
            hierarchical = AgglomerativeClustering(n_clusters=self.results_config.k)
            hierarchical.fit(dataset)
            self.cluster_indices = hierarchical.labels_
            self.cluster_medoids = self.get_cluster_medoids(dataset)
        elif implementation == "spectral":
            spectral_model = SpectralClustering(n_clusters=self.results_config.k, affinity='nearest_neighbors')
            spectral_model.fit(dataset)
            self.cluster_indices = spectral_model.labels_
            self.cluster_medoids = self.get_cluster_medoids(dataset)
        elif implementation == "dbscan":
            dbscan_model = None
            if self.dim_reduction:
                eps = 4.5 if self.results_config.eps is None else self.results_config.eps
                dbscan_model = DBSCAN(eps=4.5, min_samples=7)
            else:
                eps = 0.5 if self.results_config.eps is None else self.results_config.eps
                dbscan_model = DBSCAN(eps=0.5, min_samples=7)
            dbscan_model.fit(dataset)
            self.cluster_indices = dbscan_model.labels_
            # print(list(self.cluster_indices).count(-1))  # The number of outliers
            self.cluster_medoids = self.get_cluster_medoids(dataset)

        self.medoid_genomes = [[] for _ in self.cluster_medoids]
        self.medoid_indices = [-1 for _ in self.cluster_medoids]
        for i, medoid in enumerate(self.cluster_medoids):
            truth = [np.array_equal(i, medoid) for i in dataset]
            index = 0
            for j in range(len(truth)):
                if truth[j]:
                    index = j
            if index > -1:
                self.medoid_genomes[i] = self.archive.genotypes[index]
                self.medoid_indices[i] = index
            else:
                print("Wait a minute, we couldn't find ", medoid, " in the archive...")

        print("Clustering Finished!")
        print("\nMedoid Genomes")
        for genome in self.medoid_genomes:
            print('[' + ', '.join([str(x) for x in genome]) + '],')

    def get_cluster_medoids(self, dataset):
        """
        Get the medoids of the clusters.
        For use with clustering algorithms that are not k-medoids.
        """
        clusters = []
        index_set = set(self.cluster_indices)
        for _ in index_set:
            clusters.append(list())

        for i in range(len(self.cluster_indices)):
            cluster_index = self.cluster_indices[i]
            coords = dataset[i]
            clusters[cluster_index].append(coords)

        centroids = []
        for cluster in clusters:
            centroid = Cluster.find_closest_point(cluster)
            centroids.append(centroid)
        return centroids

    @staticmethod
    def find_closest_point(points):
        """
        Given a list of points, returns the one point that is closest to the center of the cluster.
        Works in an arbitrary number of dimensions.
        """
        # Step 1: Compute the centroid of the cluster
        total_points = len(points)
        dimensions = len(points[0])  # Assuming all points have the same number of dimensions

        centroid = [sum(point[i] for point in points) / total_points for i in range(dimensions)]

        # Step 2 and 3: Calculate the distance between each point and the centroid,
        # and find the point with the minimum distance
        closest_point = None
        min_distance = float('inf')  # Initialize with a large value

        for point in points:
            distance = math.sqrt(sum((point[i] - centroid[i]) ** 2 for i in range(dimensions)))
            if distance < min_distance:
                min_distance = distance
                closest_point = point

        # Step 4: Return the closest point
        return closest_point

    def pointMapping(self):
        min_x = min(self.reduced[:, 0])
        min_y = min(self.reduced[:, 1])
        max_x = max(self.reduced[:, 0])
        max_y = max(self.reduced[:, 1])

        print(f"i_classes: {len(self.cluster_indices)}, reduced_len: {len(self.reduced)}")
        for i, point in enumerate(self.reduced):
            c_i = self.cluster_indices[i]
            color = self.COLORS[c_i % (len(self.COLORS) - 1)]
            cluster_point = self.pointFromReductionToDisplaySpace(point, min_x, max_x, min_y, max_y, color,
                                                                  self.archive.genotypes[i])
            self.point_population.append(cluster_point)

        self.cluster_medoids = [[self.point_population[i].x, self.point_population[i].y] for i in self.medoid_indices]

        # medoids_copy = self.cluster_medoids
        # self.cluster_medoids = [[0, 0] for _ in range(len(medoids_copy))]
        # for i in range(len(medoids_copy)):
        #     cluster_point = self.pointFromReductionToDisplaySpace(medoids_copy[i], min_x, max_x, min_y, max_y,
        #                                                           None, self.medoid_genomes[i])
        #     self.cluster_medoids[i] = [cluster_point.x, cluster_point.y]

        print(self.cluster_medoids)

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
                if self.heterogeneous:
                    self.world_config.agentConfig.from_n_species_controller(controller)
                else:
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
                if self.heterogeneous:
                    self.world_config.agentConfig.from_n_species_controller(controller)
                else:
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
