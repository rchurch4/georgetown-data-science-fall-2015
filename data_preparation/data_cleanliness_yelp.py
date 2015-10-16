# Nathan Hauke
# Drop Table - Teamname
# Project 1
# Data Cleanliness Metric
#
# Usage: python data_cleanliness_yelp.py filename
# 
# Description:
# This code measures the cleanliness of our yelp data.
# The input is a file containing data collected from yelp and processed to generate new features.
# Each of our yelp data files contains data for 50 restaurants.
# We check whether each piece of data is missing, invalid, or an outlier based on
# a set of values we have judged to be reasonable.
# The invalid values in each column are tallied and averaged.
# We report the score from each attribute out of 100, and
# report the overall cleanliness score as an average of the attribute scores

import sys
import csv
import re

''' Yelp columns:
restaurant_address,
restaurant_overall_rating,
user_review,
restaurant_name,
restaurant_phone,
user_num_reviews,
user_review_date,
user_location,
restaurant_url,
user_rating,
restaurant_num_reviews,
restaurant_location,
user_name,
restaurant_latitude,
restaurant_longitude,
user_latitude,
user_longitude,
user_restaurant_distance,
user_is_local,
user_review_length,
user_rating_mean_for_restaurant_yelp,
user_rating_mean_for_restaurant_yelp_local,
user_rating_mean_for_restaurant_yelp_non_local
'''

# returns a function that checks whether the value of string x is between min and max, inclusive
# if mode is numeric ('num'), value is float(x)
# if mode is length ('len'), value is len(x)
def is_between(min, max, mode='num'):
    def num_between(x):
        try:
            return min <= float(x) <= max
        except ValueError:
            return False
    
    if mode == 'num':
        return num_between
    elif mode == 'len':
        return lambda x: min <= len(x) <= max

    
# returns a cleanliness score for each column of yelp data
# this is calculated as the number of 'dirty' records / number of records
def score_yelp(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        col_names = reader.next()
        col_scores = score_columns(reader)

    avg_col_score = sum(col_scores) / num_columns
    
    print 'attribute scores:'
    for name, score in zip(col_names, col_scores):
        print 'attribute:', name
        print 'score:', score
        print

    print 'overall_score:', avg_col_score


# determines whether each data entry is clean or dirty
# using the associated score_function for each column
def score_columns(reader):
    col_scores = [0] * num_columns
    records = 0
    for record in reader:
        records += 1
        for i in range(num_columns):
            col_scores[i] += score_functions[i](record[i])

    for i in range(num_columns):
        col_scores[i] = col_scores[i] * 100.0 / records

    return col_scores

num_columns = 23

# regular expression for matching YYYY-MM-DD format
date_re = '\d{4}-\d{2}-\d{2}$'

# each function in score_functions is specific to one attribute
# each function will return False if it detects invalid or outlying data
# this is not meant to be all encompassing
# some clean values may still be flagged as invalid or outliers, and vice versa
# the location checks are specific to DC and will be adjusted for restaurants in oter cities

score_functions = [                               # conditions for column validity:
    is_between(20, 200, 'len'),                   # address 20-200 chars
    is_between(1, 5),                             # rating 1-5
    is_between(10, 5000, 'len'),                  # review 10-5000 chars
    is_between(5, 50, 'len'),                     # restaurant_name 5-50 chars
    lambda x: len(x) in [7,10,11],                # phone 7, 10, or 11 digits long
    is_between(5, 5000),                          # user_num_reviews 5-5000
    lambda x: bool(re.match(date_re, x)),         # date matches YYYY-MM-DD format
    is_between(10, 50, 'len'),                    # user_location 10-50 chars
    is_between(10, 100, 'len'),                   # url 10-100 chars
    is_between(1, 5),                             # user_rating 1-5
    is_between(10, 10000),                        # num_reviews 10-10000
    lambda x: x == "Washington, DC",              # all restaurants should be from DC
    is_between(5, 50, 'len'),                     # user_name 5-50 chars
    is_between(38, 39),                           # within DC latitude
    is_between(-77.2, -76),                       # within DC longitude
    is_between(24, 49.5),                         # within contiguous US latitude
    is_between(-124.5, -66.5),                    # within contiguous US longitude
    is_between(0, 3000),                          # user distance < width of US
    lambda x: x in ['True', 'False'],             # is_local boolean value
    is_between(10, 5000),                         # review length 10-5000
    is_between(1, 5),                             # mean rating 1-5
    is_between(1, 5),                             # mean local rating 1-5
    is_between(1, 5)                              # mean non_local rating 1-5
    ]

score_yelp(sys.argv[1])
