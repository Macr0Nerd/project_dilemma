from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class TitForTat(Algorithm):
    algorithm_id = 'tit_for_tat'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds) -> bool:
        if not rounds:
            return True

        ratio = {True: 0, False: 0}
        for node_id, cooperation in rounds[-1].items():
            ratio[cooperation] += 1

        return ratio[True] >= ratio[False]


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


TitForTat.mutations = [TitForTwoTats, TwoTitsForTat]
TitForTwoTats.mutations = [TitForTat, TwoTitsForTat]
TwoTitsForTat.mutations = [TitForTat, TitForTwoTats]
