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

from project_dilemma.interfaces import Node, Simulation, Simulations


class SimulationTemplate(Simulation):
    @abstractmethod
    def __init__(self, nodes: Sequence[Node], simulation_id: str, simulation_rounds: Simulations = None):
        super().__init__(nodes=nodes, simulation_id=simulation_id, simulation_rounds=simulation_rounds)

    def run_simulation(self) -> Simulations:
        """run the simulation

        :return: simulation results
        :rtype: Simulations
        """
        raise NotImplemented

    def process_results(self):
        """process simulation results"""
        raise NotImplemented
