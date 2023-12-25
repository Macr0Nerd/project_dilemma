from collections.abc import Sequence
from typing import Self

from project_dilemma.interfaces import Algorithm, Rounds


class AlgorithmTemplate(Algorithm):
    algorithm_id = 'algorithm_template'

    def __init__(self, mutations: Sequence[Self]):
        super().__init__(mutations)

    @staticmethod
    def decide(rounds: Rounds) -> bool:
        # Place algorithm here
        # Return true for cooperation, and false for defection
        return True


# Set mutations here to avoid circular imports
AlgorithmTemplate.mutations = []
