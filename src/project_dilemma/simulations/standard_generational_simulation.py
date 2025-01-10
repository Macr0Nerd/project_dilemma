"""
Copyright 2023-2025 Gabriele Ron

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import math

from project_dilemma.interfaces import GenerationalSimulation, Node


class StandardGenerationalSimulation(GenerationalSimulation):
    def generation_hook(self):
        last_generation = list(self.simulation_data.values())[-1]

        simulation = self.generational_simulation(**{
            'simulation_id': 'process_last_generation',
            'nodes': self.nodes,
            'simulation_data': last_generation,
            **self.simulation_kwargs
        })

        node_points = simulation.process_results()

        algorithm_populations = {}
        algorithm_points = {}

        for node in self.nodes:
            if not algorithm_populations.get(node.algorithm):
                algorithm_populations[node.algorithm] = 0

            if not algorithm_points.get(node.algorithm):
                algorithm_points[node.algorithm] = 0

            algorithm_populations[node.algorithm] += 1
            algorithm_points[node.algorithm] += node_points[node.node_id]

        total_points = sum(algorithm_points.values())
        average_points = float(total_points)/len(algorithm_points.keys())

        for algorithm, points in algorithm_points.items():
            point_ratio = (points - average_points)/average_points
            population_change = int(algorithm_populations[algorithm] * point_ratio)

            population_change = int(math.sqrt(abs(population_change)))

            if point_ratio < 0:
                population_change *= -1

            algorithm_populations[algorithm] += population_change

        nodes = []
        for algorithm, population in algorithm_populations.items():
            for i in range(population):
                nodes.append(Node(f'{algorithm.algorithm_id}_{i}', algorithm=algorithm))

        self.nodes = nodes
