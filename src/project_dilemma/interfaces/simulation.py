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
from collections import Counter
from collections.abc import Sequence

from project_dilemma.interfaces.base import Base, RoundList
from project_dilemma.interfaces.node import Node


class Simulation(Base):
    """simulation interface

    .. note::
    all the nodes must have unique node ids

    :var simulation_id: id of the simulation
    :vartype simulation_id: str
    :var nodes: node data for the simulation
    :vartype nodes: Sequence[Node]
    """
    _required_attributes = [
        'nodes',
        'run_simulation',
        'simulation_id'
    ]

    simulation_id: str
    nodes: Sequence[Node]

    @abstractmethod
    def __init__(self, simulation_id: str, nodes: Sequence[Node]):
        self.simulation_id = simulation_id
        self.nodes = nodes

    @property
    def nodes(self) -> Sequence[Node]:
        return self.nodes

    @nodes.setter
    def nodes(self, nodes: Sequence[Node]):
        if max(Counter([node.node_id for node in nodes]).values()) > 1:
            raise ValueError('All node ids provided must be unique')

        self.nodes = nodes

    @classmethod
    @abstractmethod
    def run_simulation(cls) -> RoundList:
        """run the simulation

        :return: simulation results
        :rtype: RoundList
        """
        raise NotImplemented
