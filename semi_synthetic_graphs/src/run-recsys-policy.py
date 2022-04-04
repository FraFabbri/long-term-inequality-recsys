 
### improvements
### 1. get the graph as input, don't need to generate it in the nested-for
## 2. aggiornare grafo con edge temporali


import igraph
import numpy as np
import pickle
import os
import sys

from numpy.random import choice
from config import top_k
from config import iterations
from config import alpha
from config import vec_h_min_star, vec_s_min_star, vec_h_maj_star
from config import vec_e_rr

from policies import get_policy_update
from policies import inizialization_prob_FlipCoinPolicy
from policies import inizialization_prob_RandomPolicy
from policies import inizialization_prob_LazyPolicy
from policies import inizialization_sample_nodes

from utils import find_nodes_at_distance_2
from utils import save_info

from recsys import RecSysAlgorithms




#policy = sys.argv[1] # random, fc, lazy
policy = "fc"

#algoname = sys.argv[2] # random, adam, als, salsa

vec_algoname = ["als", "salsa"]


policies_mappings = {
    "random": inizialization_prob_RandomPolicy, 
    
    "lazy": inizialization_prob_LazyPolicy,
    
    "fc": inizialization_prob_FlipCoinPolicy
}

if policy not in policies_mappings:

    raise Exception("MARIA LUISA CHE CAZZO FAI?") 

else:

    inizialization_prob_policy =  policies_mappings[policy]


for algoname in vec_algoname:


    if algoname not in ["random", "ada", "als", "salsa"]:

        raise Exception("MARIA LUISA CHE CAZZO FAI?")



    all_graphs = []

    for h_min_star in vec_h_min_star:
    
        for h_maj_star in vec_h_maj_star:

            for s_min_star in vec_s_min_star:

                all_graphs += [x for x in os.listdir("../data/synth/") if "s_m" + str(s_min_star) in x and "hm" + str(h_min_star) in x and "hM" + str(h_maj_star) in x]


    print(all_graphs)
    
   


    history_topk = {}
    #history_dic_prob = {}
    for selected_graph in all_graphs:

        print("Code running for ", selected_graph, algoname, policy)


        config_simulation = ["sim" + str(iterations), "topk" + str(top_k), selected_graph.replace(".p", "")]
        foldername = "-".join(config_simulation)

        if foldername not in os.listdir("../out/synth/"):
            os.mkdir("../out/synth/" + foldername)


        inner_folder = "policy-" + policy + "_algoname-" + algoname

        if inner_folder not in os.listdir("../out/synth/" + foldername + "/"):
            os.mkdir("../out/synth/" + foldername + "/" + inner_folder)

        outpath_ = "../out/synth/" + foldername + "/" + inner_folder + "/"

        # loading graph
        print("Load starting graph")
        print(selected_graph)
        with open("../data/synth/" + selected_graph, "rb") as f:
            bi_partite_graph = pickle.load(f)

        N = bi_partite_graph.vcount()

        # inizializing temporal information
        for e in bi_partite_graph.es:
            e["time"] = 0


        print("Run simulations")

        # set of skipped recommendations 
        to_skip = set()

        #generate sample of nodes for each iterations
        print("Generating samples nodes alpha")
        mapping_sample_alpha = inizialization_sample_nodes(iterations, N, alpha)

        # generate probabilities for extracting nodes from each list
        print("Generating probabilities for a priori sampling")
        mapping_iterations_and_nodes = inizialization_prob_policy(iterations, mapping_sample_alpha, top_k)



        #print(mapping_iterations_and_nodes)
        # top_k and iterations already imported

        #print first-summary
        print(bi_partite_graph.summary())

        all_edges_old = set()

        for one_iter in range(iterations):

            print("----------------")
            print("iterazione ", one_iter)

            #estrai nodi a distanza 2
            dict_nodes_at_dist2 = find_nodes_at_distance_2(bi_partite_graph, mapping_sample_alpha, one_iter)


            selected_attribute = "color"
            new_instance = RecSysAlgorithms(bi_partite_graph,
                                            algoname,
                                            selected_attribute,
                                            dict_nodes_at_dist2
                                           )

            # dictionary with recommendations
            print("generate recommendation")
            filter_by_top_k = new_instance.STEP1_compute_One4All(algoname, to_skip, top_k)


            #### flip coin policy - senza raccomandare gli scartati #####


            print("apply the policy")



            bi_partite_graph, small_to_skip = get_policy_update(bi_partite_graph, filter_by_top_k, mapping_iterations_and_nodes, mapping_sample_alpha, one_iter)

            save_info(outpath_, filter_by_top_k, mapping_sample_alpha, one_iter, N, policy, algoname)

            to_skip = to_skip.union(small_to_skip)


        with open(outpath_ + "final-graph.p", "wb") as f:
            pickle.dump(bi_partite_graph, f)

