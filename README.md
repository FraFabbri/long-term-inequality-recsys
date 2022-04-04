# Exposure Inequality in People Recommender Systems: The Long-Term Effects

Official  repository for: 

Fabbri, F., Croci, M. L., Bonchi, F., & Castillo, C. (2021). [Exposure Inequality in People Recommender Systems: The Long-Term Effects](https://arxiv.org/abs/2112.08237) In Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2022)


### Abstract

People recommender systems may affect the exposure that users receive in social networking platforms, influencing attention dynamics and potentially strengthening pre-existing inequalities that disproportionately affect certain groups.
In this paper we introduce a model to simulate the feedback loop created by multiple rounds of interactions between users and a link recommender in a social network. This allows us to study the long-term consequences of those particular recommendation algorithms. Our model is equipped with several parameters to control (i) the level of homophily in the network, (ii) the relative size of the groups, (iii) the choice among several state-of-the-art link recommenders, and (iv) the choice among three different user behavior models, that decide which recommendations are accepted or rejected.
Our extensive experimentation with the proposed model shows that a minority group, if homophilic enough, can get a disproportionate advantage in exposure from all link recommenders. Instead, when it is heterophilic, it gets under-exposed. Moreover, while the homophily level of the minority affects the speed of the growth of the disparate exposure, the relative size of the minority affects the magnitude of the effect. Finally, link recommenders strengthen exposure inequalities at the individual level, exacerbating the "rich-get-richer" effect: this happens for both the minority and the majority class and independently of their level of homophily.

### Cite

For citing our work:

```
@article{fabbri2021exposure,
  title={Exposure Inequality in People Recommender Systems: The Long-Term Effects},
  author={Fabbri, Francesco and Croci, Maria Luisa and Bonchi, Francesco and Castillo, Carlos},
  journal={arXiv preprint arXiv:2112.08237},
  year={2021}
}
```

# Repository structure

Three main folders: ***"dataset", "plot"*** and ***"semi_synthetic_graphs"***.

+ [dataset/src](https://github.com/MariaLuisaCroci/simulation_framework_visibility/tree/main/dataset/src) contains the following *.py* codes:

  + `config.py` this is used to change the parameter *top_k*. May be used to change also alpha and the number of iterations, but atm those are given as input when run the file `run-policy.py`;
  
  + `policies.py` contains the three functions to use different policies (fc, lazy, random) and the function to initialize the sample alpha of nodes that receive the recommendation at each iteration;
  
  + `recsys.py` contains the class function for four different recommender systems (ada, als, random, salsa);
  
  + `utils.py` contains the functions to create graph from tsv files of edges and nodes, the function to extract nodes at distance 2 (friend-of-friend) and the function to save recommended nodes at each iteration;
  
  + `run-policy.py` is the code that has to be run whenever you want to generate recommendations over a real graph. It takes as input:
    + the **dataset**: "TUENTI-A16", "TUENTI-A30", "TUENTI-G", "POKEC-A21";
    + the sample **alpha**;
    + the number of **iterations**;
    + the **policy**: "lazy", "fc", "random";
    + the **recsys**: "ada", "als", "salsa", "random".
   
   
   
  + `make_pickle_visibility.py` is the code to use when the simulation ends. It computes and saves the dictionaries with the number of recommendations for node, group and all combination colors of target/source for each iteration:
    + dictionary `track_visibility_all_combination_color[n_iteration][source_color, target_color] = times_recommended`;
    + dictionary `track_visibility[n_iteration][color] = times_recommendation_of_that_group`. This is the dictionary used for the plot of the visibilities;
    + dictionary `track_visibility_node[n_iteration][node_id] = times_recommended`.

      It takes as input:
    + folder_data (that is the **dataset**): `["TUENTI-A16", "TUENTI-A30", "TUENTI-G", "POKEC-A21"]`;
    + the **policy**: `["lazy", "fc", "random"`]
    + the **recsys**: `["ada", "als", "salsa", "random"]`



 --------------------
 
 
 
 
 + `semi_synthetic_graphs/src` contains the code to generate synthetic graphs from real ones and the codes to run recommendations over them:

  **1. GENERATE SYNTHETIC GRAPHS:**
  
  + `config.py` is used to set the parameters for either the synthethic graph and either the recommendations in step 2 (*alpha, iterations, top_k*);
  
  + `functions_synth_from_real.py` contains the functions to change sizes and homophilies from real graph;
  
  + `gen_synth_from_real.py` is the code that has to be run to generate the synthetic graph. It takes the parameter of size and homophilies from the config file.
  
  
  
  **2. RUN RECOMMENDATIONS:**
  
  + `policies.py`, `recsys.py` and `utils.py` are the same as in dataset folder;
  
  + `run-recsys-policy.py` is the code that has to be run to generate the recommendations over synthetic graphs and it gets the parameters from `config.py`
  

  **3. COMPUTE THE VISIBILITIES:**
  
  + `make_pickle_visibility.py` and `make_pickle_visibility_hM.py` are the same as in dataset folder. The first one is for configurations with majority neutral (h<sub>M</sub> = 0.0), while the second one is for configurations with majority homophilic (h<sub>M</sub> > 0).



--------------------


+ `plot` contains folders and jupyter notebooks to produce plots and results. 
