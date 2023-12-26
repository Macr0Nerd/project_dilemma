from abc import abstractmethod
from collections.abc import MutableMapping, Sequence
import sys
from typing import Any, Optional, Type

import project_dilemma.interfaces.base as pd_int_base
import project_dilemma.interfaces.node as pd_int_node
import project_dilemma.interfaces.simulation as pd_int_simulation


class GenerationalSimulation(pd_int_simulation.SimulationBase):
    """generational simulation interface

    :var generations: number of generations to run
    :vartype generations: int
    :var simulation: simulation class to use
    :vartype simulation: Type[project_dilemma.interfaces.simulation.SimulationBase]
    :var simulation_kwargs: keyword arguments to pass into the simulation
    :vartype simulation_kwargs: MutableMapping[str, Any]
    """
    required_attributes = [
        'generation_hook'
        'generations',
        'simulation'
        'simulations_kwargs'
    ]

    generations: int
    simulation: Type[pd_int_simulation.SimulationBase]
    simulation_kwargs: MutableMapping[str, Any]
    _simulation_data: pd_int_base.Generations

    def __init__(self,
                 simulation_id: str,
                 nodes: Sequence[pd_int_node.Node],
                 generations: int,
                 simulation: Type[pd_int_simulation.SimulationBase],
                 simulation_data: Optional[pd_int_base.Simulations] = None,
                 **kwargs):
        super().__init__(nodes=nodes, simulation_id=simulation_id, simulation_data=simulation_data)
        self.generations = generations
        self.simulation = simulation
        self.simulation_kwargs = kwargs

    @abstractmethod
    def generation_hook(self):
        """process simulation information to make generational changes"""
        raise NotImplementedError

    def run_simulation(self) -> pd_int_base.Generations:
        game_id = ':'.join(sorted(node.node_id for node in self.nodes))
        for generation_index in range(len(self.simulation_data), self.generations):
            generation_id = f'generation_{generation_index}'

            if not self.simulation_data[generation_id]:
                self.simulation_data[generation_id] = {}

            simulation = self.simulation(
                f'{generation_id}[{game_id}]',
                self.nodes,
                self.simulation_data[generation_id],
                **self.simulation_kwargs
            )

            self.simulation_data[generation_id].update(simulation.process_results())
            self.generation_hook()

        return self.simulation_data

    def process_results(self) -> MutableMapping[str, Any]:
        simulation = self.simulation(
            'process_results',
            self.nodes,
            {},
            **self.simulation_kwargs
        )

        try:
            simulation.process_results()
        except NotImplementedError:
            print('The provided simulation class has not implemented results processing')
            sys.exit(1)

        results = {}
        for generation_id, generation_data in self.simulation_data.items():
            simulation.simulation_data = generation_data
            results[generation_id] = simulation.process_results()

        return results
