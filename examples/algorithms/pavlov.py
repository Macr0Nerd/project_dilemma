from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class Pavlov(Algorithm):
    algorithm_name = "pavlov"

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds, *, node_id: str, **kwargs) -> bool:
        if not rounds:
            return True

        for iter_node_id, cooperation in rounds[-1].items():
            if node_id == iter_node_id:
                continue

            if not cooperation:
                return not rounds[-1][node_id]

        return rounds[-1][node_id]
