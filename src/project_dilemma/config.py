import argparse
import os.path
import sys
import tomllib
from typing import Any, Dict, List, NotRequired, TypedDict

import platformdirs

DEFAULT_CONFIG_NAME = 'project_dilemma.toml'


class DynamicImport(TypedDict):
    file: NotRequired[str]
    object: str


class NodeConfig(TypedDict):
    node_id: str
    algorithm: DynamicImport


class ProjectDilemmaConfig(TypedDict):
    algorithms_directory: str
    nodes: List[NodeConfig]
    simulation: DynamicImport
    simulation_id: str
    simulation_arguments: Dict[str, Any]
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
    parser_config.add_argument('--simulation', help='simulation to run')
    parser_config.add_argument('--algorithms-directory', help='directory containing algorithm files',
                               dest='algorithms_directory')
    parser_config.add_argument('--simulations-directory', help='directory containing simulation files',
                               dest='simulations_directory')

    if not len(sys.argv):
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
