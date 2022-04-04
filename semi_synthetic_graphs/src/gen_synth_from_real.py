

import igraph
import os
import pickle

from functions_synth_from_real import change_sizes
from functions_synth_from_real import change_homophilies

from utils import *

from config import *


for dataset in vec_dataset:
    
    for h_maj_star in vec_h_maj_star:
        
        for h_min_star in vec_h_min_star:
            
            for s_min_star in vec_s_min_star:

                print("------ \n")
                print("Configuration Dataset:", dataset, "s_min", s_min_star, "h_min_star:", h_min_star, "h_maj_star:", h_maj_star)

                attribute = mapping_dataset_attribute[dataset]

                print("loading graph...")

                graph = return_igraph_object(dataset = dataset, attribute = attribute, generate_pajek = False)

                graph = return_bi_partite_graph(graph, attribute)

                graph = change_sizes(graph = graph, attribute = attribute, s_min_star = s_min_star)

                graph = change_homophilies(graph = graph, h_min_star = h_min_star, h_maj_star = h_maj_star)


                config_graph = (str(dataset), 
                                "s_m" + str(s_min_star),
                                "hm" + str(h_min_star), 
                                "hM" + str(h_maj_star))

                graphname = "-".join(config_graph)

                foldername = "../data/synth/"

                with open(foldername + graphname + ".p", "wb") as f:
                    pickle.dump(graph, f)

