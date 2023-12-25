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

from project_dilemma.interfaces.algorithm import Algorithm
from project_dilemma.interfaces.base import Base


class Node(Base):
    """simulation node interface

    The interface for the nodes which will run in the simulation

    :var node_id: id of the node
    :vartype node_id: str
    :var algorithm: cooperation algorithm
    :vartype algorithm: Algorithm
    """
    _required_attributes = [
        'algorithm',
        'node_id',
        'mutate',
    ]

    node_id: str
    algorithm: Algorithm

    def __init__(self, node_id: str, algorithm: Algorithm):
        self.node_id = node_id
        self.algorithm = algorithm

    def mutate(self):
        """set the node to a random algorithm mutation"""
        if self.algorithm.mutations:
            self.algorithm = random.choice(self.algorithm.mutations)
