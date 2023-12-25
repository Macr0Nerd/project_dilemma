import random
from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class RandomCooperation(Algorithm):
    algorithm_id = 'random_cooperation'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds) -> bool:
        return random.choice([True, False])
