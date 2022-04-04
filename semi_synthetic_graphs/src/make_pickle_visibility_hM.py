

import pickle
import numpy as np
import os
import operator
import sys
#from config import alpha
from config import iterations

#from config import vec_h_min_star, vec_h_maj_star, vec_s_min_star

sys.path.insert(0, '../../')


from plot.plot_utils import mapping_colors_function

vec_h_min = [0.5, 0.6, 0.7]
vec_h_maj = [0.1, 0.2, 0.3]

policy = "fc" # random, fc, lazy

vec_algoname = ["als", "salsa", "ada", "random"]

directory_out = "../out/synth/"

#all_folder_data = [x for x in os.listdir(directory_out) if "TUENTI-A16" in x]

all_folder_data = []

for hm in vec_h_min:
    
    for hM in vec_h_maj:
                            
        all_folder_data += [x for x in os.listdir(directory_out) if "hm" + str(hm) in x and "hM" + str(hM) in x]
        

for algoname in vec_algoname:        
        
    inner_folder = "policy-" + policy + "_algoname-" + algoname

    for folder_data in all_folder_data:

        print(folder_data)



        with open(directory_out + folder_data + "/" + inner_folder + "/final-graph.p", "rb") as f:
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

            with open(directory_out + folder_data +  "/" + inner_folder + "/" + policy + "-" + algoname + "-" + str(n_iter) + ".p", "rb") as f:
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


        with open(directory_out + folder_data + "/" + inner_folder + "/track_visibility_all_combination_color.p", "wb") as f:
            pickle.dump(track_visibility_all_combination_color, f)

        with open(directory_out + folder_data + "/" + inner_folder + "/track_visibility.p", "wb") as f:
            pickle.dump(track_visibility, f)

        with open(directory_out + folder_data + "/" + inner_folder + "/track_visibility_node.p", "wb") as f:
            pickle.dump(track_visibility_node, f)

