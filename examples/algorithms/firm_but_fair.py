from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class FirmButFair(Algorithm):
    algorithm_name = "firm_but_fair"

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds, *, node_id: str, **kwargs) -> bool:
        sucker_payoff_buffer = 5  # How many rounds should be considered when looking for a sucker payoff

        if not rounds or len(rounds) < sucker_payoff_buffer:
            return True

        for i in range(sucker_payoff_buffer * -1, 0):
            for iter_node_id, cooperation in rounds[i].items():
                if node_id == iter_node_id:
                    continue

                if not cooperation:
                    break
            else:
                continue

            if i == -1:
                return False

            break

        return True
