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

from project_dilemma.interfaces.base import Round, RoundList
from project_dilemma.interfaces.node import Node


def play_round(nodes: Sequence[Node],
               rounds: RoundList,
               *,
               mutations_per_mille: int,
               round_mutations: bool = False,) -> Round:
    """run a round of prisoners dilemma with each node

    :param nodes: nodes to run
    :type nodes: Sequence[Node]
    :param rounds: lsit of rounds
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
