

vec_dataset = ["TUENTI-A16"]

#vec_h_min_star =  [0.05, 0.4]
#vec_h_maj_star = [0.0]

vec_e_rr = [0.8, 0.9, 1]
vec_s_min_star = [0.3]

s_maj = 1 - vec_s_min_star[0]


#vec_h_min_star = [round(e_rr - vec_s_min_star[0], 2) for e_rr in vec_e_rr]

vec_h_min_star = [round(vec_e_rr[2] - vec_s_min_star[0], 2)]

vec_h_maj_star = [round(e_rr - s_maj, 2) for e_rr in vec_e_rr]

alpha = 20

iterations = 20

top_k = 3