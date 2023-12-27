from abc import abstractmethod
from collections.abc import MutableMapping, Sequence
from copy import deepcopy
import sys
from typing import Any, Optional

import project_dilemma.interfaces.base as pd_int_base
import project_dilemma.interfaces.node as pd_int_node
import project_dilemma.interfaces.simulation as pd_int_simulation


class GenerationalSimulation(pd_int_simulation.SimulationBase):
    """generational simulation interface

    :var generations: number of generations to run
    :vartype generations: int
    :var generational_simulation: simulation class to use
    :vartype simulation: type[SimulationBase]
    :var simulation_kwargs: keyword arguments to pass into the simulation
    :vartype simulation_kwargs: MutableMapping[str, Any]
    """
    required_attributes = [
        'generation_hook'
        'generations',
        'generational_simulation'
        'simulations_kwargs'
    ]

    generations: int
    generational_simulation: type[pd_int_simulation.SimulationBase]
    simulation_kwargs: MutableMapping[str, Any]
    _simulation_data: pd_int_base.Generations

    def __init__(self,
                 simulation_id: str,
                 nodes: Sequence[pd_int_node.Node],
                 generations: int,
                 generational_simulation: type[pd_int_simulation.SimulationBase],
                 simulation_data: Optional[pd_int_base.Simulations] = None,
                 **kwargs):
        super().__init__(nodes=nodes, simulation_id=simulation_id, simulation_data=simulation_data)
        self.generations = generations
        self.generational_simulation = generational_simulation
        self.simulation_kwargs = kwargs

    @abstractmethod
    def generation_hook(self):
        """process generational_simulation information to make generational changes"""
        raise NotImplementedError

    def run_simulation(self) -> pd_int_base.Generations:
        game_id = ':'.join(sorted(node.node_id for node in self.nodes))
        sim_data_copy = deepcopy(self.simulation_data)

        self.simulation_data = {}
        for generation_index in range(self.generations):
            generation_id = f'generation_{generation_index}'

            # Rebuild existing generational data
            if generation_index < len(self.simulation_data):
                self.simulation_data[generation_id] = sim_data_copy[generation_id]
                self.generation_hook()
                continue

            if not self.simulation_data.get(generation_id):
                self.simulation_data[generation_id] = {}

            simulation = self.generational_simulation(**{
                'simulation_id': f'{generation_id}[{game_id}]',
                'nodes': self.nodes,
                'simulation_data': self.simulation_data[generation_id],
                **self.simulation_kwargs
            })

            self.simulation_data[generation_id].update(simulation.run_simulation())
            self.generation_hook()

        return self.simulation_data

    def process_results(self) -> MutableMapping[str, Any]:
        simulation = self.generational_simulation(**{
            'simulation_id': 'process_results',
            'nodes': self.nodes,
            'simulation_data': {},
            **self.simulation_kwargs
        })

        try:
            simulation.process_results()
        except NotImplementedError:
            print('The provided generational_simulation class has not implemented results processing')
            sys.exit(1)

        results = {}
        for generation_id, generation_data in self.simulation_data.items():
            simulation.simulation_data = generation_data
            results[generation_id] = simulation.process_results()

        return results
