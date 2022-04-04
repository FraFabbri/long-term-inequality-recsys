#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import igraph
import csv
import pickle
import os
from collections import Counter


mapping_dataset_attribute = {"POKEC-A21": "age", "TUENTI-A16": "age", "TUENTI-A30": "age", "TUENTI-G": "gender"}


def return_igraph_object(dataset, attribute):
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

def compute_homophily(bi_partite_graph, selected_attribute):
    if selected_attribute == "None":
        nodes_by_selected_attribute = len([x.index for x in bi_partite_graph.vs if x["selected_attribute"] not in ["minority", "majority"]])
    else:
        nodes_by_selected_attribute = [x.index for x in bi_partite_graph.vs if x["selected_attribute"] == selected_attribute]
    induced_subgraph = bi_partite_graph.subgraph(nodes_by_selected_attribute)
    E_ii = induced_subgraph.ecount()
    E_i = sum(bi_partite_graph.degree(nodes_by_selected_attribute, mode="out"))
    n_i = len(nodes_by_selected_attribute)
    max_edges_i = n_i*(n_i-1)
    N = bi_partite_graph.vcount()
    try:
        connectance = E_ii*1./max_edges_i
    except ZeroDivisionError:
        connectance = "NULL"
    try:
        homophily = (E_ii*1./E_i) - ((n_i-1)*1./(N-1))
    except:
        homophily = "NULL"
    homophily = round(homophily, 4)
    #connectance = round(connectance, 4)
    return homophily


def percentage_edge_added(final_graph, iterations):

    track_edges_accepted = {}

    for n_iter in range(iterations):

        count_edge_accepted = 0
        initial_edges = 0 

        for e in final_graph.es:
            
            if e["time"] == 0:
                initial_edges += 1
                
       
            elif e["time"] == n_iter + 1: #le label partono da 1 per la prima iterazione, non 0 (0 rappresenta il numero di  archi iniziali)
                count_edge_accepted += 1
            

        track_edges_accepted[n_iter] = count_edge_accepted

    cum_edges_accepted = {}
    cum_ls = np.cumsum(list(track_edges_accepted.values()))

    for it, cum in zip(track_edges_accepted, cum_ls):
        cum_edges_accepted[it] = cum   

    percentage_edge_accepted = []

    for it in cum_edges_accepted:
        
        percentage = round(cum_edges_accepted[it]*100/initial_edges, 2)
        
        if percentage <= 100:
            percentage_edge_accepted.append(percentage)
                
                
    return percentage_edge_accepted


def gini_coefficient(x):
    
    sorted_x = np.sort(x)
    n = len(x)
    cumx = np.cumsum(sorted_x, dtype=float)
    # The above formula, with all weights equal to 1 simplifies to:
    return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n



def mapping_colors_function(graph):
    
    mapping_colors = {}
    
    for n in graph.vs:
        node = n.index
        color = graph.vs[n.index]["selected_attribute"]

        if color == "minority":
            color = "red"
        else:
            color = "blue"

        mapping_colors[node] = color

    return mapping_colors




def compute_size(graph, selected_attribute):
    
    nodes_selected_attribute = [node.index for node in graph.vs if node["selected_attribute"] == selected_attribute]
    
    number_nodes_selected_attribute = len(nodes_selected_attribute)
    
    N = graph.vcount()
    
    size = number_nodes_selected_attribute/N
    
    return size


def plot_loglog(indegree_graphs, dataset, ax, attribute, color, marker):
    
    degree, count = zip(*(Counter(indegree_graphs[dataset][attribute].values()).items()))
    
    ax.scatter(x = degree, y = count, color = color, marker = marker, s = 50, alpha = 0.5, edgecolors = "face", label = attribute)    
   
