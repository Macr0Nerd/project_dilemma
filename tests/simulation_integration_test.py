import json

import pytest

import project_dilemma.config
from project_dilemma.config import load_configuration, ProjectDilemmaConfig
from project_dilemma.interfaces import Node
from project_dilemma.object_loaders import create_nodes, load_algorithms, load_simulation_data, load_simulation
from project_dilemma.simulations import StandardSimulation

from algorithms.simple import AlwaysCooperate, AlwaysDefect
from algorithms.tit_for_tat import TitForTat


@pytest.fixture
def test_configuration_loading(monkeypatch):
    def mock_args():
        return {'config': 'examples/config/pytest.toml'}

    monkeypatch.setattr(project_dilemma.config, 'arguments', mock_args)

    expected: ProjectDilemmaConfig = {
        'simulation_id': 'Pytest Simulation',
        'algorithms_directory': 'examples/algorithms/',
        'nodes': [
            {'node_id': 'node_1', 'algorithm': {'file': 'simple.py', 'object': 'AlwaysCooperate'}},
            {'node_id': 'node_2', 'algorithm': {'file': 'simple.py', 'object': 'AlwaysDefect'}},
            {'node_id': 'node_3', 'algorithm': {'file': 'tit_for_tat.py', 'object': 'TitForTat'}},
        ],
        'simulation': {'object': 'StandardSimulation'},
        'simulation_arguments': {'rounds': 10},
        'simulation_data': 'examples/rounds/pytest.json',
        'simulation_data_output': 'examples/rounds/pytest.json',
        'simulation_results_output': 'examples/results/pytest.json'
    }

    actual = load_configuration()

    assert expected == actual

    return actual


@pytest.fixture
def test_object_loading(test_configuration_loading):
    with open('examples/rounds/pytest.json', 'r') as f:
        expected_rounds = json.load(f)

    actual_rounds = load_simulation_data(test_configuration_loading)

    assert expected_rounds == actual_rounds

    expected_algorithm_map = {
        'AlwaysCooperate': AlwaysCooperate,
        'AlwaysDefect': AlwaysDefect,
        'TitForTat': TitForTat
    }

    actual_algorithm_map = load_algorithms(test_configuration_loading)

    assert False not in [
        algo.algorithm_id == actual_algorithm_map[aid].algorithm_id for aid, algo in expected_algorithm_map.items()
    ]

    expected_simulation = StandardSimulation

    actual_simulation = load_simulation(test_configuration_loading)

    assert expected_simulation == actual_simulation

    expected_nodes = [
        Node('node_1', AlwaysCooperate),
        Node('node_2', AlwaysDefect),
        Node('node_3', TitForTat)
    ]

    actual_nodes = create_nodes(test_configuration_loading, expected_algorithm_map)

    assert expected_nodes == actual_nodes

    x = actual_simulation(
        simulation_id=test_configuration_loading['simulation_id'],
        nodes=actual_nodes,
        **test_configuration_loading['simulation_arguments']
    )
    return x


@pytest.fixture
def test_simulation_run(test_object_loading):
    with open('examples/rounds/pytest.json', 'r') as f:
        expected_rounds = json.load(f)

    actual_rounds = test_object_loading.run_simulation()

    assert expected_rounds == actual_rounds


def test_simulation_process(test_object_loading):
    with open('examples/rounds/pytest.json', 'r') as f:
        rounds = json.load(f)

    with open('examples/results/pytest.json', 'r') as f:
        expected_results = json.load(f)

    test_object_loading.simulation_data = rounds

    actual_results = test_object_loading.process_results()

    assert expected_results == actual_results


