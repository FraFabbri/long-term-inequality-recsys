

import pickle
import numpy as np
import os
import operator
import sys

sys.path.insert(0, '../../')


from plot.plot_utils import mapping_colors_function

directory_out = "../out/"

folder_data = sys.argv[1]



policy = sys.argv[2] # possible values: "random", "fc", "lazy"

algoname = sys.argv[3] # possible values: ["random", "ada", "als", "pagerank"]

alpha = 20

iterations = 20

foldername_iteration_sampling = folder_data + "_it" + str(iterations) + "_sampling" + str(alpha) + "_policy-" + policy + "_algoname-"  + algoname

with open(directory_out + folder_data + "/" + foldername_iteration_sampling + "/final-graph.p", "rb") as f:
    final_graph = pickle.load(f)

#print(final_graph.summary())

mapping_colors = mapping_colors_function(final_graph)



track_visibility_all_combination_color = {}
track_visibility = {}
track_visibility_node = {}




for idx, n_iter in enumerate(range(iterations)):
    
    print("iteration ", idx)
    print("--------")

    delta_combination = {("red", "red") : 0, ("red", "blue") : 0, ("blue", "red") : 0, ("blue", "blue") : 0}
    delta_visibility = {"red": 0, "blue": 0}
    visibility_node = dict.fromkeys(mapping_colors.keys(), 0)

    with open(directory_out + folder_data + "/" + foldername_iteration_sampling + "/" + policy + "-" + algoname + "-" + str(n_iter) + ".p", "rb") as f:
        recommended_nodes = pickle.load(f)

    for source in recommended_nodes:

        source_color = mapping_colors[source]

        for position in recommended_nodes[source]:

            destination = recommended_nodes[source][position]

            destination_color = mapping_colors[destination]

            delta_combination[source_color, destination_color] += 1

            delta_visibility[destination_color] += 1

            visibility_node[destination] += 1



    track_visibility_all_combination_color[n_iter] = delta_combination
    track_visibility[n_iter] = delta_visibility 
    track_visibility_node[n_iter] = visibility_node


with open(directory_out+ folder_data + "/"  + foldername_iteration_sampling+ "/track_visibility_all_combination_color.p", "wb") as f:
    pickle.dump(track_visibility_all_combination_color, f)

with open(directory_out + folder_data + "/" + foldername_iteration_sampling + "/track_visibility.p", "wb") as f:
    pickle.dump(track_visibility, f)

with open(directory_out + folder_data + "/" + foldername_iteration_sampling + "/track_visibility_node.p", "wb") as f:
    pickle.dump(track_visibility_node, f)

