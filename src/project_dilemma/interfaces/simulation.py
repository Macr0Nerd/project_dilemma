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

import project_dilemma.interfaces.base as pd_int_base
import project_dilemma.interfaces.node as pd_int_node


class SimulationBase(pd_int_base.Base):
    """simulation interface

    .. note::
    all the nodes must have unique node ids

    :var nodes: node data for the simulation
    :vartype nodes: Sequence[Type[Node]]
    :var simulation_id: id of the simulation
    :vartype simulation_id: str
    :var simulation_data: simulation round data
    :vartype simulation_data: Simulations
    """
    required_attributes = [
        'nodes',
        'process_simulation',
        'run_simulation',
        'simulation_data',
        'simulation_id',
    ]

    simulation_id: str
    _simulation_data: pd_int_base.Generations | pd_int_base.Simulations
    _nodes: Sequence[type[pd_int_node.Node]]

    @abstractmethod
    def __init__(self,
                 *,
                 nodes: Sequence[pd_int_node.Node],
                 simulation_id: str,
                 simulation_data: pd_int_base.Generations | pd_int_base.Simulations = None,
                 **kwargs):
        self.nodes = nodes
        self.simulation_id = simulation_id
        self.simulation_data = simulation_data

    @property
    def nodes(self) -> Sequence[type[pd_int_node.Node]]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: Sequence[type[pd_int_node.Node]]):
        if max(Counter([node.node_id for node in nodes]).values()) > 1:
            raise ValueError('All node ids provided must be unique')

        self._nodes = nodes

    @property
    def simulation_data(self) -> pd_int_base.Generations | pd_int_base.Simulations:
        return self._simulation_data

    @simulation_data.setter
    def simulation_data(self, simulation_data: Optional[pd_int_base.Generations | pd_int_base.Simulations]):
        if not simulation_data:
            self._simulation_data = {}
        else:
            self._simulation_data = simulation_data

    @abstractmethod
    def run_simulation(self) -> pd_int_base.Generations | pd_int_base.Simulations:
        """run the simulation

        :return: simulation results
        :rtype: Simulations
        """
        raise NotImplementedError

    @abstractmethod
    def process_results(self):
        """process simulation results"""
        raise NotImplementedError


class Simulation(SimulationBase):
    _simulation_data: pd_int_base.Simulations

    @abstractmethod
    def __init__(self,
                 *,
                 nodes: Sequence[pd_int_node.Node],
                 simulation_id: str,
                 simulation_data: pd_int_base.Simulations = None, **kwargs):
        super().__init__(nodes=nodes, simulation_id=simulation_id, simulation_data=simulation_data)

    @abstractmethod
    def run_simulation(self) -> pd_int_base.Simulations:
        raise NotImplementedError

    @abstractmethod
    def process_results(self):
        raise NotImplementedError
