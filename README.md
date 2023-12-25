# Project Dilemma
Project Dilemma is a simulation tool for testing algorithms in the prisoner's dilemma.
It provides a standard interface to define both algorithm and simulation classes so that they may be easily tested.
Inspired by [this Veritasium](https://youtu.be/mScpHTIi-kM?si=7pe8XjmjjWLhMup6) video.

## Table of Contents
* [Installation](#installation)
* [Configuration](#configuration)
  * [Config File Location](#config-file-location)
  * [Dynamic Imports](#dynamic-imports)
* [Algorithms](#algorithms)
* [Simulations](#simulations)

## Installation
1. Download git repo
2. Change into repo root directory
3. Run `pip install .`

## Configuration
### Config File Location
Project Dilemma will automatically try to load the configuration from the user's and system's configuration directories,
usually set by `$XDG_CONFIG_DIRS`. For most Linux users, this will check `~/.config/project_dilemma` and them somewhere
in `/etc`.

This behaviour can be overridden by specifying the `--config` flag to the config file you want to use.
### Config Format
Project Dilemma uses the [TOML](https://toml.io/) format for configuration files.
This is a human-readable format that is easy to write.
The schema has been provided below:

```toml
algorithms_directory = "/path/to/algorithms/"
nodes = [ { node_id = "node_1", algorithm = { file = "foo.py", object = "Foo" } },
          { node_id = "node_2", algorithm = { file = "bar/baz.py", object = "Baz" } } ]
rounds_data = "path/to/round.json"
rounds_output = "path/to/round.json"
simulation = { file = "foobar.py", object = "FooBar" }
simulation_id = "name of simulation"
simulation_arguments = { foo = "bar" }
simulation_results = "path/to/results.json"
simulations_directory = "/path/to/simulations/"
```

* algorithms_directory
  * A path to the directory containing the algorithms files
* nodes
  * An array of tables that specify a node id and an algorithm, as defined in the [Dynamic Imports](#dynamic-imports)
section
* rounds_data
  * Path to a JSON file containing previous round data
* rounds_output
  * Path to write the round data as a JSON
* simulation:
  * A [Dynamic Import](#dynamic-imports)
* simulation_id
  * The name of the simulation
* simulation_arguments
  * Arguments to pass into the simulation
* simulation_results
  * Path to write the simulation results
* simulations_directory
  * A path to the directory containing additional simulation files
  * Required for user provided simulations

### Dynamic Imports
Because a lot of the objects, such as the algorithms and simulations, can or must be provided by the user, this data
must be imported dynamically.
In order to easily import these objects without importing every simulation and algorithm, the following format can be
used to tell the program where to look for the imports:

```toml
{ file = "path/to/file", object = "ObjectToImport" }
```

* file
  * A path to the file containing the object relative to the associated directory in the config
  * Required for algorithms and user provided simulations
* object
  * The object to import
    * For builtin simulations, specify the simulation class name here

## Algorithms
Algorithms can be defined very easily.
Only four things must be done to subclass the Algorithm interface:
1. Set class name
2. Set `algorithm_id`
3. Pass in the mutations to the interface's init (see template for example)
4. Implement the `decide` function

The `decide` function is what the simulation uses to run the algorithm.
It accepts a `project_dilemma.interfaces.base.Rounds` object which can be used to get the results of prior rounds.
The function should return `True` for cooperation, and `False` for defection.

A template has been provided us `templates/algorithm_template` for ease of use.

## Simulations
Coming soon, see `project_dilemma.interfaces.simulation` for more information.

## License
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
---
This project utilizes the [platformdirs](https://github.com/platformdirs/platformdirs) project which is licensed under
the MIT License. Copyright (c) 2010-202x The platformdirs developers