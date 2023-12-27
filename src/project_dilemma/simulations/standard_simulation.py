"""
Copyright 2023 Gabriele Ron

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
from collections.abc import MutableMapping
import itertools

from project_dilemma.interfaces import Simulations
from project_dilemma.simulations.basic_simulation import BasicSimulation


class StandardSimulation(BasicSimulation):
    """runs each node against every other node and itself"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run_simulation(self) -> Simulations:
        """runs the simulation

        :return: simulation results
        :rtype: Simulations
        """
        for first_node, second_node in itertools.combinations(self.nodes, r=2):
            game_id = ':'.join(sorted([first_node.node_id, second_node.node_id]))

            simulation = BasicSimulation(
                game_id,
                [first_node, second_node],
                rounds=self.rounds,
                simulation_data=self.simulation_data,
                mutations_per_mille=self.mutations_per_mille,
                round_mutations=self.round_mutations,
                simulation_mutations=self.simulation_mutations,
                noise=self.noise,
                noise_per_mille=self.noise_per_mille
            )

            self.simulation_data.update(simulation.run_simulation())

        return self.simulation_data

    def process_results(self) -> MutableMapping[str, int]:
        """process the simulation results

        if both nodes cooperate,

        :return: node_id to simulation points
        :rtype: MutableMapping[str, int]
        """

        results = {}
        for game_id, rounds in self.simulation_data.items():
            if rounds:
                nodes = list(rounds[0].keys())

                for node in nodes:
                    if not results.get(node):
                        results[node] = 0

                for round in rounds:
                    if round[nodes[0]] and round[nodes[1]]:
                        results[nodes[0]] += 3
                        results[nodes[1]] += 3
                    elif round[nodes[0]]:
                        results[nodes[1]] += 5
                    elif round[nodes[1]]:
                        results[nodes[0]] += 5
                    else:
                        results[nodes[0]] += 1
                        results[nodes[1]] += 1

        return results
