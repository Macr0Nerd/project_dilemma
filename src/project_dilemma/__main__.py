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
import sys

from project_dilemma.config import load_configuration, ProjectDilemmaConfig
from project_dilemma.object_loaders import create_nodes, load_algorithms, load_simulation


def main() -> int:
    config: ProjectDilemmaConfig = load_configuration()

    simulation_class = load_simulation(config)
    algorithms_map = load_algorithms(config)
    nodes = create_nodes(config, algorithms_map)

    simulation = simulation_class.__init__(
        simulation_id=config['simulation_id'],
        nodes=nodes,
        **config['simulation_arguments']
    )

    simulation.run_simulation()

    return 0


if __name__ == '__main__':
    sys.exit(main())
