"""
Copyright 2023 Gabriele Ron

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from abc import abstractmethod
from collections.abc import Sequence
from typing import Optional, Self

from project_dilemma.interfaces.base import Base, RoundList


class Algorithm(Base):
    """cooperation algorithm interface

    :var algorithm_id: id of the algorithm
    :vartype algorithm_id: str
    :var mutable: if the algorithm is mutable
    :vartype mutable: bool
    :var mutations: list of possible mutations
    :vartype mutations: List[Algorithm]
    """
    _required_attributes = [
        'algorithm_id',
        'decide',
    ]

    algorithm_id: str
    mutable: bool
    mutations: Optional[Sequence[Self]]

    def __init__(self, mutations: Sequence[Self] = None) -> None:
        self.mutations = mutations

    @property
    def mutations(self) -> Optional[Sequence[Self]]:
        return self.mutations

    @mutations.setter
    def mutations(self, mutations: Optional[Sequence[Self]]):
        self.mutable = bool(mutations)
        self.mutations = mutations

    @abstractmethod
    def decide(self, rounds: RoundList) -> bool:
        """decide whether to cooperate or not

        :param rounds: the list of moves
        :type rounds: MoveList
        :return: whether to cooperate or not
        :rtype: bool
        """
        raise NotImplementedError
