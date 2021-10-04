import math
import copy
import numpy as np
import pandas as pd
from tabulate import tabulate
import readLookup

def recommend_movies(base_user_id, user_score_info, head_5):
    diff_moive_set = set()       # base user never seen before
    for userId, similarity in head_5:
        diff_moive = get_diff_moive(user_score_info[base_user_id], user_score_info[userId])
        diff_moive_set = diff_moive_set.union(diff_moive)

    recommend_lst = []

    for movieId in diff_moive_set:
        moive_score_sum = 0
        similarity_sum = 0
        user_score_count = 0
        for userId, similarity in head_5:
            # print(userId, similarity)
            if movieId in user_score_info[userId]:
                user_score_count += 1
                moive_score_sum += user_score_info[userId][movieId]*pow(similarity, 2)
                similarity_sum += similarity
            # a = []
            # a.append((movieId, moive_score_sum, similarity_sum))
            # print(a)
        if user_score_count < 3: 
            continue

        sql_movieTitle = "select title from nodemysql.movies where imdb_title_id = '"+ movieId + "' " 
        # sql_moviePoster = "select poster from nodemysql.movies where imdb_title_id = '"+ movieId + "' " 

        # print(sql_movieTitle)
        movieTitle = pd.read_sql(sql_movieTitle, readLookup.db)
        # moviePoster = pd.read_sql(sql_moviePoster, readLookup.db)
       # print(movieTitle.title[0])

        movie_score = moive_score_sum/similarity_sum
        
        recommend_lst.append((movieTitle.title[0], movie_score))
       

    recommend_lst.sort(key=lambda x: x[1], reverse=True)
    # print(recommend_lst)
    recommend_lst = recommend_lst[:5]
    print(tabulate(recommend_lst, headers=['Top 5 movies you may like', 'predict movie action']))
    # return tabulate(recommend_lst, headers=['Top 5 movies you may like', 'Movie Poster', 'predict movie score'])
    

    # print(tabulate(recommend_lst, headers=['Top 5 movies you may like', 'Movie Poster', 'predict movie score']))
    # print(type(tabulate(recommend_lst, headers=['Top 5 movies you may like', 'Movie Poster', 'predict movie score'])))
    # print(type(recommend_lst), recommend_lst)
    # return recommend_lst
def get_diff_moive(base_score, score_dict_2):
    set_1 = set([movie for movie in base_score])
    set_2 = set([movie for movie in score_dict_2])

    return set_2.difference(set_1)


def recommend_food(base_user_id, user_score_info, head_5):
    diff_food_set = set()       # base user never seen before
    for userId, similarity in head_5:
        diff_food = get_diff_food(user_score_info[base_user_id], user_score_info[userId])
        diff_food_set = diff_food_set.union(diff_food)

    recommend_lst = []

    for foodId in diff_food_set:
        food_score_sum = 0
        similarity_sum = 0
        user_score_count = 0
        for userId, similarity in head_5:
            # print(userId, similarity)
            if foodId in user_score_info[userId]:
                user_score_count += 1
                food_score_sum += user_score_info[userId][foodId]*pow(similarity, 2)
                similarity_sum += similarity
            # a = []
            # a.append((movieId, moive_score_sum, similarity_sum))
            # print(a)
        if user_score_count < 3: 
            continue

        sql_foodName = "select name from nodemysql.food where id = '"+ str(foodId) + " ' " 
        

        # print(sql_foodName)
        foodName = pd.read_sql(sql_foodName, readLookup.db)
        # print(foodName.name[0])

        food_score = food_score_sum/similarity_sum
        
        recommend_lst.append((foodName.name[0], food_score))
       

    recommend_lst.sort(key=lambda x: x[1], reverse=True)
    # print(recommend_lst)
    recommend_lst = recommend_lst[:5]
    print(tabulate(recommend_lst, headers=['Top 5 food you may like', 'predict food action']))
    # return tabulate(recommend_lst, headers=['Top 5 movies you may like', 'Movie Poster', 'predict movie score'])
    

    # print(tabulate(recommend_lst, headers=['Top 5 movies you may like', 'Movie Poster', 'predict movie score']))
    # print(type(tabulate(recommend_lst, headers=['Top 5 movies you may like', 'Movie Poster', 'predict movie score'])))
    # print(type(recommend_lst), recommend_lst)
    # return recommend_lst
def get_diff_food(base_score, score_dict_2):
    set_1 = set([food for food in base_score])
    set_2 = set([food for food in score_dict_2])

    return set_2.difference(set_1)