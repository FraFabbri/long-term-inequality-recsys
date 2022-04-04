Here there are the notebooks and the plot of the experiments. 

In folder **visibility_minority** there are also four tsv files with the visibility for N0, N1, N2, N3, N4 where:

| config          |  s<sub>M</sub> |   h<sub>M</sub>  | e<sub>mm</sub> |  s<sub>M</sub> |  h<sub>M</sub> | e<sub>MM</sub> | h<sub>m</sub> | h<sub>M</sub> |
|-----------------|:----:|:------:|:----:|:----:|:----:|:----:|:--------------:|:--------------:|
| N0 - Tuenti-A16 |  0.3 |  0.42  | 0.72 |  0.7 | 0.14 | 0.84 |   (-0.3, 0.7]  |   (-0.7, 0.3]  |
| N1 - MinHom1    |  0.1 |   0.4  |  0.5 |  0.9 |  0.0 |  0.9 |   (-0.1, 0.9]  |   (-0.9, 0.1]  |
| N2 - MinHom2    | 0.45 |   0.5  | 0.95 | 0.55 |  0.0 | 0.55 |  (-0.45, 0.55] |  (-0.55, 0.45] |
| N3 - MinHet1    |  0.3 | - 0.25 | 0.05 |  0.7 |  0.0 |  0.7 |   (-0.3, 0.7]  |   (-0.7, 0.3]  |
| N4 - MajHom1    |  0.3 |   0.5  |  0.8 |  0.7 |  0.2 |  0.9 |   (-0.3, 0.7]  |   (-0.7, 0.3]  |

Each of these tsv files refers to a configuration. 

Each row is the visibility of the minority for each recsys during time. 


That is row = recsys, column = iteration. So each tsv has 4 rows and 21 columnd (the first column is the name of the configuration and of the recsys, e.g. *N0_fc_als*).

--------------

Same in **tsv_synth** there are the tsv files for all synthetic graphs divided in two folders of 9 files each. One folder relates to configurations with majority neutral h<sub>M</sub> = 0.0, while the other relates to  configurations with majority homophilic h<sub>M</sub> > 0.0


