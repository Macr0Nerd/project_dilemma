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
from collections.abc import Sequence
import random
from typing import Optional

from project_dilemma.interfaces.base import RoundList
from project_dilemma.interfaces.node import Node
from project_dilemma.interfaces.simulation import Simulation
from project_dilemma.simulations.utils import play_round


class BasicSimulation(Simulation):
    """simulation interface

    :var mutations_per_mille: rate that mutations should occur per mille
    :vartype mutations_per_mille: int
    :var rounds: total rounds to play
    :vartype rounds: int
    :var round_list: list of rounds
    :vartype round_list: RoundList
    :var round_mutations: if nodes can mutate after a round
    :vartype round_mutations: bool
    :var simulation_mutations: if nodes can mutate after a simulation
    :vartype simulation_mutations: bool
    """
    mutations_per_mille: int
    rounds: int
    round_list: RoundList
    round_mutations: bool
    simulation_mutations: bool

    def __init__(self,
                 simulation_id: str,
                 nodes: Sequence[Node],
                 rounds: int,
                 round_list: Optional[RoundList] = None,
                 *,
                 mutations_per_mille: int = 0,
                 round_mutations: bool = False,
                 simulation_mutations: bool = False):
        super().__init__(simulation_id, nodes)
        self.rounds = rounds
        self.round_list = round_list
        self.mutations_per_mille = mutations_per_mille
        self.round_mutations = round_mutations
        self.simulation_mutations = simulation_mutations

    @classmethod
    def run_simulation(cls) -> RoundList:
        """run the simulation

        :return: simulation results
        :rtype: RoundList
        """
        while len(cls.round_list) < cls.rounds:
            cls.round_list.append(play_round(
                nodes=cls.nodes, rounds=cls.round_list,
                mutations_per_mille=cls.mutations_per_mille, round_mutations=cls.round_mutations
            ))

        if cls.simulation_mutations:
            for node in cls.nodes:
                if random.randrange(0, 1000) < cls.mutations_per_mille:
                    node.mutate()

        return cls.round_list