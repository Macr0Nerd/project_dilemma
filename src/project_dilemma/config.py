"""
Copyright 2023-2025 Gabriele Ron

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
import argparse
import os.path
import sys
import tomllib
from typing import Any, NotRequired, TypedDict

import platformdirs

DEFAULT_CONFIG_NAME = 'project_dilemma.toml'


class DynamicImport(TypedDict):
    file: NotRequired[str]
    object: str


class NodeConfig(TypedDict):
    node_id: str
    algorithm: DynamicImport
    quantity: NotRequired[int]


class ProjectDilemmaConfig(TypedDict):
    algorithms_directory: str
    generational_simulation: NotRequired[DynamicImport]
    nodes: list[NodeConfig]
    simulation: DynamicImport
    simulation_id: str
    simulation_arguments: dict[str, Any]
    simulation_data: NotRequired[str]
    simulation_data_output: NotRequired[str]
    simulation_results_output: NotRequired[str]
    simulations_directory: NotRequired[str]


def arguments() -> dict:
    """configure arguments

    :return: arguments
    :rtype: dict
    """
    parser = argparse.ArgumentParser(
        description="The prisoner's dilemma in python",
        epilog='Developed by Gabriele A. Ron (developer@groncyber.com)'
    )

    parser_config = parser.add_argument_group('configuration')
    parser_config.add_argument('-c', '--config', help='specify configuration file to use')
    parser_config.add_argument('--algorithms-directory', help='directory containing algorithm files',
                               dest='algorithms_directory')
    parser_config.add_argument('--simulations-directory', help='directory containing simulation files',
                               dest='simulations_directory')

    parser_in = parser.add_argument_group('input')
    parser_in.add_argument('--simulation-data', help='specify path to simulation data in JSON',
                           dest='generations_data')

    parser_out = parser.add_argument_group('output')
    parser_out.add_argument('-gO', '--simulation-data-output', help='output the simulation data as JSON',
                            dest='simulation_data_output')
    parser_out.add_argument('-sO', '--simulation-result-output', help='output the results as JSON',
                            dest='simulation_results_output')

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)

    args = vars(parser.parse_args())

    return args


def load_configuration() -> ProjectDilemmaConfig:
    """load configuration data

    :return: configuration data
    :rtype: ProjectDilemmaConfig
    """
    dirs = platformdirs.PlatformDirs('project_dilemma')

    args = arguments()

    config_file = args.pop('config')

    if not config_file:
        if os.path.exists(config_file := os.path.join(dirs.user_config_path, DEFAULT_CONFIG_NAME)):
            pass
        elif os.path.exists(config_file := os.path.join(dirs.site_config_path, DEFAULT_CONFIG_NAME)):
            pass
        else:
            print('Could not find a configuration file to load')
            sys.exit(1)
    else:
        if not os.path.exists(config_file):
            print('Specified configuration file does not exist')
            sys.exit(1)

    with open(config_file, 'rb') as f:
        config_file_data: ProjectDilemmaConfig = tomllib.load(f)

    args = {k: v for k, v in args.items() if v}

    # noinspection PyTypeChecker
    return {**config_file_data, **args}
