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
from typing import Optional

from project_dilemma.interfaces.base import Base, SimulationRounds
from project_dilemma.interfaces.node import Node


class Simulation(Base):
    """simulation interface

    .. note::
    all the nodes must have unique node ids

    :var nodes: node data for the simulation
    :vartype nodes: Sequence[Node]
    :var simulation_id: id of the simulation
    :vartype simulation_id: str
    :var simulation_rounds: simulation round data
    :vartype simulation_rounds: SimulationRounds
    """
    _required_attributes = [
        'nodes',
        'process_simulation',
        'run_simulation',
        'simulation_id',
        'simulation_rounds'
    ]

    simulation_id: str
    _simulation_rounds: SimulationRounds
    _nodes: Sequence[Node]

    @abstractmethod
    def __init__(self, *, nodes: Sequence[Node], simulation_id: str, simulation_rounds: SimulationRounds = None):
        self.nodes = nodes
        self.simulation_id = simulation_id
        self.simulation_rounds = simulation_rounds

    @property
    def nodes(self) -> Sequence[Node]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: Sequence[Node]):
        if max(Counter([node.node_id for node in nodes]).values()) > 1:
            raise ValueError('All node ids provided must be unique')

        self._nodes = nodes

    @property
    def simulation_rounds(self) -> SimulationRounds:
        return self._simulation_rounds

    @simulation_rounds.setter
    def simulation_rounds(self, simulation_rounds: Optional[SimulationRounds]):
        if not simulation_rounds:
            self._simulation_rounds = {}
        else:
            self._simulation_rounds = simulation_rounds

    @abstractmethod
    def run_simulation(self) -> SimulationRounds:
        """run the simulation

        :return: simulation results
        :rtype: RoundList
        """
        raise NotImplemented

    @abstractmethod
    def process_results(self):
        """process simulation results"""
        raise NotImplemented
