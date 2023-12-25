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

from project_dilemma.interfaces import Node, Simulation, SimulationRounds
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
    round_mutations: bool
    simulation_mutations: bool
    simulation_rounds: SimulationRounds

    def __init__(self,
                 simulation_id: str,
                 nodes: Sequence[Node],
                 rounds: int,
                 simulation_rounds: Optional[SimulationRounds] = None,
                 *,
                 mutations_per_mille: int = 0,
                 round_mutations: bool = False,
                 simulation_mutations: bool = False):
        super().__init__(nodes=nodes, simulation_id=simulation_id, simulation_rounds=simulation_rounds)
        self.rounds = rounds
        self.mutations_per_mille = mutations_per_mille
        self.round_mutations = round_mutations
        self.simulation_mutations = simulation_mutations

    def run_simulation(self) -> SimulationRounds:
        """run the simulation

        :return: simulation results
        :rtype: RoundList
        """
        game_id = ':'.join(sorted(node.node_id for node in self.nodes))

        if not self.simulation_rounds.get(game_id):
            self.simulation_rounds[self.simulation_id] = []

        while len(self.simulation_rounds[self.simulation_id]) < self.rounds:
            self.simulation_rounds[self.simulation_id].append(play_round(
                nodes=self.nodes, rounds=self.simulation_rounds[self.simulation_id],
                mutations_per_mille=self.mutations_per_mille, round_mutations=self.round_mutations
            ))

        if self.simulation_mutations:
            for node in self.nodes:
                if random.randrange(0, 1000) < self.mutations_per_mille:
                    node.mutate()

        return self.simulation_rounds

    def process_results(self):
        raise NotImplemented
