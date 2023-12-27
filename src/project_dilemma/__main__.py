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
import json
import sys

from project_dilemma.config import load_configuration, ProjectDilemmaConfig
from project_dilemma.interfaces import GenerationalSimulation
from project_dilemma.object_loaders import create_nodes, load_algorithms, load_simulation_data, load_simulation


def main() -> int:
    config: ProjectDilemmaConfig = load_configuration()

    simulation_class = load_simulation(config)
    generational_simulation_class = None
    if issubclass(simulation_class, GenerationalSimulation):
        generational_simulation_class = load_simulation(config, generational=True)

    algorithms_map = load_algorithms(config)
    nodes = create_nodes(config, algorithms_map)
    simulation_data = load_simulation_data(config)

    simulation = simulation_class(
        simulation_id=config['simulation_id'],
        nodes=nodes,
        simulation_data=simulation_data,
        generational_simulation=generational_simulation_class,
        **config['simulation_arguments']
    )

    simulation_rounds = simulation.run_simulation()

    if config.get('simulation_data_output'):
        try:
            with open(config['simulation_data_output'], 'w') as f:
                json.dump(simulation_rounds, f)
        except FileNotFoundError:
            print('Rounds output file could not be written to')
            return 1

    simulation_results = simulation.process_results()

    if config.get('simulation_results_output'):
        try:
            with open(config['simulation_results_output'], 'w') as f:
                json.dump(simulation_results, f)
        except FileNotFoundError:
            print('Simulation output file could not be written to')
            return 1
        except NotImplementedError:
            print('This simulation class has not implemented results processing')
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
