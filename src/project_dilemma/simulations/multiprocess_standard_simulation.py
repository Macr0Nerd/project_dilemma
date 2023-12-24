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
import multiprocessing

from project_dilemma.interfaces.base import Round, RoundList
from project_dilemma.simulations.basic_simulation import BasicSimulation


class MultiprocessStandardSimulation(BasicSimulation):
    """runs each node against every other node and itself using multiprocessing

    :var pool_size: multiprocessing pool size
    :vartype pool_size: int
    """
    pool_size: int

    def __init__(self, pool_size: int = multiprocessing.cpu_count(), **kwargs):
        super().__init__(**kwargs)
        self.pool_size = pool_size

    def _collect_round(self, result: Round):
        """callback to collect simulation results from the pool"""
        self.round_list.append(result)

    @classmethod
    def run_simulation(cls) -> RoundList:
        """runs the simulation

        :return: simulation results
        :rtype: RoundList
        """
        cls.round_list.append([])
        simulations = []
        for index, first_node in enumerate(cls.nodes):
            for second_node in cls.nodes[index:]:
                simulations.append(BasicSimulation(
                    [first_node, second_node],
                    rounds=cls.rounds,
                    mutations_per_mille=cls.mutations_per_mille,
                    round_mutations=cls.round_mutations,
                    simulation_mutations=cls.simulation_mutations
                ))

        pool = multiprocessing.Pool(processes=cls.pool_size)
        for simulation in simulations:
            pool.apply_async(simulation.run_simulation, callback=cls._collect_round)

        pool.close()
        pool.join()

        return cls.round_list
