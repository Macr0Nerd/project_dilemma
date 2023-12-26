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
import itertools
import multiprocessing

from project_dilemma.interfaces import Simulations
from project_dilemma.simulations import BasicSimulation, StandardSimulation


class MultiprocessStandardSimulation(StandardSimulation):
    """runs each node against every other node and itself using multiprocessing

    :var pool_size: multiprocessing pool size
    :vartype pool_size: int
    """
    pool_size: int

    def __init__(self, pool_size: int = multiprocessing.cpu_count(), **kwargs):
        super().__init__(**kwargs)
        self.pool_size = pool_size

    def _collect_round(self, result: Simulations):
        """callback to collect simulation results from the pool"""
        self.simulation_data.update(result)

    def run_simulation(self) -> Simulations:
        """runs the simulation

        :return: simulation results
        :rtype: Simulations
        """
        simulations = []
        for first_node, second_node in itertools.combinations(self.nodes, r=2):
            game_id = ':'.join(sorted([first_node.node_id, second_node.node_id]))

            simulations.append(BasicSimulation(
                game_id,
                [first_node, second_node],
                rounds=self.rounds,
                simulation_data=self.simulation_data,
                mutations_per_mille=self.mutations_per_mille,
                round_mutations=self.round_mutations,
                simulation_mutations=self.simulation_mutations,
                noise=self.noise,
                noise_per_mille=self.noise_per_mille
            ))

        pool = multiprocessing.Pool(processes=self.pool_size)
        for simulation in simulations:
            pool.apply_async(simulation.run_simulation, callback=self._collect_round)

        pool.close()
        pool.join()

        return self.simulation_data
