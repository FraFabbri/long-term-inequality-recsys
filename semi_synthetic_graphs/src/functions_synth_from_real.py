
import igraph
import os
import csv
import sys
import numpy as np
from numpy.random import choice
from itertools import permutations
from random import shuffle

import random
from collections import Counter
from collections import defaultdict


from utils import return_igraph_object, return_bi_partite_graph, compute_homophily, compute_size
from utils import mapping_dataset_attribute


def change_sizes(graph, attribute, s_min_star = None):

    

    V_min, s_min = compute_size(graph, "minority")
    V_maj, s_maj = compute_size(graph, "majority")

    print("\n")
    print("initial sizes s_min:", s_min, "s_maj:", s_maj, "\n")

    print("initial homophilies h_m:", compute_homophily(graph, "minority"), "h_M:", compute_homophily(graph, "majority"))
    

    if s_min_star != None:

        num_nodes = graph.vcount()

        num_min_nodes = len(V_min)
        num_maj_nodes = len(V_maj)
        
        

        num_min_star_nodes = int(num_nodes*s_min_star)
        
        num_nodes_sample  = abs(num_min_star_nodes - num_min_nodes)

        if num_min_star_nodes > num_min_nodes:

            nodes_from_blue_to_red = np.random.choice(V_maj, num_nodes_sample, replace = False)

            nodes_from_blue_to_red = set(nodes_from_blue_to_red)

            V_min = set(V_min)

            V_maj = set(V_maj)

            V_maj.difference_update(nodes_from_blue_to_red)

            V_min.update(nodes_from_blue_to_red)


        if num_min_star_nodes < num_min_nodes:

            nodes_from_red_to_blue  = np.random.choice(V_min, num_nodes_sample, replace = False)

            nodes_from_red_to_blue = set(nodes_from_red_to_blue)

            V_min = set(V_min)

            V_maj = set(V_maj)

            V_min.difference_update(nodes_from_red_to_blue)

            V_maj.update(nodes_from_red_to_blue)


        """
        age: young--> minority; old --> majority
        gender: 1(female) --> minority; 2 (male) --> majority

        """

        for min_node in V_min:

            if attribute == "age":

                graph.vs[min_node][attribute] = "young"

            elif attribute == "gender":

                graph.vs[min_node][attribute] = "1"

            graph.vs[min_node]["selected_attribute"] = "minority"

            

        for maj_node in V_maj:

            if attribute == "age":

                graph.vs[maj_node][attribute] = "old"

            elif attribute == "gender":

                graph.vs[maj_node][attribute] = "2"

            graph.vs[maj_node]["selected_attribute"] = "majority"




        new_s_min = compute_size(graph, "minority")[1]
        new_s_maj = compute_size(graph, "majority")[1]

        print("\n")
        print("final sizes s*_min:", new_s_min, "s*_maj:", new_s_maj, "\n")

        print("final homophilies h_m:", compute_homophily(graph, "minority"), "h_M:", compute_homophily(graph, "majority"), "\n")
    
    print("\n")
    print(graph.summary())



    return graph



def change_homophilies(graph, h_min_star = None, h_maj_star = None):
    
    V_min, s_min = compute_size(graph, "minority")
    V_maj, s_maj = compute_size(graph, "majority")
    
    #print("s_min:", s_min, "s_maj:", s_maj)

    if h_min_star != None and (h_min_star > s_maj or h_min_star <= -s_min):
        print("\n")
        print("h*_min must be in range: (", -s_min,",", s_maj, "]")

    if h_maj_star != None and (h_maj_star > s_min or h_maj_star <= -s_maj):
        print("\n")
        print("h*_maj must be in range: (", -s_maj,",", s_min, "]")    
        
        
    nodes_attribute = {}

    for n in graph.vs:

        attribute = graph.vs[n.index]["selected_attribute"]

        nodes_attribute[n.index] = attribute


    edge_list = graph.get_edgelist()


    mapping_edges = {("minority", "minority"): [], 
                    ("minority", "majority"): [], 
                    ("majority", "majority"): [], 
                    ("majority", "minority"): []}
    
    for source, destination in edge_list:

        source_attribute = nodes_attribute[source]

        destination_attribute = nodes_attribute[destination]

        mapping_edges[source_attribute, destination_attribute].append((source, destination))

        
    print("\n")
    print("Computing starting homophilies")    

    h_min = compute_homophily(graph, "minority")
    h_maj = compute_homophily(graph, "majority")

    print("h_min:", h_min, "h_maj:", h_maj)
    
    
    if h_min_star != None and h_min_star <= s_maj and h_min_star > -s_min:

        print("\n")
        print("Changing h_m")

        E_mm =  len(mapping_edges["minority", "minority"])

        E_m = len(mapping_edges["minority", "minority"]) + len(mapping_edges["minority", "majority"])

        E_mm_star = int(E_m*(h_min_star + s_min))

        sample_min = abs(E_mm - E_mm_star)

        edges_min_to_remove = []

        edges_min_to_add = []


        if h_min > h_min_star:

            print("Rewiring", sample_min, "edges from E_mm to E_mM")

            sample_edge_idx = np.random.choice(len((mapping_edges["minority", "minority"])), sample_min, replace = False)

            sample_new_destinations = np.random.choice(V_maj, sample_min)

            for edge_idx, new_destination in zip(sample_edge_idx, sample_new_destinations):

                edges_min_to_remove.append(mapping_edges["minority", "minority"][edge_idx])

                edges_min_to_add.append((mapping_edges["minority", "minority"][edge_idx][0], new_destination))

        elif h_min < h_min_star:

            print("Rewiring", sample_min, "edges from E_mM to E_mm")

            sample_edge_idx = np.random.choice(len((mapping_edges["minority", "majority"])), sample_min, replace = False)

            sample_new_destinations = np.random.choice(V_min, sample_min)

            for edge_idx, new_destination in zip(sample_edge_idx, sample_new_destinations):

                edges_min_to_remove.append(mapping_edges["minority", "majority"][edge_idx])

                edges_min_to_add.append((mapping_edges["minority", "majority"][edge_idx][0], new_destination))

        graph.delete_edges(edges_min_to_remove)
        #print(graph.summary())

        graph.add_edges(edges_min_to_add)
        #print(graph.summary())





    if h_maj_star != None and h_maj_star <= s_min and h_maj_star > -s_maj:

        print("\n")
        print("Changing h_M")

        E_MM = len(mapping_edges["majority", "majority"])

        E_M = len(mapping_edges["majority", "majority"]) + len(mapping_edges["majority", "minority"])

        E_MM_star = int(E_M*(h_maj_star + s_maj))

        sample_maj = abs(E_MM - E_MM_star)

        edges_maj_to_remove = []

        edges_maj_to_add = []

        if h_maj > h_maj_star:

            print("Rewiring", sample_maj, "edges from E_MM to E_Mm")

            sample_edge_idx = np.random.choice(len(mapping_edges["majority", "majority"]), sample_maj, replace = False)

            sample_new_destinations = np.random.choice(V_min, sample_maj)


            for edge_idx, new_destination in zip(sample_edge_idx, sample_new_destinations):

                edges_maj_to_remove.append(mapping_edges["majority", "majority"][edge_idx])

                edges_maj_to_add.append((mapping_edges["majority", "majority"][edge_idx][0], new_destination))


        elif h_maj < h_maj_star:

            print("Rewiring", sample_maj, "edges from E_Mm to E_MM")

            sample_edge_idx = np.random.choice(len(mapping_edges["majority", "minority"]), sample_maj, replace = False)

            sample_new_destinations = np.random.choice(V_maj, sample_maj)


            #for edge_idx, new_destination in tqdm(zip(sample_edge_idx, sample_new_destinations)):
            for edge_idx, new_destination in zip(sample_edge_idx, sample_new_destinations):

                edges_maj_to_remove.append(mapping_edges["majority", "minority"][edge_idx])

                edges_maj_to_add.append((mapping_edges["majority", "minority"][edge_idx][0], new_destination))

                
        graph.delete_edges(edges_maj_to_remove)
        #print(graph.summary())
        
        
        graph.add_edges(edges_maj_to_add)       
        #print(graph.summary())

    print("\n")

    h_min_final = compute_homophily(graph, "minority")
    print("h*_min:", h_min_star, "- final homophily minority:", h_min_final)


    h_maj_final = compute_homophily(graph, "majority")
    print("h*_maj:", h_maj_star, "- final homophily majority: ", h_maj_final)
    
    print("\n", graph.summary())

    return graph

