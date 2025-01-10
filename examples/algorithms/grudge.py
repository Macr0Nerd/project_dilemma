from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class GrimTrigger(Algorithm):
    algorithm_id = 'grim_trigger'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds, **kwargs) -> bool:
        if not rounds:
            return True

        return False not in rounds[-1].values()
