# clean_and_feature_generation_yelp.py
# Version 1.2
#
# Description:
# Script to generate extra features. 
# Current version is based on yelp_dc_pilot_2.csv.
# List of features generated:
    #   restaurant_latitude
    #   restaurant_longitude
    #   user_latitude, 
    #   user_longitude   
    #   user_restaurant_distance   
    #   user_is_local    
    #   user_review_length    
    #   mean_restaurant_rating_yelp
    #   mean_restaurant_rating_yelp_local
    #   mean_restaurant_rating_yelp_local	
#
# File Dependencies:
#   geocode_lookup_table.csv
#   input_data_path (user-defined)

import pandas as pd
import numpy as np
import os
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import time
import sys

################
# Set Data File Paths (USER-DEFINED)
#
# Set the input data source and the output data
# files as a string. Relative or absolute path
# may be used. 
################

input_data_path = 'data/yelp_dc_1.csv'
output_data_path = 'data/yelp_dc_1_cleaned_features.csv'

################
# Data loading
################

# Load data in as a Pandas DataFrame.
d = pd.read_csv(input_data_path)
num_rows = len(d) # this should only be changed during testing.

################
# Data cleaning
################

def data_cleaning():

    # Clean up address formatting
    for i in range(len(d)):
        d.loc[i, 'restaurant_address'] = d.loc[i, 'restaurant_address'].replace('Washington, DC', ', Washington, DC')

    # Extract and coerce user_num_reviews to a float
    for i in range(len(d)):
        number_extract = d.loc[i, 'user_num_reviews'][0:d.loc[i, 'user_num_reviews'].find('review')]
        d.loc[i, 'user_num_reviews'] = float(number_extract.strip())
        
    print 'data_cleaning() complete'

################
# Feature generating main methods
# 
# Note: Some of the feature generation scrip takes time
# to run (e.g. grabbing geocodes), that is why this script
# has been made modular by allowing one to specify which 
# main methods (e.g. which features) to run in the end. 
################

def make_restaurant_geocode():
    # Generates: 
    #   d.restaurant_latitude
    #   d.restaurant_longitude
    
    global d
    # Assign geocode based on restaurant_location
    for i in range(num_rows):
        # Restaurant geocode
        if d.loc[i, 'restaurant_location'] == "Washington, DC":
            d.loc[i, 'restaurant_latitude'] = 38.8949549
            d.loc[i, 'restaurant_longitude'] = -77.0366456
        elif d.loc[i, 'restaurant_location'] == "Nashville, TN":
            d.loc[i, 'restaurant_latitude'] = 36.1622296
            d.loc[i, 'restaurant_longitude'] = -86.774353
    print 'make_restaurant_geocode() complete'

def make_user_geocode():
    # Generates: 
    #   d.user_latitude, 
    #   d.user_longitude
    
    global d
    
    # Load in lookup table for geocodes
    geocode_lookup_table_df = pd.read_csv('data/geocode_lookup_table.csv')
    # Make dictionary out of lookup table
    a = geocode_lookup_table_df.user_location
    b = geocode_lookup_table_df.user_latitude
    c = geocode_lookup_table_df.user_longitude
    dict_keys = list(a)
    dict_values = zip(list(b), list(c))
    geocode_lookup_table = dict(zip(dict_keys, dict_values))

    # Get lat/long for cities and store in dataframe
    for i in range(num_rows): 
        d.loc[i, 'user_latitude'] = geocode_lookup_table[d.loc[i, 'user_location']][0]
        d.loc[i, 'user_longitude'] = geocode_lookup_table[d.loc[i, 'user_location']][1]
    # replace missing values with NaN
    #d = d.applymap(lambda x: np.nan if isinstance(x, basestring) and x.isspace() else x)
    print 'make_user_geocode() complete'    
        
def make_user_restaurant_distance():
    # Generates:
    #   d.user_restaurant_distance
    # Description:
    #   Uses the Vincenty distance formula to calculate distance between
    #   two points on a sphere, using the latitude and longitude. 
    
    global d
    for i in range(num_rows): 
        restaurant_geocode = (d.loc[i, 'restaurant_latitude'], d.loc[i, 'restaurant_longitude'])
        user_geocode = (d.loc[i, 'user_latitude'], d.loc[i, 'user_longitude'])
        try: 
            d.loc[i, 'user_restaurant_distance'] = vincenty(restaurant_geocode, user_geocode).miles
        except: # crashing when lat/long is missing
            continue
    print 'make_user_restaurant_distance() complete'
        
def make_user_is_local():
    # Generates:
    #   d.is_local
    # Description:
    #   User is considered local if he or she is within the distance_threshold.
    
    global d
    distance_threshold = 50 # in miles
    for i in range(num_rows): 
        if  d.loc[i, 'user_restaurant_distance'] <= distance_threshold:
            d.loc[i, 'user_is_local'] = True
        else:
            d.loc[i, 'user_is_local'] = False
    print 'make_user_is_local() is complete'

def make_user_review_length():
    # Generates:
    #   d.user_review_length

    global d
    for i in range(num_rows): # need to set this to len(d) later
        d.loc[i, 'user_review_length'] = len(d.loc[i, 'user_review']) 
    print 'make_user_review_length() is complete'

def make_user_rating_mean_for_restaurant_yelp():
    # Generates:
    #   d.user_rating_mean_for_restaurant_yelp
    # Description:
    #   Mean of all yelp user ratings in data set by restaurant. 
        
    global d
    mean_ratings = d.groupby('restaurant_name')['user_rating'].mean()
    d = d.join(mean_ratings, on='restaurant_name', rsuffix='_mean_for_restaurant_yelp')
    print 'make_user_rating_mean_for_restaurant_yelp() is complete'
        
def make_user_rating_mean_for_restaurant_yelp_local():
    # Generates:
    #   d.user_rating_mean_for_restaurant_yelp_local
    
    # replace missing values with NaN
    #d = d.applymap(lambda x: np.nan if isinstance(x, basestring) and x.isspace() else x)
    global d
    mean_ratings = d.groupby(['user_is_local', 'restaurant_name'])['user_rating'].mean()
    mean_ratings_local = mean_ratings[1] # there's surely a better way to do this
    #d = d.join(mean_ratings, on=['user_is_local', 'restaurant_name'], rsuffix='_mean_for_restaurant_yelp_local')
    d = d.join(mean_ratings_local, on=['restaurant_name'], rsuffix='_mean_for_restaurant_yelp_local')
    print 'make_user_rating_mean_for_restaurant_yelp_local() is complete'
    
def make_user_rating_mean_for_restaurant_yelp_non_local():
    # Generates:
    #   d.user_rating_mean_for_restaurant_yelp_non_local

    global d
    mean_ratings = d.groupby(['user_is_local', 'restaurant_name'])['user_rating'].mean()
    mean_ratings_non_local = mean_ratings[0]
    d = d.join(mean_ratings_non_local, on=['restaurant_name'], rsuffix='_mean_for_restaurant_yelp_non_local')    
    print 'make_user_rating_mean_for_restaurant_yelp_non_local() is complete'

'''    
having issues with sd (probably caused by missing values). holding off for now. 
    
def make_user_rating_sd_for_restaurant_yelp():
    # Generates:
    #   d.user_rating_sd_for_restaurant_yelp
    # NOTE: Omitting for now, since getting some NaN in local version of the function below
    
    global d
    sd_ratings = d.groupby('restaurant_name')['user_rating'].std()
    d = d.join(sd_ratings, on='restaurant_name', rsuffix='_sd_for_restaurant_yelp')
    
def make_user_rating_sd_for_restaurant_yelp_local():
    # Generates:
    #   d.user_rating_sd_for_restaurant_yelp_local
    #
    # NOTE: Omitting for now, since getting some NaN

    global d
    sd_ratings = d.groupby(['user_is_local', 'restaurant_name'])['user_rating'].std()
    sd_ratings_local = sd_ratings[1]
    # check
    print sd_ratings
    print sd_ratings_local
    d = d.join(sd_ratings_local, on=['restaurant_name'], rsuffix='_mean_for_restaurant_yelp_local')
    
def make_user_rating_sd_for_restaurant_yelp_non_local():
    # place holder
    pass
    
'''    
    
################
# Run main methods
################

global_main_switch = True # set to true to quickly run all 
                          # properly working main methods

if False or global_main_switch: # data cleaning
    data_cleaning()
if True or global_main_switch: # geocode-based features
    make_restaurant_geocode()
    make_user_geocode()
    make_user_restaurant_distance()
    make_user_is_local()
if False or global_main_switch: # review text-based features
    make_user_review_length()
if False or global_main_switch: # aggregate mean yelp ratings
    make_user_rating_mean_for_restaurant_yelp()
    make_user_rating_mean_for_restaurant_yelp_local()
    make_user_rating_mean_for_restaurant_yelp_non_local()
if False: # aggregate sd yelp ratings
    make_user_rating_sd_for_restaurant_yelp()
    make_user_rating_sd_for_restaurant_yelp_local()
    make_user_rating_sd_for_restaurant_yelp_non_local() 
    

################
# Check out results
################

#print d.head(10)

################
# Save results
################

d.to_csv(output_data_path, index=False)

print input_data_path, 'cleaned and features added' # success message

