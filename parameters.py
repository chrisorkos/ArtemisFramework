from parameters_species_repository import *

# Meta parameters
meta_para = {
    "IS_NEW_PROGRAM": True,
    "REPEAT_PROGRAM_CODE": None,  # Simulation number to be repeated
    "REPEAT_PROGRAM_PATH": None,  # Output path of the simulation to be repeated
    "NUM_REPEATS": 1,  # Number of simulations to be executed with the current parameter set
    "IS_RUN_SAMPLE_SPATIAL_DATA_FIRST": True,  # Execute sample_spatial_data() before running the batch set?
}

# Master parameters
master_para = {
    "graph_para": {
        # Parameters for generating the spatial network files used in the simulation
        "SPATIAL_TEST_SET": 1,
        "SPATIAL_DESCRIPTION": "artemis_01",
        "GRAPH_TYPE": "lattice",  # Choices: "manual", "lattice", "line", etc.
        "ADJACENCY_MANUAL_SPEC": None,  # Use a list of lists to manually specify the patch adjacency matrix
        "LATTICE_GRAPH_CONNECTIVITY": 0.75,
        "IS_LATTICE_INCLUDE_DIAGONALS": False,
        "IS_LATTICE_WRAPPED": True,
        "RANDOM_GRAPH_CONNECTIVITY": None,
        "SMALL_WORLD_NUM_NEIGHBOURS": None,
        "SMALL_WORLD_SHORTCUT_PROBABILITY": None,
        "CLUSTER_NUM_NEIGHBOURS": None,
        "CLUSTER_PROBABILITY": None,
        "IS_HABITAT_PROBABILITY_REBALANCED": True,
        "HABITAT_TYPE_MANUAL_ALL_SPEC": None,
        "HABITAT_SPATIAL_AUTO_CORRELATION": -1.0,  # Range: [-1, 1]
        "HABITAT_TYPE_MANUAL_OVERWRITE": {0: 0, 200: 1},
        "PATCH_SIZE_MANUAL_SPEC": None,
        "MIN_SIZE": 1.0,
        "MAX_SIZE": 1.0,
        "QUALITY_TYPE": "gradient",  # Choices: 'manual', 'random', etc.
        "QUALITY_MANUAL_SPEC": None,
        "QUALITY_SPATIAL_AUTO_CORRELATION": 1.0,
        "MIN_QUALITY": 1.0,
        "MAX_QUALITY": 1.0,
        "QUALITY_FLUCTUATION": 0.0,
        "QUALITY_AXIS": "x+y",  # Choices: 'x', 'y', 'x+y'
        "IS_ENVIRONMENT_NATURAL_RESTORATION": False,
        "RESTORATION_PARA": {
            "IS_QUALITY_CHANGE": False,
            "QUALITY_CHANGE_PROBABILITY": None,
            "QUALITY_CHANGE_SCALE": None,  # Range: (0, 1]
            "QUALITY_DESIRED": None,
            "IS_HABITAT_CHANGE": False,
            "HABITAT_CHANGE_PROBABILITY": None,
            "HABITAT_TYPE_NUM_DESIRED": None,
        },
    },
    "main_para": {
        # Control parameters
        "IS_SIMULATION": True,
        "NUM_TRANSIENT_STEPS": 10000,
        "NUM_RECORD_STEPS": 1000,
        "NUM_PATCHES": 400,
        "MODEL_TIME_TYPE": "discrete",  # Choices: 'continuous', 'discrete'
        "EULER_STEP": 0.1,  # Only used if continuous
        "STEPS_TO_DAYS": 1,
        "ECO_PRIORITIES": {
            0: {'foraging', 'direct_impact', 'growth', 'dispersal'},
            1: {},
            2: {},
            3: {},
        },
        "MAX_CENTRALITY_MEASURE": 10,
        "ASSUMED_MAX_PATH_LENGTH": 3,
        "IS_SAVE_ADJ_VARIABLES": False,
        "IS_LOAD_ADJ_VARIABLES": False,

        # Generation data - set before spatial habitat generation
        "SPECIES_TYPES": {
            0: "prey",
            1: "predator_one",
            2: "predator_two",
        },
        "HABITAT_TYPES": {
            0: 'habitat_type_0',
            1: 'habitat_type_1',
        },
        "GENERATED_SPEC": {
            "FEEDING": {
                "IS_SPECIES_SCORES_SPECIFIED": True,
                "MIN_SCORE": None,
                "MAX_SCORE": None,
                "HABITAT_SCORES": {
                    0: [0.8, 0.4, 0.4],
                    1: [0.4, 0.8, 0.8],
                },
            },
            "TRAVERSAL": {
                "IS_SPECIES_SCORES_SPECIFIED": True,
                "MIN_SCORE": None,
                "MAX_SCORE": None,
                "HABITAT_SCORES": {
                    0: [1.0, 1.0, 1.0],
                    1: [1.0, 1.0, 1.0],
                },
            },
        },

        # Initial choice of species and habitats
        "INITIAL_SPECIES_SET": {0, 1, 2},
        "INITIAL_HABITAT_SET": {0, 1},
        "INITIAL_HABITAT_BASE_PROBABILITIES": None,
        "IS_CALCULATE_HURST": False,
        "IS_RECORD_METRICS_LM_VECTORS": False,
    },
    "plot_save_para": {
        "IS_ALLOW_FILE_CREATION": True,
        "IS_SUB_FOLDERS": False,
        "SUB_FOLDER_CAPACITY": 3,
        "IS_PRINT_KEY_OUTPUTS_TO_CONSOLE": True,
        "IS_PRINT_DISTANCE_METRICS_TO_CONSOLE": True,
        "IS_SAVE": True,
        "IS_PLOT": True,
        "IS_PLOT_DISTANCE_METRICS_LM": False,
        "PLOT_INIT_NETWORK": True,
        "MANUAL_SPATIAL_NETWORK_SAVE_STEPS": [],
        "IS_SAVE_LOCAL_POP_HISTORY_CSV": True,
        "IS_SAVE_SYSTEM_STATE_DATA": True,
        "IS_SAVE_PATCH_DATA": False,
        "IS_SAVE_PATCH_LOCAL_POP_DATA": False,
        "IS_ODE_RECORDINGS": False,
        "IS_SAVE_DISTANCE_METRICS": False,
    },
}

# Execute the simulation with the parameters
if __name__ == "__main__":
    # Place your simulation execution code here
    pass

