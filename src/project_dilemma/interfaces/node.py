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
import random
from typing import Self

import project_dilemma.interfaces.algorithm as pd_int_algorithm
import project_dilemma.interfaces.base as pd_int_base


class Node(pd_int_base.Base):
    """simulation node interface

    The interface for the nodes which will run in the simulations

    :var node_id: id of the node
    :vartype node_id: str
    :var algorithm: cooperation algorithm
    :vartype algorithm: type[Algorithm]
    """
    _required_attributes = [
        'algorithm',
        'node_id',
        'mutate',
    ]

    node_id: str
    algorithm: type[pd_int_algorithm.Algorithm]

    def __init__(self, node_id: str, algorithm: type[pd_int_algorithm.Algorithm], **kwargs):
        self.node_id = node_id
        self.algorithm = algorithm

    def __eq__(self, other: Self):
        return (self.node_id == other.node_id) and (self.algorithm == other.algorithm)

    def mutate(self):
        """set the node to a random algorithm mutation"""
        if self.algorithm.mutations:
            self.algorithm = random.choice(self.algorithm.mutations)
