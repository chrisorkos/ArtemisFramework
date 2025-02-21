import shutil
import numpy as np
import os
import networkx as nx  # Import NetworkX with alias 'nx'


# ----------------------------- FOLDER PREPARATION ----------------------- #

def save_array(file, array):
    """Save a numpy array to a CSV file."""
    with open(file, mode='w') as f:
        np.savetxt(f, array, delimiter=', ', newline='\n', fmt='%.20f')

def check_and_create_directory(test_set, dir_path, can_overwrite_existing_dataset):
    """Check if a directory exists and create it if needed. Optionally overwrite existing directory."""
    if os.path.exists(dir_path):
        if not can_overwrite_existing_dataset:
            raise Exception("This spatial dataset already exists.")
        else:
            # Overwrite: delete the existing directory then re-create a fresh empty directory
            print(f"Test set {test_set} already existed - deleting previous files and clearing directory.")
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)
    else:
        os.makedirs(dir_path)

def create_description_file(desc, dir_path):
    """Create a description file in the specified directory."""
    with open(file=f'{dir_path}/description.txt', mode='w') as f:
        f.write(desc)


# ----------------------------- CONSTRUCTING THE SPATIAL NETWORK ----------------------- #

def generate_patch_position_adjacency(num_patches, graph_para):
    """Generate positions and adjacency matrix for patches."""
    num_rows = int(np.ceil(np.sqrt(num_patches)))
    num_columns = int(np.ceil(num_patches / num_rows))
    position_array = np.zeros([num_patches, 2])
    
    for patch in range(num_patches):
        x = np.mod(patch, num_columns)
        y = np.floor(patch / num_columns)
        position_array[patch, 0] = x
        position_array[patch, 1] = y

    graph_type = graph_para["GRAPH_TYPE"]
    adjacency_array = np.zeros([num_patches, num_patches])
    adjacency_spec = graph_para.get("ADJACENCY_MANUAL_SPEC", None)
    
    if graph_type == "manual":
        # Check and use manual adjacency specification
        if adjacency_spec is not None and isinstance(adjacency_spec, list) and len(adjacency_spec) == num_patches:
            for x in range(num_patches):
                if isinstance(adjacency_spec[x], list) and len(adjacency_spec[x]) == num_patches:
                    for y in range(num_patches):
                        if adjacency_spec[x][y] not in [0, 1]:
                            raise Exception("Values should only be '0' or '1'.")
                        if adjacency_spec[x][y] != adjacency_spec[y][x]:
                            raise Exception("Matrix is not symmetric.")
                else:
                    raise Exception(f"Row {x} is not a list with the correct number of columns.")
                if adjacency_spec[x][x] != 1:
                    raise Exception("Diagonals should all be 1 unless the patch is removed.")
            adjacency_array = np.asarray(adjacency_spec)
        else:
            raise Exception("Incorrect number of rows or invalid format.")
    else:
        # Check if user mistakenly provided manual adjacency while graph type is not 'manual'
        if adjacency_spec is not None and isinstance(adjacency_spec, list):
            raise Exception("Check that graph type is `manual' or clear the manual adjacency specification.")
        
        # Generate adjacency matrix based on graph type
        if graph_type == "lattice":
            for x in range(num_patches):
                for y in range(num_patches):
                    is_suitable = False
                    if graph_para["IS_LATTICE_INCLUDE_DIAGONALS"]:
                        test_distance = 1.999
                    else:
                        test_distance = 1.001

                    if np.linalg.norm(np.array([position_array[x, 0] - position_array[y, 0],
                                                position_array[x, 1] - position_array[y, 1]])) < test_distance:
                        is_suitable = True

                    if graph_para["IS_LATTICE_WRAPPED"]:
                        min_x_dist = num_columns
                        min_y_dist = num_rows
                        if position_array[x, 0] == num_columns - 1:
                            patch_x_x_possible = [position_array[x, 0], -1]
                        else:
                            patch_x_x_possible = [position_array[x, 0]]
                        if position_array[y, 0] == num_columns - 1:
                            patch_y_x_possible = [position_array[y, 0], -1]
                        else:
                            patch_y_x_possible = [position_array[y, 0]]
                        if position_array[x, 1] == num_rows - 1:
                            patch_x_y_possible = [position_array[x, 1], -1]
                        else:
                            patch_x_y_possible = [position_array[x, 1]]
                        if position_array[y, 1] == num_rows - 1:
                            patch_y_y_possible = [position_array[y, 1], -1]
                        else:
                            patch_y_y_possible = [position_array[y, 1]]
                        for patch_x_x in patch_x_x_possible:
                            for patch_y_x in patch_y_x_possible:
                                min_x_dist = min(min_x_dist, np.abs(patch_x_x - patch_y_x))
                        for patch_x_y in patch_x_y_possible:
                            for patch_y_y in patch_y_y_possible:
                                min_y_dist = min(min_y_dist, np.abs(patch_x_y - patch_y_y))
                        if np.linalg.norm(np.array([min_x_dist, min_y_dist])) < test_distance:
                            is_suitable = True

                    if is_suitable:
                        draw = np.random.binomial(n=1, p=graph_para["LATTICE_GRAPH_CONNECTIVITY"])
                        adjacency_array[x, y] = draw
                        adjacency_array[y, x] = draw
        elif graph_type == "line":
            for x in range(num_patches):
                if x > 0:
                    adjacency_array[x - 1, x] = 1
                if x < num_patches - 1:
                    adjacency_array[x, x + 1] = 1
        elif graph_type == "star":
            for x in range(num_patches):
                adjacency_array[x, 0] = 1
                adjacency_array[0, x] = 1
        elif graph_type == "random":
            for x in range(num_patches):
                for y in range(x):
                    draw = np.random.binomial(n=1, p=graph_para["RANDOM_GRAPH_CONNECTIVITY"])
                    adjacency_array[x, y] = draw
                    adjacency_array[y, x] = draw
        elif graph_type == "small_world":
            graph = nx.watts_strogatz_graph(n=num_patches,
                                            k=graph_para["SMALL_WORLD_NUM_NEIGHBOURS"],
                                            p=graph_para["SMALL_WORLD_SHORTCUT_PROBABILITY"])
            adjacency_array = nx.to_numpy_array(graph)
            if len(graph.nodes) == 0:
                raise Exception("Small World graph failed to generate - probably unsuitable number of neighbours.")
        elif graph_type == "scale_free":
            graph = nx.scale_free_graph(n=num_patches)
            adjacency_array = nx.to_numpy_array(nx.to_undirected(graph))
            adjacency_array[adjacency_array > 1] = 1
        elif graph_type == "cluster":
            graph = nx.powerlaw_cluster_graph(n=num_patches,
                                              m=graph_para["CLUSTER_NUM_NEIGHBOURS"],
                                              p=graph_para["CLUSTER_PROBABILITY"])
            adjacency_array = nx.to_numpy_array(graph)
        else:
            raise Exception("Unknown graph type specified.")
    
    if adjacency_array.shape[0] != num_patches or adjacency_array.shape[1] != num_patches:
        raise Exception("Graph generation process has failed to produce adjacency array of size NxN.")
    else:
        for x in range(num_patches):
            adjacency_array[x, x] = 1
        adjacency_array = np.maximum(adjacency_array, adjacency_array.T)
    
    return adjacency_array, position_array

def generate_patch_quality(num_patches, adjacency_array, position_array, graph_para):
    """Generate the quality of each patch."""
    quality_type = graph_para["QUALITY_TYPE"]
    max_quality = graph_para["MAX_QUALITY"]
    min_quality = graph_para["MIN_QUALITY"]
    if max_quality < min_quality or max_quality > 1.0 or min_quality < 0.0:
        raise Exception("Max and min quality parameters must be in [0, 1].")
    
    if quality_type == "manual":
        quality_spec = graph_para["QUALITY_MANUAL_SPEC"]
        if quality_spec is not None and isinstance(quality_spec, list) and len(quality_spec) == num_patches:
            quality_array = np.zeros(shape=(num_patches, 1))
            for patch_num in range(num_patches):
                patch_quality = quality_spec[patch_num]
                if 0.0 <= patch_quality <= 1.0:
                    quality_array[patch_num] = patch_quality
                else:
                    raise Exception("Invalid patch quality specified.")
        else:
            raise Exception("Invalid manual specification for patch quality.")
    elif quality_type == "random":
        quality_array = min_quality + np.random.rand(num_patches, 1) * (max_quality - min_quality)
    elif quality_type == "auto_correlation":
        auto_correlation = graph_para["QUALITY_SPATIAL_AUTO_CORRELATION"]
        quality_array = np.zeros(shape=(num_patches, 1))
        quality_array[0, 0] = np.random.rand()
        for x in range(1, num_patches):
            quality_array[x, 0] = auto_correlation * quality_array[x - 1] + (1 - auto_correlation) * np.random.rand()
    else:
        raise Exception("Unknown quality type specified.")
    
    return quality_array

def save_graph_and_quality(num_patches, adjacency_array, position_array, quality_array, graph_para):
    """Save the graph and quality data."""
    graph_type = graph_para["GRAPH_TYPE"]
    save_array(f"{graph_para['FOLDER_PATH']}/adjacency_array.csv", adjacency_array)
    save_array(f"{graph_para['FOLDER_PATH']}/position_array.csv", position_array)
    save_array(f"{graph_para['FOLDER_PATH']}/quality_array.csv", quality_array)
    create_description_file(f"Graph type: {graph_type}\nQuality type: {graph_para['QUALITY_TYPE']}", graph_para['FOLDER_PATH'])


# ----------------------------- EXECUTE ----------------------- #

def execute_network(graph_para, can_overwrite_existing_dataset=False):
    """Main function to execute network graph generation and saving."""
    num_patches = graph_para["NUM_PATCHES"]
    dir_path = graph_para["FOLDER_PATH"]
    
    check_and_create_directory("Spatial Network", dir_path, can_overwrite_existing_dataset)
    
    adjacency_array, position_array = generate_patch_position_adjacency(num_patches, graph_para)
    quality_array = generate_patch_quality(num_patches, adjacency_array, position_array, graph_para)
    
    save_graph_and_quality(num_patches, adjacency_array, position_array, quality_array, graph_para)


# Example configuration
graph_parameters = {
    "NUM_PATCHES": 100,
    "GRAPH_TYPE": "lattice",
    "LATTICE_GRAPH_CONNECTIVITY": 0.3,
    "IS_LATTICE_INCLUDE_DIAGONALS": True,
    "IS_LATTICE_WRAPPED": True,
    "QUALITY_TYPE": "random",
    "MAX_QUALITY": 1.0,
    "MIN_QUALITY": 0.0,
    "FOLDER_PATH": "network_data",
}

execute_network(graph_parameters, can_overwrite_existing_dataset=True)

