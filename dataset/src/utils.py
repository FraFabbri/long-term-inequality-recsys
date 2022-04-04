


import igraph
import csv
import pickle
import pandas as pd
import numpy as np
import os

from sympy.solvers import solve
from sympy import Symbol
from tqdm import tqdm
from random import shuffle
from itertools import permutations
from numpy.random import choice




#################################################################################

def return_igraph_object(dataset, attribute, generate_pajek = False):
    """
    :param directory:
    :param edges_filename: file which contains list of edges
    :param nodes_filename: file which contains nodes with properties
    :param selected_column:
    :return:
    """
    
    directory = "../data/%s/"%dataset
    
    
    edges_filename = "graph_edges_by_%s.tsv"%attribute
    nodes_filename = "graph_nodes_by_%s.tsv"%attribute
    
    
    if generate_pajek == True:
        nodes_file = open(directory + nodes_filename, "r")
        nodes_reader = csv.reader(nodes_file, delimiter="\t")
        header = nodes_reader.next()
        count = 0
        for _ in nodes_reader:
            count +=1
        nodes_file.close()

        pajek_file = open(directory + "pajek_file_%s.net"%attribute, "w")
        pajek_writer = csv.writer(pajek_file, delimiter="\t")
        pajek_writer.writerow(["*network",  "new"])
        pajek_writer.writerow(["*Vertices", count])

        nodes_file = open(directory + nodes_filename, "r")
        nodes_reader = csv.reader(nodes_file, delimiter="\t")
        #header = nodes_reader.next()
        header = next(nodes_reader)
        for row in nodes_reader:
            n = int(row[0]) + 1
            #id_ = "'" + str(n) + "'"
            row = [n] #+ row[1:]
            #row = " ".join(map(str, row))
            pajek_writer.writerow(row)
        nodes_file.close()

        pajek_writer.writerow(["*Arcs"])
        

        edges_file = open(directory + edges_filename, "r")
        edges_reader = csv.reader(edges_file, delimiter="\t") 
        for edge in edges_reader:
            u,v = edge
            u = int(u)+1
            v = int(v)+1
            edge = [u,v]
            pajek_writer.writerow(edge)
        edges_file.close()
        pajek_file.close()    
    
    g = igraph.read(filename=directory + "pajek_file_%s.net"%attribute, format = "pajek")

    nodes_file = open(directory + nodes_filename, "r+")
    nodes_reader = csv.reader(nodes_file, delimiter="\t")
    
    header = next(nodes_reader)
    attribute = header[1]
    
    for row in nodes_reader:
        n = int(row[0])
        g.vs[n][attribute] = row[1]
        
    nodes_file.close()
    print(g.summary())
    return g
###############################################################################################################

def return_bi_partite_graph(graph, selected_attribute):
    distr_attributes = {}
    for n in graph.vs:
        if n[selected_attribute] not in distr_attributes:
            distr_attributes[n[selected_attribute]] = 0
        distr_attributes[n[selected_attribute]] += 1
    distr_attributes = sorted(distr_attributes.items(), key = lambda x: x[1])
    minority, majority = list(zip(*distr_attributes))[0]
    for n in graph.vs:
        if n[selected_attribute] == minority:
            n["selected_attribute"] = "minority"
        if n[selected_attribute] == majority:
            n["selected_attribute"] = "majority"
    #len_g = len(graph.vs)
    #print "Selected Attribute: %s"%selected_attribute
    #print "Minority: %s %s"%(distr_attributes[0][1]*1./len_g, minority)
    #print "Majority: %s %s"%(distr_attributes[1][1]*1./len_g, majority)
    # select subgraph
    #igraph.summary(graph)
    reduce_graph = False
    if reduce_graph:
        #graph = graph.subgraph([x for x in graph.vs if x.index < 2000])
        graph = graph.clusters().giant()
    print(graph.summary())
    return graph


###############################################################################################################


def find_nodes_at_distance_2(graph, mapping_sample_alpha, one_iter):

    dict_nodes_at_dist2 = {}

    for n in mapping_sample_alpha[one_iter]:
    
        nodes_at_distance_2 = graph.neighborhood(vertices = n, order=2, mode="out", mindist = 2)
        
    
        if nodes_at_distance_2 != []:
            dict_nodes_at_dist2[n] = nodes_at_distance_2
            
    return dict_nodes_at_dist2




##############################################################################################################


#save_info(outpath_, dic_prob)
def save_info(outpath_, filter_by_top_k, mapping_sample_alpha, one_iter, N, policy, algoname):
    """
    
    save one step of recommendations
    
    """
    source_nodes = mapping_sample_alpha[one_iter]
    
    sample_filter_by_top_k = {}
    
    for node in source_nodes:
        
        if node in filter_by_top_k:
            
            sample_filter_by_top_k[node] = filter_by_top_k[node]
           
    #print % real-sample
    
    real_sample_percentage = len(sample_filter_by_top_k.keys())*100/N
    
    
    print("Real sample: ", real_sample_percentage, " %")
    
    
    with open(outpath_ + policy + "-" + algoname + "-" + str(one_iter) + ".p", "wb") as f:
        pickle.dump(sample_filter_by_top_k, f)
    
