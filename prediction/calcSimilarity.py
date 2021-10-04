import math
import copy
import numpy as np
import pandas as pd
from tabulate import tabulate
from readLookup import db, get_user_info_movies, get_same_movie, can_calc_similarity_movies, get_user_info_food, get_same_food, can_calc_similarity_food
from recommendation import recommend_movies, recommend_food

# calculate the similarity of the rate between two users
def calc_person_rate_movies(score_dict_1, score_dict_2):
    intersection_set = get_same_movie(score_dict_1, score_dict_2)
    score_lst_1 = np.array([score_dict_1[movieId] for movieId in intersection_set])
    score_lst_2 = np.array([score_dict_2[movieId] for movieId in intersection_set])

    return sim_distance(score_lst_1, score_lst_2)

def calc_person_rate_food(score_dict_1, score_dict_2):
    intersection_set = get_same_food(score_dict_1, score_dict_2)
    score_lst_1 = np.array([score_dict_1[foodId] for foodId in intersection_set])
    score_lst_2 = np.array([score_dict_2[foodId] for foodId in intersection_set])

    return sim_distance(score_lst_1, score_lst_2)

def sim_distance(lst1, lst2): #Euclidean distance: calculate similarity
    # sum_value = 0
    # for x1, x2 in zip(lst1, lst2):
    #     sum_value += pow(x1 - x2, 2)
    # # print(x1, x2)
    # # print(1/(1+math.sqrt(sum_value)))
    # return 1/(1+math.sqrt(sum_value)) #similarity
    

    tmp = np.sum(lst1*lst2)   # cosine similarity
    non = np.linalg.norm(lst1) * np.linalg.norm(lst2)
    return np.round(tmp/float(non),9)

# top 5
def calc_similarity_movies(base_user_id):
    user_score_info = get_user_info_movies()
    base_score_dict = user_score_info[base_user_id]
    
    similarity_lst = []
    similarity_lst_output = []
    
    for user_id, score_dict in user_score_info.items():
        if ((user_id == base_user_id) or (not can_calc_similarity_movies(base_score_dict, score_dict))):
            continue
        similarity = calc_person_rate_movies(base_score_dict, score_dict)
        #print(similarity)
        sql = "select name from nodemysql.users where id = "+ str(user_id) + " "
        # print(sql)
        userName = pd.read_sql(sql, db)
        
        similarity_lst.append((user_id, similarity))
        similarity_lst_output.append((userName.name[0], similarity))

    similarity_lst.sort(key=lambda x: x[1], reverse=True)
    similarity_lst_output.sort(key=lambda x: x[1], reverse=True)
    head_5 = similarity_lst[:5]
    # print(head_5)
    print(tabulate(similarity_lst_output[:5], headers=['userName', 'Movie Similarity']))
    recommend_movies(base_user_id, user_score_info, head_5)
    
def calc_similarity_food(base_user_id):
    user_score_info = get_user_info_food()
    base_score_dict = user_score_info[base_user_id]
    
    similarity_lst = []
    similarity_lst_output = []
    
    for user_id, score_dict in user_score_info.items():
        if ((user_id == base_user_id) or (not can_calc_similarity_food(base_score_dict, score_dict))):
            continue
        similarity = calc_person_rate_food(base_score_dict, score_dict)
        #print(similarity)
        sql = "select name from nodemysql.users where id = "+ str(user_id) + " "
        # print(sql)
        userName = pd.read_sql(sql, db)
        
        similarity_lst.append((user_id, similarity))
        similarity_lst_output.append((userName.name[0], similarity))

    similarity_lst.sort(key=lambda x: x[1], reverse=True)
    similarity_lst_output.sort(key=lambda x: x[1], reverse=True)
    head_5 = similarity_lst[:5]
    # print(head_5)
    print(tabulate(similarity_lst_output[:5], headers=['userName', 'Food Similarity']))
    recommend_food(base_user_id, user_score_info, head_5)
