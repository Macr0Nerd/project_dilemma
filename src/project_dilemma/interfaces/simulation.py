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

from project_dilemma.interfaces import Generations, Node, Simulations
from project_dilemma.interfaces.base import Base


class SimulationBase(Base):
    """simulation interface

    .. note::
    all the nodes must have unique node ids

    :var nodes: node data for the simulation
    :vartype nodes: Sequence[Node]
    :var simulation_id: id of the simulation
    :vartype simulation_id: str
    :var simulation_data: simulation round data
    :vartype simulation_data: Simulations
    """
    _required_attributes = [
        'nodes',
        'process_simulation',
        'run_simulation',
        'simulation_data',
        'simulation_id',
    ]

    simulation_id: str
    _simulation_data: Generations | Simulations
    _nodes: Sequence[Node]

    @abstractmethod
    def __init__(self, *, nodes: Sequence[Node], simulation_id: str, simulation_data: Generations | Simulations = None):
        self.nodes = nodes
        self.simulation_id = simulation_id
        self.simulation_data = simulation_data

    @property
    def nodes(self) -> Sequence[Node]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: Sequence[Node]):
        if max(Counter([node.node_id for node in nodes]).values()) > 1:
            raise ValueError('All node ids provided must be unique')

        self._nodes = nodes

    @property
    def simulation_data(self) -> Generations | Simulations:
        return self._simulation_data

    @simulation_data.setter
    def simulation_data(self, simulation_data: Optional[Generations | Simulations]):
        if not simulation_data:
            self._simulation_data = {}
        else:
            self._simulation_data = simulation_data

    @abstractmethod
    def run_simulation(self) -> Generations | Simulations:
        """run the simulation

        :return: simulation results
        :rtype: Simulations
        """
        return NotImplemented

    @abstractmethod
    def process_results(self):
        """process simulation results"""
        return NotImplemented


class Simulation(SimulationBase):
    _simulation_data: Simulations

    @abstractmethod
    def __init__(self, *, nodes: Sequence[Node], simulation_id: str, simulation_data: Simulations = None):
        super().__init__(nodes=nodes, simulation_id=simulation_id, simulation_data=simulation_data)

    @abstractmethod
    def run_simulation(self) -> Simulations:
        return NotImplemented

    @abstractmethod
    def process_results(self):
        return NotImplemented
