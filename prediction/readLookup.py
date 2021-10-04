import pandas as pd
import pymysql

db = pymysql.connect(
  host = "158.247.60.15",
  port = 6033,
  user = "richard_xia",
  password = "Dnsnetworks#123",
  database = "nodemysql",
)

get_movies = "select * from nodemysql.lookup where action = 'like' || action = 'dislike'"
get_food = "select * from nodemysql.food_lookup where action = 'like' || action = 'dislike'"
data_movies = pd.read_sql(get_movies, db)
data_food = pd.read_sql(get_food, db)

# calculate similarity between two users
# sql object to dictionary
def get_user_info_movies():
    user_info_movies = {}

    for i in range(len(data_movies)):
      userId = data_movies.userId[i]
      movieId = data_movies.movieId[i]
      if (data_movies.action[i] == 'like'): score = 1
      elif (data_movies.action[i] == 'dislike'): score = 0

      user_info_movies.setdefault(userId, {})
      user_info_movies[userId][movieId] = score
    # print(user_info[27])
    return(user_info_movies)

def get_user_info_food():
    user_info_food = {}

    for i in range(len(data_food)):
      userId = data_food.userId[i]
      foodId = data_food.foodId[i]
      if (data_food.action[i] == 'like'): score = 1
      elif (data_food.action[i] == 'dislike'): score = 0

      user_info_food.setdefault(userId, {})
      user_info_food[userId][foodId] = score

    return(user_info_food)

#get the same movie of two users
def get_same_movie(score_dict_1, score_dict_2):
    set_1 = set([movie for movie in score_dict_1])
    set_2 = set([movie for movie in score_dict_2])

    intersection_set = set_1.intersection(set_2)
    return intersection_set

def get_same_food(score_dict_1, score_dict_2):
    set_1 = set([food for food in score_dict_1])
    set_2 = set([food for food in score_dict_2])

    intersection_set = set_1.intersection(set_2)
    return intersection_set

# if same movie >= 10, start calculate similarity
def can_calc_similarity_movies(score_dict_1, score_dict_2, same_movie_number = 10):
    intersection_set = get_same_movie(score_dict_1, score_dict_2)
    return len(intersection_set) >= same_movie_number

def can_calc_similarity_food(score_dict_1, score_dict_2, same_food_number = 10):
    intersection_set = get_same_food(score_dict_1, score_dict_2)
    return len(intersection_set) >= same_food_number

    