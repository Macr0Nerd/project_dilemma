from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class TwoTitsForTat(Algorithm):
    algorithm_id = 'two_tits_for_tat'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds) -> bool:
        if not rounds:
            return True

        tit_or_tat = []
        for round in rounds[-2:]:
            ratio = {True: 0, False: 0}
            for node_id, cooperation in round.items():
                ratio[cooperation] += 1

            tit_or_tat.append(ratio[True] >= ratio[False])

        return tit_or_tat[0] and tit_or_tat[-1]
