import math

import copy
import numpy as np
from typing import List

import pygame

from .AbstractBehavior import AbstractBehavior
from ..agent.MazeAgent import MazeAgent
from ..util.geometry.Point import Point
from ..util.geometry.ConvexHull import ConvexHull as CH
from ..util.geometry.Polygon import Polygon

class SubBehaviors(AbstractBehavior):
    def __init__(self, name="SubcomponentViz", behavior_classes=None, r_disk_size=10, history=1, to_draw=True):
        super().__init__(name=name, history_size=history)
        self.population = None
        self.world = None
        self.r = r_disk_size
        self.sub_behaviors = []
        self.behavior_classes = behavior_classes
        self.to_draw = to_draw
        self.polygon_set = []
        self.text_baselines = []
        self.sub_swarm_classes = []
        self.sub_populations = []
        self.colors = [
            (164, 22, 27),
            (255, 209, 0),
            (246, 150, 198),
            (44, 221, 13),
            (44, 221, 13),
            (63, 181, 139),
            (176, 123, 214),
            (15, 129, 86)
        ]

    def attach_world(self, world):
        self.population = world.population
        self.world = world

    def getAdjacencyList(self):
        n = len(self.population)
        adjL = {}
        r_d2 = self.r ** 2
        for i, agent_i in enumerate(self.population):
            adjL[i] = []
            for j in range(n):
                agent_j = self.population[j]
                dist_p2 = ((agent_i.x_pos - agent_j.x_pos) ** 2) + ((agent_i.y_pos - agent_j.y_pos) ** 2)
                if dist_p2 < r_d2:
                    adjL[i].append(j)
        return adjL

    def DFS(self, adjL, key, seen=None):
        """
        Recursively Exhaust All Nodes. No goal state, just search everything
        """
        if seen is None:
            seen = [key]
        else:
            seen += [key]
        for edge in adjL[key]:
            if edge not in seen:
                seen = self.DFS(adjL, edge, seen)
        return seen

    def classify_from_clusters(self, vec):
        cluster_means = [[1.3009, 0.0725, 0.0003, 0.0049, 1.2807], [1.3174, 0.0492, 0.0054, 0.0033, 0.9614], [1.331, 0.0369, 0.0117, 0.0042, 0.6171]]
        v = np.array(vec)
        dists = [np.linalg.norm(np.array(mean) - v) for mean in cluster_means]
        return np.argmin(dists)

    def calculate(self):
        """
        Given a set of points and a radius, r, use the set of points to determine the connected subcomponents of the graph
        """
        self.polygon_set = []
        self.sub_behaviors = []
        self.text_baselines = []
        self.sub_swarm_classes = []
        self.sub_populations = []
        if not self.world:
            self.set_value(math.nan)
            return

        adjL = self.getAdjacencyList()
        visited = set()
        components = []
        for v, e in adjL.items():
            if v not in visited:
                component = self.DFS(adjL, v, [])
                visited = visited.union(component)
                components.append(component)

        for c in components:
            self.sub_populations.append([self.population[i] for i in c])

        # Calculate Behaviors
        for p in self.sub_populations:
            behavior = []
            for b in self.behavior_classes:
                b.attach_world(self.world)
                b.attach_population(p)
                b.calculate()
                behavior.append(b.out_current())
            self.sub_behaviors.append(behavior)

        self.set_value(self.sub_behaviors)

        for c in components:
            PADDING = 10
            points = [Point.from_agent(self.world.population[i]) for i in c]
            x, y = [p.x for p in points], [p.y for p in points]
            min_x, min_y, max_x, max_y = min(x), min(y), max(x), max(y)
            points = [
                Point(min_x - PADDING, min_y - PADDING),
                Point(min_x - PADDING, max_y + PADDING),
                Point(max_x + PADDING, max_y + PADDING),
                Point(max_x + PADDING, min_y - PADDING)
            ]
            self.text_baselines.append(Point(min_x - PADDING, max_y + 2 * PADDING))
            poly = Polygon(points)
            self.polygon_set.append(poly)

    def draw(self, screen):
        if self.to_draw:

            micro_classes = {
                "A" : [],
                "B" : [],
                "C" : []
            }

            for i, poly in enumerate(self.polygon_set):
                b_vec = [round(self.sub_behaviors[i][j][1], 3) for j in range(len(self.behavior_classes))]
                poly_class = self.classify_from_clusters(b_vec)
                class_name_color = {
                    0: ("C", (27, 134, 161)),
                    1: ("B", (246, 150, 198)),
                    2: ("A", (255, 209, 0))
                }

                # color = self.colors[poly_class % len(self.colors)]
                name, color = class_name_color[poly_class]
                micro_classes[name].append(len(self.sub_populations[i]))
                poly.draw(screen, color=color, width=3)

                font = pygame.font.Font(None, 20)
                text = font.render(f"Class {name}", True, color)
                textpos = (self.text_baselines[i].x, self.text_baselines[i].y)
                screen.blit(text, textpos)

            eq = f"{len(self.population)}C -> "
            first = True
            for key in micro_classes:
                for count in micro_classes[key]:
                    if not first:
                        eq += "+ "
                    else:
                        first = False
                    eq += f"{count}{key}"

            font = pygame.font.Font(None, 50)
            text = font.render(eq, True, (255, 255, 255))
            textpos = (20, 20)
            screen.blit(text, textpos)

    def out_average(self):
        return self.out_current()
