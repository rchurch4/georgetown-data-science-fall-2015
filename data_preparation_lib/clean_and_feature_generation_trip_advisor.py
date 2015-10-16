################
# clean_and_feature_generation_trip_advisor.py
# Version 4
# Python 2
# 
# Description:
# Function to generate extra features. This is used in
# data_preparation_trip_advisor.py. 
# 
# List of features generated:
#   restaurant_latitude
#   restaurant_longitude
#   user_latitude, 
#   user_longitude   
#   user_restaurant_distance   
#   user_is_local    
#   user_review_length    
#   mean_restaurant_rating_trip_advisor
#   mean_restaurant_rating_trip_advisor_local
#   mean_restaurant_rating_trip_advisor_local	
#
# References used:
# For checking for missing value:
#   http://stackoverflow.com/questions/944700/how-to-check-for-nan-in-python
################

import pandas as pd
import numpy as np
import os
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import time
import sys
import math

def clean_and_feature_generation_trip_advisor(input_file_paths):
    # input: 
    #   input_file_paths
    #       takes the input file paths as a list of strings.
    #       these paths point to csv files created from
    #       the original scraped json files. 
    # output: 
    #   One csv per input csv file is created. 
    # return
    #   None

    print 'Starting feature additions and basic cleaning.'
    
    ################
    # Begin adding features and basic cleaning.
    ################

    for i, current_input_file_path in enumerate(input_file_paths):

        # Dynamically make output file paths
        current_output_file_path = current_input_file_path.replace('.csv', '_cleaned_features_.csv')
        print "Current file: ", current_input_file_path
        
        ################
        # Data loading
        ################

        # Load data in as a Pandas DataFrame.
        d = pd.read_csv(current_input_file_path)
        num_rows = len(d) # this should only be changed during testing.

        ################
        # Data cleaning
        ################

        def data_cleaning():
            pass
            #print 'data_cleaning() complete'

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
            
            # Assign geocode based on restaurant_location.
            # Since the number of cities we are investigating is
            # relatively small (definitely under 10 in the foreseeable
            # future), hardcoding in the latitude and longitude seems
            # like the quickest approach. 
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
            # replace missing values with NaN (does not seem necessary as of right now)
            #d = d.applymap(lambda x: np.nan if isinstance(x, basestring) and x.isspace() else x)
            print 'make_user_geocode() complete'    
                
        def make_user_restaurant_distance():
            # Generates:
            #   d.user_restaurant_distance
            # Description:
            #   Uses the Vincenty distance formula to calculate distance between
            #   two points on a sphere, using the latitude and longitude. 
            
            for i in range(num_rows): 
                restaurant_geocode = (d.loc[i, 'restaurant_latitude'], d.loc[i, 'restaurant_longitude'])
                user_geocode = (d.loc[i, 'user_latitude'], d.loc[i, 'user_longitude'])
                try: 
                    d.loc[i, 'user_restaurant_distance'] = vincenty(restaurant_geocode, user_geocode).miles
                except: # avoid crashing when lat/long is missing
                    continue
            print 'make_user_restaurant_distance() complete'
                
        def make_user_is_local():
            # Generates:
            #   d.is_local
            # Description:
            #   User is considered local if he or she is within the distance_threshold.
            
            distance_threshold = 50 # in miles
            for i in range(num_rows): 
                if math.isnan(d.loc[i, 'user_restaurant_distance']):
                    d.loc[i, 'user_is_local'] = np.NaN
                elif d.loc[i, 'user_restaurant_distance'] <= distance_threshold:
                    d.loc[i, 'user_is_local'] = True
                else:
                    d.loc[i, 'user_is_local'] = False
            print 'make_user_is_local() is complete'

        def make_user_review_length():
            # Generates:
            #   d.user_review_length

            for i in range(num_rows): # need to set this to len(d) later
                d.loc[i, 'user_review_length'] = len(d.loc[i, 'user_review']) 
            print 'make_user_review_length() is complete'

        def make_user_rating_mean_for_restaurant_trip_advisor(d):
            # Generates:
            #   d.user_rating_mean_for_restaurant_trip_advisor
            # Description:
            #   Mean of all trip_advisor user ratings in data set by restaurant. 
            # Input:
            #   The same dataframe all functions here are working with.
            #   for some reason, only the functions that use d.groupby
            #   require passing d as an argument. the other functions
            #   have access to d already. that is the reasons for this
            #   input.             

            mean_ratings = d.groupby('restaurant_name')['user_rating'].mean()

            d = d.join(mean_ratings, on='restaurant_name', rsuffix='_mean_for_restaurant_trip_advisor')
            print 'make_user_rating_mean_for_restaurant_trip_advisor() is complete'
                
        def make_user_rating_mean_for_restaurant_trip_advisor_local(d):
            # Generates:
            #   d.user_rating_mean_for_restaurant_trip_advisor_local
            # Input:
            #   The same dataframe all functions here are working with.
            #   for some reason, only the functions that use d.groupby
            #   require passing d as an argument. the other functions
            #   have access to d already. that is the reasons for this
            #   input.             
            
            # replace missing values with NaN
            #d = d.applymap(lambda x: np.nan if isinstance(x, basestring) and x.isspace() else x)
            #global d
            mean_ratings = d.groupby(['user_is_local', 'restaurant_name'])['user_rating'].mean()
            mean_ratings_local = mean_ratings[1] # there's surely a better way to do this
            #d = d.join(mean_ratings, on=['user_is_local', 'restaurant_name'], rsuffix='_mean_for_restaurant_trip_advisor_local')
            d = d.join(mean_ratings_local, on=['restaurant_name'], rsuffix='_mean_for_restaurant_trip_advisor_local')
            print 'make_user_rating_mean_for_restaurant_trip_advisor_local() is complete'
            
        def make_user_rating_mean_for_restaurant_trip_advisor_non_local(d):
            # Generates:
            #   d.user_rating_mean_for_restaurant_trip_advisor_non_local
            # Input:
            #   The same dataframe all functions here are working with.
            #   for some reason, only the functions that use d.groupby
            #   require passing d as an argument. the other functions
            #   have access to d already. that is the reasons for this
            #   input. 

            mean_ratings = d.groupby(['user_is_local', 'restaurant_name'])['user_rating'].mean()
            mean_ratings_non_local = mean_ratings[0]
            d = d.join(mean_ratings_non_local, on=['restaurant_name'], rsuffix='_mean_for_restaurant_trip_advisor_non_local')    
            print 'make_user_rating_mean_for_restaurant_trip_advisor_non_local() is complete'
            
        ################
        # Run main methods
        ################

        global_main_switch = True # set to true to quickly run all main methods

        if False or global_main_switch: # data cleaning
            data_cleaning()
        if True or global_main_switch: # geocode-based features
            make_restaurant_geocode()
            make_user_geocode()
            make_user_restaurant_distance()
            make_user_is_local()
        if False or global_main_switch: # review text-based features
            make_user_review_length()
        if False or global_main_switch: # aggregate mean trip_advisor ratings
            make_user_rating_mean_for_restaurant_trip_advisor(d)
            make_user_rating_mean_for_restaurant_trip_advisor_local(d)
            make_user_rating_mean_for_restaurant_trip_advisor_non_local(d)
            
        ################
        # Save results
        ################

        d.to_csv(current_output_file_path, index=False)

        print 'finished creating', current_output_file_path # success message

