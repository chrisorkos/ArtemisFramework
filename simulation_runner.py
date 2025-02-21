#!/usr/bin/env python3

import random
import numpy as np
from datetime import datetime
import importlib
import sys

from simulation_obj import Simulation_obj
from data_manager_functions import plot_network_properties, create_adjacency_path_list, save_network_properties
from data_manager import load_json
from sample_spatial_data import run_sample_spatial_data

# --------------------------------- MAIN PROGRAMS --------------------------------- #

def new_program(master_para, parameters_basename):
    """Start a new simulation with fresh parameters."""
    print("\nBeginning a fresh simulation.")
    
    # Initialize random seeds
    np_seed = np.random.randint(4294967296)
    random_seed = np.random.randint(4294967296)
    np.random.seed(np_seed)
    random.seed(random_seed)
    
    # Metadata for the simulation
    metadata = {
        "numpy_seed": np_seed,
        "random_seed": random_seed,
        "program_start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # Run the program
    call_program(parameters=master_para, metadata=metadata, parameters_basename=parameters_basename)

def repeat_program(parameters_basename, sim_number, sim_path):
    """Repeat an existing simulation based on previously saved parameters."""
    print(f"\nRepeating simulation: {sim_number}.")
    
    # Load parameters and metadata
    loaded_parameters = load_json(f"{sim_path}/parameters.json")
    loaded_metadata = load_json(f"{sim_path}/metadata.json")
    
    # Restore seeds
    np.random.seed(loaded_metadata["numpy_seed"])
    random.seed(loaded_metadata["random_seed"])
    
    # Update metadata
    loaded_metadata["Copy of simulation"] = sim_number
    
    # Run the program
    call_program(parameters=loaded_parameters, metadata=loaded_metadata, parameters_basename=parameters_basename)

def call_program(parameters, metadata, parameters_basename):
    """Initialize and run the simulation."""
    simulation_obj = Simulation_obj(parameters=parameters, metadata=metadata,
                                    parameters_filename=parameters_basename + ".py")
    
    # Plot network properties if enabled
    if parameters["plot_save_para"]["IS_ALLOW_FILE_CREATION"] and parameters["plot_save_para"]["PLOT_INIT_NETWORK"]:
        adjacency_path_list = create_adjacency_path_list(
            patch_list=simulation_obj.system_state.patch_list,
            patch_adjacency_matrix=simulation_obj.system_state.patch_adjacency_matrix
        )
        
        plot_network_properties(
            patch_list=simulation_obj.system_state.patch_list,
            sim_path=simulation_obj.sim_path,
            step="initial_network",
            adjacency_path_list=adjacency_path_list,
            is_biodiversity=False,
            is_reserves=True,
            is_label_habitat_patches=False,
            is_retro=False
        )
        
        if parameters["plot_save_para"]["IS_SAVE"]:
            save_network_properties(
                system_state=simulation_obj.system_state,
                sim_path=simulation_obj.sim_path,
                step="initial_network"
            )
    
    # Run the full simulation if enabled
    if parameters["main_para"]["IS_SIMULATION"]:
        simulation_obj.full_simulation()

# --------------------------------- EXECUTE --------------------------------- #

def execution():
    """Main execution function."""
    if len(sys.argv) > 1:
        # Optionally pass in an argument specifying the parameters file to use
        parameters_basename = sys.argv[1]
    else:
        # Default parameters file
        parameters_basename = "parameters"
    
    # Import and reload parameters file
    parameters_file = importlib.import_module(parameters_basename)
    importlib.reload(parameters_file)

    master_para = getattr(parameters_file, "master_para")
    meta_para = getattr(parameters_file, "meta_para")
    
    if meta_para.get("IS_RUN_SAMPLE_SPATIAL_DATA_FIRST", False):
        run_sample_spatial_data(parameters=master_para, is_output_files=True)
    
    num_repeats = meta_para.get("NUM_REPEATS", 1)

    for simulation in range(num_repeats):
        if meta_para.get("IS_NEW_PROGRAM", True):
            new_program(master_para=master_para, parameters_basename=parameters_basename)
        else:
            repeat_program(
                parameters_basename=parameters_basename,
                sim_number=meta_para.get("REPEAT_PROGRAM_CODE", 0),
                sim_path=meta_para.get("REPEAT_PROGRAM_PATH", "")
            )

if __name__ == '__main__':
    execution()

