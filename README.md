# Project Dilemma
## Table of Contents
* [Configuration](#configuration)

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
simulation = { file = "foobar.py", object = "FooBar" }
simulation_id = "name of simulation"
simulation_arguments = { foo = "bar" }
simulations_directory = "/path/to/simulations/"
```

* algorithms_directory
  * A path to the directory containing the algorithms files
* nodes
  * An array of tables that specify a node id and an algorithm, as defined in the [Dynamic Imports](#dynamic-imports)
section
* simulation:
  * A [Dynamic Imports](#dynamic-imports)
* simulation_id
  * The name of the simulation
* simulation_arguments
  * Arguments to pass into the simulation
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