# Artemis Framework

Python framework for simulating population dynamics across spatial habitat networks.

The framework includes functionality for population dynamics, predator-prey interactions, dispersal, habitat patches, environmental perturbations, network analysis, simulation data management, and visualisation.

## Requirements

- Python 3.x
- NumPy
- SciPy
- Matplotlib
- NetworkX

Install the external Python packages with:

```bash
pip install numpy scipy matplotlib networkx
```

## Running the Framework

The main entry point is:

```bash
python simulation_runner.py
```

By default, `simulation_runner.py` uses the parameters defined in `parameters.py`.

A different parameters module can be supplied as a command-line argument:

```bash
python simulation_runner.py parameters_module
```

The parameters control the simulation configuration, including the spatial network, number of patches, simulation length, population dynamics, perturbations, data saving, and plotting options.

## Main Modules

`simulation_runner.py` starts new simulations or repeats existing simulations.

`simulation_obj.py` creates and manages the simulation object and its system state.

`population_dynamics.py` contains the population-dynamics functionality.

`predator_prey_dynamics.py` contains predator-prey dynamics.

`diffusion_population_model.py` contains the population diffusion model.

`species.py` defines species used by the simulations.

`local_population.py` manages local populations associated with habitat patches.

`habitat_patch.py` represents habitat patches within the spatial network.

`system_state.py` and `system_state_functions.py` manage the state of the simulation.

`perturbation.py` handles environmental and population perturbations.

`sample_spatial_data.py` generates sample spatial data used to initialise simulations.

`data_manager.py` and `data_manager_functions.py` handle simulation data, saving, loading, network analysis, and plotting.

`parameters.py` contains the main simulation configuration.

`parameters_species_repository.py` contains species parameter sets.

`degree_distribution.py` provides network degree-distribution functionality.

`re_analysis.py` provides functionality for analysing saved simulation results.

## Configuration

The main settings are contained in `parameters.py`.

These include options for:

- Spatial network type and connectivity
- Habitat type and spatial properties
- Patch size and quality
- Number of patches
- Number of simulation steps
- Discrete or continuous population models
- Population dispersal and interactions
- Environmental and population perturbations
- Saving simulation data
- Generating plots and network analyses
- Repeating simulations

The default configuration also supports generating sample spatial data before running a simulation.

## Outputs

Depending on the options enabled in `parameters.py`, the framework can save simulation data and analysis outputs such as:

- Population history data
- System-state data
- Patch and local-population data
- Network properties
- Distance metrics
- Pickled Python objects
- CSV files
- Plots and other visualisations

## Project Status

The supplied project archive contains the Python source files required by the framework, but it also imports `patch` and `simulation_utils`, which are not included in the supplied archive.

Those modules should be added from the original project source before expecting the complete framework to run successfully.

## Notes

The project is configured through Python parameter files rather than a separate configuration file. Changes to the experiment setup should therefore be made in the relevant parameter module before running the simulation.
