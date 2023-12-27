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

from project_dilemma.interfaces import Node, Round, Rounds, Simulation, Simulations


def play_round(nodes: Sequence[type[Node]],
               rounds: Rounds,
               *,
               mutations_per_mille: int,
               round_mutations: bool = False,) -> Round:
    """run a round of prisoners dilemma with each node

    :param nodes: nodes to run
    :type nodes: Sequence[type[Node]]
    :param rounds: list of rounds
    :type rounds: RoundList
    :param mutations_per_mille: rate that mutations should occur per mille
    :type mutations_per_mille: int
    :param round_mutations: if mutations are enabled for rounds
    :type round_mutations: bool
    :return: round results
    :rtype: Round
    """
    move: Round = {}
    for node in nodes:
        move[node.node_id] = node.algorithm.decide(rounds)

        if round_mutations and random.randrange(0, 1000) < mutations_per_mille:
            node.mutate()

    return move


class BasicSimulation(Simulation):
    """basic simulation

    :var mutations_per_mille: rate that mutations should occur per mille
    :vartype mutations_per_mille: int
    :var noise: if noise is enabled
    :var noise_per_mille:
    :var rounds: total rounds to play
    :vartype rounds: int
    :var round_mutations: if nodes can mutate after a round
    :vartype round_mutations: bool
    :var simulation_mutations: if nodes can mutate after a simulation
    :vartype simulation_mutations: bool
    """
    mutations_per_mille: int
    noise: bool
    noise_per_mille: int
    rounds: int
    round_mutations: bool
    simulation_mutations: bool

    def __init__(self,
                 simulation_id: str,
                 nodes: Sequence[Node],
                 rounds: int,
                 simulation_data: Optional[Simulations] = None,
                 *,
                 mutations_per_mille: int = 0,
                 noise: bool = False,
                 noise_per_mille: int = 0,
                 round_mutations: bool = False,
                 simulation_mutations: bool = False,
                 **kwargs):
        super().__init__(nodes=nodes, simulation_id=simulation_id, simulation_data=simulation_data)
        self.rounds = rounds
        self.mutations_per_mille = mutations_per_mille
        self.noise = noise
        self.noise_per_mille = noise_per_mille
        self.round_mutations = round_mutations
        self.simulation_mutations = simulation_mutations

    def run_simulation(self) -> Simulations:
        """run the simulation

        :return: simulation results
        :rtype: Rounds
        """
        game_id = ':'.join(sorted(node.node_id for node in self.nodes))

        if not self.simulation_data.get(game_id):
            self.simulation_data[game_id] = []

        while len(self.simulation_data[game_id]) < self.rounds:
            self.simulation_data[game_id].append(play_round(
                nodes=self.nodes, rounds=self.simulation_data[game_id],
                mutations_per_mille=self.mutations_per_mille, round_mutations=self.round_mutations
            ))

            if self.noise:
                for node, decision in self.simulation_data[game_id][-1].items():
                    if random.randrange(0, 1000) < self.noise_per_mille:
                        self.simulation_data[game_id][-1][node] = not decision

        if self.simulation_mutations:
            for node in self.nodes:
                if random.randrange(0, 1000) < self.mutations_per_mille:
                    node.mutate()

        return self.simulation_data

    def process_results(self):
        raise NotImplementedError
