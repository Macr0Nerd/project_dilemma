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
from project_dilemma.interfaces.base import RoundList
from project_dilemma.simulations.basic_simulation import BasicSimulation


class StandardSimulation(BasicSimulation):
    """runs each node against every other node and itself"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def run_simulation(cls) -> RoundList:
        """runs the simulation

        :return: simulation results
        :rtype: RoundList
        """
        cls.round_list.append([])
        for index, first_node in enumerate(cls.nodes):
            for second_node in cls.nodes[index:]:
                simulation = BasicSimulation(
                    f'{first_node.node_id}:{second_node.node_id}',
                    [first_node, second_node],
                    rounds=cls.rounds,
                    mutations_per_mille=cls.mutations_per_mille,
                    round_mutations=cls.round_mutations,
                    simulation_mutations=cls.simulation_mutations
                )

                cls.round_list[-1].append(simulation.run_simulation())

        return cls.round_list
