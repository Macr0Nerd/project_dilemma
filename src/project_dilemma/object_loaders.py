import importlib
import json
import os.path
import sys
from typing import Dict, List

from project_dilemma.config import ProjectDilemmaConfig
from project_dilemma.interfaces import Algorithm, Generations, Node, SimulationBase, Simulations
from project_dilemma.simulations import simulations_map


def create_nodes(config: ProjectDilemmaConfig, algorithms_map: Dict[str, type[Algorithm]]) -> List[type[Node]]:
    """create the simulation nodes

    :param config: configuration data
    :type config: ProjectDilemmaConfig
    :param algorithms_map: map of algorithm class names to algorithms
    :type algorithms_map: Dict[str, type[Algorithm]]
    :return: list of nodes
    :rtype: List[type[Node]]
    """
    nodes = []

    for node in config['nodes']:
        nodes.append(Node(node['node_id'], algorithms_map[node['algorithm']['object']]))

    return nodes


def load_algorithms(config: ProjectDilemmaConfig) -> Dict[str, type[Algorithm]]:
    """load all algorithms used

    :param config: configuration data
    :type config: ProjectDilemmaConfig
    :return: map of algorithm class names to algorithms
    :rtype: Dict[str, type[Algorithm]]
    """
    sys.path.append(config['algorithms_directory'])

    algorithms = [node['algorithm'] for node in config['nodes']]
    algorithm_map: Dict[str, type[Algorithm]] = {}

    for algorithm in algorithms:
        if algorithm_map.get(algorithm['object']):
            continue

        if not os.path.exists(os.path.join(config['algorithms_directory'], algorithm['file'])):
            print(f"Algorithm file {algorithm['file']} could not be found")
            sys.exit(1)

        algorithm_module = importlib.import_module(algorithm['file'].strip('.py'))
        algorithm_map[algorithm['object']] = getattr(algorithm_module, algorithm['object'])

    return algorithm_map


def load_simulation_data(config: ProjectDilemmaConfig) -> Generations | Simulations:
    """load round data

    :param config: configuration data
    :type config: ProjectDilemmaConfig
    :return: simulation rounds or generations
    :rtype: Generations | Simulations
    """
    data = {}

    # noinspection PyTypedDict
    if config.get('simulation_data'):
        try:
            # noinspection PyTypedDict
            with open(config['simulation_data'], 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print('Rounds data file not found')
            sys.exit(1)

    return data


def load_simulation(config: ProjectDilemmaConfig, *, generational: bool = False) -> type[SimulationBase]:
    """load the simulation

    :param config: configuration data
    :type config: ProjectDilemmaConfig
    :param generational: if the generational simulation should be loaded
    :type generational: bool
    :return: the configured simulation
    :rtype: type[SimulationBase]
    """
    key = 'simulation'
    if generational:
        key = 'generational_' + key

    if config[key].get('file'):
        if not config.get('simulations_directory'):
            print('A simulations directory is required to use user provided simulations')
            sys.exit(1)

        sys.path.append(config['simulations_directory'])

        if not os.path.exists(os.path.join(config['simulations_directory'], config[key]['file'])):
            print(f'The {"generational " if generational else ""}simulation file could not be found')
            sys.exit(1)

        simulation_module = importlib.import_module(config[key]['file'].strip('.py'))
        simulation = getattr(simulation_module, config[key]['object'])
    else:
        simulation = simulations_map[config[key]['object']]

    return simulation
