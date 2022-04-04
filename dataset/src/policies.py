#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import warnings


from numpy.random import choice
from itertools import permutations
import igraph
import pickle
from random import shuffle



warnings.filterwarnings("ignore")




def get_policy_update(bi_partite_graph, filter_by_top_k, mapping_iterations_and_nodes, mapping_sample_alpha, n_iter):
    """
    
    bi_partite_graph: input graph
    
    filter_by_top_k: dictionary where for each node you have a dictionary position: destination_node (position < top_k)
    
    to_skip: set of all recommendations already submitted
    
    mapping_iterations_and_nodes: nested dictionary with iterations and for each one the id of nodes and for each node the idx of accepted recsys
    
    top_k: number of rec generated
    
    n_iter: current iteration
    
    """
    
    #accepted recommendation
    all_accepted_edges = set()
    
    small_to_skip = set()

    #for source_node in filter_by_top_k:
    for source_node in mapping_sample_alpha[n_iter]:
        
        if source_node in filter_by_top_k:
        
            accepted_positions = mapping_iterations_and_nodes[n_iter][source_node]


            mapping_position_to_node = filter_by_top_k[source_node]

            for position in mapping_position_to_node:

                if position in accepted_positions:


                    destination_node = mapping_position_to_node[position]

                    all_accepted_edges.update([(source_node, destination_node)])


                else:

                    removed_destination = mapping_position_to_node[position]

                    small_to_skip.update([(source_node, removed_destination)])
                

    #print("add-edges")
    #print(len(all_accepted_edges.intersection(small_to_skip)))
    
    
    #print("Count")
    #print(len(all_accepted_edges))
    #print(len(small_to_skip))
    
    all_accepted_edges = list(all_accepted_edges)
    bi_partite_graph.add_edges(all_accepted_edges, attributes = {"time": [n_iter+1]*len(all_accepted_edges)})
    
    return bi_partite_graph, small_to_skip




# initialize probabilities for flip-policy
def inizialization_prob_FlipCoinPolicy(iterations, mapping_sample_alpha, top_k):
    """
    
    """
    # here we apply the flip-policy (before generating the recommendations)
    
    # weight proportional to position in the list 
    prob_ = [1./np.log2(i+2) for i in range(top_k)]
    prob_ = np.array(prob_)/sum(prob_)
    mapping_iterations_and_nodes = {}

   
    for one_iter in range(iterations):
        
        mapping_iterations_and_nodes[one_iter] = {}       

        for n in mapping_sample_alpha[one_iter]:
            to_add = set()

            for idx, one_prob in enumerate(prob_):

                decision = choice(a=[1,0], size=1, p=[one_prob, 1-one_prob])[0]
                if decision:

                    # accept the recommendation
                    to_add.update([idx])
                else:
                    pass

            # update nested-dictionary
            mapping_iterations_and_nodes[one_iter][n] = to_add
    
    return mapping_iterations_and_nodes



# initialize probabilities for flip-policy
def inizialization_prob_RandomPolicy(iterations, mapping_sample_alpha, top_k):
    """
    
    """
    # here we apply the flip-policy (before generating the recommendations)
    
    mapping_iterations_and_nodes = {}

   
    for one_iter in range(iterations):
        
        mapping_iterations_and_nodes[one_iter] = {}       

        for n in mapping_sample_alpha[one_iter]:
            
            
            lst_top_k = list(range(top_k))
            to_add = choice(a=lst_top_k, size=1)[0]
            
            to_add = {to_add}
            
            # update nested-dictionary
            mapping_iterations_and_nodes[one_iter][n] = to_add
    
    return mapping_iterations_and_nodes




# initialize probabilities for flip-policy
def inizialization_prob_LazyPolicy(iterations, mapping_sample_alpha, top_k):
    """
    
    """
    # here we apply the flip-policy (before generating the recommendations)
    
    mapping_iterations_and_nodes = {}

   
    for one_iter in range(iterations):
        
        mapping_iterations_and_nodes[one_iter] = {}       

        for n in mapping_sample_alpha[one_iter]:
            
            to_add = set([0])

            # update nested-dictionary
            mapping_iterations_and_nodes[one_iter][n] = to_add
    
    return mapping_iterations_and_nodes








def inizialization_sample_nodes(iterations, N, alpha):
    
    percentage_sampled = round(N*alpha/100)
    
    mapping_sample_alpha = {}
    
    for one_iter in range(iterations):
        
        sample = np.random.choice(N, percentage_sampled, replace = False)
        
        mapping_sample_alpha[one_iter] = set(sample)
        
    return mapping_sample_alpha
