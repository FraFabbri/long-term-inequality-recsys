

import numpy as np
from numpy.random import uniform
from scipy.sparse import csr_matrix
from scipy import sparse

import implicit


from tqdm import tqdm


class RecSysAlgorithms():
  
    
    def __init__(self, graph, selected_method, selected_attribute, edges_at_distance_2):
   
        self.graph = graph
        
        ##### MA QUESTO SERVE ????
        self.selected_attribute = selected_attribute ######### BY ATTRIBUTE #########
        
        
        # filter methods
        self.edges_at_distance_2 = edges_at_distance_2
        self.available_methods = [
            
            "ada", 
            
            "als",
            
            "random",
            
            "salsa"
            
        ]
        
        
        self.algoname = selected_method
        
        """
        
        if self.algoname  == "als":
            
            self.initialize_ALS()
        
        """
        
        # mapping-out
        #all_out = self.graph.neighbors(mode="out")
        #self.mapping_out = {idx: set(set_v) - set([idx]) for idx, set_v in enumerate(all_out)}
        self.mapping_out = {idx: set(self.graph.neighbors(idx, mode="out")) - set([idx]) for idx in range(self.graph.vcount())}

        # mapping-it
        #all_in = self.graph.neighbors(mode="in")
        #self.mapping_in = {idx: set(set_v) - set([idx]) for idx, set_v in enumerate(all_in)}
        self.mapping_in = {idx: set(self.graph.neighbors(idx, mode="in")) - set([idx]) for idx in range(self.graph.vcount())}
        
        for n in self.graph.vs:
            
            n["name"] = n.index
            
        self.dic_names_id = {node["name"]: node.index for node in self.graph.vs}
        
        
        
    def initialize_SALSA(self):
    
        dic_output_SALSA = {}
        
        
        
        for source in self.edges_at_distance_2:
        
            nodes_dist_1 = self.graph.neighbors(source, mode = "out")
            
            nodes_dist_2 = self.edges_at_distance_2[source]
            
            lst_nodes = nodes_dist_1 + nodes_dist_2
            
            subgraph = self.graph.subgraph(lst_nodes)
            
            edgelist = subgraph.get_edgelist()
            
            if len(edgelist) != 0:
            
                edgelist_with_names = [(int(subgraph.vs[x]["name"]), int(subgraph.vs[y]["name"])) for (x, y) in edgelist]
                
                dic_authority_scores = get_authority_scores(edgelist_with_names)
                
                dic_output_SALSA[source] = dic_authority_scores
            
            
                
        self.dic_output_SALSA = dic_output_SALSA
        
        
        
    
    def compute_SALSA(self, t):
    
        u, v = t[0], t[1]
        
        if u in self.dic_output_SALSA: 
        
                
            out = self.dic_output_SALSA[u][v]
            
        else:
        
            out = 0.
            
        return out 
        
        
        
        
    
    def find_bridges(self, t):
        
        u,v = t[0], t[1]
        
        outlinks_from_u = self.mapping_out[u]
        
        inlinks_to_v = self.mapping_in[v]
        
        bridges = outlinks_from_u.intersection(inlinks_to_v)
        
        return list(bridges)


    def compute_Random(self, t):
        
        out = np.random.uniform(low = 0, high = 1)
        
        return out
    
        
    def compute_DirectedAdamicAdar(self, t):
        
        bridges = self.find_bridges(t)
        
        out = list(map(lambda n: 1./np.log2(len(self.mapping_out[n])+1), bridges))
        
        return sum(out)

    
    def initialize_ALS(self):
        """
        generate user-item matrix
        """
        

        #num_factors = 100
        num_factors = 300
        
        #adj_sparse_matrix = get_sparse_adj_martrix(self.graph)
        
        adj_sparse_matrix = get_sparse_adj_matrix(self.graph)
        
        num_iterations = 10
        
        model = implicit.als.AlternatingLeastSquares(factors = num_factors, calculate_training_loss = True,  iterations = num_iterations)
        
        model.fit(adj_sparse_matrix.T)
        
        
        
        self.ALS__U_I = (model.user_factors, model.item_factors)
        
        
    
        
        
        
    def compute_ALS(self, t):
        
        """
        user-user embeddings product
        """
        
        u,v = t[0], t[1]
        
        # index [0] selects the user-matrix 

        u_vector = self.ALS__U_I[0][u,:]
        
        # index [1] selects the item-matrix 
        v_vector = self.ALS__U_I[1][v,:]
        
        
        out = np.dot(u_vector, v_vector)
        
        return out

    
    
    

    def STEP1_compute_One4All(self, algoname, to_skip, top_k):

        if algoname == "ada":

            method = self.compute_DirectedAdamicAdar


        elif algoname == "random":

            method = self.compute_Random

        elif algoname == "als":

            method = self.compute_ALS
            
            self.initialize_ALS()

        elif algoname == "pagerank":

            method = self.compute_PersonalizedPagerank
            
        elif algoname == "salsa":
        
            method = self.compute_SALSA
            
            self.initialize_SALSA()
            

        else:

            print("No algorithm selected")
            return

        #dic_prob = dict((el, []) for el in self.edges_at_distance_2)
        dic_prob = {}

        c = 0 ##### MA QUESTO SERVE ????



        for source in tqdm(self.edges_at_distance_2):

            dic_prob[source] = {}

            lst = self.edges_at_distance_2[source]

            lst_destination = [destination for destination in lst if (source, destination) not in to_skip]


            if algoname == "pagerank":



                scores = method(source, lst_destination)

                dic_prob[source] = {destination: score for (destination, score) in zip(lst_destination, scores)}


            else:


                for destination in lst_destination:

                    #if (source, destination,) not in to_skip:

                    score = method((source, destination))

                    dic_prob[source][destination] = score

        filter_by_top_k = {}

        for source_node in dic_prob:

            lst_topk = sorted(dic_prob[source_node].items(), key=lambda x: x[1], reverse=True)[:top_k]

            mapping_position_and_id = {position: node_id for (position, (node_id, score)) in enumerate(lst_topk)}

            filter_by_top_k[source_node] = mapping_position_and_id


        return filter_by_top_k
                
#######################


def get_sparse_adj_matrix(graph):

    N = graph.vcount()
    
    edgelist = graph.get_edgelist()
    
    binary_value = [1] * len(edgelist)
        
    adjacency_matrix = csr_matrix((binary_value, list(zip(*edgelist))), shape = (N,N))
        
    return adjacency_matrix

##############################################################################################################################


def get_sparse_adj_martrix_SALSA(edgelist, N):
    
    weights = [1]*len(edgelist)
    
    adjacency_matrix = csr_matrix((weights, zip(*edgelist)), shape = (N, N))
    
    return adjacency_matrix
    
    
    
##################################################################################################    
    
    

def get_authority_scores(edgelist):
    
    old_nodes = set()
    
    for (u,v) in edgelist:
        
        old_nodes.update({u,v})
        
    old_nodes_dic = {x: idx for idx, x in enumerate(old_nodes)}
    
    new_edgelist = [(old_nodes_dic[x], old_nodes_dic[y]) for (x, y) in edgelist] 
    
    adj_matrix = get_sparse_adj_martrix_SALSA(new_edgelist, len(old_nodes_dic))
    
    array_aut = np.ones(len(old_nodes_dic))

    array_aut /=sum(array_aut)
    
    column_normalization = adj_matrix.sum(0)

    row_normalization = adj_matrix.sum(1)
    
    mat_column = adj_matrix/column_normalization
    
    mat_row = adj_matrix/row_normalization
    
    mat_column[~np.isfinite(mat_column)] = 0.
    
    mat_row[~np.isfinite(mat_row)] = 0.    
    
    mat_combined = np.dot(mat_column.T, mat_row)
    
    array_aut_0 = np.reshape(array_aut, (len(array_aut), 1)).T

    array_aut_1 = np.dot(array_aut_0, mat_combined)
    
    threshold = 0.01
    
    while True:
        array_aut_1 = np.dot(array_aut_0, mat_combined)
        
        err = abs(array_aut_0 - array_aut_1).mean()
        
        if err < threshold:
            break
            
        array_aut_0 = array_aut_1.copy()
    
    array_aut_1 = array_aut_1.tolist()[0]
    
    out = {node: array_aut_1[old_nodes_dic[node]] for node in old_nodes_dic}
    
    return out




