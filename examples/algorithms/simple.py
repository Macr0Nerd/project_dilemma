from collections.abc import Sequence
import random
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class AlwaysCooperate(Algorithm):
    algorithm_id = 'always_cooperate'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds, **kwargs) -> bool:
        return True


class AlwaysDefect(Algorithm):
    algorithm_id = 'always_defect'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds, **kwargs) -> bool:
        return False


class RandomCooperation(Algorithm):
    algorithm_id = 'random_cooperation'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds, **kwargs) -> bool:
        return random.choice([True, False])


AlwaysCooperate.mutations = [AlwaysDefect, RandomCooperation]
AlwaysDefect.mutations = [AlwaysCooperate, RandomCooperation]
RandomCooperation.mutations = [AlwaysCooperate, AlwaysDefect]
