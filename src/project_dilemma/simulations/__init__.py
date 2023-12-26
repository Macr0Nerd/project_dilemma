from project_dilemma.simulations.basic_simulation import BasicSimulation
from project_dilemma.simulations.standard_simulation import StandardSimulation
from project_dilemma.simulations.multiprocess_standard_simulation import MultiprocessStandardSimulation

__all__ = ['simulations_map', 'BasicSimulation', 'StandardSimulation', 'MultiprocessStandardSimulation']

simulations_map = {
    'BasicSimulation': BasicSimulation,
    'StandardSimulation': StandardSimulation,
    'MultiprocessStandardSimulation': MultiprocessStandardSimulation
}
