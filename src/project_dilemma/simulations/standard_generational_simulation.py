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
            algorithm_populations[algorithm] += population_change

        nodes = []
        for algorithm, population in algorithm_populations.items():
            for i in range(population):
                nodes.append(Node(f'{algorithm.algorithm_id}_{i}', algorithm=algorithm))

        self.nodes = nodes
