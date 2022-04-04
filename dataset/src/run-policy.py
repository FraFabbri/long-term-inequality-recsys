

### STEPS
###
### 0. LOADDATASET AS IGRAPH OBJECT
### 1. GENERATE alpha-SAMPLE OF NODES FOR EACH ITERATION 
### 2. GENERATE ACCEPTED NODES BY SELECTED POLICY FOR EACH ITERATION ###
### 3. RUN SIMULATIONS


# HOW-TO-RUN
# *policy* possible values: ["random", "fc", "lazy"]
# *algoname* possible values: ["random", "ada", "als", "salsa"]
# python3 run-policy.py -nomedataset -alpha -numero_iterazioni -policy -algoname



import igraph
import numpy as np
import pickle
import os
import sys

from numpy.random import choice
from numpy.random import uniform
#from config import name_datasets
from config import mapping_dataset_attribute
from config import top_k
#from config import iterations
#from config import alpha

from policies import *

from utils import *

from recsys import RecSysAlgorithms



input_dataset = sys.argv[1]

alpha = int(sys.argv[2])

iterations = int(sys.argv[3])


policy = sys.argv[4] # possible values: "random", "fc", "lazy"

algoname = sys.argv[5] # possible values: ["random", "ada", "als", "salsa"]




policies_mappings = {
    "random": inizialization_prob_RandomPolicy, 
    
    "lazy": inizialization_prob_LazyPolicy,
    
    "fc": inizialization_prob_FlipCoinPolicy
}




if policy not in policies_mappings:

    raise Exception("MARIA LUISA CHE CAZZO FAI?") 

else:

    inizialization_prob_policy =  policies_mappings[policy]


if algoname not in ["random", "ada", "als", "salsa"]:

    raise Exception("MARIA LUISA CHE CAZZO FAI?") 



attribute = mapping_dataset_attribute[input_dataset]

history_topk = {}
#history_dic_prob = {}

print("Code running for ", input_dataset, algoname, policy)

foldername = input_dataset

if foldername not in os.listdir("../out/"):
    os.mkdir("../out/" + foldername)

foldername_iteration_sampling = foldername + "_it" + str(iterations) + "_sampling" + str(alpha) + "_policy-" + policy + "_algoname-" + algoname

if foldername_iteration_sampling not in os.listdir("../out/" + foldername):
    os.mkdir("../out/" + foldername + "/" + foldername_iteration_sampling)

outpath_ = "../out/" + foldername + "/" + foldername_iteration_sampling + "/"


# 0. LOAD DATASET AS IGRAPH OBJECT
graph = return_igraph_object(input_dataset, attribute)
print("Graph loaded")

#return bipartite graph
bi_partite_graph = return_bi_partite_graph(graph, attribute)
print("Graph converted in bipartite graph")

N = bi_partite_graph.vcount()

# inizializing temporal information
for e in bi_partite_graph.es:
    e["time"] = 0


print("Run simulations")

# set of skipped recommendations 
to_skip = set()

# 1. GENERATE alpha-SAMPLE OF NODES FOR EACH ITERATION 
print("Generating samples nodes alpha")
mapping_sample_alpha = inizialization_sample_nodes(iterations, N, alpha)

### 2. GENERATE ACCEPTED NODES BY SELECTED POLICY FOR EACH ITERATION ###
print("Generating probabilities for a priori sampling - %s"%policy)
mapping_iterations_and_nodes = inizialization_prob_policy(iterations, mapping_sample_alpha, top_k)



#print first-summary
print(bi_partite_graph.summary())


### 3. RUN SIMULATIONS

all_edges_old = set()

for one_iter in range(iterations):

    print("----------------")
    print("iterazione ", one_iter)

    #estrai nodi a distanza 2
    print("extract nodes at distance 2")
    dict_nodes_at_dist2 = find_nodes_at_distance_2(bi_partite_graph, mapping_sample_alpha, one_iter)

    #print("numero nodi sorgente in dict_nodes_at_dist2: ", len(dict_nodes_at_dist2) , " - ", len(dict_nodes_at_dist2)*100/N, "%")


    selected_attribute = "color"
    new_instance = RecSysAlgorithms(bi_partite_graph,
                                    algoname,
                                    selected_attribute,
                                    dict_nodes_at_dist2
                                   )





    # dictionary with recommendations filter_by_top_k source_node: position: destination_node
    print("generate recommendations")
    filter_by_top_k = new_instance.STEP1_compute_One4All(algoname, to_skip, top_k)


    #### flip coin policy - senza raccomandare gli scartati #####


    print("apply the policy")



    bi_partite_graph, small_to_skip = get_policy_update(bi_partite_graph, filter_by_top_k, mapping_iterations_and_nodes, mapping_sample_alpha, one_iter)

    save_info(outpath_, filter_by_top_k, mapping_sample_alpha, one_iter, N, policy, algoname)

    to_skip = to_skip.union(small_to_skip)


with open(outpath_ + "final-graph.p", "wb") as f:
    pickle.dump(bi_partite_graph, f)

