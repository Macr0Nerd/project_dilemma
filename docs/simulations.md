# Simulations
There are four included simulations in the project.
These are:
* BasicSimulation
* StandardSimulation
* MultiprocessingStandardSimulation
* StandardGenerationalSimulation

All of these accept the same arguments, with minor additional configuration options for the latter two.
The parameters for configuring these simulations are:
* rounds | int
  * How many rounds should be run in each simulation
* noise | bool
  * If the simulation is noisy (decisions may randomly be flipped)
* noise_per_mille | int
  * How noisy the simulation is as a per mille representation
    * i.e. 999 = 99.9%, 250 = 25.0%
* round_mutations | bool
  * If mutations are enabled at the end of every round
* simulation_mutations | bool
  * If mutations are enabled at the end of every simulation (only useful for generational simulations)
* mutations_per_mille
  * How frequent mutations should occur as a per mille representation
    * i.e. 999 = 99.9%, 250 = 25.0%

# StandardSimulation
This takes each node and pits it against each other node in multiple 1:1 matches, as is standard for the prisoner's
dilemma.

## MultiprocessingStandardSimulation
This runs the StandardSimulation on multiple processes so that it can run faster for larger simulations.
It has one additional argument:
* pool_size | int
  * How many processes should be spawned
  * Default is the number of CPU cores of the system

# StandardGenerationalSimulation
This runs multiple generations of simulations and applies a function after each round to make changes before the next.
This function takes the processed results of the last generation and for each __algorithm__ calculates a change in the
population size for each __algorithm__ based on the ratio of the difference of the algorithm points and the average
points per algorithm to the average points per algorithm.

    points_distance = (algorithm_points - average_points)/average_points
    population_change = floor(sqrt(abs(algorithm_population * points_distance))) * sign_of_points_distance

This simulation accepts one additional argument:
* generations | int
  * The number of generations to run

**WARNING: USING A LOT OF GENERATIONS, ROUNDS, AND NODES CAN CAUSE THIS SIMULATION TO USE A LOT OF PROCESSING POWER**
