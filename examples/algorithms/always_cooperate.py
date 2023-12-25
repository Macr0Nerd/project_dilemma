from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class AlwaysCooperate(Algorithm):
    algorithm_id = 'always_cooperate'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds) -> bool:
        return True
