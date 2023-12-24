from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm
from project_dilemma.interfaces.base import RoundList


class TitForTat(Algorithm):
    algorithm_id = 'tit_for_tat'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: RoundList) -> bool:
        if not rounds:
            return True

        ratio = {True: 0, False: 0}
        for node_id, cooperation in rounds[-1].items():
            ratio[cooperation] += 1

        return ratio[True] >= ratio[False]
