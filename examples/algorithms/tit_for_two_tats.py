from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class TitForTwoTats(Algorithm):
    algorithm_id = 'tit_for_two_tats'

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

        return tit_or_tat[0] or tit_or_tat[-1]
