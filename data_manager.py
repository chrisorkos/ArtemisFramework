import os
import shutil
import numpy as np
import sys
from datetime import datetime
from data_manager_functions import dump_json, load_json, update_local_population_nets
from simulation_utils import write_parameters_file, write_metadata_file, write_average_population_data
from simulation_utils import write_perturbation_history_data, global_species_time_series_properties
from simulation_utils import write_population_history_data, write_system_state

def generate_simulation_number(minimum=99, save_data=True, use_sub_folders=False, sub_folder_capacity=100):
    """
    Generates the next available simulation number and creates the necessary folder structure.
    """
    sim_path = 'results'
    sim_number = 100

    if use_sub_folders:
        current_parent_folder_num = 0
        while os.path.exists(f'results/par_{current_parent_folder_num + 1}'):
            current_parent_folder_num += 1
        
        folder_list = os.listdir(f'results/par_{current_parent_folder_num}')
        folder_list = [f for f in folder_list if not f.startswith('.')]  # exclude hidden files
        folder_int_list = list(map(int, folder_list))

        if folder_int_list:
            sim_number = max(folder_int_list) + 1
        else:
            sim_number = minimum + 1

        if len(folder_int_list) >= sub_folder_capacity:
            sim_path = f'results/par_{current_parent_folder_num + 1}/{sim_number}'
        else:
            sim_path = f'results/par_{current_parent_folder_num}/{sim_number}'
    else:
        sim_number = minimum + 1
        while os.path.exists(f'results/{sim_number}'):
            sim_number += 1
        sim_path = f'results/{sim_number}'

    if save_data:
        os.makedirs(sim_path)

    return sim_number, sim_path

def write_initial_files(parameters, metadata, sim_path, parameters_filename):
    """
    Writes the initial files including parameters and metadata.
    """
    try:
        parameters_file = os.path.join(sim_path, "parameters.json")
        dump_json(data=parameters, filename=parameters_file)

        metadata["write_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        metadata_file = os.path.join(sim_path, "metadata.json")
        dump_json(data=metadata, filename=metadata_file)

        shutil.copy(parameters_filename, sim_path)
        shutil.copy("parameters_species_repository.py", sim_path)
    except Exception as e:
        print(f"Error writing initial files: {e}")

def save_adj_variables(patch_list, spatial_set_number):
    """
    Saves patch-related variables to the appropriate directory.
    """
    base_dir = f'spatial_data_files/test_{spatial_set_number}/adj_variables/'

    for patch in patch_list:
        try:
            sms_file = os.path.join(base_dir, f'species_movement_scores/sms_{patch.number}.json')
            ssl_file = os.path.join(base_dir, f'stepping_stone_list/ssl_{patch.number}.json')
            al_file = os.path.join(base_dir, f'adjacency_list/al_{patch.number}.json')

            dump_json(data=patch.species_movement_scores, filename=sms_file)
            dump_json(data=patch.stepping_stone_list, filename=ssl_file)
            dump_json(data=patch.adjacency_lists, filename=al_file)
        except Exception as e:
            print(f"Error saving adjacency variables for patch {patch.number}: {e}")

def load_adj_variables(patch_list, spatial_set_number):
    """
    Loads patch-related variables from the appropriate directory.
    """
    base_dir = f'spatial_data_files/test_{spatial_set_number}/adj_variables/'

    for patch in patch_list:
        try:
            sms_file = os.path.join(base_dir, f'species_movement_scores/sms_{patch.number}.json')
            ssl_file = os.path.join(base_dir, f'stepping_stone_list/ssl_{patch.number}.json')
            al_file = os.path.join(base_dir, f'adjacency_list/al_{patch.number}.json')

            patch.species_movement_scores = load_json(input_file=sms_file)
            patch.stepping_stone_list = load_json(input_file=ssl_file)
            patch.adjacency_lists = load_json(input_file=al_file)
        except Exception as e:
            print(f"Error loading adjacency variables for patch {patch.number}: {e}")

def save_reserve_list(reserve_list, spatial_set_number):
    """
    Saves the reserve list to the appropriate directory.
    """
    file_path = f'spatial_data_files/test_{spatial_set_number}/reserve_list/reserve_list.json'
    try:
        dump_json(data=reserve_list, filename=file_path)
    except Exception as e:
        print(f"Error saving reserve list: {e}")

def load_reserve_list(spatial_set_number):
    """
    Loads the reserve list from the appropriate directory.
    """
    file_path = f'spatial_data_files/test_{spatial_set_number}/reserve_list/reserve_list.json'
    try:
        return load_json(input_file=file_path)
    except Exception as e:
        print(f"Error loading reserve list: {e}")
        return None

def print_key_outputs_to_console(simulation_obj):
    """
    Prints key simulation outputs to the console.
    """
    try:
        update_local_population_nets(system_state=simulation_obj.system_state)
        np.set_printoptions(threshold=sys.maxsize)

        print("\n******************** SIMULATION OUTPUTS: BEGIN ********************\n")
        print(f"Numpy seed: {simulation_obj.metadata['numpy_seed']}")
        print(f"Random seed: {simulation_obj.metadata['random_seed']}")

        print("\n********** SPATIAL NETWORK DESCRIPTION **********\n")
        print(f"{len(simulation_obj.system_state.patch_list)}, "
              f"{len(simulation_obj.system_state.habitat_type_dictionary)}")
        print(f"Habitat species traversal: {simulation_obj.system_state.habitat_species_traversal}")
        print(f"Habitat species feeding: {simulation_obj.system_state.habitat_species_feeding}")

        for habitat_num, habitat_history in simulation_obj.system_state.habitat_amounts_history.items():
            print(f"{habitat_num}: {habitat_history[-1]}")

        print("\n********** LOCAL POPULATION OUTPUTS **********\n")
        for patch in simulation_obj.system_state.patch_list:
            for local_population in patch.local_populations.values():
                output_str = (f"{simulation_obj.sim_number}, {patch.number}, {patch.habitat_type_num}, "
                              f"{local_population.name}, {local_population.occupancy}, {local_population.population}, "
                              f"{local_population.internal_change}, {local_population.population_enter}, "
                              f"{local_population.population_leave}, {local_population.source}, {local_population.sink}, "
                              f"{local_population.maximum_foraging_distance}, "
                              f"{local_population.weighted_foraging_distance}, "
                              f"{local_population.average_population}, {local_population.average_internal_change}, "
                              f"{local_population.average_population_enter}, {local_population.average_population_leave}, "
                              f"{local_population.average_source}, {local_population.average_sink}, "
                              f"{local_population.st_dev_population}, {local_population.max_abs_population}, "
                              f"{local_population.population_period_weak}, {local_population.population_period_med}, "
                              f"{local_population.population_period_strong}, "
                              f"{local_population.recent_occupancy_change_frequency};")
                print(output_str)

        if simulation_obj.parameters["plot_save_para"]["IS_PRINT_DISTANCE_METRICS_TO_CONSOLE"]:
            print("\n********** SPECIES AND DISTANCE METRIC OUTPUTS **********\n")
            print('{')
            for counter, (key, value) in enumerate(simulation_obj.system_state.distance_metrics_store.items()):
                output_str = (f'"METRIC_KEY_{key}": '
                              f'{json.dumps(value, ensure_ascii=True, default=set_default, skipkeys=True)}')
                is_final_item = (counter == len(simulation_obj.system_state.distance_metrics_store) - 1)
                print(format_dictionary_to_JSON_string(output_str, is_final_item=is_final_item, is_indenting=False))
            print('}')

        print("\n******************** SIMULATION OUTPUTS: END ********************\n")
        np.set_printoptions(threshold=1000)
    except Exception as e:
        print(f"Error printing simulation outputs: {e}")

def save_all_data(simulation_obj):
    """
    Saves all relevant data at the end of the simulation.
    """
    try:
        metadata = simulation_obj.metadata
        species_set = simulation_obj.system_state.species_set
        patch_list = simulation_obj.system_state.patch_list
        parameters = simulation_obj.parameters
        sim_path = simulation_obj.sim_path

        # Function calls to save various types of data
        write_parameters_file(parameters=parameters, sim_path=sim_path)
        write_metadata_file(metadata=metadata, sim_path=sim_path)
        write_average_population_data(species_set=species_set, sim_path=sim_path)
        write_perturbation_history_data(system_state=simulation_obj.system_state, sim_path=sim_path)
        global_species_time_series_properties(system_state=simulation_obj.system_state, sim_path=sim_path)
        write_population_history_data(system_state=simulation_obj.system_state, sim_path=sim_path)
        write_system_state(system_state=simulation_obj.system_state, sim_path=sim_path)
    except Exception as e:
        print(f"Error saving all data: {e}")

