import numpy as np

class Patch:

    def __init__(
            self,
            position=None,  # co-ordinates of the bottom-left corner of the patch square
            patch_number=0,
            patch_quality=0.0,
            patch_size=0.0,
            habitat_type=None,
            habitat_type_num=0,
    ):
        # Set default value for position if none is provided
        if position is None:
            position = np.zeros([2, 1])
        
        self.number = patch_number
        self.local_populations = {}  # Initialize as an empty dictionary
        self.habitat_type = habitat_type
        self.habitat_type_num = habitat_type_num
        self.quality = patch_quality
        self.size = patch_size
        self.degree = 0  # can change
        self.centrality = 0.0  # can change
        self.local_clustering = []  # can change, takes a list of three values - LCC for all/same/different habitats
        self.position = position  # cannot change
        self.adjacency_lists = {}  # to reduce computational waste
        self.sum_competing_for_resources = 0.0
        self.set_of_adjacent_patches = set()
        self.set_of_xy_adjacent_patches = set()
        self.this_habitat_species_feeding = {}
        self.this_habitat_species_traversal = {}
        self.stepping_stone_list = []
        self.biodiversity = 0.0
        self.is_reserve = 0  # set to 1 if is a reserve
        self.reserve_order = []  # empty list if not a reserve, otherwise [cluster_num, patch_num_within_cluster]
        self.num_times_perturbed = 0  # add 1 every time this patch is chosen to be subject to a perturbation
        self.num_times_meaningfully_perturbed = 0  # only count net change in population due to dispersal events etc.
        self.latest_perturbation_code = 0.1  # helps with visualisation of perturbation histories
        #
        # History dictionaries - update (with step as key) if changed by a patch perturbation
        self.habitat_history = {0: habitat_type_num}
        self.quality_history = {0: patch_quality}
        self.size_history = {0: patch_size}
        self.removal_history = {}
        self.degree_history = {}
        self.set_of_adjacent_patches_history = {}
        self.centrality_history = {}
        self.local_clustering_history = {}
        self.adjacency_history_list = []  # records multiple changes per step
        self.perturbation_history_list = []  # records multiple changes per step
        self.latest_perturbation_code_history = {}
        #
        # The largest object when printing to JSON:
        self.species_movement_scores = {}

    def update_biodiversity(self):
        """Update biodiversity based on local populations."""
        num_species_counted = 0
        for local_pop in self.local_populations.values():
            if local_pop.population > local_pop.species.minimum_population_size:
                num_species_counted += 1
        self.biodiversity = num_species_counted

    def increment_perturbation_count(self):
        """Increment the perturbation count."""
        self.num_times_perturbed += 1

    def increment_meaningful_perturbation_count(self):
        """Increment the meaningful perturbation count."""
        self.num_times_meaningfully_perturbed += 1

